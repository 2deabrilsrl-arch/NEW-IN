# 📁 ESTRUCTURA DEL PROYECTO - NEW IN ROBOT

Guía visual de todos los archivos y carpetas del proyecto.

---

## 🗂️ ESTRUCTURA COMPLETA

```
C:\Users\santiago\NEW IN\
│
├── 📄 newin_robot.py              # ⚙️ Script principal (CORE)
├── 📄 config.env                  # 🔧 Configuración (EDITAR AQUÍ)
│
├── 📖 README.md                   # 📚 Documentación completa
├── 📖 README_QUICK_START.md       # ⚡ Guía rápida (empezar aquí)
├── 📖 INSTALL.md                  # 🚀 Instalación paso a paso
├── 📖 RESUMEN_AUDITORIA.md        # 🔍 Informe técnico de auditoría
├── 📖 CHANGELOG.md                # 📝 Historial de cambios
├── 📖 ESTRUCTURA_PROYECTO.md      # 📁 Este archivo
│
├── 📂 bin\                        # 🛠️ Scripts de utilidad
│   ├── install.cmd                # 🔨 Instalador automático
│   ├── daily.cmd                  # ▶️ Ejecución diaria
│   ├── refresh.cmd                # 🔄 Refresh semanal (lunes)
│   ├── create_tasks.cmd           # ⏰ Crear tareas programadas
│   ├── check_health.cmd           # 🏥 Diagnóstico completo
│   ├── who.cmd                    # 👤 Test de conexión
│   ├── list_categories.cmd        # 📋 Listar categorías TN
│   └── check_category.cmd         # ✅ Verificar categoría
│
├── 📂 data\                       # 💾 Datos persistentes (autogenerado)
│   ├── state.json                 # 📊 Estado de última ejecución
│   └── newin_category.json        # 🏷️ Categoría persistida
│
├── 📂 logs\                       # 📜 Logs de ejecución (autogenerado)
│   ├── daily.log                  # 📝 Log de ejecuciones diarias
│   └── refresh.log                # 📝 Log de refresh semanales
│
└── 📂 docs\                       # 📚 Documentación adicional
    └── (vacía por ahora)
```

---

## 📄 ARCHIVOS PRINCIPALES

### newin_robot.py ⚙️

**QUÉ ES:** Script principal de Python que hace toda la magia.

**QUÉ HACE:**
- Consulta ingresos de Dragonfish
- Busca productos en Tiendanube por SKU
- Asigna categoría NEW IN
- Limpia categoría los lunes

**CUÁNDO SE USA:** Lo ejecutan los scripts de `bin/`

**NO EDITAR** (a menos que sepas lo que haces)

---

### config.env 🔧

**QUÉ ES:** Archivo de configuración con todas las credenciales.

**QUÉ CONTIENE:**
- Tokens de Dragonfish y Tiendanube
- IDs de tienda y categoría
- Configuración de comportamiento

**EDITAR:** ✅ SÍ - Este archivo debe editarse con tus credenciales

**IMPORTANTE:** 
- No compartir (contiene tokens secretos)
- Hacer backup antes de modificar
- Usar el formato correcto

**Ejemplo:**
```env
TN_STORE_ID=6566743
TN_ACCESS_TOKEN=tu_token_aqui
NEWIN_CATEGORY_ID=34799819
```

---

## 📚 DOCUMENTACIÓN

### README.md 📖

**QUÉ ES:** Documentación completa del proyecto.

**CONTIENE:**
- Descripción del proyecto
- Características
- Correcciones de la v11
- Requisitos
- Guía de instalación
- Guía de uso
- Arquitectura
- Troubleshooting

**LEER:** Después del Quick Start

---

### README_QUICK_START.md ⚡

**QUÉ ES:** Guía rápida para empezar en 10 minutos.

**CONTIENE:**
- Instalación express
- Configuración mínima
- Primera ejecución
- Comandos básicos

**LEER:** ✅ PRIMERO - Empieza aquí

---

### INSTALL.md 🚀

