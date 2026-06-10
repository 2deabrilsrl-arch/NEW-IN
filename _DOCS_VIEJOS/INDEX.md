# 📑 ÍNDICE - NEW IN ROBOT v11.0.0-FIXED

Tabla de contenidos completa del proyecto.

---

## 🚀 EMPEZAR AQUÍ

**Si es tu primera vez con el proyecto:**

1. 📖 **README_QUICK_START.md** - Guía rápida (10 minutos)
2. 🚀 **INSTALL.md** - Instalación paso a paso
3. ✅ **CHECKLIST_INSTALACION.md** - Lista de verificación

---

## 📚 DOCUMENTACIÓN

| Archivo | Descripción | ¿Cuándo leer? |
|---------|-------------|---------------|
| **README.md** | Documentación completa del proyecto | Después del Quick Start |
| **README_QUICK_START.md** | ⚡ Guía rápida de inicio | PRIMERO - Empezar aquí |
| **INSTALL.md** | Guía detallada de instalación | Si tienes problemas |
| **CHECKLIST_INSTALACION.md** | Lista de verificación paso a paso | Durante instalación |
| **ESTRUCTURA_PROYECTO.md** | Explicación de cada archivo | Si no entiendes la estructura |
| **RESUMEN_AUDITORIA.md** | 🔍 Informe técnico de auditoría | Para entender las correcciones |
| **CHANGELOG.md** | Historial de cambios y versiones | Para ver qué cambió |
| **INDEX.md** | Este archivo - Índice general | Cuando estés perdido |

---

## ⚙️ ARCHIVOS PRINCIPALES

| Archivo | Tipo | ¿Editar? | Descripción |
|---------|------|----------|-------------|
| **newin_robot.py** | Python | ❌ NO | Script principal - Hace toda la magia |
| **config.env** | Config | ✅ SÍ | Configuración - Editar con tus credenciales |

---

## 🛠️ SCRIPTS DE UTILIDAD (bin/)

### Instalación y configuración

| Script | Descripción | Cuándo usar |
|--------|-------------|-------------|
| **install.cmd** | Instalador automático | Primera vez |
| **create_tasks.cmd** | Crear tareas programadas | Después de instalar (como Admin) |

### Ejecución

| Script | Descripción | Cuándo usar |
|--------|-------------|-------------|
| **daily.cmd** | Ejecución diaria | Manual o automático (diario 14:00) |
| **refresh.cmd** | Refresh semanal | Manual o automático (lunes 14:00) |

### Diagnóstico

| Script | Descripción | Cuándo usar |
|--------|-------------|-------------|
| **check_health.cmd** | Diagnóstico completo | Cuando algo no funciona |
| **who.cmd** | Test de conexión | Para verificar credenciales |
| **list_categories.cmd** | Listar categorías TN | Para encontrar ID de categoría |
| **check_category.cmd** | Verificar categoría | Después de editar config.env |

---

## 💾 DATOS PERSISTENTES (data/)

| Archivo | Tipo | Descripción | ¿Editar? |
|---------|------|-------------|----------|
| **state.json** | JSON | Estado de última ejecución | ❌ NO (autogenerado) |
| **newin_category.json** | JSON | Categoría persistida | ❌ NO (autogenerado) |

**Nota:** Estos archivos se crean automáticamente en la primera ejecución.

---

## 📜 LOGS (logs/)

| Archivo | Descripción | Rotación |
|---------|-------------|----------|
| **daily.log** | Log de ejecuciones diarias | Manual (cuando sea muy grande) |
| **refresh.log** | Log de refresh semanales | Manual (cuando sea muy grande) |

**Nota:** Los logs se crean automáticamente en la primera ejecución.

---

## 🗂️ ESTRUCTURA VISUAL

```
C:\Users\santiago\NEW IN\
│
├── 📄 ARCHIVOS PRINCIPALES
│   ├── newin_robot.py              ⚙️ Script principal
│   └── config.env                  🔧 Configuración (EDITAR)
│
├── 📖 DOCUMENTACIÓN
│   ├── INDEX.md                    📑 Este archivo
│   ├── README.md                   📚 Doc completa
│   ├── README_QUICK_START.md       ⚡ Quick start
│   ├── INSTALL.md                  🚀 Instalación
│   ├── CHECKLIST_INSTALACION.md    ✅ Checklist
│   ├── ESTRUCTURA_PROYECTO.md      📁 Estructura
│   ├── RESUMEN_AUDITORIA.md        🔍 Auditoría
│   └── CHANGELOG.md                📝 Cambios
│
├── 🛠️ SCRIPTS (bin/)
│   ├── INSTALACIÓN
│   │   ├── install.cmd             🔨 Instalador
│   │   └── create_tasks.cmd        ⏰ Crear tareas
│   │
│   ├── EJECUCIÓN
│   │   ├── daily.cmd               ▶️ Diario
│   │   └── refresh.cmd             🔄 Semanal
│   │
│   └── DIAGNÓSTICO
│       ├── check_health.cmd        🏥 Diagnóstico
│       ├── who.cmd                 👤 Test conexión
│       ├── list_categories.cmd     📋 Listar cats
│       └── check_category.cmd      ✅ Verificar cat
│
├── 💾 DATOS (data/) - Autogenerado
│   ├── state.json                  📊 Estado
│   └── newin_category.json         🏷️ Categoría
│
└── 📜 LOGS (logs/) - Autogenerado
    ├── daily.log                   📝 Log diario
    └── refresh.log                 📝 Log refresh
```

---

## 🎯 RUTAS RÁPIDAS POR TAREA

### 🆕 Primera instalación

