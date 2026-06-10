@echo off
REM ============================================================
REM NEW IN ROBOT - VERIFICAR CATEGORIA
REM ============================================================
REM Verifica que la categoría configurada existe en Tiendanube
REM ============================================================

cd /d "%~dp0\.."
python newin_robot.py check_cat --env config.env
pause
