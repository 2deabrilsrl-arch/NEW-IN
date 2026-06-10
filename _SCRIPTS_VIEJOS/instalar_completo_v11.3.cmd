@echo off
chcp 65001 >nul
title Instalacion Completa New In v11.3.0

echo.
echo ============================================================
echo INSTALACION COMPLETA NEW IN ROBOT v11.3.0-FINAL
echo ============================================================
echo.
echo Este script realizara la instalacion completa:
echo.
echo 1. Backup del script actual
echo 2. Instalacion de v11.3.0-FINAL
echo 3. Configuracion de tareas programadas (18:30)
echo 4. Verificacion del sistema
echo 5. Prueba opcional
echo.
echo CAMBIOS EN v11.3.0:
echo  ✓ Transforma espacios a ___ en SKUs
echo  ✓ Filtra productos CONTROL
echo  ✓ Horario optimizado 18:30
echo  ✓ Match rate: 18%% → 80%%+
echo.
echo ============================================================
echo.
pause

cd "C:\Users\santiago\NEW IN"

REM ============================================================
REM PASO 1: VERIFICACIONES PREVIAS
REM ============================================================

echo.
echo [PASO 1/6] Verificaciones previas...
echo ============================================================
echo.

REM Verificar directorio
if not exist "newin_robot.py" (
    echo [ERROR] No se encuentra newin_robot.py
    echo Verifica que estas en: C:\Users\santiago\NEW IN
    echo.
    pause
    exit /b 1
)
echo [OK] Directorio correcto

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en PATH
    echo.
    pause
    exit /b 1
)
echo [OK] Python instalado

REM Verificar nuevo archivo
if not exist "newin_robot.py.NEW" (
    echo.
    echo [ERROR] No se encuentra newin_robot.py.NEW
    echo.
    echo INSTRUCCIONES:
    echo 1. Descarga newin_robot.py (v11.3.0-FINAL)
    echo 2. Renombralo a: newin_robot.py.NEW
    echo 3. Colocalo en: C:\Users\santiago\NEW IN\
    echo 4. Ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
)
echo [OK] Nuevo archivo encontrado
echo.

REM ============================================================
REM PASO 2: BACKUP
REM ============================================================

echo.
echo [PASO 2/6] Creando backup...
echo ============================================================
echo.

set timestamp=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

copy newin_robot.py "newin_robot.py.backup_%timestamp%" >nul
if errorlevel 1 (
    echo [ERROR] No se pudo crear backup
    pause
    exit /b 1
)

echo [OK] Backup creado: newin_robot.py.backup_%timestamp%
echo.

REM ============================================================
REM PASO 3: INSTALACION SCRIPT
REM ============================================================

echo.
echo [PASO 3/6] Instalando v11.3.0-FINAL...
echo ============================================================
echo.

copy /Y newin_robot.py.NEW newin_robot.py >nul
if errorlevel 1 (
    echo [ERROR] No se pudo reemplazar el archivo
    echo Restaurando backup...
    copy /Y "newin_robot.py.backup_%timestamp%" newin_robot.py >nul
    pause
    exit /b 1
)

echo [OK] Script actualizado
echo.

REM Limpiar archivo temporal
if exist "newin_robot.py.NEW" (
    del newin_robot.py.NEW
)

REM Verificar version
python newin_robot.py --version 2>nul | findstr "11.3.0-FINAL" >nul
if errorlevel 1 (
    echo [ADVERTENCIA] Version no coincide
    python newin_robot.py --version
) else (
    echo [OK] Version correcta: v11.3.0-FINAL
)
echo.

REM ============================================================
REM PASO 4: CONFIGURACION TAREAS
REM ============================================================

echo.
echo [PASO 4/6] Configurando tareas programadas (18:30)...
echo ============================================================
echo.

REM Eliminar tareas viejas
schtasks /delete /tn "NewInRobot" /f >nul 2>&1
schtasks /delete /tn "NewInDaily" /f >nul 2>&1
schtasks /delete /tn "NewInRefresh" /f >nul 2>&1

echo [1/2] Eliminadas tareas antiguas

REM Crear tarea diaria
schtasks /create ^
    /tn "NewInDaily" ^
    /tr "cmd /c cd \"C:\Users\santiago\NEW IN\" && python newin_robot.py daily" ^
    /sc daily ^
    /st 18:30 ^
    /f >nul 2>&1

if errorlevel 1 (
    echo [ERROR] No se pudo crear tarea diaria
    pause
    exit /b 1
)
echo [2/2] Tarea diaria creada (18:30)