1. **README_QUICK_START.md** - Empezar aquí
2. **INSTALL.md** - Guía detallada
3. **CHECKLIST_INSTALACION.md** - Verificar pasos
4. `bin\install.cmd` - Ejecutar instalador
5. `config.env` - Editar credenciales
6. `bin\who.cmd` - Verificar conexión

---

### ▶️ Uso diario

- **Ejecutar manual:** `bin\daily.cmd`
- **Ver logs:** `logs\daily.log`
- **Ver estado:** `data\state.json`
- **Diagnóstico:** `bin\check_health.cmd`

---

### 🔄 Refresh semanal

- **Ejecutar manual:** `bin\refresh.cmd`
- **Ver logs:** `logs\refresh.log`
- **Programar automático:** `bin\create_tasks.cmd`

---

### 🐛 Troubleshooting

1. **check_health.cmd** - Diagnóstico completo
2. **logs\daily.log** - Ver qué pasó
3. **README.md** → Sección Troubleshooting
4. **RESUMEN_AUDITORIA.md** - Problemas conocidos

---

### 🔧 Configuración

- **Editar:** `config.env`
- **Verificar:** `bin\check_category.cmd`
- **Listar categorías:** `bin\list_categories.cmd`
- **Test conexión:** `bin\who.cmd`

---

### 📊 Monitoreo

- **Logs diarios:** `notepad logs\daily.log`
- **Logs refresh:** `notepad logs\refresh.log`
- **Estado actual:** `notepad data\state.json`
- **Categoría:** `notepad data\newin_category.json`

---

### ⏰ Tareas programadas

- **Crear:** `bin\create_tasks.cmd` (como Admin)
- **Verificar:** Windows + R → `taskschd.msc`
- **Buscar:** "NewIn" en la lista

---

## 📊 TAMAÑOS DE ARCHIVOS

| Categoría | Archivos | Tamaño total (aprox) |
|-----------|----------|----------------------|
| **Python** | 1 archivo | 34 KB |
| **Configuración** | 1 archivo | 3 KB |
| **Documentación** | 8 archivos | 50 KB |
| **Scripts** | 8 archivos | 20 KB |
| **Datos** | 2 archivos (después de 1ra ejecución) | 1 KB |
| **Logs** | 2 archivos (crecen con el tiempo) | Variable |
| **TOTAL (inicial)** | - | ~110 KB |

---

## 🔐 ARCHIVOS SENSIBLES

### ⚠️ NO compartir:

- ❌ `config.env` - Contiene tokens secretos
- ❌ `data/state.json` - Info de tu tienda
- ❌ `logs/*.log` - Puede contener datos sensibles

### ✅ OK compartir:

- ✅ `newin_robot.py` - Código público
- ✅ `README.md` - Documentación
- ✅ `bin/*.cmd` - Scripts de utilidad
- ✅ Todos los archivos de documentación

---

## 📖 ORDEN DE LECTURA RECOMENDADO

### Para usuarios nuevos:

1. **INDEX.md** (este archivo) - Para orientarte
2. **README_QUICK_START.md** - Quick start
3. **CHECKLIST_INSTALACION.md** - Durante instalación
4. **ESTRUCTURA_PROYECTO.md** - Para entender la estructura
5. **README.md** - Documentación completa
6. **INSTALL.md** - Si necesitas más detalles

### Para administradores:

1. **RESUMEN_AUDITORIA.md** - Informe técnico
2. **CHANGELOG.md** - Qué cambió
3. **README.md** - Arquitectura y flujos
4. **ESTRUCTURA_PROYECTO.md** - Detalles de implementación

### Para troubleshooting:

1. `bin\check_health.cmd` - Ejecutar primero
2. `logs\daily.log` - Ver errores
3. **README.md** → Troubleshooting
4. **RESUMEN_AUDITORIA.md** → Problemas conocidos

---

## 🆘 AYUDA RÁPIDA

### ¿Algo no funciona?

```cmd
bin\check_health.cmd    # Diagnóstico automático
notepad logs\daily.log  # Ver qué pasó
```

### ¿No entiendo un archivo?

- Ver **ESTRUCTURA_PROYECTO.md** - Explica cada archivo

### ¿Necesito ayuda con instalación?

- Ver **INSTALL.md** - Guía paso a paso
- Ver **CHECKLIST_INSTALACION.md** - Lista de verificación

### ¿Quiero info técnica?

- Ver **RESUMEN_AUDITORIA.md** - Auditoría completa
- Ver **CHANGELOG.md** - Cambios técnicos

---

## 📊 RESUMEN EJECUTIVO

| Item | Valor |
|------|-------|
| **Versión** | 11.0.0-FIXED |
| **Fecha** | Diciembre 2024 |
| **Archivos totales** | 20 archivos |
| **Tamaño total** | ~110 KB (sin logs) |
| **Lenguaje** | Python 3.8+ |
| **Plataforma** | Windows 10/11 |
| **Dependencias** | requests |

---

## ✅ VERIFICACIÓN RÁPIDA

Después de descargar, deberías tener:

- [ ] 1 script Python (`.py`)
- [ ] 1 archivo de config (`.env`)
- [ ] 8 archivos de documentación (`.md`)
- [ ] 8 scripts de utilidad (`.cmd` en `bin/`)

**Total:** 18 archivos principales

**Carpetas vacías (se crean automáticamente):**
- [ ] `data/` - Para estado
- [ ] `logs/` - Para logs
- [ ] `docs/` - Para docs adicionales

---

## 🎉 ¡LISTO PARA EMPEZAR!

Si tienes todos los archivos, continúa con:

→ **README_QUICK_START.md** para instalación rápida

→ **INSTALL.md** para instalación detallada

---

**Última actualización:** 2024-12-01  
**Versión:** 11.0.0-FIXED  
**Proyecto:** NEW IN ROBOT
