@echo off
REM ============================================================
REM NEW IN ROBOT - LISTAR CATEGORIAS
REM ============================================================
REM Lista todas las categorías de Tiendanube
REM ============================================================

cd /d "%~dp0\.."
python newin_robot.py list_cats --env config.env
pause
