# ============================================================
# SCRIPT DE DIAGNOSTICO NEW IN
# Analiza logs para extraer SKUs asignados y no macheados
# ============================================================

cd "C:\Users\santiago\NEW IN\logs"

$fecha = Get-Date -Format "yyyy-MM-dd_HHmm"
$reportPath = "C:\Users\santiago\NEW IN\logs\REPORTE_NEW_IN_$fecha.txt"

Write-Host ""
Write-Host "=== ANALIZANDO LOGS DE NEW IN ===" -ForegroundColor Cyan
Write-Host "Leyendo: daily.log" -ForegroundColor Yellow
Write-Host ""

# Leer el daily.log
$logContent = Get-Content "daily.log" -Raw -Encoding UTF8

# Inicializar variables
$skusSinMatch = @()
$skusAsignados = @()

# Extraer todas las lineas relevantes
$lines = $logContent -split "`n"

$output = @"
============================================================
REPORTE NEW IN - Analisis de SKUs
Generado: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
============================================================

"@

# Buscar ejecuciones desde el 29/12
$enEjecucion = $false
$fechaActual = ""
$ejecucionNum = 0

foreach ($line in $lines) {
    # Detectar inicio de ejecucion
    if ($line -match "DAILY RUN - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})") {
        $fechaActual = $matches[1]
        if ($fechaActual -ge "2025-12-29") {
            $enEjecucion = $true
            $ejecucionNum++
            $output += "`n`n========================================`n"
            $output += "EJECUCION #$ejecucionNum - $fechaActual`n"
            $output += "========================================`n"
        } else {
            $enEjecucion = $false
        }
    }
    
    if ($enEjecucion) {
        # SKUs unicos detectados
        if ($line -match "SKUs únicos: (\d+)") {
            $output += "SKUs unicos detectados: $($matches[1])`n"
        }
        
        # Match rate
        if ($line -match "SKUs con match: (\d+) / (\d+) \((\d+)%\)") {
            $output += "Match exitoso: $($matches[1]) de $($matches[2]) ($($matches[3])%)`n"
        }
        
        # SKUs sin match
        if ($line -match "SKUs sin match: (\d+) \(primeros 20\): \[([^\]]+)\]") {
            $cantidad = $matches[1]
            $skusList = $matches[2] -replace "'", "" -replace '"', "" -split ", "
            $output += "`nSKUs SIN MATCH ($cantidad):`n"
            foreach ($sku in $skusList) {
                if ($sku.Trim() -ne "") {
                    $output += "  [NO MATCH] $sku`n"
                    $skusSinMatch += [PSCustomObject]@{
                        Fecha = $fechaActual
                        SKU = $sku.Trim()
                    }
                }
            }
        }
        
        # Productos asignados
        if ($line -match "Asignados (\d+) productos a categoría") {
            $output += "`nProductos ASIGNADOS a categoria: $($matches[1])`n"
        }
        
        # Asignando producto especifico
        if ($line -match "Asignando producto id=(\d+).*SKU:\s*([^\s]+)") {
            $productId = $matches[1]
            $skuAsignado = $matches[2].Trim()
            $output += "  [OK] $skuAsignado (Product ID: $productId)`n"
            $skusAsignados += [PSCustomObject]@{
                Fecha = $fechaActual
                SKU = $skuAsignado
                ProductID = $productId
            }
        }
    }
}

# Resumen final
$output += "`n`n============================================================`n"
$output += "RESUMEN GENERAL (desde 29/12/2025)`n"
$output += "============================================================`n"
$output += "Total ejecuciones analizadas: $ejecucionNum`n"
$output += "Total SKUs SIN MATCH: $($skusSinMatch.Count)`n"
$output += "Total SKUs ASIGNADOS: $($skusAsignados.Count)`n"

if ($skusSinMatch.Count -gt 0) {
    $output += "`n--- LISTADO COMPLETO: SKUs NO MACHEADOS ---`n"
    $uniqueSinMatch = $skusSinMatch | Sort-Object Fecha, SKU -Unique
    foreach ($item in $uniqueSinMatch) {
        $output += "$($item.Fecha) | [NO MATCH] $($item.SKU)`n"
    }
}

if ($skusAsignados.Count -gt 0) {
    $output += "`n--- LISTADO COMPLETO: SKUs ASIGNADOS A NEW IN ---`n"
    $uniqueAsignados = $skusAsignados | Sort-Object Fecha, SKU -Unique
    foreach ($item in $uniqueAsignados) {
        $output += "$($item.Fecha) | [OK] $($item.SKU) | Product ID: $($item.ProductID)`n"
    }
}

# Guardar reporte
$output | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "REPORTE GENERADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivo: $reportPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "RESUMEN:"
Write-Host "  Ejecuciones analizadas: $ejecucionNum"
Write-Host "  SKUs sin match: $($skusSinMatch.Count)" -ForegroundColor Yellow
Write-Host "  SKUs asignados: $($skusAsignados.Count)" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Enter para abrir el reporte..."
Read-Host

# Abrir el reporte
notepad $reportPath
