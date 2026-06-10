@echo off
REM ============================================================
REM NEW IN ROBOT - INSTALADOR
REM ============================================================
REM Este script configura el proyecto por primera vez:
REM 1. Verifica Python
REM 2. Instala dependencias
REM 3. Crea directorios necesarios
REM 4. Verifica configuración
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo NEW IN ROBOT - INSTALADOR v11
echo ============================================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "newin_robot.py" (
    echo [ERROR] No se encuentra newin_robot.py
    echo Ejecuta este script desde la carpeta del proyecto.
    pause
    exit /b 1
)

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH
    echo Instala Python 3.8+ desde https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python %PYVER% encontrado
echo.

REM Instalar dependencias
echo [2/5] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install requests
if errorlevel 1 (
    echo [ERROR] Fallo instalacion de dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

REM Crear directorios
echo [3/5] Creando directorios...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "bin" mkdir bin
echo [OK] Directorios creados
echo.

REM Verificar config.env
echo [4/5] Verificando configuracion...
if not exist "config.env" (
    echo [WARN] No se encuentra config.env
    echo Copia el archivo de ejemplo y configuralo con tus credenciales.
    pause
)
echo.

REM Test de conexión
echo [5/5] Probando conexion...
python newin_robot.py who --env config.env
if errorlevel 1 (
    echo [WARN] Fallo el test de conexion
    echo Verifica tu configuracion en config.env
) else (
    echo [OK] Test de conexion exitoso
)
echo.

echo ============================================================
echo INSTALACION COMPLETA
echo ============================================================
echo.
echo Proximos pasos:
echo 1. Verifica config.env con tus credenciales
echo 2. Ejecuta: python newin_robot.py who --env config.env
echo 3. Ejecuta: python newin_robot.py daily --env config.env
echo 4. Configura las tareas programadas con bin\create_tasks.cmd
echo.

pause
