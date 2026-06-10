@echo off
REM ============================================================
REM NEW IN ROBOT - CONFIGURADOR DE TAREAS v2.3 EDITABLE
REM ============================================================
REM INSTRUCCIONES:
REM 1. Abri este archivo con bloc de notas (clic derecho -> Editar)
REM 2. En la linea 17, donde dice TU_PASSWORD_AQUI, pone tu contraseña
REM 3. Guarda el archivo
REM 4. Ejecuta como Administrador
REM 5. DESPUES DE EJECUTAR, BORRA TU CONTRASEÑA DE LA LINEA 17
REM ============================================================

setlocal

REM ===== EDITA ESTA LINEA CON TU CONTRASEÑA =====
set "USER_PASSWORD=TU_PASSWORD_AQUI"
REM ===============================================

echo.
echo ============================================================
echo NEW IN ROBOT - CONFIGURADOR DE TAREAS v2.3
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

REM Verificar que se haya configurado la contraseña
if "%USER_PASSWORD%"=="TU_PASSWORD_AQUI" (
    echo [ERROR] Debes editar el archivo y configurar tu contraseña
    echo.
    echo Instrucciones:
    echo 1. Clic derecho en este archivo -^> Editar
    echo 2. Busca la linea 17: set "USER_PASSWORD=TU_PASSWORD_AQUI"
    echo 3. Reemplaza TU_PASSWORD_AQUI con tu contraseña real
    echo 4. Guarda el archivo
    echo 5. Ejecuta nuevamente como Administrador
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
echo [INFO] Contraseña configurada: OK
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
    echo   - Contraseña incorrecta (verifica la linea 17 del script)
    echo   - Usuario incorrecto (actual: %COMPUTERNAME%\%USERNAME%)
    echo   - Permisos insuficientes
    echo.
    pause
    exit /b 1
)

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
    echo   - Contraseña incorrecta (verifica la linea 17 del script)
    echo   - Usuario incorrecto (actual: %COMPUTERNAME%\%USERNAME%)
    echo   - Permisos insuficientes
    echo.
    pause
    exit /b 1
)

echo [OK] Tarea semanal creada: NewInWeeklyRefresh (LUN 17:55 hs)
echo.

REM Limpiar variable de contraseña por seguridad
set "USER_PASSWORD="

REM ============================================================
REM AJUSTES FINALES
REM ============================================================
echo [CONFIG] Aplicando configuraciones avanzadas...

REM Habilitar ejecucion sin usuario y tareas perdidas
schtasks /Change /TN "NewInDaily" /IT >nul 2>&1
schtasks /Change /TN "NewInDaily" /Z >nul 2>&1

schtasks /Change /TN "NewInWeeklyRefresh" /IT >nul 2>&1
schtasks /Change /TN "NewInWeeklyRefresh" /Z >nul 2>&1

echo [OK] Configuraciones aplicadas
echo.

REM ============================================================
REM VERIFICACION FINAL
REM ============================================================
echo ============================================================
echo VERIFICANDO TAREAS CREADAS
echo ============================================================
echo.

echo Tarea diaria:
schtasks /Query /TN "NewInDaily" /FO LIST | findstr /C:"Nombre de tarea" /C:"Hora" /C:"Estado"
echo.

echo Tarea semanal:
schtasks /Query /TN "NewInWeeklyRefresh" /FO LIST | findstr /C:"Nombre de tarea" /C:"Hora" /C:"Estado"
echo.

REM ============================================================
REM RECORDATORIO DE SEGURIDAD
REM ============================================================
echo ============================================================
echo IMPORTANTE - SEGURIDAD
echo ============================================================
echo.
echo [!!!] AHORA DEBES HACER LO SIGUIENTE:
echo.
echo 1. Abri este archivo con bloc de notas (clic derecho -^> Editar)
echo 2. En la linea 17, BORRA tu contraseña
echo 3. Deja la linea asi: set "USER_PASSWORD=TU_PASSWORD_AQUI"
echo 4. Guarda el archivo
echo.
echo [CRITICO] No dejes tu contraseña guardada en el archivo
echo.

REM ============================================================
REM AJUSTE MANUAL OPCIONAL
REM ============================================================
echo ============================================================
echo CONFIGURACION OPCIONAL
echo ============================================================
echo.
echo Si tenes una laptop y queres que las tareas se ejecuten
echo incluso cuando esta desenchufada, hace esto:
echo.
echo 1. Abri "Programador de tareas" (taskschd.msc)
echo 2. Busca "NewInDaily"
echo 3. Propiedades -^> Condiciones
echo 4. Desmarca: "Iniciar solo si esta conectado a corriente"
echo 5. Repeti para "NewInWeeklyRefresh"
echo.

REM ============================================================
REM RESUMEN
REM ============================================================
echo ============================================================
echo TAREAS CONFIGURADAS EXITOSAMENTE
echo ============================================================
echo.
echo Tareas creadas:
echo   1. NewInDaily (diaria 18:00 hs)
echo   2. NewInWeeklyRefresh (lunes 17:55 hs)
echo.
echo Proxima ejecucion daily: HOY 18:00
echo Proxima ejecucion refresh: Proximo lunes 17:55
echo.
echo Para probar manualmente:
echo   cd "%PROJECT_DIR%\BIN"
echo   daily.cmd
echo.
echo Logs:
echo   - Daily:   logs\daily.log
echo   - Reportes: logs\reportes_diarios\
echo.

pause
