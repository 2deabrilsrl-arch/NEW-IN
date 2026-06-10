# 🚀 GUÍA DE INSTALACIÓN - NEW IN ROBOT

Guía paso a paso para instalar y configurar NEW IN ROBOT desde cero.

---

## ⚠️ ANTES DE EMPEZAR

### Requisitos previos
✅ Python 3.8 o superior instalado  
✅ Windows 10/11  
✅ Acceso a Zoologic Dragonfish con REST API habilitado  
✅ Acceso a Tiendanube con permisos de API  
✅ Conexión a internet  

### Información que necesitarás
📝 Token JWT de Dragonfish  
📝 Token de acceso de Tiendanube  
📝 ID de tu tienda en Tiendanube  
📝 ID de la categoría NEW IN (o nombre para crearla)  

---

## 📥 PASO 1: DESCARGAR EL PROYECTO

### Opción A: Desde archivo ZIP

1. Descargar `NEW_IN_ROBOT_v11.zip`
2. Extraer en: `C:\Users\santiago\NEW IN\`
3. Verificar que la estructura es correcta

### Opción B: Desde archivos individuales

Crear la siguiente estructura:

```
C:\Users\santiago\NEW IN\
│
├── newin_robot.py
├── config.env
├── README.md
├── CHANGELOG.md
├── INSTALL.md (este archivo)
│
├── bin\
│   ├── install.cmd
│   ├── daily.cmd
│   ├── refresh.cmd
│   ├── create_tasks.cmd
│   ├── check_health.cmd
│   ├── who.cmd
│   ├── list_categories.cmd
│   └── check_category.cmd
│
├── data\          (se crea automáticamente)
├── logs\          (se crea automáticamente)
└── docs\          (opcional)
```

---

## 🐍 PASO 2: INSTALAR PYTHON

### 2.1 Verificar si Python está instalado

Abrir **CMD** (Command Prompt) y ejecutar:
```cmd
python --version
```

### 2.2 Si no está instalado

1. Ir a [python.org/downloads](https://www.python.org/downloads/)
2. Descargar Python 3.11 o superior
3. **IMPORTANTE:** Durante instalación, marcar:
   - ✅ **"Add Python to PATH"**
   - ✅ "Install pip"
4. Reiniciar CMD después de instalar

### 2.3 Verificar instalación

```cmd
python --version
pip --version
```

Deberías ver algo como:
```
Python 3.11.6
pip 23.3.1
```

---

## 📦 PASO 3: INSTALAR DEPENDENCIAS

### 3.1 Navegar al proyecto

```cmd
cd "C:\Users\santiago\NEW IN"
```

### 3.2 Opción A: Usar el instalador automático

```cmd
bin\install.cmd
```

El instalador:
- Verifica Python
- Instala `requests`
- Crea directorios
- Prueba conexión

### 3.2 Opción B: Instalación manual

```cmd
python -m pip install requests
```

---

## ⚙️ PASO 4: CONFIGURAR EL PROYECTO

### 4.1 Editar config.env

Abrir `config.env` con **Notepad** o tu editor preferido:

```cmd
notepad config.env
```

### 4.2 Configurar Dragonfish

```env
# URL de la API (usualmente localhost)
DF_BASE_URL=http://localhost:8009/api.Dragonfish

# Cliente ID (usualmente WEB)
DF_IDCLIENTE=WEB

# Token JWT (obtener desde Dragonfish)
DF_JWTOKEN=tu_token_jwt_completo_aqui

# Base de datos
DF_BASEDEDATOS=NADIN25

# Filtros de movimientos
DF_ORIGENDESTINO=STOCK
DF_TIPO=1
DF_MOTIVO=ING
```

#### 🔑 ¿Cómo obtener el token JWT de Dragonfish?

**Opción A: Desde Dragonfish (v15+)**
1. Abrir Dragonfish
2. Ir a: Configuración → Parámetros del sistema → Cliente REST API
3. Click en: Acciones → Obtener Token
4. Ingresar usuario y fecha de expiración
5. Copiar el token generado

**Opción B: Solicitar a soporte**
- Contactar a Mesa de Ayuda de Zoologic
- Proporcionar: IdCliente, Clave Privada, Usuario y Contraseña
- Recibirás el token (vigencia: 2 años)

### 4.3 Configurar Tiendanube

```env
# ID de tu tienda (lo ves en la URL de tu admin)
TN_STORE_ID=6566743

