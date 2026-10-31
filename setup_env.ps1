# Windows용 MuJoCo 로보틱스 학습 환경 자동 구축 스크립트 (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  MuJoCo Robotics Tutorials - Windows 환경 자동 설치" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 현재 스크립트가 위치한 폴더로 이동
Set-Location -Path $PSScriptRoot

# 1. uv 설치 여부 확인 및 자동 설치
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    # 기본 설치 경로 확인
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

# 2. Python 3.11 및 가상환경(.venv) 패키지 동기화
Write-Host ""
Write-Host "[2/3] Python 3.11 및 로보틱스 필수 패키지(MuJoCo, JAX, CasADi, Jupyter 등) 설치 중..." -ForegroundColor Cyan
uv sync

# 3. Jupyter 커널 등록
Write-Host ""
Write-Host "[3/3] Jupyter Notebook 커널('Python (MuJoCo Robotics)') 등록 중..." -ForegroundColor Cyan
uv run python -m ipykernel install --user --name mujoco-robotics --display-name "Python (MuJoCo Robotics)"

# 4. 설치 검증
Write-Host ""
Write-Host "[검증] 주요 패키지 임포트 확인 중..." -ForegroundColor Cyan
uv run python -c "import mujoco, numpy, jax, casadi, mediapy, imageio_ffmpeg; print(f'  - MuJoCo: {mujoco.__version__}\n  - NumPy: {numpy.__version__}\n  - JAX: {jax.__version__}\n  - CasADi: {casadi.__version__}\n  - FFmpeg(내장): {imageio_ffmpeg.get_ffmpeg_exe()}')"

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  환경 설정이 모두 완료되었습니다!" -ForegroundColor Green
Write-Host "  - VS Code / Cursor / Antigravity에서 .ipynb 파일을 열고" -ForegroundColor White
Write-Host "    커널로 '.venv (Python 3.11)' 또는 'Python (MuJoCo Robotics)'를 선택하세요." -ForegroundColor White
Write-Host "  - 브라우저에서 실행하려면 'run_jupyter.bat'을 실행하거나" -ForegroundColor White
Write-Host "    터미널에 'uv run jupyter lab'을 입력하세요." -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green

