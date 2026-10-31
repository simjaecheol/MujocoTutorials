@echo off
chcp 65001 > nul
title MuJoCo Robotics Tutorials - Jupyter Lab
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    if exist "%USERPROFILE%\.local\bin\uv.exe" set "PATH=%USERPROFILE%\.local\bin;%PATH%"
    if exist "%USERPROFILE%\.cargo\bin\uv.exe" set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
)

if not exist ".venv" (
    echo [안내] 가상환경(.venv)이 없습니다. 먼저 환경을 설치합니다...
    call "%~dp0setup_env.bat"
)

echo Jupyter Lab을 시작합니다... (종료하려면 이 창에서 Ctrl+C를 누르세요)
uv run jupyter lab
pause

