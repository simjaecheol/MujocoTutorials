# 05. 직접 전사법(Direct Transcription) 궤적 최적화 및 모델 예측 제어(MPC)

> **실습 노트북 바로가기**: [Notebook 05: `05_direct_transcription_mpc.ipynb` 웹에서 보기](../notebooks/05_direct_transcription_mpc.ipynb)

---

## 학습 목표
1. **언더액추에이티드(Underactuated) 카트폴 동역학**:
   * 카트 위치($p$)와 막대 각도($\theta$)로 이루어진 4차원 상태 공간에서 제한된 카트 추력($-3 \le u \le 3$)만으로 아래로 처진 막대($\theta = \pi$)를 위로 세우는($\theta = 0$) 스윙업 문제 이해
2. **MuJoCo 이산 동역학의 CasADi 심볼릭 래핑 (`CasadiMujocoWrap`)**:
   * `casadi.Callback`과 유한차분(`enable_fd=True`)을 사용해 C 기반 `mujoco.mj_step`을 비선형 계획법(NLP) 솔버가 미분할 수 있는 심볼릭 함수로 연결
3. **직접 전사법 (Direct Transcription) + IPOPT 풀이**:
   * 시간 구간 $T=50$ 동안의 상태 $x_{0:T}$와 제어 입력 $u_{0:T-1}$ 전체를 결정 변수로 두고, 매 스텝 동역학 $x_{k+1} = f_{\text{MuJoCo}}(x_k, u_k)$를 등식 제약 조건으로 부여하여 스윙업 궤적 생성
4. **Warm-Start 기반 실시간 모델 예측 제어 (MPC)**:
   * 이전 제어 주기의 최적 궤적을 한 스텝 시프트(`update_init_guess`)하여 다음 주기의 초기 추측값으로 제공함으로써, 매 스텝 **단 2회의 IPOPT 반복(`max_iter=2`)**만으로 카트폴 스윙업 및 균형 유지를 달성하는 폐루프 제어 구현

