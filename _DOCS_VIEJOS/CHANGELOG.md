# 📋 CHANGELOG

Historial de cambios del proyecto NEW IN ROBOT.

---

## [11.0.0-FIXED] - 2024-12-01

### 🔥 CORRECCIONES CRÍTICAS

#### Paginación de Dragonfish
- **ANTES:** Solo consultaba página 1 (máximo 200 items por día)
- **AHORA:** Itera sobre todas las páginas hasta obtener todos los movimientos
- **IMPACTO:** Se procesaban solo los primeros 200 ingresos, perdiendo el resto
- **SOLUCIÓN:** Nueva función `df_get_movimientos_paginated()` que implementa paginación completa

#### Manejo de errores
- **ANTES:** Errores se "tragaban" y continuaba con datos vacíos
- **AHORA:** Logging completo con tracebacks y códigos de error
- **IMPACTO:** Fallos pasaban desapercibidos
- **SOLUCIÓN:** Función `log_error()` con traceback completo

#### Catchup window
- **ANTES:** Solo 4 días de historia (CATCHUP_DAYS=4)
- **AHORA:** 7 días de historia (CATCHUP_DAYS=7)
- **IMPACTO:** Si las tareas no corrían por 5+ días, se perdían movimientos
- **SOLUCIÓN:** Aumentado a 7 días para mayor seguridad

#### Validación de categorías
- **ANTES:** Error 404 al asignar categoría inexistente
- **AHORA:** Validación previa con `_validate_category_id()`
- **IMPACTO:** Fallos constantes en producción
- **SOLUCIÓN:** Validación antes de cada operación

#### Rutas hardcodeadas
- **ANTES:** Rutas fijas en `C:\Users\santiago\`
- **AHORA:** Rutas dinámicas basadas en ubicación del proyecto
- **IMPACTO:** Imposible mover el proyecto
- **SOLUCIÓN:** Variable `BASE_DIR` configurable

### ✨ NUEVAS CARACTERÍSTICAS

- Retry automático con backoff exponencial
- Logging estructurado con timestamps
- Scripts de diagnóstico (`check_health.cmd`)
- Instalador automático (`install.cmd`)
- Documentación completa (README.md)
- Validación pre-vuelo de archivos y dependencias

### 📊 MEJORAS EN LOGS

- Headers con separadores visuales
- Timestamps en cada ejecución
- Códigos de salida documentados
- Conteo de éxitos/fallos
- Rate de matching reportado

### 🔧 SCRIPTS DE UTILIDAD

Nuevos scripts en `bin/`:
- `install.cmd` - Instalador inicial
- `daily.cmd` - Ejecución diaria con logging
- `refresh.cmd` - Refresh semanal + daily
- `create_tasks.cmd` - Crear tareas programadas
- `check_health.cmd` - Diagnóstico completo
- `who.cmd` - Test de conexión
- `list_categories.cmd` - Listar categorías
- `check_category.cmd` - Verificar categoría

### 📦 REORGANIZACIÓN

Nueva estructura:
```
C:\Users\santiago\NEW IN\
├── newin_robot.py
├── config.env
├── README.md
├── CHANGELOG.md
├── bin\          # Scripts
├── data\         # Estado persistente
├── logs\         # Logs de ejecución
└── docs\         # Documentación
```

---

## [10.0.0] - 2024-10-XX (Versión anterior)

### Características
- Asignación de categoría por producto (PUT /products/{id})
- Paginación de categorías (per_page=200)
- Paginación de productos (per_page=100)
- Construcción de SKU: `Articulo#Color#Talle`
- Persistencia de categoría en JSON
- Comandos: daily, refresh, list_cats, check_cat, who

### Problemas conocidos
- ⚠️ Sin paginación en Dragonfish (solo página 1)
- ⚠️ Bajo rate de matching (~22%)
- ⚠️ Errores silenciosos
- ⚠️ Catchup muy corto (4 días)
- ⚠️ Rutas hardcodeadas

---

## [9.0.0] - 2024-09-XX

### Características
- Integración básica DF → TN
- Categorización manual
- Logs simples

---

## Convenciones de versionado

Usamos [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles de API
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs

### Códigos de cambio
- 🔥 Corrección crítica
- ✨ Nueva característica
- 🐛 Corrección de bug
- 📊 Mejora en logs
- 🔧 Herramientas
- 📦 Reorganización
- 📝 Documentación
- ⚡ Performance

---

## Próximas versiones (Roadmap)

### [11.1.0] - Planificado
- [ ] Webhook para sincronización en tiempo real
- [ ] Dashboard web para monitoreo
- [ ] Notificaciones por email en fallos
- [ ] Backup automático de estado
- [ ] Métricas de performance

### [12.0.0] - Planificado
- [ ] Soporte multi-tienda
- [ ] Sincronización bidireccional
- [ ] API REST propia
- [ ] Panel de administración web
- [ ] Integración con otros sistemas ERP

---

**Última actualización:** 2024-12-01
