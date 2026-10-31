# 03. 인터랙티브 3D 뷰어와 마우스 모캡(Mocap) 실시간 제어

> **실습 노트북 바로가기**: [Notebook 03: `03_robot_arm_mocap.ipynb` 웹에서 보기](../notebooks/03_robot_arm_mocap.ipynb)

![KUKA Mocap Interactive](../assets/imgs/kuka_mocap.gif)

---

## 학습 목표
1. **작업 공간 제어기(`OperationalSpaceController`) 모듈화**:
   * `src/controllers/osc.py`에 구현된 `OperationalSpaceController` 구조 이해
2. **노트북 내 6자유도(위치+자세) 3D 8자(Lissajous) 모캡 추종 시뮬레이션**:
   * 목표 타겟의 3차원 위치와 3차원 회전 자세가 동시에 연속적으로 변할 때 KUKA iiwa 14 로봇 팔이 추종하는 동작을 비디오로 확인
3. **Windows 인터랙티브 3D 뷰어(`mujoco.viewer.launch_passive`) 실습**:
   * 노트북 셀에서 별도의 MuJoCo 3D 뷰어 창을 실행하고, 마우스로 모캡 타겟을 실시간으로 이동(`Ctrl + 우클릭 드래그`)·회전(`Ctrl + 좌클릭 드래그`)시키며 임피던스 토크 제어기의 반응성과 외력에 대한 순응성(Compliance)을 직접 체험

