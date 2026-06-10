@echo off
REM ============================================================
REM NEW IN ROBOT - CONFIGURADOR DE TAREAS MEJORADO v2.0
REM ============================================================
REM CORRECCIONES:
REM - Ejecuta sin restricciones de bateria
REM - Ejecuta aunque el usuario no este logueado
REM - Ejecuta tareas perdidas automaticamente
REM - Usa rutas con comillas correctas
REM - Horarios: Daily 18:00, Refresh 17:55 (lunes)
REM ============================================================

setlocal

echo.
echo ============================================================
echo NEW IN ROBOT - CONFIGURADOR DE TAREAS v2.0
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
REM TAREA DIARIA
REM ============================================================
echo [1/2] Configurando tarea diaria...

REM Crear XML temporal para configuracion avanzada
set DAILY_XML=%TEMP%\newin_daily.xml

echo ^<?xml version="1.0" encoding="UTF-16"?^> > "%DAILY_XML%"
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^> >> "%DAILY_XML%"
echo   ^<RegistrationInfo^> >> "%DAILY_XML%"
echo     ^<Description^>Sincronizacion diaria de productos New In desde Dragonfish a Tiendanube^</Description^> >> "%DAILY_XML%"
echo   ^</RegistrationInfo^> >> "%DAILY_XML%"
echo   ^<Triggers^> >> "%DAILY_XML%"
echo     ^<CalendarTrigger^> >> "%DAILY_XML%"
echo       ^<StartBoundary^>2026-02-04T18:00:00^</StartBoundary^> >> "%DAILY_XML%"
echo       ^<ExecutionTimeLimit^>PT1H^</ExecutionTimeLimit^> >> "%DAILY_XML%"
echo       ^<Enabled^>true^</Enabled^> >> "%DAILY_XML%"
echo       ^<ScheduleByDay^> >> "%DAILY_XML%"
echo         ^<DaysInterval^>1^</DaysInterval^> >> "%DAILY_XML%"
echo       ^</ScheduleByDay^> >> "%DAILY_XML%"
echo     ^</CalendarTrigger^> >> "%DAILY_XML%"
echo   ^</Triggers^> >> "%DAILY_XML%"
echo   ^<Principals^> >> "%DAILY_XML%"
echo     ^<Principal^> >> "%DAILY_XML%"
echo       ^<LogonType^>Password^</LogonType^> >> "%DAILY_XML%"
echo       ^<RunLevel^>HighestAvailable^</RunLevel^> >> "%DAILY_XML%"
echo     ^</Principal^> >> "%DAILY_XML%"
echo   ^</Principals^> >> "%DAILY_XML%"
echo   ^<Settings^> >> "%DAILY_XML%"
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^> >> "%DAILY_XML%"
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^> >> "%DAILY_XML%"
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^> >> "%DAILY_XML%"
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^> >> "%DAILY_XML%"
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^> >> "%DAILY_XML%"
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^> >> "%DAILY_XML%"
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^> >> "%DAILY_XML%"
echo     ^<Enabled^>true^</Enabled^> >> "%DAILY_XML%"
echo     ^<Hidden^>false^</Hidden^> >> "%DAILY_XML%"
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^> >> "%DAILY_XML%"
echo     ^<WakeToRun^>false^</WakeToRun^> >> "%DAILY_XML%"
echo     ^<ExecutionTimeLimit^>PT72H^</ExecutionTimeLimit^> >> "%DAILY_XML%"
echo     ^<Priority^>7^</Priority^> >> "%DAILY_XML%"
echo   ^</Settings^> >> "%DAILY_XML%"
echo   ^<Actions^> >> "%DAILY_XML%"
echo     ^<Exec^> >> "%DAILY_XML%"
echo       ^<Command^>"%PROJECT_DIR%\BIN\daily.cmd"^</Command^> >> "%DAILY_XML%"
echo       ^<WorkingDirectory^>%PROJECT_DIR%^</WorkingDirectory^> >> "%DAILY_XML%"
echo     ^</Exec^> >> "%DAILY_XML%"
echo   ^</Actions^> >> "%DAILY_XML%"
echo ^</Task^> >> "%DAILY_XML%"

REM Crear tarea desde XML
schtasks /Create /TN "NewInDaily" /XML "%DAILY_XML%" /F

if errorlevel 1 (
    echo [ERROR] Fallo al crear tarea diaria
    del "%DAILY_XML%"
    pause
    exit /b 1
)

del "%DAILY_XML%"
echo [OK] Tarea diaria creada: NewInDaily (18:00 hs, todos los dias)
echo.

REM ============================================================
REM TAREA SEMANAL (LUNES)
REM ============================================================
echo [2/2] Configurando tarea semanal...

REM Crear XML temporal para configuracion avanzada
set REFRESH_XML=%TEMP%\newin_refresh.xml

