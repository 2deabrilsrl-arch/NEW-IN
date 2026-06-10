@echo off
REM ============================================================
REM NEW IN ROBOT - REFRESH SEMANAL
REM ============================================================
REM Este script ejecuta el flujo semanal (lunes):
REM - Limpia la categoría NEW IN de todos los productos
REM - Resetea el estado para empezar la semana fresco
REM - Ejecuta el daily update inmediatamente después
REM ============================================================

setlocal

REM Cambiar a directorio del proyecto
cd /d "%~dp0\.."

REM Configurar paths
set PROJECT_DIR=%CD%
set LOG_FILE=%PROJECT_DIR%\logs\refresh.log
set CONFIG_FILE=%PROJECT_DIR%\config.env

REM Verificar archivos
if not exist "%CONFIG_FILE%" (
    echo [ERROR] No se encuentra config.env
    echo Ubicacion esperada: %CONFIG_FILE%
    exit /b 1
)

if not exist "newin_robot.py" (
    echo [ERROR] No se encuentra newin_robot.py
    echo Ubicacion esperada: %PROJECT_DIR%\newin_robot.py
    exit /b 1
)

REM Crear timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set DATE=%%c-%%b-%%a
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set TIME=%%a:%%b
)

REM Log header
echo. >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"
echo WEEKLY REFRESH - %DATE% %TIME% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"

REM Ejecutar refresh
python newin_robot.py refresh --env "%CONFIG_FILE%" >> "%LOG_FILE%" 2>&1

REM Capturar resultado
set RESULT=%errorlevel%

REM Log footer
echo. >> "%LOG_FILE%"
echo [RESULT] Exit code: %RESULT% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"

if %RESULT% equ 0 (
    echo [SUCCESS] Refresh completado - Ver: %LOG_FILE%
    
    REM Si refresh OK, ejecutar daily inmediatamente
    echo [INFO] Ejecutando daily update...
    call "%~dp0daily.cmd"
    
) else (
    echo [ERROR] Refresh fallo con codigo %RESULT% - Ver: %LOG_FILE%
)

exit /b %RESULT%
