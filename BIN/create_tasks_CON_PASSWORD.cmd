@echo off
REM ============================================================
REM NEW IN ROBOT - CONFIGURADOR DE TAREAS v2.2 CON PASSWORD
REM ============================================================
REM Esta version solicita tu contraseña para configurar las tareas
REM correctamente y que se ejecuten sin estar logueado
REM ============================================================

setlocal

echo.
echo ============================================================
echo NEW IN ROBOT - CONFIGURADOR DE TAREAS v2.2
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
if not exist "BIN\daily.cmd" (
    echo [ERROR] No se encuentra BIN\daily.cmd
    echo Ubicacion esperada: %PROJECT_DIR%\BIN\daily.cmd
    pause
    exit /b 1
)

if not exist "BIN\refresh.cmd" (
    echo [ERROR] No se encuentra BIN\refresh.cmd
    echo Ubicacion esperada: %PROJECT_DIR%\BIN\refresh.cmd
    pause
    exit /b 1
)

echo [INFO] Proyecto detectado en: %PROJECT_DIR%
echo [INFO] Usuario actual: %USERNAME%
echo.

REM ============================================================
REM SOLICITAR PASSWORD
REM ============================================================
echo ============================================================
echo CREDENCIALES REQUERIDAS
echo ============================================================
echo.
echo Para que las tareas se ejecuten automaticamente sin que
echo estes logueado, necesito tu contraseña de Windows.
echo.
echo [IMPORTANTE] La contraseña NO se guarda en ningun archivo.
echo Solo se usa para configurar las tareas programadas.
echo.
echo Usuario: %USERNAME%

REM Solicitar contraseña (PowerShell para entrada segura)
set "PSCOMMAND=powershell -Command "$password = Read-Host 'Contraseña' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password); [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)""

for /f "usebackq delims=" %%p in (`%PSCOMMAND%`) do set "USER_PASSWORD=%%p"

if "%USER_PASSWORD%"=="" (
    echo.
    echo [ERROR] No se ingreso contraseña
    pause
    exit /b 1
)

echo.
echo [OK] Contraseña recibida
echo.

REM ============================================================
REM LIMPIAR TAREAS VIEJAS
REM ============================================================
echo [CLEANUP] Eliminando tareas viejas (si existen)...
schtasks /Delete /TN "NewIn-Daily" /F >nul 2>&1
schtasks /Delete /TN "NewInDaily" /F >nul 2>&1
schtasks /Delete /TN "NewIn-WeeklyRefresh" /F >nul 2>&1
schtasks /Delete /TN "NewInWeeklyRefresh" /F >nul 2>&1
echo [OK] Limpieza completada
echo.

REM ============================================================
REM TAREA DIARIA CON PASSWORD
REM ============================================================
echo [1/2] Configurando tarea diaria...

schtasks /Create ^
    /SC DAILY ^
    /ST 18:00 ^
    /TN "NewInDaily" ^
    /TR "\"%PROJECT_DIR%\BIN\daily.cmd\"" ^
    /RU "%COMPUTERNAME%\%USERNAME%" ^
    /RP "%USER_PASSWORD%" ^
    /RL HIGHEST ^
    /F

if errorlevel 1 (
    echo [ERROR] Fallo al crear tarea diaria
    echo [INFO] Posibles causas:
    echo   - Contraseña incorrecta
    echo   - Permisos insuficientes
    echo.
    pause
    exit /b 1
)

REM Ajustar configuraciones avanzadas
schtasks /Change /TN "NewInDaily" /IT >nul 2>&1
schtasks /Change /TN "NewInDaily" /Z >nul 2>&1

echo [OK] Tarea diaria creada: NewInDaily (18:00 hs)
echo.

REM ============================================================
REM TAREA SEMANAL CON PASSWORD
REM ============================================================
echo [2/2] Configurando tarea semanal...

schtasks /Create ^
    /SC WEEKLY ^
    /D MON ^
    /ST 17:55 ^
    /TN "NewInWeeklyRefresh" ^
    /TR "\"%PROJECT_DIR%\BIN\refresh.cmd\"" ^
    /RU "%COMPUTERNAME%\%USERNAME%" ^
    /RP "%USER_PASSWORD%" ^
    /RL HIGHEST ^
    /F