echo ^<?xml version="1.0" encoding="UTF-16"?^> > "%REFRESH_XML%"
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^> >> "%REFRESH_XML%"
echo   ^<RegistrationInfo^> >> "%REFRESH_XML%"
echo     ^<Description^>Limpieza semanal (lunes) de la categoria New In antes de la sincronizacion diaria^</Description^> >> "%REFRESH_XML%"
echo   ^</RegistrationInfo^> >> "%REFRESH_XML%"
echo   ^<Triggers^> >> "%REFRESH_XML%"
echo     ^<CalendarTrigger^> >> "%REFRESH_XML%"
echo       ^<StartBoundary^>2026-02-09T17:55:00^</StartBoundary^> >> "%REFRESH_XML%"
echo       ^<ExecutionTimeLimit^>PT1H^</ExecutionTimeLimit^> >> "%REFRESH_XML%"
echo       ^<Enabled^>true^</Enabled^> >> "%REFRESH_XML%"
echo       ^<ScheduleByWeek^> >> "%REFRESH_XML%"
echo         ^<DaysOfWeek^> >> "%REFRESH_XML%"
echo           ^<Monday /^> >> "%REFRESH_XML%"
echo         ^</DaysOfWeek^> >> "%REFRESH_XML%"
echo         ^<WeeksInterval^>1^</WeeksInterval^> >> "%REFRESH_XML%"
echo       ^</ScheduleByWeek^> >> "%REFRESH_XML%"
echo     ^</CalendarTrigger^> >> "%REFRESH_XML%"
echo   ^</Triggers^> >> "%REFRESH_XML%"
echo   ^<Principals^> >> "%REFRESH_XML%"
echo     ^<Principal^> >> "%REFRESH_XML%"
echo       ^<LogonType^>Password^</LogonType^> >> "%REFRESH_XML%"
echo       ^<RunLevel^>HighestAvailable^</RunLevel^> >> "%REFRESH_XML%"
echo     ^</Principal^> >> "%REFRESH_XML%"
echo   ^</Principals^> >> "%REFRESH_XML%"
echo   ^<Settings^> >> "%REFRESH_XML%"
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^> >> "%REFRESH_XML%"
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^> >> "%REFRESH_XML%"
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^> >> "%REFRESH_XML%"
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^> >> "%REFRESH_XML%"
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^> >> "%REFRESH_XML%"
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^> >> "%REFRESH_XML%"
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^> >> "%REFRESH_XML%"
echo     ^<Enabled^>true^</Enabled^> >> "%REFRESH_XML%"
echo     ^<Hidden^>false^</Hidden^> >> "%REFRESH_XML%"
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^> >> "%REFRESH_XML%"
echo     ^<WakeToRun^>false^</WakeToRun^> >> "%REFRESH_XML%"
echo     ^<ExecutionTimeLimit^>PT72H^</ExecutionTimeLimit^> >> "%REFRESH_XML%"
echo     ^<Priority^>7^</Priority^> >> "%REFRESH_XML%"
echo   ^</Settings^> >> "%REFRESH_XML%"
echo   ^<Actions^> >> "%REFRESH_XML%"
echo     ^<Exec^> >> "%REFRESH_XML%"
echo       ^<Command^>"%PROJECT_DIR%\BIN\refresh.cmd"^</Command^> >> "%REFRESH_XML%"
echo       ^<WorkingDirectory^>%PROJECT_DIR%^</WorkingDirectory^> >> "%REFRESH_XML%"
echo     ^</Exec^> >> "%REFRESH_XML%"
echo   ^</Actions^> >> "%REFRESH_XML%"
echo ^</Task^> >> "%REFRESH_XML%"

REM Crear tarea desde XML
schtasks /Create /TN "NewInWeeklyRefresh" /XML "%REFRESH_XML%" /F

if errorlevel 1 (
    echo [ERROR] Fallo al crear tarea semanal
    del "%REFRESH_XML%"
    pause
    exit /b 1
)

del "%REFRESH_XML%"
echo [OK] Tarea semanal creada: NewInWeeklyRefresh (LUN 17:55 hs)
echo.

REM ============================================================
REM VERIFICACION
REM ============================================================
echo ============================================================
echo VERIFICANDO TAREAS CREADAS
echo ============================================================
echo.

schtasks /Query /TN "NewInDaily" /FO LIST | findstr /C:"Nombre de tarea" /C:"Hora" /C:"Estado"
echo.
schtasks /Query /TN "NewInWeeklyRefresh" /FO LIST | findstr /C:"Nombre de tarea" /C:"Hora" /C:"Estado"
echo.

REM ============================================================
REM RESUMEN
REM ============================================================
echo ============================================================
echo TAREAS CONFIGURADAS EXITOSAMENTE
echo ============================================================
echo.
echo Configuracion aplicada:
echo   [+] Sin restricciones de bateria
echo   [+] Ejecuta aunque no estes logueado
echo   [+] Ejecuta tareas perdidas automaticamente
echo   [+] Sin condiciones de red o inactividad
echo.
echo Tareas creadas:
echo   1. NewInDaily (diaria 18:00 hs)
echo   2. NewInWeeklyRefresh (lunes 17:55 hs)
echo.
echo Proxima ejecucion daily: HOY 18:00
echo Proxima ejecucion refresh: Proximo lunes 17:55
echo.
echo Para verificar las tareas:
echo   - Abri "Programador de tareas" (taskschd.msc)
echo   - Busca "NewIn" en la lista
echo.
echo Para ejecutar manualmente:
echo   - Daily:   BIN\daily.cmd
echo   - Refresh: BIN\refresh.cmd
echo.
echo Para ver logs:
echo   - Daily:   logs\daily.log
echo   - Refresh: logs\refresh.log
echo   - Reportes: logs\reportes_diarios\
echo.

pause
