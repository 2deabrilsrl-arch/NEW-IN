# ============================================================
# COPIAR DATOS PARA DIAGNOSTICO
# Copia los archivos JSON a la carpeta outputs para compartir
# ============================================================

$fecha = Get-Date -Format "yyyy-MM-dd_HHmm"

Write-Host ""
Write-Host "=== COPIANDO ARCHIVOS PARA DIAGNOSTICO ===" -ForegroundColor Cyan
Write-Host ""

# Crear carpeta de diagnostico
$outputDir = "C:\Users\santiago\NEW IN\diagnostico_$fecha"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

# Copiar archivos
Copy-Item "C:\Users\santiago\NEW IN\data\current_snapshot.json" "$outputDir\" -ErrorAction SilentlyContinue
Copy-Item "C:\Users\santiago\NEW IN\data\state.json" "$outputDir\" -ErrorAction SilentlyContinue
Copy-Item "C:\Users\santiago\NEW IN\data\newin_category.json" "$outputDir\" -ErrorAction SilentlyContinue
Copy-Item "C:\Users\santiago\NEW IN\logs\daily.log" "$outputDir\" -ErrorAction SilentlyContinue

Write-Host "Archivos copiados a: $outputDir" -ForegroundColor Green
Write-Host ""
Write-Host "Contenido:"
Get-ChildItem $outputDir | ForEach-Object {
    Write-Host "  - $($_.Name) ($($_.Length) bytes)"
}

Write-Host ""
Write-Host "Ahora puedes compartir esta carpeta completa" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Enter para abrir la carpeta..."
Read-Host

# Abrir carpeta
explorer $outputDir
