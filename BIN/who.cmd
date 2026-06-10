@echo off
REM ============================================================
REM NEW IN ROBOT - WHO AM I
REM ============================================================
REM Muestra información de conexión y realiza test básico
REM ============================================================

cd /d "%~dp0\.."
python newin_robot.py who --env config.env
pause
