@echo off
chcp 65001 >nul
title Configurar Tareas New In - 18:30

echo.
echo ============================================================
echo CONFIGURACION DE TAREAS PROGRAMADAS NEW IN
echo Horario: 18:30 (fin de jornada laboral)
echo ============================================================
echo.
echo Este script creara dos tareas programadas:
echo.
echo 1. TAREA DIARIA (18:30 todos los dias)
echo    - Procesa ingresos del dia
echo    - Asigna productos a categoria New In
echo.
echo 2. TAREA SEMANAL REFRESH (Lunes 18:30)
echo    - Limpia categoria New In
echo    - Resetea estado para nueva semana
echo.
echo ============================================================
echo.
pause

cd "C:\Users\santiago\NEW IN"

REM Verificar que el script existe
if not exist "newin_robot.py" (
    echo [ERROR] No se encuentra newin_robot.py
    echo Verifica que estas en: C:\Users\santiago\NEW IN
    pause
    exit /b 1
)

REM Verificar ruta de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en PATH
    echo Instala Python 3.x y agregalo al PATH
    pause
    exit /b 1
)

echo.
echo [1/3] Eliminando tareas existentes (si existen)...
echo.

REM Eliminar tareas viejas si existen
schtasks /delete /tn "NewInRobot" /f >nul 2>&1
schtasks /delete /tn "NewInRefresh" /f >nul 2>&1
schtasks /delete /tn "NewInDaily" /f >nul 2>&1

echo [OK] Tareas antiguas eliminadas
echo.

echo [2/3] Creando tarea DIARIA (18:30)...
echo.

REM Crear tarea diaria
schtasks /create ^
    /tn "NewInDaily" ^
    /tr "cmd /c cd \"C:\Users\santiago\NEW IN\" && python newin_robot.py daily" ^
    /sc daily ^
    /st 18:30 ^
    /f

if errorlevel 1 (
    echo [ERROR] No se pudo crear la tarea diaria
    pause
    exit /b 1
)

echo [OK] Tarea diaria creada exitosamente
echo.

echo [3/3] Creando tarea SEMANAL REFRESH (Lunes 18:30)...
echo.

REM Crear tarea semanal (lunes)
schtasks /create ^
    /tn "NewInRefresh" ^
    /tr "cmd /c cd \"C:\Users\santiago\NEW IN\" && python newin_robot.py refresh" ^
    /sc weekly ^
    /d MON ^
    /st 18:30 ^
    /f

if errorlevel 1 (
    echo [ERROR] No se pudo crear la tarea semanal
    pause
    exit /b 1
)

echo [OK] Tarea semanal creada exitosamente
echo.

echo ============================================================
echo TAREAS CREADAS EXITOSAMENTE
echo ============================================================
echo.
echo TAREA DIARIA:
echo   Nombre: NewInDaily
echo   Horario: 18:30 todos los dias
echo   Accion: Procesa ingresos del dia
echo.
echo TAREA SEMANAL:
echo   Nombre: NewInRefresh  
echo   Horario: Lunes 18:30
echo   Accion: Limpia categoria y resetea estado
echo.

REM Mostrar tareas creadas
echo Verificando tareas programadas...
echo.
schtasks /query /tn "NewInDaily" /fo LIST /v | findstr /C:"Nombre de tarea" /C:"Siguiente hora de ejecución" /C:"Estado"
echo.
schtasks /query /tn "NewInRefresh" /fo LIST /v | findstr /C:"Nombre de tarea" /C:"Siguiente hora de ejecución" /C:"Estado"
echo.

echo ============================================================
echo VENTAJAS DEL HORARIO 18:30
echo ============================================================
echo.
echo 1. Procesa TODO el dia laboral (8:30-18:00)
echo 2. Da tiempo para sincronizacion Dragonfish-TN
echo 3. Repositor termino sus tareas del dia
echo 4. Match rate mas alto (mas productos sincronizados)
echo 5. No interfiere con horario laboral
echo.

echo ============================================================
echo PROXIMOS PASOS
echo ============================================================
echo.
echo 1. Las tareas se ejecutaran automaticamente
echo 2. Primera ejecucion: Hoy a las 18:30
echo 3. Refresh semanal: Proximo lunes a las 18:30
echo 4. Revisa logs en: C:\Users\santiago\NEW IN\logs\
echo.
echo Para ejecutar manualmente:
echo   python newin_robot.py daily     (actualizacion diaria)
echo   python newin_robot.py refresh   (limpieza semanal)
echo.

echo ============================================================
echo.
pause