if errorlevel 1 (
    echo [ERROR] Fallo al crear tarea semanal
    echo [INFO] Posibles causas:
    echo   - Contraseña incorrecta
    echo   - Permisos insuficientes
    echo.
    pause
    exit /b 1
)

REM Ajustar configuraciones avanzadas
schtasks /Change /TN "NewInWeeklyRefresh" /IT >nul 2>&1
schtasks /Change /TN "NewInWeeklyRefresh" /Z >nul 2>&1

echo [OK] Tarea semanal creada: NewInWeeklyRefresh (LUN 17:55 hs)
echo.

REM Limpiar variable de contraseña por seguridad
set "USER_PASSWORD="

REM ============================================================
REM CONFIGURACION MANUAL ADICIONAL
REM ============================================================
echo [CONFIG] Aplicando configuraciones avanzadas...
echo.
echo Las tareas fueron creadas con tu contraseña.
echo Ahora vamos a deshabilitar las restricciones de bateria.
echo.

REM Crear XML temporal para deshabilitar restricciones de batería
set DAILY_XML=%TEMP%\newin_daily_fix.xml

schtasks /Query /TN "NewInDaily" /XML > "%DAILY_XML%"

REM Usar PowerShell para modificar el XML
powershell -Command "(Get-Content '%DAILY_XML%') -replace '<DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>', '<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>' -replace '<StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>', '<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>' | Set-Content '%DAILY_XML%'"

schtasks /Create /TN "NewInDaily" /XML "%DAILY_XML%" /F /RU "%COMPUTERNAME%\%USERNAME%" /RP "%USER_PASSWORD%" >nul 2>&1

del "%DAILY_XML%"

REM Repetir para tarea semanal
set REFRESH_XML=%TEMP%\newin_refresh_fix.xml

schtasks /Query /TN "NewInWeeklyRefresh" /XML > "%REFRESH_XML%"

powershell -Command "(Get-Content '%REFRESH_XML%') -replace '<DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>', '<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>' -replace '<StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>', '<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>' | Set-Content '%REFRESH_XML%'"

schtasks /Create /TN "NewInWeeklyRefresh" /XML "%REFRESH_XML%" /F /RU "%COMPUTERNAME%\%USERNAME%" /RP "%USER_PASSWORD%" >nul 2>&1

del "%REFRESH_XML%"

echo [OK] Configuraciones avanzadas aplicadas
echo.

REM ============================================================
REM VERIFICACION FINAL
REM ============================================================
echo ============================================================
echo VERIFICANDO TAREAS CREADAS
echo ============================================================
echo.

echo Tarea diaria:
schtasks /Query /TN "NewInDaily" /FO LIST | findstr /C:"Nombre de tarea" /C:"Hora" /C:"Estado" /C:"Modo de inicio"
echo.

echo Tarea semanal:
schtasks /Query /TN "NewInWeeklyRefresh" /FO LIST | findstr /C:"Nombre de tarea" /C:"Hora" /C:"Estado" /C:"Modo de inicio"
echo.

REM ============================================================
REM RESUMEN
REM ============================================================
echo ============================================================
echo TAREAS CONFIGURADAS EXITOSAMENTE
echo ============================================================
echo.
echo Configuracion aplicada:
echo   [+] Ejecuta sin estar logueado (usa tu contraseña)
echo   [+] Sin restricciones de bateria
echo   [+] Ejecuta tareas perdidas automaticamente
echo   [+] Con privilegios elevados
echo.
echo Tareas creadas:
echo   1. NewInDaily (diaria 18:00 hs)
echo   2. NewInWeeklyRefresh (lunes 17:55 hs)
echo.
echo Proxima ejecucion daily: HOY 18:00
echo Proxima ejecucion refresh: Proximo lunes 17:55
echo.
echo Para verificar funcionamiento:
echo   cd "%PROJECT_DIR%\BIN"
echo   daily.cmd
echo.
echo Logs:
echo   - Daily:   logs\daily.log
echo   - Refresh: logs\refresh.log
echo   - Reportes: logs\reportes_diarios\
echo.

pause
