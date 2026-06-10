@echo off
chcp 65001 >nul
title Sistema New In - Menú de Diagnóstico

:MENU
cls
echo.
echo ============================================
echo     SISTEMA NEW IN - MENÚ PRINCIPAL
echo ============================================
echo.
echo 1. Diagnóstico Completo
echo 2. Ejecutar Actualización Manual
echo 3. Ver Último Log
echo 4. Ver Estado Actual
echo 5. Verificar Tarea Programada
echo 6. Habilitar Tarea Programada
echo 7. Ejecutar Tarea Ahora
echo 8. Ver Productos en New In
echo 9. Salir
echo.
echo ============================================
set /p opcion="Selecciona una opción (1-9): "

if "%opcion%"=="1" goto DIAGNOSTICO
if "%opcion%"=="2" goto EJECUTAR
if "%opcion%"=="3" goto VER_LOG
if "%opcion%"=="4" goto ESTADO
if "%opcion%"=="5" goto VER_TAREA
if "%opcion%"=="6" goto HABILITAR_TAREA
if "%opcion%"=="7" goto EJECUTAR_TAREA
if "%opcion%"=="8" goto VER_PRODUCTOS
if "%opcion%"=="9" goto SALIR
goto MENU

:DIAGNOSTICO
cls
echo.
echo Ejecutando diagnóstico completo...
echo.
python diagnostico_new_in.py
echo.
pause
goto MENU

:EJECUTAR
cls
echo.
echo Ejecutando actualización manual...
echo ============================================
echo.
python scripts\actualizar_new_in.py
echo.
echo ============================================
echo Actualización completada. Revisa el resultado arriba.
echo.
pause
goto MENU

:VER_LOG
cls
echo.
echo Mostrando último log generado...
echo ============================================
echo.
for /f "delims=" %%f in ('dir logs\*.log /b /o-d /tc 2^>nul') do (
    echo Archivo: %%f
    echo.
    type logs\%%f
    goto :log_mostrado
)
echo No se encontraron logs.
:log_mostrado
echo.
echo ============================================
pause
goto MENU

:ESTADO
cls
echo.
echo ============================================
echo     ESTADO ACTUAL DEL SISTEMA
echo ============================================
echo.

if exist data\ultima_sincronizacion.txt (
    echo Última sincronización:
    type data\ultima_sincronizacion.txt
    echo.
) else (
    echo ⚠ No hay registro de última sincronización
    echo.
)

if exist data\productos_new_in.json (
    echo Productos en New In:
    for /f %%i in ('powershell -Command "(Get-Content data\productos_new_in.json -Raw | ConvertFrom-Json).Count"') do echo   %%i productos
    echo.
) else (
    echo ⚠ No hay archivo de productos
    echo.
)

echo Logs disponibles:
dir logs\*.log /b 2>nul | find /c /v "" && (
    echo   Se encontraron logs
) || (
    echo   ⚠ No hay logs
)
echo.

echo Tarea programada:
schtasks /query /fo LIST 2>nul | findstr /I /C:"new in" /C:"dragonfish" /C:"tiendanube" >nul && (
    echo   ✓ Tarea encontrada
) || (
    echo   ⚠ No se encontró tarea programada
)
echo.
echo ============================================
pause
goto MENU

:VER_TAREA
cls
echo.
echo Buscando tareas programadas...
echo ============================================
echo.
schtasks /query /fo LIST /v | findstr /I /C:"new" /C:"in" /C:"dragonfish" /C:"tiendanube"
if errorlevel 1 (
    echo.
    echo ⚠ No se encontraron tareas relacionadas
    echo.
    echo Para crear una tarea:
    echo   1. Abre Task Scheduler ^(taskschd.msc^)
    echo   2. Selecciona "Create Basic Task"
    echo   3. Configura según la guía de diagnóstico
)
echo.
echo ============================================
pause
goto MENU

:HABILITAR_TAREA
cls
echo.
echo Habilitando tarea programada...
echo.
set /p nombre_tarea="Ingresa el nombre de la tarea (o presiona Enter para intentar con nombre por defecto): "

if "%nombre_tarea%"=="" (
    set nombre_tarea=Actualizar New In - Tiendanube
)

schtasks /change /tn "%nombre_tarea%" /enable
echo.
if errorlevel 1 (
    echo ⚠ No se pudo habilitar la tarea
    echo Verifica que el nombre sea correcto
) else (
    echo ✓ Tarea habilitada exitosamente
)
echo.
pause
goto MENU

:EJECUTAR_TAREA
cls
echo.
echo Ejecutando tarea programada ahora...
echo.
set /p nombre_tarea="Ingresa el nombre de la tarea (o presiona Enter para usar el nombre por defecto): "

if "%nombre_tarea%"=="" (
    set nombre_tarea=Actualizar New In - Tiendanube
)

schtasks /run /tn "%nombre_tarea%"
echo.
if errorlevel 1 (
    echo ⚠ No se pudo ejecutar la tarea
    echo Verifica que el nombre sea correcto y que la tarea exista
) else (
    echo ✓ Tarea iniciada
    echo Espera unos segundos y revisa los logs
)
echo.
pause
goto MENU

:VER_PRODUCTOS
cls
echo.
echo Productos actuales en categoría New In:
echo ============================================
echo.

if exist data\productos_new_in.json (
    powershell -Command "$json = Get-Content data\productos_new_in.json -Raw | ConvertFrom-Json; Write-Host 'Total de productos:' $json.Count; Write-Host ''; $json | Select-Object -First 10 | ForEach-Object { Write-Host '  •' $_.nombre '(SKU:' $_.sku ')' }"
    echo.
    echo ^(Mostrando primeros 10 productos^)
) else (
    echo ⚠ No existe el archivo de productos
)

echo.
echo ============================================
pause
goto MENU

:SALIR
cls
echo.
echo Saliendo del menú de diagnóstico...
echo.
exit /b

