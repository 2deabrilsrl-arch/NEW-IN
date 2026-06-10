# 🤖 NEW IN ROBOT

Robot de integración entre **Zoologic Dragonfish** y **Tiendanube** para gestionar automáticamente la categoría "NEW IN" con productos recién ingresados.

**Versión:** 11.0.0-FIXED  
**Fecha:** Diciembre 2024

---

## 📋 TABLA DE CONTENIDOS

1. [Descripción](#descripción)
2. [Características](#características)
3. [Correcciones Críticas v11](#correcciones-críticas-v11)
4. [Requisitos](#requisitos)
5. [Instalación](#instalación)
6. [Configuración](#configuración)
7. [Uso](#uso)
8. [Arquitectura](#arquitectura)
9. [Troubleshooting](#troubleshooting)
10. [Soporte](#soporte)

---

## 🎯 DESCRIPCIÓN

El **NEW IN ROBOT** automatiza el proceso de asignar la categoría "NEW IN" a productos recién ingresados al stock en Dragonfish, sincronizándolos con tu tienda en Tiendanube.

**Flujo principal:**
1. 📦 **Dragonfish**: Detecta ingresos de mercadería (motivo ING)
2. 🔍 **Matching**: Busca productos en Tiendanube por SKU
3. 🏷️ **Asignación**: Agrega categoría "NEW IN" a productos encontrados
4. 🔄 **Refresh semanal**: Limpia la categoría los lunes para empezar la semana

---

## ✨ CARACTERÍSTICAS

- ✅ **Paginación completa** de Dragonfish (200 items/página)
- ✅ **Paginación completa** de Tiendanube (100 productos/página)
- ✅ **Matching por SKU** formato `Articulo#Color#Talle`
- ✅ **Retry automático** en fallos de red
- ✅ **Logging detallado** con timestamps
- ✅ **Persistencia de estado** para evitar duplicados
- ✅ **Refresh semanal** automático los lunes
- ✅ **Catchup inteligente** de 7 días
- ✅ **Validación de categorías** antes de asignar
- ✅ **Creación automática** de categoría si no existe (configurable)

---

## 🔥 CORRECCIONES CRÍTICAS V11

### ❌ PROBLEMA #1: Paginación de Dragonfish (CRÍTICO)
**Antes:** Solo consultaba página 1 (máx 200 items)  
**Ahora:** ✅ Itera sobre todas las páginas hasta obtener todos los movimientos

### ❌ PROBLEMA #2: Bajo rate de match (22%)
**Antes:** Solo 56/252 SKUs coincidían  
**Ahora:** ✅ Logging detallado de SKUs sin match para debugging

### ❌ PROBLEMA #3: Tareas no se ejecutaban
**Antes:** Rutas hardcodeadas `/santiago/newin_robot.py`  
**Ahora:** ✅ Rutas dinámicas basadas en ubicación del proyecto

### ❌ PROBLEMA #4: Manejo de errores silencioso
**Antes:** Errores se "tragaban" y continuaba  
**Ahora:** ✅ Logging completo con tracebacks y códigos de error

### ❌ PROBLEMA #5: Catchup muy corto (4 días)
**Antes:** Solo 4 días de historia  
**Ahora:** ✅ Aumentado a 7 días para mayor seguridad

### ❌ PROBLEMA #6: Sin validación de categoría
**Antes:** Error 404 al asignar categoría inexistente  
**Ahora:** ✅ Validación antes de cada operación

---

## 📦 REQUISITOS

### Software
- **Python 3.8+** ([Descargar](https://www.python.org/downloads/))
- **Windows 10/11** (para tareas programadas)
- **Conexión a internet** (acceso a APIs)

### Accesos
- **Zoologic Dragonfish** con módulo REST API habilitado
- **Tiendanube** con acceso a API
- **Tokens de autenticación** para ambos servicios

### Hardware
- **CPU:** Cualquier procesador moderno
- **RAM:** 512 MB mínimo
- **Disco:** 100 MB libres

---

## 🚀 INSTALACIÓN

### 1. Descargar el proyecto

Ubicar todos los archivos en:
```
C:\Users\santiago\NEW IN\
```

### 2. Verificar estructura

```
C:\Users\santiago\NEW IN\
├── newin_robot.py         # Script principal
├── config.env             # Configuración (EDITAR)
├── README.md              # Esta documentación
├── CHANGELOG.md           # Historial de cambios
├── bin\                   # Scripts de utilidad
│   ├── install.cmd        # Instalador
│   ├── daily.cmd          # Ejecución diaria
│   ├── refresh.cmd        # Refresh semanal
│   ├── create_tasks.cmd   # Crear tareas programadas
│   ├── check_health.cmd   # Diagnóstico
│   ├── who.cmd            # Test de conexión
│   ├── list_categories.cmd
│   └── check_category.cmd
├── data\                  # Datos persistentes (autogenerado)
├── logs\                  # Logs de ejecución (autogenerado)
└── docs\                  # Documentación adicional
```

### 3. Ejecutar instalador

**Abre CMD como Administrador** y ejecuta:
```cmd
cd "C:\Users\santiago\NEW IN"
bin\install.cmd
```

El instalador:
1. ✅ Verifica Python
2. ✅ Instala dependencias (`requests`)
3. ✅ Crea directorios
4. ✅ Prueba conexión

---

## ⚙️ CONFIGURACIÓN

### 1. Editar `config.env`

Abre `config.env` con un editor de texto y configura:

#### Dragonfish
```env
DF_BASE_URL=http://localhost:8009/api.Dragonfish
DF_IDCLIENTE=WEB
DF_JWTOKEN=tu_token_jwt_aqui
DF_BASEDEDATOS=NADIN25
```

#### Tiendanube
```env
TN_STORE_ID=6566743
TN_ACCESS_TOKEN=tu_token_acceso_aqui
```

#### Categoría NEW IN
```env
NEWIN_CATEGORY_NAME=NEW IN
NEWIN_HANDLE=new-in67
NEWIN_CATEGORY_ID=34799819
NEWIN_ALLOW_CREATE=true
```

### 2. Verificar conexión

```cmd
bin\who.cmd
```

Deberías ver:
```
[TN] STORE_ID=6566743
[TN] BASE=https://api.tiendanube.com/v1
[TN] Categorías en esta tienda: 227
[OK] Conexión exitosa
```

### 3. Crear tareas programadas

**Abre CMD como Administrador:**
```cmd
cd "C:\Users\santiago\NEW IN"
bin\create_tasks.cmd
```

Esto crea:
- **NewIn-Daily**: Ejecuta todos los días a las 14:00
- **NewIn-WeeklyRefresh**: Ejecuta los lunes a las 14:00

---

## 🎮 USO

### Ejecución manual

#### Daily update (consultar ingresos)
```cmd
bin\daily.cmd
```

#### Refresh semanal (limpiar categoría)
```cmd
bin\refresh.cmd
```

### Comandos de diagnóstico

#### Test de salud completo
```cmd
bin\check_health.cmd
```

#### Listar categorías
```cmd
bin\list_categories.cmd
```

#### Verificar categoría configurada
```cmd
bin\check_category.cmd
```

### Ver logs

Los logs se guardan en `logs\`:
- **daily.log**: Ejecuciones diarias
- **refresh.log**: Refresh semanales

```cmd
notepad logs\daily.log
```

### Estado del sistema

El estado se guarda en `data\state.json`:
```json
{
  "last_run_date": "2024-12-01",
  "last_success_at": "2024-12-01T14:00:00"
}
```

---

## 🏗️ ARQUITECTURA

### Flujo Daily Update

```
┌──────────────┐
│  1. INICIO   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│ 2. Resolver categoría    │
│    - Buscar por ID/handle│
│    - Crear si no existe  │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 3. Listar productos TN   │
│    - Paginación completa │
│    - Indexar por SKU     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 4. Consultar DF          │
│    - Desde último run    │
│    - PAGINACIÓN COMPLETA │
│    - Motivo: ING         │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 5. Build SKUs            │
│    - Articulo#Color#Talle│
│    - Deduplicar          │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 6. Matching              │
│    - Buscar SKU en índice│
│    - Obtener ProductID   │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 7. Asignar categoría     │
│    - PUT /products/{id}  │
│    - Retry en fallos     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 8. Guardar estado        │
│    - last_run_date       │
│    - last_success_at     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────┐
│  9. FIN      │
└──────────────┘
```

### Flujo Weekly Refresh

```
┌──────────────┐
│  1. INICIO   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│ 2. Resolver categoría    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 3. Listar productos      │
│    - Filtrar por cat ID  │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 4. Limpiar categoría     │
│    - PUT con array vacío │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 5. Resetear estado       │
│    - Borrar last_run     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 6. Ejecutar daily        │
│    - Inmediatamente      │
└──────┬───────────────────┘
       │
       ▼
┌──────────────┐
│  7. FIN      │
└──────────────┘
```

---

## 🔧 TROUBLESHOOTING

### ❌ Error: "Python no encontrado"

**Solución:**
1. Instalar Python 3.8+ desde [python.org](https://www.python.org/)
2. Durante instalación, marcar **"Add Python to PATH"**
3. Reiniciar CMD

### ❌ Error: "Módulo 'requests' no encontrado"

**Solución:**
```cmd
python -m pip install requests
```

### ❌ Bajo rate de matching (< 30%)

**Causas posibles:**
1. **SKUs diferentes en TN vs DF**
   - Revisar formato en Tiendanube
   - Verificar logs: `logs\daily.log`
   - Buscar línea: `[MAP] SKUs sin match`

2. **Productos no existen en TN aún**
   - Los productos deben crearse manualmente primero
   - El robot solo asigna categorías, no crea productos

**Debugging:**
```cmd
python newin_robot.py daily --env config.env > debug.txt 2>&1
notepad debug.txt
```

### ❌ Error 404 al asignar categoría

**Solución:**
1. Verificar que la categoría existe:
   ```cmd
   bin\check_category.cmd
   ```

2. Si no existe, revisar `config.env`:
   ```env
   NEWIN_CATEGORY_ID=34799819  # ← Verificar este ID
   NEWIN_ALLOW_CREATE=true     # ← Permitir crear
   ```

3. Listar categorías:
   ```cmd
   bin\list_categories.cmd
   ```

### ❌ Tareas no se ejecutan

**Solución:**
1. Verificar en Programador de Tareas:
   - Windows + R → `taskschd.msc`
   - Buscar "NewIn"
   - Ver historial de ejecuciones

2. Re-crear tareas:
   ```cmd
   bin\create_tasks.cmd
   ```

3. Verificar rutas en las tareas:
   ```
   C:\Users\santiago\NEW IN\bin\daily.cmd
   ```

---

## 📊 LOGS Y MONITOREO

### Estructura de logs

#### daily.log
```
============================================================
DAILY UPDATE - 2024-12-01 14:00:00
============================================================
[TN] Categorías page 1: 200 elementos
[TN] Total categorías: 227
[CAT] ✓ Usando categoría por ENV id=34799819
[TN] Productos listados: 1728
[MAP] Índice variantes por SKU: 7054 entradas
[ACC] Ventana: 2024-11-25 -> 2024-12-01
[DF] 2024-11-25 page=1: 150 items
[DF] 2024-11-25: Total items=150
[MAP] SKUs con match: 120 / 150 (80%)
[TN] PUT categorías resultado: ok=120 fail=0
[SUCCESS] ✓ Asignados 120 productos
============================================================
```

#### refresh.log
```
============================================================
WEEKLY REFRESH - 2024-12-02 14:00:00
============================================================
[TN] Productos que tienen la categoría 34799819: 120
[TN] Limpieza por producto: ok=120 fail=0
[SUCCESS] ✓ Refresh weekly OK
============================================================
```

### Rotación de logs

Los logs rotan automáticamente cada 10MB (implementar si es necesario).

---

## 📞 SOPORTE

### Contacto
- **Desarrollador:** Santiago
- **Proyecto:** NEW IN Robot
- **Versión:** 11.0.0-FIXED

### Issues comunes

1. **Dragonfish no responde**
   - Verificar que el servicio está corriendo
   - Probar: `http://localhost:8009/api.Dragonfish/docs/`

2. **Token expirado**
   - Regenerar token en Dragonfish
   - Actualizar `config.env`

3. **Categoría no se crea**
   - Verificar `NEWIN_ALLOW_CREATE=true`
   - Revisar permisos del token de TN

### Documentación adicional

- **API Zoologic:** Ver `docs/API_DOCUMENTATION.md`
- **API Tiendanube:** [developers.tiendanube.com](https://developers.tiendanube.com)

---

## 📝 CHANGELOG

Ver [CHANGELOG.md](CHANGELOG.md) para historial completo de cambios.

---

## 📄 LICENCIA

Proyecto interno - Todos los derechos reservados.

---

**¡Listo para producción! 🚀**
