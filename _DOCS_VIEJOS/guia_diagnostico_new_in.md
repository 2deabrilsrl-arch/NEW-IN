# Guía de Diagnóstico y Solución - Sistema "New In"

## 📋 PASO 1: Verificar Última Ejecución

### 1.1 Revisar logs más recientes
```bash
# Ve al directorio de tu proyecto
cd "C:\ruta\a\tu\proyecto\new-in"

# Ver los últimos logs generados
dir logs\*.log /O-D /TC

# Leer el log más reciente completo
type logs\[nombre-del-log-mas-reciente].log

# O ver las últimas 50 líneas
powershell -Command "Get-Content logs\[nombre-del-log-mas-reciente].log -Tail 50"
```

### 1.2 Verificar archivo de estado
```bash
# Ver cuándo se ejecutó por última vez
type data\ultima_sincronizacion.txt

# Ver productos actualmente en New In
type data\productos_new_in.json
```

---

## 🔍 PASO 2: Identificar el Problema

### 2.1 Verificar si existe tarea programada

**Opción A - Windows Task Scheduler:**
```powershell
# Buscar tareas relacionadas
schtasks /query /fo LIST /v | findstr /I "new in dragonfish tiendanube"
```

**Opción B - Manual:**
1. Presiona `Win + R`
2. Escribe: `taskschd.msc`
3. Busca tareas relacionadas con "New In", "Dragonfish" o "Tiendanube"
4. Verifica:
   - ✓ Estado: ¿Está habilitada?
   - ✓ Última ejecución: ¿Cuándo fue?
   - ✓ Resultado: ¿Fue exitosa?
   - ✓ Próxima ejecución: ¿Está programada?

### 2.2 Verificar el script principal
```bash
# Asegurarte de que existe el script
dir scripts\actualizar_new_in.py

# Ver el contenido para verificar que no haya cambios
type scripts\actualizar_new_in.py
```

### 2.3 Probar ejecución manual
```bash
# Ejecutar manualmente con logging completo
python scripts\actualizar_new_in.py

# Si necesitas ver más detalle
python scripts\actualizar_new_in.py --debug
```

**⚠️ Observa:**
- ¿Se ejecuta sin errores?
- ¿Genera un nuevo archivo de log?
- ¿Muestra errores de conexión a APIs?
- ¿Hay problemas de autenticación?

---

## 🛠️ PASO 3: Soluciones Comunes

### 3.1 Si la tarea programada NO existe

**Recrear la tarea en Task Scheduler:**

1. Abre Task Scheduler (`taskschd.msc`)
2. Clic derecho en "Task Scheduler Library" → "Create Basic Task"
3. Configura:
   - **Name:** Actualizar New In - Tiendanube
   - **Description:** Sincronización automática de categoría New In
   - **Trigger:** Diario a las 2:00 AM (o tu horario preferido)
   - **Action:** Start a program
   - **Program:** `C:\ruta\a\python.exe`
   - **Arguments:** `C:\ruta\a\tu\proyecto\new-in\scripts\actualizar_new_in.py`
   - **Start in:** `C:\ruta\a\tu\proyecto\new-in`

4. En "Settings":
   - ✓ Run whether user is logged on or not
   - ✓ Run with highest privileges
   - ✓ If task fails, restart every: 10 minutes
   - ✓ Attempt to restart up to: 3 times

### 3.2 Si la tarea está deshabilitada

```powershell
# Habilitar tarea
schtasks /change /tn "Actualizar New In - Tiendanube" /enable

# Ejecutar inmediatamente para probar
schtasks /run /tn "Actualizar New In - Tiendanube"
```

### 3.3 Si hay errores de autenticación API

**Verificar credenciales:**
```bash
# Ver archivo de configuración (sin mostrar las claves completas)
type config\credentials.json
```

**Probar conexión a Dragonfish:**
```python
# Crear archivo: test_dragonfish.py
import sys
sys.path.append('scripts')
from dragonfish_api import DragonfishAPI

api = DragonfishAPI()
print("✓ Conexión exitosa a Dragonfish")
productos = api.obtener_productos_recientes(dias=7)
print(f"✓ Productos obtenidos: {len(productos)}")
```

```bash
python test_dragonfish.py
```

**Probar conexión a Tiendanube:**
```python
# Crear archivo: test_tiendanube.py
import sys
sys.path.append('scripts')
from tiendanube_api import TiendanubeAPI

api = TiendanubeAPI()
print("✓ Conexión exitosa a Tiendanube")
categorias = api.obtener_categorias()
print(f"✓ Categorías encontradas: {len(categorias)}")
```

