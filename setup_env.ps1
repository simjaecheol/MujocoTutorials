# Windows용 MuJoCo 로보틱스 학습 환경 자동 구축 스크립트 (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  MuJoCo Robotics Tutorials - Windows 환경 자동 설치" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 현재 스크립트가 위치한 폴더로 이동
Set-Location -Path $PSScriptRoot

# 0. Git 서브모듈(assets/mujoco_menagerie) 확인 및 초기화
if (-not (Test-Path "assets\mujoco_menagerie\universal_robots_ur5e\scene.xml")) {
    Write-Host "[0/3] 'assets/mujoco_menagerie' Git 서브모듈 초기화 중..." -ForegroundColor Cyan
    git submodule update --init --recursive
}

# 1. uv 설치 여부 확인 및 자동 설치
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    $uvPaths = @(
        "$env:USERPROFILE\.local\bin",
        "$env:USERPROFILE\.cargo\bin",
        "$env:LOCALAPPDATA\Microsoft\WinGet\Links"
    )
    foreach ($p in $uvPaths) {
        if (Test-Path "$p\uv.exe") {
            $env:PATH = "$p;$env:PATH"
            break
        }
    }
}

if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "[1/3] 'uv' 패키지 매니저가 설치되어 있지 않습니다. 공식 설치 스크립트로 설치를 진행합니다..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | iex
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:PATH"
} else {
    $uvVer = uv --version
    Write-Host "[1/3] 'uv' 패키지 매니저 확인 완료 ($uvVer)" -ForegroundColor Green
}

# 2. Python 3.11 및 가상환경(.venv) 패키지 동기화 (src/ 통합 모듈 포함)
Write-Host ""
Write-Host "[2/3] Python 3.11 및 로보틱스 필수 패키지(MuJoCo, dm_control, JAX, CasADi, MkDocs 등) 설치 중..." -ForegroundColor Cyan
uv sync

# 3. Jupyter 커널 등록
Write-Host ""
Write-Host "[3/3] Jupyter Notebook 커널('Python (MuJoCo Robotics)') 등록 중..." -ForegroundColor Cyan
uv run python -m ipykernel install --user --name mujoco-robotics --display-name "Python (MuJoCo Robotics)"

# 4. 설치 검증
Write-Host ""
Write-Host "[검증] 주요 패키지 임포트 확인 중..." -ForegroundColor Cyan
uv run python -c "import mujoco, dm_control, utils, controllers, tasks, numpy, jax, casadi, mediapy, imageio_ffmpeg; from tasks import task_suite; print(f'  - MuJoCo: {mujoco.__version__}\n  - 통합 패키지(src/tasks) 태스크: {len(task_suite.TASK_FACTORIES)}종 로드 완료\n  - NumPy: {numpy.__version__}\n  - JAX: {jax.__version__}\n  - CasADi: {casadi.__version__}\n  - FFmpeg(내장): {imageio_ffmpeg.get_ffmpeg_exe()}')"

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  환경 설정이 모두 완료되었습니다!" -ForegroundColor Green
Write-Host "  - 실습 노트북 경로: notebooks/01_... ~ 06_...ipynb" -ForegroundColor White
Write-Host "  - Jupyter Lab 실행: 'run_jupyter.bat' 더블클릭" -ForegroundColor White
Write-Host "  - 웹 문서 로컬 확인: 'run_docs.bat' 더블클릭 (http://127.0.0.1:8000)" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
