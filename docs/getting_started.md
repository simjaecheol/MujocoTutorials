# 시작 가이드 (Windows 설치 및 실행 방법)

이 프로젝트는 **Windows** 환경에서 별도의 복잡한 시스템 설정 없이 즉시 실습할 수 있도록 설계되었습니다.

---

## 1. 원클릭 환경 설치 (`setup_env.bat`)

프로젝트 루트 폴더의 **`setup_env.bat`** 파일을 더블클릭하거나, PowerShell 터미널에서 다음 명령어를 실행합니다:

```powershell
.\setup_env.ps1
```

### 자동 수행되는 작업
1. **`uv` 패키지 매니저 확인 및 자동 설치**: 시스템에 `uv`가 없으면 공식 설치 스크립트를 통해 자동으로 설치합니다.
2. **Python 3.11 및 가상환경(`.venv`) 생성**: Windows용 사전 빌드 휠(Wheel) 호환성이 가장 뛰어난 Python 3.11을 자동으로 내려받고 `.venv` 가상환경에 모든 패키지를 설치합니다.
   * 핵심 물리/로보틱스: `mujoco>=3.3.3`, `dm-control>=1.0.31`, `dm-env>=1.6`
   * 수치 최적화/자동 미분: `numpy`, `jax`, `jaxlib`, `casadi` (IPOPT 솔버 내장)
   * 시각화/멀티미디어: `matplotlib`, `mediapy`, `imageio-ffmpeg` (내장 FFmpeg 바이너리 제공)
   * 노트북/문서화: `jupyterlab`, `notebook`, `ipykernel`, `mkdocs-material`, `mkdocs-jupyter`
3. **Jupyter 커널 등록**: VS Code, Cursor, Antigravity, Jupyter Lab에서 바로 선택할 수 있는 **`Python (MuJoCo Robotics)`** 커널을 등록합니다.

---

## 2. 실습 노트북(`notebooks/*.ipynb`) 실행하기

### 방법 A: VS Code / Cursor / Antigravity 내장 노트북 에디터
1. `notebooks/` 폴더 안의 `01_mujoco_basic.ipynb` ~ `06_aloha_bimanual_sim.ipynb` 파일을 엽니다.
2. 우측 상단 **커널 선택(Select Kernel)** 버튼을 눌러 **`.venv (Python 3.11)`** 또는 **`Python (MuJoCo Robotics)`**를 선택합니다.
3. 첫 번째 코드 셀(`init_notebook()`)부터 순서대로 `Shift + Enter`를 눌러 실행합니다.

### 방법 B: Jupyter Lab 브라우저 실행 (`run_jupyter.bat`)
프로젝트 루트의 **`run_jupyter.bat`**을 더블클릭하거나 터미널에서 아래 명령어를 실행합니다:

```powershell
uv run jupyter lab
```

---

## 3. 웹 문서 로컬 서버 실행 (`run_docs.bat`)

현재 보고 계신 웹 문서 사이트를 로컬 PC에서 띄워 확인하려면 **`run_docs.bat`**을 더블클릭하거나 아래 명령어를 실행하세요:

```powershell
uv run mkdocs serve
```

브라우저에서 `http://127.0.0.1:8000`으로 접속하면 가이드 문서와 렌더링된 6개의 Jupyter Notebook을 웹에서 바로 탐색할 수 있습니다.

---

## 4. MuJoCo 3D 인터랙티브 뷰어 조작법 (Windows)

`03_robot_arm_mocap.ipynb`와 `06_aloha_bimanual_sim.ipynb`, 또는 `uv run python src/viewer.py` 실행 시 열리는 3D 뷰어의 마우스·키보드 조작법입니다:

| 동작 | 마우스 / 키보드 조작 |
| :--- | :--- |
| **카메라 회전 (Rotate)** | 마우스 **왼쪽 버튼** 드래그 |
| **카메라 이동 (Pan)** | 마우스 **오른쪽 버튼** 드래그 |
| **카메라 줌 (Zoom)** | 마우스 **휠 스크롤** |
| **물체 / 모캡 타겟 선택** | 대상 물체 위에서 **마우스 왼쪽 더블클릭** |
| **선택한 물체 이동 / 외력(Force) 인가** | `Ctrl` + **마우스 오른쪽 드래그** |
| **선택한 물체 회전 / 토크(Torque) 인가** | `Ctrl` + **마우스 왼쪽 드래그** |
| **시뮬레이션 일시정지 / 재개** | `Space` (스페이스바) |
| **에피소드 초기화 (Reset)** | `Backspace` |

