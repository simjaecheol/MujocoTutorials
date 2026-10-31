@echo off
chcp 65001 > nul
title MuJoCo Robotics Tutorials - Web Documentation Server
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

echo ==========================================================
echo   웹 문서 서버(MkDocs)를 시작합니다...
echo   브라우저에서 http://127.0.0.1:8000 으로 접속하세요.
echo   (종료하려면 이 창에서 Ctrl+C를 누르세요)
echo ==========================================================
uv run mkdocs serve
pause