```bash
python test_tiendanube.py
```

### 3.4 Si las credenciales expiraron

1. **Dragonfish:** Regenera tu token en el panel de Dragonfish
2. **Tiendanube:** Regenera tu Access Token en Configuración → Apps
3. Actualiza `config\credentials.json`
4. Ejecuta manualmente para probar

### 3.5 Si hay problemas de red/firewall

```bash
# Probar conectividad
ping api.zoologic.com
ping api.tiendanube.com

# Si falla, revisar:
# - Configuración de firewall
# - Proxy corporativo
# - VPN activa
```

---

## 📊 PASO 4: Verificar Resultados

Después de solucionar:

```bash
# 1. Ejecutar manualmente
python scripts\actualizar_new_in.py

# 2. Verificar que se generó un nuevo log
dir logs\*.log /O-D /TC

# 3. Ver el log para confirmar éxito
type logs\[log-mas-reciente].log | findstr /I "éxito exitosa completado"

# 4. Verificar en Tiendanube
# - Ve a tu tienda
# - Busca la categoría "New In"
# - Confirma que tiene productos recientes
```

---

## 📝 PASO 5: Monitoreo Continuo

### Crear script de verificación rápida

**Guardar como: `verificar_estado.bat`**
```batch
@echo off
echo ============================================
echo ESTADO DEL SISTEMA NEW IN
echo ============================================
echo.

echo Ultima sincronizacion:
type data\ultima_sincronizacion.txt
echo.

echo Log mas reciente:
for /f "delims=" %%f in ('dir logs\*.log /b /o-d /tc') do (
    echo %%f
    type logs\%%f | findstr /I "completado error warning"
    goto :done
)
:done
echo.

echo Productos actuales en New In:
powershell -Command "(Get-Content data\productos_new_in.json | ConvertFrom-Json).length"
echo.

echo Proxima ejecucion programada:
schtasks /query /tn "Actualizar New In - Tiendanube" /fo LIST | findstr /I "Next Run Time"
echo.
echo ============================================
pause
```

**Uso:**
```bash
verificar_estado.bat
```

---

## 🚨 Checklist de Problemas Comunes

- [ ] ¿Existe la tarea programada?
- [ ] ¿Está habilitada la tarea?
- [ ] ¿Las credenciales de API son válidas?
- [ ] ¿El script principal existe y no tiene errores?
- [ ] ¿Hay conectividad a internet?
- [ ] ¿Los logs muestran el problema específico?
- [ ] ¿Python está instalado y accesible?
- [ ] ¿Las dependencias (requests, etc.) están instaladas?

---

## 📞 Si Nada Funciona

Ejecuta este diagnóstico completo y compárteme el resultado:

```bash
# Guardar como: diagnostico_completo.bat
@echo off
echo ===== DIAGNOSTICO COMPLETO ===== > diagnostico.txt
echo. >> diagnostico.txt

echo FECHA Y HORA: >> diagnostico.txt
date /t >> diagnostico.txt
time /t >> diagnostico.txt
echo. >> diagnostico.txt

echo ESTRUCTURA DE ARCHIVOS: >> diagnostico.txt
tree /F >> diagnostico.txt
echo. >> diagnostico.txt

echo ULTIMO LOG: >> diagnostico.txt
for /f "delims=" %%f in ('dir logs\*.log /b /o-d /tc') do (
    type logs\%%f >> diagnostico.txt
    goto :next
)
:next
echo. >> diagnostico.txt

echo TAREA PROGRAMADA: >> diagnostico.txt
schtasks /query /tn "Actualizar New In - Tiendanube" /fo LIST /v >> diagnostico.txt
echo. >> diagnostico.txt

echo VERSION DE PYTHON: >> diagnostico.txt
python --version >> diagnostico.txt
echo. >> diagnostico.txt

echo DEPENDENCIAS INSTALADAS: >> diagnostico.txt
pip list | findstr /I "requests json" >> diagnostico.txt

echo ===== FIN DEL DIAGNOSTICO ===== >> diagnostico.txt
type diagnostico.txt
```

Ejecuta esto y comparte el contenido de `diagnostico.txt`

---

## ✅ Comando Rápido de Emergencia

Si solo quieres que funcione YA:

```bash
# 1. Ir al proyecto
cd "C:\ruta\a\tu\proyecto\new-in"

# 2. Ejecutar manualmente
python scripts\actualizar_new_in.py

# 3. Si funciona, asegúrate de que esté programado
schtasks /run /tn "Actualizar New In - Tiendanube"
```
