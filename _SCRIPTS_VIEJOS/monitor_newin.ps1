# ============================================================
# MONITOR NEW IN - Extrae informacion de logs
# Correccion: Busca "DAILY UPDATE" no "DAILY RUN"
# ============================================================

param(
    [int]$Dias = 7
)

cd "C:\Users\santiago\NEW IN\logs"

Write-Host ""
Write-Host "=== MONITOR NEW IN - Ultimos $Dias dias ===" -ForegroundColor Cyan
Write-Host ""

# Calcular fecha limite
$fechaLimite = (Get-Date).AddDays(-$Dias).ToString("yyyy-MM-dd")

# Leer log
$logContent = Get-Content "daily.log" -Encoding UTF8

# Buscar todas las ejecuciones
$ejecuciones = @()
$lineaActual = 0

foreach ($line in $logContent) {
    $lineaActual++
    
    if ($line -match "^DAILY UPDATE - (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})") {
        $fecha = $matches[1]
        $hora = $matches[2]
        
        if ($fecha -ge $fechaLimite) {
            $ejecuciones += [PSCustomObject]@{
                Fecha = $fecha
                Hora = $hora
                Linea = $lineaActual
                SKUs = 0
                Match = ""
                SinMatch = ""
                Asignados = 0
            }
        }
    }
}

Write-Host "Ejecuciones encontradas: $($ejecuciones.Count)" -ForegroundColor Yellow
Write-Host ""

# Extraer detalles de cada ejecucion
$indice = 0
foreach ($ejecucion in $ejecuciones) {
    $inicio = $ejecucion.Linea
    $fin = if ($indice -lt $ejecuciones.Count - 1) { $ejecuciones[$indice + 1].Linea } else { $logContent.Count }
    
    $bloque = $logContent[$inicio..$fin] -join "`n"
    
    # Extraer informacion
    if ($bloque -match "SKUs únicos: (\d+)") {
        $ejecucion.SKUs = [int]$matches[1]
    }
    
    if ($bloque -match "SKUs con match: (\d+) / (\d+) \((\d+)%\)") {
        $ejecucion.Match = "$($matches[1])/$($matches[2]) ($($matches[3])%)"
    }
    
    if ($bloque -match "SKUs sin match: (\d+).*: \[([^\]]+)\]") {
        $cantidad = $matches[1]
        $ejemplos = $matches[2] -replace "'", "" -replace '"', "" -split "," | Select-Object -First 3
        $ejecucion.SinMatch = "$cantidad ejemplos: $($ejemplos -join ', ')"
    }
    
    if ($bloque -match "Asignados (\d+) productos") {
        $ejecucion.Asignados = [int]$matches[1]
    }
    
    if ($bloque -match "sin movimientos") {
        $ejecucion.SKUs = 0
        $ejecucion.Match = "Sin movimientos"
    }
    
    $indice++
}

# Mostrar resultados
Write-Host "FECHA       HORA      SKUs  Match        Asignados" -ForegroundColor Green
Write-Host "=========== ========  ====  ===========  =========" -ForegroundColor Green

foreach ($e in $ejecuciones) {
    $color = if ($e.Asignados -gt 0) { "Green" } elseif ($e.SKUs -gt 0) { "Yellow" } else { "Gray" }
    
    $linea = "{0,-11} {1,-8}  {2,4}  {3,-11}  {4,9}" -f `
        $e.Fecha, $e.Hora, $e.SKUs, $e.Match, $e.Asignados
    
    Write-Host $linea -ForegroundColor $color
    
    if ($e.SinMatch) {
        Write-Host "            >> Sin match: $($e.SinMatch)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== RESUMEN ===" -ForegroundColor Cyan
$totalSKUs = ($ejecuciones | Measure-Object -Property SKUs -Sum).Sum
$totalAsignados = ($ejecuciones | Measure-Object -Property Asignados -Sum).Sum

Write-Host "Total SKUs detectados: $totalSKUs"
Write-Host "Total productos asignados: $totalAsignados" -ForegroundColor Green

if ($totalSKUs -gt 0) {
    $matchRate = [math]::Round(($totalAsignados / $totalSKUs) * 100, 1)
    $color = if ($matchRate -lt 30) { "Red" } elseif ($matchRate -lt 70) { "Yellow" } else { "Green" }
    Write-Host "Match rate promedio: $matchRate%" -ForegroundColor $color
}

Write-Host ""
Write-Host "Presiona Enter para salir..."
Read-Host
