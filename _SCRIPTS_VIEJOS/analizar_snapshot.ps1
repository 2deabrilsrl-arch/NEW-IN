# ============================================================
# ANALIZAR SNAPSHOT - Ver productos asignados a New In
# ============================================================

cd "C:\Users\santiago\NEW IN\data"

Write-Host ""
Write-Host "=== ANALIZANDO SNAPSHOT Y STATE ===" -ForegroundColor Cyan
Write-Host ""

# Leer snapshot
if (Test-Path "current_snapshot.json") {
    $snapshot = Get-Content "current_snapshot.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    
    Write-Host "Total productos en snapshot: $($snapshot.Count)" -ForegroundColor Yellow
    Write-Host ""
    
    # Productos desde el 29/12
    Write-Host "=== PRODUCTOS AGREGADOS DESDE 29/12 ===" -ForegroundColor Green
    $recientes = $snapshot | Where-Object { $_.date_added -ge "2025-12-29" }
    
    if ($recientes) {
        Write-Host "Total desde 29/12: $($recientes.Count)" -ForegroundColor Yellow
        Write-Host ""
        $recientes | ForEach-Object {
            Write-Host "$($_.date_added) | $($_.sku) | Product ID: $($_.product_id)"
        }
    } else {
        Write-Host "No hay productos agregados desde el 29/12" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "=== ULTIMOS 20 PRODUCTOS EN SNAPSHOT ===" -ForegroundColor Green
    $snapshot | Select-Object -Last 20 | ForEach-Object {
        Write-Host "$($_.date_added) | $($_.sku) | Product ID: $($_.product_id)"
    }
    
} else {
    Write-Host "ERROR: No existe current_snapshot.json" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== STATE.JSON ===" -ForegroundColor Cyan

if (Test-Path "state.json") {
    $state = Get-Content "state.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Host "Last run: $($state.last_run)"
    Write-Host "Last refresh: $($state.last_refresh)"
} else {
    Write-Host "ERROR: No existe state.json" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== CATEGORIA NEW IN ===" -ForegroundColor Cyan

if (Test-Path "newin_category.json") {
    $categoria = Get-Content "newin_category.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Host "Category ID: $($categoria.category_id)"
    Write-Host "Handle: $($categoria.handle)"
    Write-Host "Productos en categoria: $($categoria.product_ids.Count)" -ForegroundColor Yellow
    
    if ($categoria.product_ids.Count -gt 0) {
        Write-Host ""
        Write-Host "Product IDs en New In:"
        $categoria.product_ids | ForEach-Object {
            Write-Host "  - $_"
        }
    }
} else {
    Write-Host "ERROR: No existe newin_category.json" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona Enter para salir..."
Read-Host
