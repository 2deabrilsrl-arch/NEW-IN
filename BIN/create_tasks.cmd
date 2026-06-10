@echo off
REM ============================================================
REM NEW IN ROBOT - CREADOR DE TAREAS PROGRAMADAS
REM ============================================================
REM Este script crea las tareas programadas en Windows:
REM - NewIn-Daily: Ejecuta todos los días a las 14:00
REM - NewIn-WeeklyRefresh: Ejecuta los lunes a las 14:00
REM
REM IMPORTANTE: Debe ejecutarse como Administrador
REM ============================================================

setlocal

echo.
echo ============================================================
echo NEW IN ROBOT - CONFIGURADOR DE TAREAS
echo ============================================================
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script requiere permisos de Administrador
    echo.
    echo Haz clic derecho en el archivo y selecciona:
    echo "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

REM Cambiar a directorio del proyecto
cd /d "%~dp0\.."
set PROJECT_DIR=%CD%

REM Verificar archivos necesarios
if not exist "bin\daily.cmd" (
    echo [ERROR] No se encuentra bin\daily.cmd
    echo Ubicacion esperada: %PROJECT_DIR%\bin\daily.cmd
    pause
    exit /b 1
)

if not exist "bin\refresh.cmd" (
    echo [ERROR] No se encuentra bin\refresh.cmd
    echo Ubicacion esperada: %PROJECT_DIR%\bin\refresh.cmd
    pause
    exit /b 1
)

echo [INFO] Proyecto detectado en: %PROJECT_DIR%
echo.

REM ============================================================
REM TAREA DIARIA
REM ============================================================
echo [1/2] Configurando tarea diaria...

REM Eliminar tarea existente si existe
schtasks /Delete /TN "NewIn-Daily" /F >nul 2>&1

REM Crear tarea diaria a las 14:00
schtasks /Create ^
    /SC DAILY ^
    /ST 14:00 ^
    /TN "NewIn-Daily" ^
    /TR "\"%PROJECT_DIR%\bin\daily.cmd\"" ^
    /RL HIGHEST ^
    /F

if errorlevel 1 (
    echo [ERROR] Fallo al crear tarea diaria
    pause
    exit /b 1
)

echo [OK] Tarea diaria creada: NewIn-Daily (14:00 hs)
echo.

REM ============================================================
REM TAREA SEMANAL (LUNES)
REM ============================================================
echo [2/2] Configurando tarea semanal...

REM Eliminar tarea existente si existe
schtasks /Delete /TN "NewIn-WeeklyRefresh" /F >nul 2>&1

REM Crear tarea semanal los lunes a las 14:00
schtasks /Create ^
    /SC WEEKLY ^
    /D MON ^
    /ST 14:00 ^
    /TN "NewIn-WeeklyRefresh" ^
    /TR "\"%PROJECT_DIR%\bin\refresh.cmd\"" ^
    /RL HIGHEST ^
    /F

if errorlevel 1 (
    echo [ERROR] Fallo al crear tarea semanal
    pause
    exit /b 1
)

echo [OK] Tarea semanal creada: NewIn-WeeklyRefresh (LUN 14:00 hs)
echo.

REM ============================================================
REM RESUMEN
REM ============================================================
echo ============================================================
echo TAREAS CONFIGURADAS EXITOSAMENTE
echo ============================================================
echo.
echo Tareas creadas:
echo   1. NewIn-Daily (diaria 14:00)
echo   2. NewIn-WeeklyRefresh (lunes 14:00)
echo.
echo Para verificar las tareas:
echo   - Abri "Programador de tareas" en Windows
echo   - Busca "NewIn" en la lista
echo.
echo Para ejecutar manualmente:
echo   - Daily:   bin\daily.cmd
echo   - Refresh: bin\refresh.cmd
echo.
echo Para ver logs:
echo   - Daily:   logs\daily.log
echo   - Refresh: logs\refresh.log
echo.

pause