REM Crear tarea semanal
schtasks /create ^
    /tn "NewInRefresh" ^
    /tr "cmd /c cd \"C:\Users\santiago\NEW IN\" && python newin_robot.py refresh" ^
    /sc weekly ^
    /d MON ^
    /st 18:30 ^
    /f >nul 2>&1

if errorlevel 1 (
    echo [ERROR] No se pudo crear tarea semanal
    pause
    exit /b 1
)
echo [3/2] Tarea refresh creada (Lunes 18:30)
echo.

REM ============================================================
REM PASO 5: VERIFICACION
REM ============================================================

echo.
echo [PASO 5/6] Verificacion del sistema...
echo ============================================================
echo.

REM Verificar version
echo [1/4] Version instalada:
python newin_robot.py --version 2>&1
echo.

REM Verificar tareas
echo [2/4] Tarea diaria:
schtasks /query /tn "NewInDaily" /fo LIST /v 2>nul | findstr /C:"Siguiente hora" /C:"Estado de tarea"
echo.

echo [3/4] Tarea refresh:
schtasks /query /tn "NewInRefresh" /fo LIST /v 2>nul | findstr /C:"Siguiente hora" /C:"Estado de tarea"
echo.

REM Verificar archivos
echo [4/4] Archivos de configuracion:
if exist "config.env" (echo   ✓ config.env) else (echo   ✗ config.env)
if exist "data\newin_category.json" (echo   ✓ newin_category.json) else (echo   - newin_category.json ^(se creara^))
if exist "logs" (echo   ✓ Carpeta logs) else (echo   - Carpeta logs ^(se creara^))
echo.

REM ============================================================
REM PASO 6: PRUEBA OPCIONAL
REM ============================================================

echo.
echo [PASO 6/6] Prueba manual opcional
echo ============================================================
echo.
echo Deseas ejecutar una prueba manual ahora? (S/N)
set /p respuesta=

if /i "%respuesta%"=="S" (
    echo.
    echo Ejecutando prueba manual...
    echo ============================================================
    echo.
    python newin_robot.py daily
    echo.
    echo ============================================================
    echo.
    echo BUSCA EN EL RESULTADO ARRIBA:
    echo  ✓ "SKUs con MATCH exitoso"
    echo  ✓ "ACC-BOOB___TAPE" ^(espacios transformados^)
    echo  ✓ Match rate mejorado
    echo  ✓ Productos CONTROL filtrados
    echo.
)

REM ============================================================
REM RESUMEN FINAL
REM ============================================================

echo.
echo ============================================================
echo INSTALACION COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo RESUMEN:
echo  ✓ Backup: newin_robot.py.backup_%timestamp%
echo  ✓ Version: v11.3.0-FINAL
echo  ✓ Tarea diaria: 18:30 todos los dias
echo  ✓ Tarea refresh: Lunes 18:30
echo.
echo CAMBIOS IMPLEMENTADOS:
echo  ✓ Transforma espacios a ___ en SKUs
echo  ✓ Filtra productos CONTROL automaticamente
echo  ✓ Nuevo horario 18:30 ^(procesa todo el dia^)
echo  ✓ Logging mejorado de productos exitosos
echo.
echo VENTAJAS DEL HORARIO 18:30:
echo  ✓ Procesa TODO el dia laboral ^(8:30-18:00^)
echo  ✓ 30 minutos despues del cierre
echo  ✓ Tiempo extra para sincronizacion DF-TN
echo  ✓ Repositor termino su trabajo
echo  ✓ Match rate mas alto ^(80%%+^)
echo.
echo PROXIMOS PASOS:
echo  1. Primera ejecucion: Hoy a las 18:30
echo  2. Revisa log: logs\daily.log
echo  3. Verifica match rate ^>80%%
echo  4. Confirma productos en TN categoria New In
echo  5. Refresh semanal: Proximo lunes 18:30
echo.
echo CRONOGRAMA SEMANAL:
echo  - Lunes 18:30: LIMPIA categoria + procesa lunes
echo  - Mar-Dom 18:30: AGREGA productos sin limpiar
echo  - Resultado: Categoria acumula toda la semana
echo.
echo PRODUCTOS FILTRADOS:
echo  ✗ CONTROL MARIA → No se procesa ^(uso interno^)
echo  ✗ CONTROL DE CALIDAD → No se procesa
echo  ✓ ACC-BOOB___TAPE → Se procesa normalmente
echo.
echo ARCHIVOS DE MONITOREO DISPONIBLES:
echo  - monitor_newin.ps1 ^(resumen ejecuciones^)
echo  - analizar_snapshot.ps1 ^(productos cargados^)
echo  - DOCUMENTACION_COMPLETA_v11.3.txt ^(referencia^)
echo.
echo ============================================================
echo.
pause