# Token de acceso (obtener desde Tiendanube)
TN_ACCESS_TOKEN=tu_token_acceso_aqui
```

#### 🔑 ¿Cómo obtener el token de Tiendanube?

1. Ir a: [partners.tiendanube.com](https://partners.tiendanube.com)
2. Crear una app privada o usar una existente
3. Instalar la app en tu tienda
4. Copiar el Access Token
5. **IMPORTANTE:** El token debe tener permisos de:
   - ✅ Lectura de productos
   - ✅ Escritura de productos
   - ✅ Lectura de categorías
   - ✅ Escritura de categorías

### 4.4 Configurar categoría NEW IN

```env
# Nombre de la categoría
NEWIN_CATEGORY_NAME=NEW IN

# Handle (slug en la URL)
NEWIN_HANDLE=new-in67

# ID específico (si lo conoces)
NEWIN_CATEGORY_ID=34799819

# Permitir crear si no existe
NEWIN_ALLOW_CREATE=true
```

#### 🔍 ¿Cómo encontrar el ID de la categoría?

**Opción A: Con el robot**
```cmd
bin\list_categories.cmd
```

**Opción B: Desde Tiendanube**
1. Ir a: Admin → Productos → Categorías
2. Click en la categoría NEW IN
3. El ID está en la URL: `...categories/{ID}/edit`

**Opción C: Dejar que el robot la cree**
```env
NEWIN_ALLOW_CREATE=true
```

### 4.5 Guardar config.env

**¡IMPORTANTE!** Guardar el archivo después de editar.

---

## ✅ PASO 5: VERIFICAR INSTALACIÓN

### 5.1 Test de conexión

```cmd
bin\who.cmd
```

**Resultado esperado:**
```
============================================================
WHO AM I
============================================================
[TN] STORE_ID=6566743
[TN] BASE=https://api.tiendanube.com/v1
[TN] TOKEN_HASH=...
[TN] Categorías en esta tienda: 227
[OK] Conexión exitosa
```

### 5.2 Listar categorías

```cmd
bin\list_categories.cmd
```

Deberías ver todas tus categorías listadas.

### 5.3 Verificar categoría configurada

```cmd
bin\check_category.cmd
```

**Si existe:**
```
[CHECK] ✓ Existe: id=34799819 name.es='NEW IN'
```

**Si no existe:**
```
[CHECK] ✗ Categoría id=34799819 NO existe
```

En este caso:
- Verifica el ID en `config.env`
- O activa `NEWIN_ALLOW_CREATE=true` para crearla

### 5.4 Diagnóstico completo

```cmd
bin\check_health.cmd
```

Esto verifica:
- ✅ Archivos presentes
- ✅ Directorios creados
- ✅ Python instalado
- ✅ Dependencias instaladas
- ✅ Conexión a APIs
- ✅ Tareas programadas

---

## 🔄 PASO 6: PRIMERA EJECUCIÓN

### 6.1 Ejecución manual de prueba

```cmd
bin\daily.cmd
```

**Qué hace:**
1. Consulta ingresos en Dragonfish (últimos 7 días)
2. Busca productos en Tiendanube por SKU
3. Asigna categoría NEW IN

**Ver resultado:**
```cmd
notepad logs\daily.log
```

**Resultado esperado:**
```
[SUCCESS] ✓ Asignados 50 productos a categoría id=34799819
```

### 6.2 Ver productos asignados

1. Ir a: Tiendanube Admin → Productos → Categorías
2. Click en "NEW IN"
3. Deberías ver los productos recién ingresados

---

## ⏰ PASO 7: PROGRAMAR TAREAS AUTOMÁTICAS

### 7.1 Crear tareas programadas

**Abrir CMD como Administrador:**
- Click derecho en el botón de Windows
- Seleccionar: "Terminal (Admin)" o "Símbolo del sistema (Admin)"

```cmd
cd "C:\Users\santiago\NEW IN"
bin\create_tasks.cmd
```

### 7.2 Tareas creadas

**NewIn-Daily:**
- Frecuencia: Todos los días
- Hora: 14:00
- Acción: Ejecuta `bin\daily.cmd`

**NewIn-WeeklyRefresh:**
- Frecuencia: Lunes
- Hora: 14:00
- Acción: Ejecuta `bin\refresh.cmd` (limpia + daily)

### 7.3 Verificar tareas

1. Presionar: Windows + R
2. Escribir: `taskschd.msc`
3. Enter
4. Buscar: "NewIn" en la lista

### 7.4 Configurar notificaciones (opcional)

En el Programador de Tareas:
1. Click derecho en la tarea
2. Propiedades → Acciones → Enviar correo (si está disponible)
3. O usar Event Viewer para alertas

---

## 🎯 PASO 8: MONITOREO Y MANTENIMIENTO

### 8.1 Ver logs regularmente

```cmd
notepad logs\daily.log
notepad logs\refresh.log
```

### 8.2 Verificar estado

```cmd
notepad data\state.json
```

**Contenido esperado:**
```json
{
  "last_run_date": "2024-12-01",
  "last_success_at": "2024-12-01T14:00:00"
}
```

### 8.3 Diagnóstico semanal

Ejecutar cada semana:
```cmd
bin\check_health.cmd
```

### 8.4 Backups (recomendado)

Hacer backup semanal de:
- `config.env` (credenciales)
- `data\state.json` (estado)
- `logs\` (historial)

---

## 🐛 TROUBLESHOOTING

### Problema: "Python no encontrado"

**Solución:**
1. Reinstalar Python con "Add to PATH" marcado
2. Reiniciar CMD
3. Verificar: `python --version`

### Problema: "requests no encontrado"

**Solución:**
```cmd
python -m pip install requests
```

### Problema: "Error 404 al asignar categoría"

**Solución:**
1. Verificar ID en `config.env`
2. Ejecutar: `bin\check_category.cmd`
3. Activar creación: `NEWIN_ALLOW_CREATE=true`

### Problema: "Bajo rate de matching"

**Causas:**
- SKUs en Tiendanube diferentes a Dragonfish
- Productos no existen en Tiendanube aún

**Solución:**
1. Ver logs: `logs\daily.log`
2. Buscar: `[MAP] SKUs sin match`
3. Verificar formato de SKUs en TN

### Problema: "Tareas no se ejecutan"

**Solución:**
1. Verificar en Programador de Tareas
2. Ver historial de la tarea
3. Re-crear: `bin\create_tasks.cmd`
4. Verificar permisos (ejecutar como Admin)

---

## 📚 RECURSOS ADICIONALES

### Documentación
- README.md - Documentación completa
- CHANGELOG.md - Historial de cambios
- docs/ - Documentación adicional

### APIs
- Dragonfish: `http://localhost:8009/api.Dragonfish/docs/`
- Tiendanube: [developers.tiendanube.com](https://developers.tiendanube.com)

### Soporte
- Zoologic: [zoologic.com.ar](https://www.zoologic.com.ar)
- Tiendanube: [soporte.tiendanube.com](https://soporte.tiendanube.com)

---

## ✅ CHECKLIST FINAL

Antes de pasar a producción:

- [ ] Python instalado y en PATH
- [ ] Dependencia `requests` instalada
- [ ] `config.env` configurado con todos los tokens
- [ ] Test de conexión exitoso (`bin\who.cmd`)
- [ ] Categoría NEW IN existe o se puede crear
- [ ] Primera ejecución manual exitosa
- [ ] Tareas programadas creadas
- [ ] Logs visibles en `logs\`
- [ ] Backup de `config.env` realizado

---

## 🎉 ¡LISTO!

Si llegaste hasta aquí, el robot está instalado y funcionando.

**Próximos pasos:**
1. Monitorear logs diariamente la primera semana
2. Verificar productos asignados en Tiendanube
3. Ajustar horarios de tareas si es necesario
4. Configurar alertas de errores

**¡Bienvenido a NEW IN ROBOT! 🤖**

---

**Última actualización:** 2024-12-01  
**Versión del robot:** 11.0.0-FIXED
