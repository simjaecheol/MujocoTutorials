# 07. MuJoCo Playground & MJX: 대규모 병렬 시뮬레이션과 로봇 강화학습

> **실습 노트북 바로가기**: [Notebook 07: `07_mujoco_playground_mjx.ipynb` 웹에서 보기](../notebooks/07_mujoco_playground_mjx.ipynb)

![MuJoCo Playground Banner](../assets/imgs/playground_banner.png)

---

## 학습 목표

1. **MuJoCo MJX (`mujoco.mjx`)와 `jax.vmap` 대규모 병렬 시뮬레이션**:
   * `mjx.put_model(mj_model)`, `mjx.make_data(mj_model)`을 통해 물리 모델과 상태를 JAX(XLA) 배열로 변환
   * `jax.jit` 및 `jax.vmap`을 활용하여 단일 디바이스에서 **1,024개 이상의 독립적인 로봇 환경을 동시에 스텝 진행**하고 배치 크기별 처리량(Steps/sec) 벤치마크 수행
2. **Playground 환경 설계 패턴 (`sim_dt` vs `ctrl_dt`, `reward.tolerance`) & 병렬 MPPI 제어**:
   * 물리 적분 타임스텝(`sim_dt`)과 에이전트 제어 주기(`ctrl_dt`, 서브스테핑) 분리 아키텍처
   * DeepMind Control Suite의 표준 가우시안 보상 함수 `reward.tolerance(x, bounds, margin)` 구현
   * 매 제어 스텝마다 수십 개의 후보 행동 시퀀스를 병렬 롤아웃하여 최적 제어 입력을 계산하는 **MPPI(Model Predictive Path Integral)** 제어기 실습
3. **사족보행(Quadruped Locomotion — Unitree Go1) 조이스틱 추종, 외란 및 도메인 랜덤화**:
   * `assets/mujoco_menagerie/unitree_go1` 모델을 활용한 12자유도 트로트(Trot) 보행 제어 및 **3D 조이스틱 목표 속도 화살표(`mjGEOM_ARROW`)** 시각화
   * 주행 중 측면 속도 충격(**Velocity Kick Perturbation**) 인가 실험 및 **4개 발 스윙 피크(`swing_peak` $2 \times 2$ 그리드)** 보행 진단 플롯 작성
   * **Sim-to-Real 도메인 랜덤화(Domain Randomization)**: `jax.vmap`을 이용해 바닥 마찰계수(`geom_friction`), 관절 전기자 관성(`dof_armature`), 몸통 하중(`body_mass`)을 병렬 월드마다 무작위화
4. **다지 로봇 손 조작(Dexterous Manipulation — LEAP Hand $SO(3)$ 큐브 회전) & 비대칭 액터-크리틱**:
   * `assets/mujoco_menagerie/leap_hand` 모델과 3D 큐브를 조합한 **인핸드 큐브 방향 제어(`LeapCubeReorient`)** 씬 구성
   * 실제 로봇 센서 관측(`obs["state"]`)과 시뮬레이터 내부 특권 관측(`obs["privileged_state"]`)을 분리하는 **비대칭 액터-크리틱(Asymmetric Actor-Critic)** 관측 공간 설계
5. **`mujoco_playground` & `brax` PPO 강화학습 및 에너지 페널티 파인튜닝**:
   * 프로젝트 내 `assets/mujoco_menagerie` 서브모듈을 `mujoco_playground`에 직접 바인딩하여 중복 다운로드를 방지하고, 에너지(`energy`) 및 관절 가속도(`dof_acc`) 페널티 커리큘럼 파인튜닝을 적용하는 레시피 학습

