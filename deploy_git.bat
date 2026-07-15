@echo off
python deploy_git.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Execution failed.
)
pause
