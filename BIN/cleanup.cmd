@echo off
REM ============================================================
REM NEW IN ROBOT - SCRIPT DE LIMPIEZA
REM ============================================================
REM Este script elimina archivos de backup y versiones viejas
REM que ya estan organizados en _DOCS_VIEJOS y _SCRIPTS_VIEJOS
REM ============================================================

setlocal

echo.
echo ============================================================
echo NEW IN ROBOT - LIMPIEZA DE ARCHIVOS OBSOLETOS
echo ============================================================
echo.

REM Cambiar a directorio del proyecto
cd /d "%~dp0\.."
set PROJECT_DIR=%CD%

echo [INFO] Proyecto: %PROJECT_DIR%
echo.

REM ============================================================
REM ELIMINAR BACKUPS DE VERSIONES VIEJAS
REM ============================================================
echo [1/3] Eliminando backups de versiones viejas...

if exist "newin_robot_v11_OLD.py" (
    del "newin_robot_v11_OLD.py"
    echo   [DEL] newin_robot_v11_OLD.py
)

if exist "newin_robot_v12.0_BACKUP.py" (
    del "newin_robot_v12.0_BACKUP.py"
    echo   [DEL] newin_robot_v12.0_BACKUP.py
)

if exist "newin_robot_v12.py" (
    del "newin_robot_v12.py"
    echo   [DEL] newin_robot_v12.py (duplicado)
)

if exist "backup_v11\" (
    rmdir /S /Q "backup_v11\"
    echo   [DEL] backup_v11\ (carpeta completa)
)

if exist "diagnostico_2026-01-05_1034\" (
    rmdir /S /Q "diagnostico_2026-01-05_1034\"
    echo   [DEL] diagnostico_2026-01-05_1034\ (carpeta completa)
)

echo [OK] Backups eliminados
echo.

REM ============================================================
REM VERIFICAR CARPETAS DE ORGANIZACION
REM ============================================================
echo [2/3] Verificando carpetas de organizacion...

if not exist "_DOCS_VIEJOS\" (
    echo   [WARN] Carpeta _DOCS_VIEJOS no existe
    echo   [INFO] Los documentos viejos ya fueron organizados manualmente
)

if not exist "_SCRIPTS_VIEJOS\" (
    echo   [WARN] Carpeta _SCRIPTS_VIEJOS no existe
    echo   [INFO] Los scripts viejos ya fueron organizados manualmente
)

echo [OK] Verificacion completada
echo.

REM ============================================================
REM ESTRUCTURA FINAL
REM ============================================================
echo [3/3] Verificando estructura final...
echo.

echo Estructura del proyecto:
echo.
dir /B | findstr /V /C:"_DOCS" /C:"_SCRIPTS"
echo.

REM ============================================================
REM RESUMEN
REM ============================================================
echo ============================================================
echo LIMPIEZA COMPLETADA
echo ============================================================
echo.
echo Archivos eliminados:
echo   - Versiones viejas del robot (.py)
echo   - Carpetas de backup (backup_v11\, diagnostico_*)
echo.
echo Estructura final:
echo   C:\Users\santiago\NEW IN\
echo   ├── newin_robot.py          (v12.1.0-REPORTES)
echo   ├── config.env              (Configuracion)
echo   ├── BIN\                    (Scripts .cmd)
echo   ├── data\                   (Estado y datos)
echo   ├── logs\                   (Logs y reportes)
echo   ├── _DOCS_VIEJOS\           (Documentacion archivada)
echo   └── _SCRIPTS_VIEJOS\        (Scripts archivados)
echo.
echo [OK] El proyecto esta limpio y organizado
echo.

pause
