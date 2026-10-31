# 02. 로봇 팔(매니퓰레이터) 기구학 및 제어

> **실습 노트북 바로가기**: [Notebook 02: `02_robot_arms.ipynb` 웹에서 보기](../notebooks/02_robot_arms.ipynb)

![KUKA Follows Circle](../assets/imgs/kuka_follows_circle.gif)

---

## 학습 목표
1. **산업용·연구용 로봇 팔 모델 다루기**:
   * `assets/robots/universal_robots_ur5e` (6-DoF)
   * `assets/robots/franka_emika_panda` (7-DoF 여유 자유도)
   * `assets/robots/kuka_iiwa_14` (7-DoF 토크 제어)
2. **미분 역기구학 (Differential Inverse Kinematics, Diff-IK)**:
   * 3차원 위치 오차 $e_p = p_{\text{ee}} - p_{\text{target}}$와 쿼터니언 자세 오차 $q_{\text{err}} = q_{\text{ee}} \otimes q_{\text{target}}^{-1}$ (`mju_quat2Vel`) 계산
   * 엔드이펙터 기하 자코비안(`mj_jacSite`) 의사역행렬을 통한 관절 위치 제어:
     $$\Delta q = -J^\dagger e$$
3. **영공간(Null-Space) 선호도 최적화**:
   * 여유 자유도(Redundancy)를 활용하여 엔드이펙터 궤적 추종($J \Delta q = -e$)과 동시에 초기 홈 관절 자세($q_0$)를 유지하는 이차 계획법(QP)의 KKT 해석적 해 도출:
     $$\begin{bmatrix} 2 K_n^T K_n & J^T \\ J & 0 \end{bmatrix} \begin{bmatrix} \Delta q \\ \lambda \end{bmatrix} = \begin{bmatrix} 2 K_n^T K_n (q_0 - q) \\ -e \end{bmatrix}$$
4. **작업 공간 제어 (Operational Space Control, OSC - 토크 제어)**:
   * 작업 공간 관성 행렬 $M_x = (J M^{-1} J^T)^{-1}$ (`mj_solveM` 활용)
   * 작업 공간 임피던스 가속도 명령 + 중력/코리올리 보상(`data.qfrc_bias`) + 동역학 일관 의사역행렬($\bar{J} = M^{-1} J^T M_x$)을 통한 영공간 토크 투영:
     $$\tau = J^T M_x \left(-K_p e - K_d J \dot{q}\right) + \tau_{\text{bias}} + \left(I - J^T \bar{J}^T\right) \left(-K_{p,\text{null}}(q - q_0) - K_{d,\text{null}}\dot{q}\right)$$

