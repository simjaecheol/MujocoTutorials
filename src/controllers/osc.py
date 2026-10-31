"""
작업 공간 임피던스 제어기 (Operational Space Controller, OSC) + 영공간(Null-space) 자세 제어기.
"""
import mujoco
import numpy as np


class OperationalSpaceController:
    """작업 공간 임피던스 제어(OSC) + 영공간(Null-space) 자세 제어기"""

    def __init__(
        self,
        model: mujoco.MjModel,
        target_body_name: str = "target",
        site_name: str = "attachment_site",
    ):
        self.model = model
        self.mocap_id = model.body(target_body_name).mocapid[0]
        self.site_id = model.site(site_name).id

        # 연산용 배열 사전 할당 (매 스텝 메모리 할당 오버헤드 방지)
        self.M_inv = np.zeros((model.nv, model.nv))
        self.jac = np.zeros((6, model.nv))
        self.error = np.zeros(6)
        self.error_pos = self.error[:3]
        self.error_ori = self.error[3:]
        self.site_quat = np.zeros(4)
        self.target_quat_conj = np.zeros(4)
        self.error_quat = np.zeros(4)

        # 작업 공간 임피던스 제어 게인 (Kp, Kd)
        impedance_pos = np.asarray([100.0, 100.0, 100.0])  # 위치 강성 [N/m]
        impedance_ori = np.asarray([50.0, 50.0, 50.0])     # 회전 강성 [Nm/rad]
        self.Kp = np.concatenate([impedance_pos, impedance_ori], axis=0)

        damping_ratio = 1.0
        damping_pos = damping_ratio * 2 * np.sqrt(impedance_pos)
        damping_ori = damping_ratio * 2 * np.sqrt(impedance_ori)
        self.Kd = np.concatenate([damping_pos, damping_ori], axis=0)

        # 영공간(Null-space) 초기 관절 자세 선호 게인
        self.q0 = model.key(0).qpos.copy()
        self.Kp_null = np.asarray([75.0, 75.0, 50.0, 50.0, 40.0, 25.0, 25.0][:model.nv])
        self.Kd_null = damping_ratio * 2 * np.sqrt(self.Kp_null)

    def compute_torque(self, data: mujoco.MjData) -> np.ndarray:
        """현재 상태에서 목표 모캡 타겟을 추종하기 위한 관절 토크 벡터(tau)를 계산합니다."""
        # 1. 위치 및 자세 오차 계산
        self.error_pos[:] = data.site(self.site_id).xpos - data.mocap_pos[self.mocap_id]
        target_ori = data.mocap_quat[self.mocap_id]
        mujoco.mju_negQuat(self.target_quat_conj, target_ori)
        mujoco.mju_mat2Quat(self.site_quat, data.site(self.site_id).xmat)
        mujoco.mju_mulQuat(self.error_quat, self.site_quat, self.target_quat_conj)
        mujoco.mju_quat2Vel(self.error_ori, self.error_quat, 1.0)

        # 2. 엔드이펙터 기하 자코비안 계산
        mujoco.mj_jacSite(self.model, data, self.jac[:3], self.jac[3:], self.site_id)

        # 3. 작업 공간 관성 행렬 Mx = (J * M^{-1} * J^T)^{-1} 계산
        mujoco.mj_solveM(self.model, data, self.M_inv, np.eye(self.model.nv))
        Mx_inv = self.jac @ self.M_inv @ self.jac.T
        Mx = np.linalg.pinv(Mx_inv)

        # 4. 작업 공간 임피던스 토크 + 중력/코리올리 보상 토크
        tau = self.jac.T @ Mx @ (-self.Kp * self.error - self.Kd * (self.jac @ data.qvel)) + data.qfrc_bias

        # 5. 영공간(Null-space) 관절 자세 안정화 토크 투영
        Jbar = self.M_inv @ self.jac.T @ Mx
        ddq = -self.Kp_null * (data.qpos - self.q0) - self.Kd_null * data.qvel
        tau += (np.eye(self.model.nv) - self.jac.T @ Jbar.T) @ ddq

        # 액추에이터 토크 한계 범위 내로 클리핑
        np.clip(tau, *self.model.actuator_ctrlrange.T, out=tau)
        return tau

