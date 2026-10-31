# 프로젝트 통합 아키텍처 (Architecture)

기존의 단일 로봇 팔 튜토리얼과 `aloha_sim` 양팔 로봇 시뮬레이션 패키지를 하나의 일관된 구조로 통합하였습니다.

---

## 1. 전체 디렉토리 구조

```text
MujocoTutorials/
├── assets/                            # 모든 로봇 및 3D 물체 모델 통합 디렉토리
│   ├── mujoco_menagerie/              # [Git Submodule] Google DeepMind 공식 50+종 로봇 모델 및 3D 메쉬
│   ├── robots/                        # 튜토리얼 전용 커스텀 MJCF 설정 (메쉬는 mujoco_menagerie 서브모듈 공유)
│   │   ├── franka_emika_panda/        # 모캡 타겟 및 엔드이펙터 카메라가 포함된 Panda XML
│   │   ├── kuka_iiwa_14/              # 직접 토크 제어(<motor>) 및 모캡 타겟이 포함된 KUKA iiwa 14 XML
│   │   ├── universal_robots_ur5e/     # 모캡 타겟 및 엔드이펙터 카메라가 포함된 UR5e XML
│   │   └── aloha/                     # ALOHA 2 PBR 텍스처 및 4-카메라 워크스테이션 모델
│   ├── objects/                       # 조작 작업용 3D 물체 에셋
│   │   ├── edr/                       # 서랍장(drawer), 노트북(laptop), 마커펜, 헤드폰 등
│   │   ├── gso/                       # Google Scanned Objects (그릇, 컵, 공구함, 식기건조대 등)
│   │   ├── letters/                   # 알파벳 블록 에셋
│   │   ├── mujoco/                    # 마커펜 및 유연체(Flex) 수건 모델
│   │   └── ycb/                       # YCB 벤치마크 물체 (바나나, 그릇, 드라이버, 가위 등)
│   └── imgs/                          # 문서 및 노트북용 데모 GIF / 이미지
│
├── src/                               # 통합 파이썬 소스 디렉토리
│   ├── controllers/                   # 로봇 제어기 모듈
│   │   └── osc.py                     # 작업 공간 임피던스 제어기 (OperationalSpaceController)
│   ├── tasks/                         # dm_control.composer 기반 20종 양팔 조작 태스크
│   │   ├── task_suite.py              # TASK_FACTORIES 및 create_task_env() 팩토리 함수
│   │   ├── base/                      # AlohaTask 베이스 클래스 및 작업대(Arena) 구성
│   │   ├── test/                      # 태스크별 유닛 테스트 모음
│   │   └── ...                        # hand_over.py, drawer_open.py, laptop_close.py 등
│   ├── utils/                         # 공통 유틸리티 및 에셋 경로 헬퍼
│   │   ├── notebook_setup.py          # Windows FFmpeg 연결, 한글 폰트, 루트 경로 및 에셋 경로 설정
│   │   ├── oobb_utils.py              # 3D Oriented Bounding Box(OOBB) 충돌/교차 계산
│   │   └── success_detector_utils.py
│   ├── viewer.py                      # ALOHA 2 인터랙티브 3D 뷰어 실행기
│   └── run_eval.py                    # 태스크 평가 스크립트
│
├── notebooks/                         # 단계별 실습 Jupyter Notebook (.ipynb)
│   ├── 01_mujoco_basic.ipynb
│   ├── 02_robot_arms.ipynb
│   ├── 03_robot_arm_mocap.ipynb
│   ├── 04_optimization.ipynb
│   ├── 05_direct_transcription_mpc.ipynb
│   ├── 06_aloha_bimanual_sim.ipynb
│   └── 07_mujoco_playground_mjx.ipynb
│
├── docs/                              # MkDocs 웹 문서 소스
├── mkdocs.yml                         # MkDocs Material 설정 파일
├── pyproject.toml                     # uv 패키지 및 빌드 설정
├── setup_env.bat / setup_env.ps1      # 원클릭 환경 구축 스크립트
├── run_jupyter.bat                    # Jupyter Lab 실행 스크립트
└── run_docs.bat                       # 로컬 웹 문서 서버 실행 스크립트
```

---

## 2. 핵심 모듈 사용법 (`src/` 내장 모듈)

### 2.1 노트북 환경 초기화 (`init_notebook`)
`notebooks/` 폴더 안에서 실행하더라도 자동으로 프로젝트 루트 디렉토리를 찾아 작업 경로를 맞추고, Windows 내장 `ffmpeg`와 한글 폰트를 설정합니다:

```python
from utils.notebook_setup import init_notebook

project_root = init_notebook()
```

### 2.2 로봇 모델 경로 조회 (`get_robot_scene_path`, `list_menagerie_robots`)
튜토리얼 기본 로봇(`"ur5e"`, `"panda"`, `"kuka"`, `"aloha"`)뿐만 아니라, `assets/mujoco_menagerie` 서브모듈에 포함된 **50종 이상의 모든 공식 로봇 모델**(`"unitree_go2"`, `"boston_dynamics_spot"`, `"shadow_hand"` 등)을 이름만으로 불러올 수 있습니다:

```python
import mujoco
from utils import get_robot_scene_path, list_menagerie_robots

# 1) 튜토리얼 커스텀 설정 로봇 로드 ("ur5e", "panda", "kuka", "aloha")
xml_path = get_robot_scene_path("kuka")
model = mujoco.MjModel.from_xml_path(xml_path)

# 2) MuJoCo Menagerie 서브모듈 내 전체 로봇 목록 확인 및 로드
print(list_menagerie_robots()[:5])
go2_xml = get_robot_scene_path("unitree_go2")
```

### 2.3 작업 공간 제어기 (`OperationalSpaceController`)
모캡 타겟(`target`)을 추종하는 작업 공간 임피던스 토크 제어기를 한 줄로 생성할 수 있습니다:

```python
from controllers import OperationalSpaceController

controller = OperationalSpaceController(model)
tau = controller.compute_torque(data)
```

### 2.4 ALOHA 2 20종 조작 태스크 생성 (`task_suite.create_task_env`)
`dm_control.composer` 기반의 양팔 로봇 조작 환경을 즉시 생성합니다:

```python
from tasks import task_suite

env = task_suite.create_task_env(
    task_name="HandOverBanana",
    time_limit=10.0,
    random_state=42,
    camera_resolution=(360, 640),
)
timestep = env.reset()
```

