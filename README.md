# MuJoCo Robotics Tutorials (Windows Edition)

**Windows 환경**에서 [MuJoCo](https://mujoco.org/) 물리 엔진과 **Jupyter Notebook(`.ipynb`)**을 통해 로보틱스의 기초부터 매니퓰레이터 제어, 수치 최적화, 궤적 생성 및 모델 예측 제어(MPC)까지 단계별로 학습할 수 있는 튜토리얼 프로젝트입니다.

모든 튜토리얼은 별도의 시스템 설정(예: FFmpeg 수동 설치, Linux 전용 렌더링 설정 등) 없이 Windows에서 즉시 실행되도록 구성되어 있습니다.

---

## 1. 환경 설치 방법 (빠른 시작)

이 프로젝트는 초고속 파이썬 패키지 매니저인 **[`uv`](https://docs.astral.sh/uv/)**를 사용하여, PC에 Python이 설치되어 있지 않더라도 **Python 3.11 다운로드부터 가상환경(`.venv`) 생성, 필수 패키지 설치, Jupyter 커널 등록까지 한 번에 자동 처리**합니다.

### 방법 A: 원클릭 자동 설치 (권장)
프로젝트 폴더의 **[`setup_env.bat`](./setup_env.bat)** 파일을 더블클릭하거나, PowerShell 터미널에서 아래 명령어를 실행하세요:

```powershell
.\setup_env.ps1
```

이 스크립트는 다음 작업을 자동으로 수행합니다:
1. `uv` 패키지 매니저 확인 (미설치 시 자동 설치)
2. Python 3.11 및 필수 패키지(`mujoco`, `numpy`, `matplotlib`, `mediapy`, `imageio-ffmpeg`, `jax`, `casadi`, `jupyterlab` 등)를 `.venv`에 설치
3. Jupyter 커널 **`Python (MuJoCo Robotics)`** 자동 등록

### 방법 B: `uv` 명령어 직접 실행
이미 `uv`를 사용 중이라면 아래 명령어로 바로 동기화할 수 있습니다:

```powershell
uv sync
```

### 방법 C: 기존 `pip` + `venv` 사용 시
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. 튜토리얼 실행 방법

### 1) VS Code / Cursor / Antigravity 내장 에디터에서 실행
1. 원하는 `.ipynb` 노트북 파일을 엽니다.
2. 우측 상단 **커널 선택(Select Kernel)**에서 **`.venv (Python 3.11)`** 또는 **`Python (MuJoCo Robotics)`**를 선택합니다.
3. 위에서부터 순서대로 셀(`Shift + Enter`)을 실행하며 학습합니다.

### 2) 웹 브라우저(Jupyter Lab)에서 실행
**[`run_jupyter.bat`](./run_jupyter.bat)** 파일을 더블클릭하거나 터미널에서 아래 명령어를 실행하세요:

```powershell
uv run jupyter lab
```

---

## 3. 커리큘럼 및 주요 내용

노트북 번호 순서(`01` → `05`)대로 학습하시는 것을 권장합니다.

| 순서 및 파일 | 주요 학습 내용 | 데모 미리보기 |
| :--- | :--- | :---: |
| **[01_mujoco_basic.ipynb](./01_mujoco_basic.ipynb)**<br>MuJoCo 기초 및 물리 시뮬레이션 | - MJCF(XML) 모델링 문법 및 기본 요소<br>- 정적 모델(`mjModel`)과 동적 상태(`mjData`) 구조<br>- 자유도(DoF), 일반화 좌표계(`qpos`, `qvel`), 쿼터니언<br>- 뒤집히는 팽이(Tippe-Top) 및 카오스 진자 시뮬레이션<br>- 타임스텝(`timestep`)과 에너지 보존, 수치 발산 분석<br>- 접촉력(Contact Force), 마찰, 힘줄, 액추에이터, 가속도계 센서<br>- 깊이/세그멘테이션 카메라, 투영 행렬, 도미노 및 동적 카메라 워킹 | ![dominoes](./imgs/dominoes.gif) |
| **[02_robot_arms.ipynb](./02_robot_arms.ipynb)**<br>로봇 팔(매니퓰레이터) 기구학 및 제어 | - 6자유도 **UR5e**, 7자유도 **Franka Emika Panda**, **KUKA iiwa 14** 제어<br>- 미분 역기구학(Differential IK): 자코비안(`mj_jacSite`) 및 쿼터니언 자세 오차<br>- 영공간(Null-Space) 제어: KKT 조건을 이용한 여유 자유도 관절 자세 최적화<br>- 작업 공간 제어(Operational Space Control, OSC): 작업 공간 관성 행렬($\Lambda$)과 중력/코리올리 보상을 통한 **직접 토크 제어** | ![kuka_follows_circle](./imgs/kuka_follows_circle.gif) |
| **[03_robot_arm_mocap.ipynb](./03_robot_arm_mocap.ipynb)**<br>인터랙티브 3D 뷰어 & 마우스 모캡 제어 | - `OperationalSpaceController` 모듈화 및 3차원 8자(Lissajous) 모캡 궤적 추종<br>- MuJoCo 내장 인터랙티브 3D 뷰어(`mujoco.viewer.launch_passive`) 실행<br>- 마우스 드래그(`Ctrl` + 클릭)로 타겟을 실시간 이동/회전시키고 로봇에 외력을 가하며 임피던스 순응성(Compliance) 체험 | ![kuka_mocap](./imgs/kuka_mocap.gif) |
| **[04_optimization.ipynb](./04_optimization.ipynb)**<br>로보틱스를 위한 비볼록 수치 최적화 | - 뉴턴 방법(Newton's Method)과 **레벤버그-마쿼트(Levenberg-Marquardt)** 정규화<br>- 비선형 최소제곱법과 **가우스-뉴턴(Gauss-Newton)** 근사법 ($H \approx J^T J$)<br>- `mujoco.minimize.least_squares` 및 JAX 자동 미분 실습<br>- 등식 제약 조건부 최적화: **페널티 방법(Penalty)**, **원시-쌍대 KKT 뉴턴-랩슨(Primal-Dual)**, **증강 라그랑지안(Augmented Lagrangian)** 비교 | ![augmented_lagrangian](./imgs/augmented_lagrangian.png) |
| **[05_direct_transcription_mpc.ipynb](./05_direct_transcription_mpc.ipynb)**<br>직접 전사법 궤적 최적화 및 MPC | - 언더액추에이티드 카트폴(Cart-Pole / 도립진자) 동역학 모델링<br>- `casadi.Callback`을 이용한 MuJoCo 이산 동역학 심볼릭 래핑(`enable_fd`)<br>- **직접 전사법(Direct Transcription)** NLP 정식화 및 **IPOPT** 솔버를 통한 스윙업(Swing-up) 궤적 생성<br>- **Warm-start** 기반 실시간 **모델 예측 제어(MPC)** 루프 구현 | - |

---

## 4. 프로젝트 구조

```text
MujocoTutorials/
├── 01_mujoco_basic.ipynb              # 1단계: MuJoCo 기초 및 물리 시뮬레이션
├── 02_robot_arms.ipynb                # 2단계: 매니퓰레이터 기구학(Diff-IK) 및 토크 제어(OSC)
├── 03_robot_arm_mocap.ipynb           # 3단계: 인터랙티브 3D 뷰어 및 마우스 모캡 실시간 제어
├── 04_optimization.ipynb              # 4단계: 비볼록 수치 최적화 및 증강 라그랑지안
├── 05_direct_transcription_mpc.ipynb  # 5단계: 직접 전사법 궤적 최적화 및 카트폴 MPC
├── utils/
│   └── notebook_setup.py              # Windows 내장 FFmpeg 연결, 한글 폰트, 루트 경로 자동 설정
├── robot/
│   └── robot_arms/                    # UR5e, Franka Panda, KUKA iiwa 14 MJCF 모델 및 메쉬 에셋
├── imgs/                              # 튜토리얼 데모 GIF 및 이미지
├── pyproject.toml                     # uv 프로젝트 및 의존성 설정 파일
├── requirements.txt                   # pip 호환용 패키지 목록
├── setup_env.bat / setup_env.ps1      # Windows 원클릭 가상환경 및 패키지 자동 설치 스크립트
└── run_jupyter.bat                    # Jupyter Lab 실행 런처 스크립트
```

---

## 5. 참고 자료 (References)

| 참고 자료 | 저자 / 출처 | 설명 |
| :--- | :--- | :--- |
| [MuJoCo Official Tutorials](https://github.com/google-deepmind/mujoco) | Google DeepMind | 공식 MuJoCo Python 바인딩 및 최적화 튜토리얼 |
| [mjctrl](https://github.com/kevinzakka/mjctrl) | Kevin Zakka | MuJoCo 기반 단일 파일 로보틱스 제어기 구현 모음 |
| [Robotic Manipulation](https://manipulation.mit.edu/) | Russ Tedrake (MIT) | 매니퓰레이션 기구학 및 제어 강의 노트 |
| [Nonlinear Least Squares Notes](https://www.seas.ucla.edu/~vandenbe/133B/lectures/nllseq.pdf) | Lieven Vandenberghe (UCLA) | 비선형 최소제곱법 및 제약 조건부 최적화 강의 노트 |
