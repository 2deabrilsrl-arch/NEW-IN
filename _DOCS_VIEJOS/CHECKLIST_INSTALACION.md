# ✅ CHECKLIST DE INSTALACIÓN - NEW IN ROBOT

Lista de verificación completa para instalación y puesta en marcha.

---

## 📋 FASE 1: PRE-INSTALACIÓN

### Requisitos previos

- [ ] Windows 10/11 instalado
- [ ] Permisos de Administrador disponibles
- [ ] Conexión a internet activa
- [ ] Dragonfish ejecutándose (para test)
- [ ] Tiendanube con acceso a admin

### Credenciales necesarias

- [ ] Token JWT de Dragonfish
  - ¿Dónde obtener? → Dragonfish: Config → Cliente REST API → Obtener Token
  - Formato: `eyJ0eXAiOiJKV1QiLCJhbGc...`
  
- [ ] Token de acceso Tiendanube
  - ¿Dónde obtener? → [partners.tiendanube.com](https://partners.tiendanube.com)
  - Formato: `accb4de2caf771902f651fe...`
  
- [ ] ID de tienda Tiendanube
  - ¿Dónde ver? → URL del admin: `.../6566743/...`
  - Formato: `6566743`
  
- [ ] ID de categoría NEW IN (o nombre para crear)
  - ¿Dónde ver? → Admin → Productos → Categorías → ID en URL
  - Formato: `34799819`

---

## 📥 FASE 2: DESCARGA Y UBICACIÓN

### Descargar proyecto

- [ ] Archivo descargado: `NEW_IN_ROBOT_v11.zip` (o archivos individuales)
- [ ] Extraído en ubicación correcta

### Verificar estructura

```
C:\Users\santiago\NEW IN\
├── newin_robot.py           ✓
├── config.env               ✓
├── README.md                ✓
├── bin\
│   ├── install.cmd          ✓
│   ├── daily.cmd            ✓
│   ├── refresh.cmd          ✓
│   └── ...                  ✓
└── ...
```

**Checklist de archivos:**
- [ ] `newin_robot.py` presente
- [ ] `config.env` presente
- [ ] Carpeta `bin\` presente con 8 archivos .cmd
- [ ] Archivos README presentes

---

## 🐍 FASE 3: PYTHON

### Verificar Python

Abrir CMD:
```cmd
python --version
```

- [ ] Python 3.8 o superior instalado
- [ ] Versión mostrada: `Python 3.x.x`

### Si no está instalado

- [ ] Ir a [python.org/downloads](https://www.python.org/downloads/)
- [ ] Descargar Python 3.11+
- [ ] **IMPORTANTE:** Marcar "Add Python to PATH" durante instalación
- [ ] Reiniciar CMD después de instalar
- [ ] Verificar nuevamente: `python --version`

---

## 📦 FASE 4: INSTALACIÓN

### Ejecutar instalador

```cmd
cd "C:\Users\santiago\NEW IN"
bin\install.cmd
```

**Verificar resultados:**
- [ ] [OK] Python encontrado
- [ ] [OK] Dependencias instaladas
- [ ] [OK] Directorios creados

### Si hay errores

- **Error: Python no encontrado**
  - [ ] Verificar PATH: `where python`
  - [ ] Reinstalar Python con "Add to PATH"
  
- **Error: pip no funciona**
  - [ ] Ejecutar: `python -m pip install --upgrade pip`
  - [ ] Reintentar instalación

---

## ⚙️ FASE 5: CONFIGURACIÓN

### Editar config.env

```cmd
notepad config.env
```

**Sección: Dragonfish**
- [ ] `DF_BASE_URL` configurado
- [ ] `DF_JWTOKEN` pegado (token completo)
- [ ] `DF_BASEDEDATOS` configurado
- [ ] `DF_IDCLIENTE` configurado

**Sección: Tiendanube**
- [ ] `TN_STORE_ID` configurado
- [ ] `TN_ACCESS_TOKEN` pegado (token completo)

**Sección: Categoría NEW IN**
- [ ] `NEWIN_CATEGORY_NAME` configurado
- [ ] `NEWIN_HANDLE` configurado
- [ ] `NEWIN_CATEGORY_ID` configurado (o vacío)
- [ ] `NEWIN_ALLOW_CREATE` configurado (`true` o `false`)

**Sección: Comportamiento**
- [ ] `CATCHUP_DAYS` verificado (default: 7)

**IMPORTANTE:**
- [ ] Archivo guardado después de editar
- [ ] Sin espacios extra en tokens
- [ ] Sin comillas en valores
- [ ] Formato: `KEY=value` (sin espacios alrededor de `=`)

---

## ✅ FASE 6: VERIFICACIÓN

### Test 1: Conexión

```cmd
bin\who.cmd
```

**Verificar salida:**
- [ ] `[TN] STORE_ID=...` mostrado
- [ ] `[TN] Categorías: X` mostrado (X > 0)
- [ ] Sin errores de conexión
- [ ] Sin errores de autenticación

**Si falla:**
- [ ] Verificar tokens en `config.env`
- [ ] Verificar que Dragonfish está corriendo
- [ ] Verificar conexión a internet

---

### Test 2: Listar categorías

```cmd
bin\list_categories.cmd
```

**Verificar:**
- [ ] Se listan las categorías de tu tienda
- [ ] La categoría NEW IN aparece (si existe)
- [ ] IDs y nombres correctos

---

### Test 3: Verificar categoría

```cmd
bin\check_category.cmd
```

**Resultado esperado:**
- [ ] `[CHECK] ✓ Existe: id=...` (si categoría existe)
- [ ] O `[CHECK] ✗ NO existe` (si no existe)

**Si no existe:**
- [ ] Verificar `NEWIN_CATEGORY_ID` en `config.env`
- [ ] O activar `NEWIN_ALLOW_CREATE=true`
- [ ] Ejecutar `bin\who.cmd` para crear automáticamente

---

### Test 4: Diagnóstico completo

```cmd
bin\check_health.cmd
```

**Verificar todas las secciones:**
- [ ] ✅ Archivos: OK
- [ ] ✅ Directorios: OK
- [ ] ✅ Python: OK
- [ ] ✅ Dependencias: OK
- [ ] ✅ Conexión: OK

---

## ▶️ FASE 7: PRIMERA EJECUCIÓN

### Ejecución manual

```cmd
bin\daily.cmd
```

**Monitorear salida:**
- [ ] Inicia sin errores
- [ ] Conecta a Dragonfish
- [ ] Conecta a Tiendanube
- [ ] Lista productos
- [ ] Consulta movimientos
- [ ] Reporta SKUs encontrados

**Resultado esperado:**
```
[SUCCESS] ✓ Asignados X productos a categoría id=...
```

**Verificar log:**
```cmd
notepad logs\daily.log
```

**En el log debe verse:**
- [ ] Timestamp de ejecución
- [ ] Categorías listadas
- [ ] Productos listados
- [ ] Ventana de fechas consultadas
- [ ] SKUs con/sin match
- [ ] Resultado de asignaciones

---

### Verificar en Tiendanube

1. Ir a: Admin → Productos → Categorías
2. Click en "NEW IN"
3. **Verificar:**
   - [ ] Productos asignados
   - [ ] Los productos son ingresos recientes

---

### Analizar matching

**Del log, buscar línea:**
```
[MAP] SKUs con match: X / Y (Z%)
```

**Verificar:**
- [ ] Porcentaje de match > 50% (ideal: >80%)
- [ ] Si es bajo (<30%), investigar:
  - [ ] Ver: `[MAP] SKUs sin match`
  - [ ] Comparar formato con SKUs en Tiendanube
  - [ ] Verificar que productos existen en TN

---

## ⏰ FASE 8: TAREAS PROGRAMADAS

### Crear tareas

**Abrir CMD como Administrador:**
- [ ] Click derecho en botón Windows
- [ ] Seleccionar "Terminal (Admin)" o "CMD (Admin)"

```cmd
cd "C:\Users\santiago\NEW IN"
bin\create_tasks.cmd
```

**Verificar creación:**
- [ ] Tarea "NewIn-Daily" creada
- [ ] Tarea "NewIn-WeeklyRefresh" creada
- [ ] Sin errores

---

### Verificar en Programador de Tareas

1. Presionar: Windows + R
2. Escribir: `taskschd.msc`
3. Enter

**Verificar:**
- [ ] Tarea "NewIn-Daily" visible
  - [ ] Trigger: Diario 14:00
  - [ ] Acción: `C:\Users\santiago\NEW IN\bin\daily.cmd`
  - [ ] Estado: Listo
  
- [ ] Tarea "NewIn-WeeklyRefresh" visible
  - [ ] Trigger: Semanal, Lunes 14:00
  - [ ] Acción: `C:\Users\santiago\NEW IN\bin\refresh.cmd`
  - [ ] Estado: Listo

---

### Configurar notificaciones (opcional)

En el Programador de Tareas:
- [ ] Click derecho en tarea → Propiedades
- [ ] Pestaña "Historial": Habilitar
- [ ] Configurar eventos en Event Viewer si deseas alertas

---

## 📊 FASE 9: MONITOREO

### Primera semana

**Revisar logs diariamente:**
```cmd
notepad logs\daily.log
```

**Verificar:**
- [ ] Día 1: Ejecutó correctamente
- [ ] Día 2: Ejecutó correctamente
- [ ] Día 3: Ejecutó correctamente
- [ ] Día 4: Ejecutó correctamente
- [ ] Día 5: Ejecutó correctamente
- [ ] Día 6: Ejecutó correctamente
- [ ] Día 7: Ejecutó correctamente

**En cada día verificar:**
- [ ] Timestamp presente
- [ ] Sin errores
- [ ] SKUs procesados
- [ ] Productos asignados

---

### Primera semana (Lunes)

**Verificar refresh:**
```cmd
notepad logs\refresh.log
```

**Debe verse:**
- [ ] Limpieza de categoría ejecutada
- [ ] X productos limpiados
- [ ] Estado reseteado
- [ ] Daily ejecutado inmediatamente después

---

### Verificar en Tiendanube

**Cada día:**
- [ ] La categoría NEW IN tiene productos
- [ ] Los productos son ingresos recientes

**Cada lunes:**
- [ ] La categoría se limpia correctamente
- [ ] Se vuelve a poblar con ingresos de la semana

---

## 🔧 FASE 10: MANTENIMIENTO

### Semanal

- [ ] Ejecutar diagnóstico: `bin\check_health.cmd`
- [ ] Revisar logs: `logs\daily.log`
- [ ] Verificar estado: `data\state.json`

### Mensual

- [ ] Backup de `config.env`
- [ ] Backup de `data\`
- [ ] Backup de `logs\`
- [ ] Verificar espacio en disco
- [ ] Revisar rate de matching
- [ ] Ajustar configuración si es necesario

---

## 🎯 CHECKLIST FINAL

### ✅ TODO LISTO SI:

- [ ] Python instalado y funcionando
- [ ] Dependencias instaladas
- [ ] `config.env` configurado con todas las credenciales
- [ ] Test de conexión exitoso (`bin\who.cmd`)
- [ ] Categoría verificada (`bin\check_category.cmd`)
- [ ] Primera ejecución manual exitosa (`bin\daily.cmd`)
- [ ] Productos asignados visibles en Tiendanube
- [ ] Tareas programadas creadas
- [ ] Tareas verificadas en Programador de Tareas
- [ ] Logs generándose correctamente
- [ ] Estado guardándose en `data\state.json`

### 🎉 SI TODOS LOS CHECKS ESTÁN ✅:

**¡El proyecto está completamente instalado y funcionando!**

---

## ❓ SI ALGO FALLA

### Recursos de ayuda:

1. **README_QUICK_START.md** - Guía rápida
2. **INSTALL.md** - Instalación detallada
3. **README.md** - Documentación completa
4. **RESUMEN_AUDITORIA.md** - Info técnica
5. **ESTRUCTURA_PROYECTO.md** - Qué hace cada archivo

### Comandos de diagnóstico:

```cmd
bin\check_health.cmd    # Diagnóstico completo
bin\who.cmd             # Test de conexión
notepad logs\daily.log  # Ver qué pasó
```

### Si nada funciona:

1. Ejecutar diagnóstico completo
2. Copiar todo el output
3. Copiar logs completos
4. Contactar soporte con toda la información

---

**Última actualización:** 2024-12-01  
**Versión:** 11.0.0-FIXED

**¡Éxito con tu instalación! 🚀**
