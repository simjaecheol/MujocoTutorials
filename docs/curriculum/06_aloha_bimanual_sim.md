# 06. ALOHA 2 양팔 로봇(Bimanual Manipulation) 시뮬레이션 및 벤치마크 태스크

> **실습 노트북 바로가기**: [Notebook 06: `06_aloha_bimanual_sim.ipynb` 웹에서 보기](../notebooks/06_aloha_bimanual_sim.ipynb)

![ALOHA 2 Walkthrough](../assets/imgs/aloha/walkthrough.png)

---

## 학습 목표
1. **ALOHA 2 양팔 매니퓰레이터 구조 이해**:
   * `assets/robots/aloha/scene_pbr.xml` 모델 분석
   * 양팔 6자유도(ViperX 300s × 2) + 그리퍼 손가락(2 × 2)으로 구성된 16차원 일반화 위치(`nq=16`)와 `<equality>` 구속을 통한 14차원 제어 입력(`nu=14`) 매핑 이해
   * 4대의 카메라(`overhead_cam`, `worms_eye_cam`, `wrist_cam_left`, `wrist_cam_right`) 멀티뷰 렌더링
2. **양팔 미분 역기구학 (Bimanual Differential IK)**:
   * 왼손 그리퍼(`left/gripper`)와 오른손 그리퍼(`right/gripper`)의 자코비안을 각각 추출하여 감쇠 최소제곱법(Damped Least Squares)으로 양손의 3D 포즈와 그리퍼 개폐를 동시에 제어
3. **`dm_control.composer` 기반 20종 일상 물체 조작 태스크(`task_suite`) 실습**:
   * `HandOverBanana`, `DrawerOpen`, `LaptopClose`, `BowlOnRack`, `MarkerRemoveLid`, `ToolsPlaceScrewdriverInLeftCompartment`, `BlocksSpelling`, `TowelFoldInHalf` 등 20개 태스크 환경 생성 및 언어 지시문(`get_instruction()`), 보상 판정(3D OOBB 교차 검사) 실습
4. **Windows 인터랙티브 3D 뷰어로 태스크 직접 체험**:
   * 노트북에서 바로 ALOHA 2 작업 환경을 3D 인터랙티브 뷰어로 띄워 마우스 드래그로 물체를 조작하고 태스크 성공(`reward >= 1.0`) 감지 확인

