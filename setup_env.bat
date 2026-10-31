@echo off
chcp 65001 > nul
title MuJoCo Robotics Tutorials - Setup Environment
echo ==========================================================
echo   MuJoCo Robotics Tutorials - Windows 환경 자동 설치
echo ==========================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_env.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [오류] 설치 중 문제가 발생했습니다. 위 오류 메시지를 확인해 주세요.
    pause
    exit /b %ERRORLEVEL%
)

echo.
pause

