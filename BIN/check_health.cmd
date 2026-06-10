@echo off
REM ============================================================
REM NEW IN ROBOT - DIAGNOSTICO DE SALUD
REM ============================================================
REM Este script verifica el estado completo del sistema:
REM - Conexión a APIs
REM - Archivos de configuración
REM - Directorios
REM - Estado de tareas programadas
REM - Logs recientes
REM ============================================================

setlocal enabledelayedexpansion

cd /d "%~dp0\.."
set PROJECT_DIR=%CD%

echo.
echo ============================================================
echo NEW IN ROBOT - DIAGNOSTICO DE SALUD
echo ============================================================
echo.
echo Proyecto: %PROJECT_DIR%
echo Fecha: %date% %time%
echo.

REM ============================================================
REM 1. VERIFICAR ARCHIVOS
REM ============================================================
echo [1/7] Verificando archivos...
set MISSING=0

if not exist "newin_robot.py" (
    echo [ERROR] newin_robot.py no encontrado
    set MISSING=1
)

if not exist "config.env" (
    echo [ERROR] config.env no encontrado
    set MISSING=1
)

if not exist "bin\daily.cmd" (
    echo [WARN] bin\daily.cmd no encontrado
)

if not exist "bin\refresh.cmd" (
    echo [WARN] bin\refresh.cmd no encontrado
)

if %MISSING% equ 1 (
    echo [ERROR] Faltan archivos criticos
    pause
    exit /b 1
)

echo [OK] Archivos principales presentes
echo.

REM ============================================================
REM 2. VERIFICAR DIRECTORIOS
REM ============================================================
echo [2/7] Verificando directorios...

if not exist "data" (
    echo [WARN] Directorio data\ no existe, creando...
    mkdir data
)

if not exist "logs" (
    echo [WARN] Directorio logs\ no existe, creando...
    mkdir logs
)

echo [OK] Directorios OK
echo.

REM ============================================================
REM 3. VERIFICAR PYTHON
REM ============================================================
echo [3/7] Verificando Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH
    echo Instala Python 3.8+ desde https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do (
    echo [OK] Python %%i encontrado
)
echo.

REM ============================================================
REM 4. VERIFICAR DEPENDENCIAS
REM ============================================================
echo [4/7] Verificando dependencias...

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Modulo 'requests' no instalado
    echo Ejecuta: python -m pip install requests
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.

REM ============================================================
REM 5. TEST DE CONEXIÓN
REM ============================================================
echo [5/7] Probando conexion a APIs...

python newin_robot.py who --env config.env
set RESULT=%errorlevel%

if %RESULT% neq 0 (
    echo [WARN] Fallo el test de conexion (codigo %RESULT%)
    echo Verifica config.env
) else (
    echo [OK] Conexion exitosa
)
echo.

REM ============================================================
REM 6. VERIFICAR TAREAS PROGRAMADAS
REM ============================================================
echo [6/7] Verificando tareas programadas...

schtasks /Query /TN "NewIn-Daily" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Tarea NewIn-Daily no encontrada
    echo Ejecuta bin\create_tasks.cmd para crearla
) else (
    echo [OK] Tarea NewIn-Daily existe
)

schtasks /Query /TN "NewIn-WeeklyRefresh" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Tarea NewIn-WeeklyRefresh no encontrada
    echo Ejecuta bin\create_tasks.cmd para crearla
) else (
    echo [OK] Tarea NewIn-WeeklyRefresh existe
)
echo.

REM ============================================================
REM 7. VERIFICAR LOGS RECIENTES
REM ============================================================
echo [7/7] Verificando logs recientes...

if exist "logs\daily.log" (
    for %%F in (logs\daily.log) do (
        echo [INFO] daily.log - Tamano: %%~zF bytes - Modificado: %%~tF
    )
) else (
    echo [INFO] daily.log aun no existe (primera ejecucion pendiente)
)

if exist "logs\refresh.log" (
    for %%F in (logs\refresh.log) do (
        echo [INFO] refresh.log - Tamano: %%~zF bytes - Modificado: %%~tF
    )
) else (
    echo [INFO] refresh.log aun no existe (primera ejecucion pendiente)
)
echo.

REM ============================================================
REM ESTADO
REM ============================================================
if exist "data\state.json" (
    echo Estado guardado:
    type "data\state.json"
    echo.
) else (
    echo [INFO] Sin estado guardado (primera ejecucion pendiente)
)

echo.
echo ============================================================
echo DIAGNOSTICO COMPLETO
echo ============================================================
echo.

pause