**QUÉ ES:** Guía detallada de instalación paso a paso.

**CONTIENE:**
- Requisitos previos
- Instalación de Python
- Instalación de dependencias
- Configuración detallada
- Verificación
- Programación de tareas
- Troubleshooting

**LEER:** Si tienes problemas con la instalación

---

### RESUMEN_AUDITORIA.md 🔍

**QUÉ ES:** Informe técnico de auditoría del código.

**CONTIENE:**
- Hallazgos críticos
- Análisis de logs
- Correcciones implementadas
- Mejoras de rendimiento
- Recomendaciones

**LEER:** Para entender qué se corrigió y por qué

---

### CHANGELOG.md 📝

**QUÉ ES:** Historial de cambios entre versiones.

**CONTIENE:**
- Versión 11.0.0-FIXED (actual)
- Versión 10.0.0 (anterior)
- Próximas versiones (roadmap)

**LEER:** Para ver historial de cambios

---

## 🛠️ SCRIPTS (bin/)

### install.cmd 🔨

**QUÉ HACE:**
1. Verifica Python instalado
2. Instala dependencia `requests`
3. Crea directorios
4. Prueba conexión

**CUÁNDO USAR:** Primera vez, después de descargar

**CÓMO USAR:**
```cmd
bin\install.cmd
```

---

### daily.cmd ▶️

**QUÉ HACE:**
1. Ejecuta `newin_robot.py daily`
2. Guarda logs en `logs\daily.log`
3. Reporta resultado

**CUÁNDO USAR:**
- Manualmente para probar
- Automáticamente todos los días (tarea programada)

**CÓMO USAR:**
```cmd
bin\daily.cmd
```

---

### refresh.cmd 🔄

**QUÉ HACE:**
1. Ejecuta `newin_robot.py refresh`
2. Limpia categoría NEW IN
3. Resetea estado
4. Ejecuta daily inmediatamente

**CUÁNDO USAR:**
- Manualmente si quieres resetear
- Automáticamente los lunes (tarea programada)

**CÓMO USAR:**
```cmd
bin\refresh.cmd
```

---

### create_tasks.cmd ⏰

**QUÉ HACE:**
1. Crea tarea "NewIn-Daily" (diaria 14:00)
2. Crea tarea "NewIn-WeeklyRefresh" (lunes 14:00)

**CUÁNDO USAR:** Después de instalar

**CÓMO USAR:**
```cmd
# Abrir CMD como Administrador
bin\create_tasks.cmd
```

**IMPORTANTE:** Requiere permisos de Administrador

---

### check_health.cmd 🏥

**QUÉ HACE:**
1. Verifica archivos presentes
2. Verifica directorios
3. Verifica Python y dependencias
4. Prueba conexión a APIs
5. Verifica tareas programadas
6. Muestra logs recientes
7. Muestra estado guardado

**CUÁNDO USAR:**
- Cuando algo no funciona
- Para diagnóstico completo

**CÓMO USAR:**
```cmd
bin\check_health.cmd
```

---

### who.cmd 👤

**QUÉ HACE:**
- Muestra info de conexión
- Lista algunas categorías
- Muestra producto de ejemplo

**CUÁNDO USAR:**
- Para verificar que la conexión funciona
- Para ver datos de tu tienda

**CÓMO USAR:**
```cmd
bin\who.cmd
```

---

### list_categories.cmd 📋

**QUÉ HACE:**
- Lista TODAS las categorías de Tiendanube

**CUÁNDO USAR:**
- Para encontrar el ID de tu categoría NEW IN
- Para verificar nombres y handles

**CÓMO USAR:**
```cmd
bin\list_categories.cmd
```

---

### check_category.cmd ✅

**QUÉ HACE:**
- Verifica que la categoría configurada existe

**CUÁNDO USAR:**
- Después de editar `config.env`
- Si hay errores 404 al asignar

**CÓMO USAR:**
```cmd
bin\check_category.cmd
```

---

## 💾 DATOS (data/)

### state.json 📊

**QUÉ ES:** Estado de última ejecución exitosa.

**CONTIENE:**
```json
{
  "last_run_date": "2024-12-01",
  "last_success_at": "2024-12-01T14:00:00",
  "last_refresh_at": "2024-12-02T14:00:00"
}
```

**NO EDITAR** (se actualiza automáticamente)

**LEER:** Para ver cuándo fue la última ejecución

---

### newin_category.json 🏷️

**QUÉ ES:** Categoría persistida para no buscarla cada vez.

**CONTIENE:**
```json
{
  "category_id": 34799819,
  "handle": "new-in67",
  "updated_at": "2024-12-01T14:00:00",
  "source": "env"
}
```

**NO EDITAR** (se actualiza automáticamente)

---

## 📜 LOGS (logs/)

### daily.log 📝

**QUÉ CONTIENE:**
- Timestamp de cada ejecución
- Categorías listadas
- Productos procesados
- SKUs con/sin match
- Resultado de asignaciones
- Errores si los hay

**LEER:** Para ver qué pasó en cada ejecución diaria

**EJEMPLO:**
```
============================================================
DAILY UPDATE - 2024-12-01 14:00:00
============================================================
[TN] Categorías: 227
[TN] Productos: 1728
[MAP] SKUs con match: 120 / 150 (80%)
[SUCCESS] ✓ Asignados 120 productos
```

---

### refresh.log 📝

**QUÉ CONTIENE:**
- Timestamp de cada refresh
- Productos con categoría NEW IN
- Resultado de limpieza

**LEER:** Para ver qué pasó en cada refresh semanal

**EJEMPLO:**
```
============================================================
WEEKLY REFRESH - 2024-12-02 14:00:00
============================================================
[TN] Productos con categoría: 120
[TN] Limpieza: ok=120 fail=0
[SUCCESS] ✓ Refresh OK
```

---

## 🎯 FLUJO DE TRABAJO

### Primera vez

1. Descargar proyecto → `C:\Users\santiago\NEW IN\`
2. Ejecutar → `bin\install.cmd`
3. Editar → `config.env`
4. Verificar → `bin\who.cmd`
5. Probar → `bin\daily.cmd`
6. Programar → `bin\create_tasks.cmd`

### Uso diario

- **Automático:** Las tareas se ejecutan solas
- **Manual:** `bin\daily.cmd` o `bin\refresh.cmd`
- **Monitoreo:** `notepad logs\daily.log`

### Diagnóstico

1. `bin\check_health.cmd` - Diagnóstico completo
2. `notepad logs\daily.log` - Ver qué pasó
3. `notepad data\state.json` - Ver último estado

---

## 📊 TAMAÑOS APROXIMADOS

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| newin_robot.py | ~34 KB | Script principal |
| config.env | ~3 KB | Configuración |
| README.md | ~14 KB | Doc completa |
| logs/daily.log | Variable | Crece con el tiempo |
| data/state.json | ~200 bytes | Estado mínimo |

**Total proyecto:** ~100 KB (sin logs)

---

## 🔐 SEGURIDAD

### Archivos sensibles (NO compartir)

- ❌ `config.env` - Contiene tokens
- ❌ `data/state.json` - Info de tu tienda
- ❌ `logs/*.log` - Puede tener datos sensibles

### Archivos seguros (OK compartir)

- ✅ `newin_robot.py` - Script público
- ✅ `README.md` - Documentación
- ✅ `bin/*.cmd` - Scripts de utilidad

---

## 📞 AYUDA RÁPIDA

**¿Archivo falta?**
- Verificar que extrajiste todo el ZIP
- Ejecutar `bin\install.cmd` para crear carpetas

**¿No entiendo un archivo?**
- Ver esta guía (ESTRUCTURA_PROYECTO.md)
- Ver README.md para más detalles

**¿Algo no funciona?**
- Ejecutar `bin\check_health.cmd`
- Ver logs en `logs\`

---

**Última actualización:** 2024-12-01  
**Versión:** 11.0.0-FIXED
