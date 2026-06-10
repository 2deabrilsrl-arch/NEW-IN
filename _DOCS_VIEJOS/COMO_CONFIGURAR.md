# 🔧 GUÍA: CÓMO CONFIGURAR config.env

Esta guía te explica **paso a paso** cómo editar el archivo `config.env` con tus credenciales.

---

## 📝 PASO 1: ABRIR EL ARCHIVO

### Opción A: Con Notepad (recomendado)

1. Abrí la carpeta del proyecto:
   ```
   C:\Users\santiago\NEW IN\
   ```

2. Hacé **click derecho** en el archivo `config.env`

3. Seleccioná: **"Abrir con" → "Bloc de notas"** (Notepad)

### Opción B: Desde CMD

```cmd
cd "C:\Users\santiago\NEW IN"
notepad config.env
```

---

## ✏️ PASO 2: EDITAR LAS LÍNEAS NECESARIAS

El archivo tiene **comentarios** (líneas que empiezan con `#`) explicando cada cosa.
Solo tenés que editar las líneas **SIN** el `#`.

### 📍 SECCIÓN 1: DRAGONFISH

**BUSCÁ estas líneas:**

```env
# Token JWT para autenticación (obtener desde Dragonfish)
DF_JWTOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4MjM0NzgzMDAsInVzdWFyaW8iOiJTQU5USSIsInBhc3N3b3JkIjoiNjNjZTk5N2M3OTI0ZmZmMThmMDg1ZTczOTk4NmFkNjAyY2QyZTlhNDc2ZTM1ZTMyOTI0YjRhY2E1ZjM0ZDE4NSJ9.ZpxvcKgmXxv1aGHN2cnEU49FXgyu-HRDCq_bWuKJ0b4
```

**LO QUE TENÉS QUE HACER:**

1. Copiá tu token JWT desde Dragonfish (es un texto larguísimo)
2. Reemplazá TODO lo que está después del `=`

**ANTES:**
```env
DF_JWTOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**DESPUÉS (con tu token):**
```env
DF_JWTOKEN=tu_token_completo_que_copiaste_de_dragonfish
```

**⚠️ IMPORTANTE:**
- NO pongas comillas `"` alrededor del token
- NO dejes espacios antes ni después del `=`
- El token es un texto MUY largo (100+ caracteres) - eso es normal

---

**BUSCÁ esta línea:**

```env
# Base de datos a consultar
DF_BASEDEDATOS=NADIN25
```

**LO QUE TENÉS QUE HACER:**

Reemplazá `NADIN25` con el nombre de tu base de datos.

**EJEMPLO:**
```env
DF_BASEDEDATOS=MIBASEDEDATOS
```

---

### 📍 SECCIÓN 2: TIENDANUBE

**BUSCÁ estas líneas:**

```env
# ID de tu tienda en Tiendanube
TN_STORE_ID=6566743

# Token de acceso a la API de Tiendanube
TN_ACCESS_TOKEN=accb4de2caf771902f651fe3c2d2877c6a6609c6
```

**LO QUE TENÉS QUE HACER:**

1. **TN_STORE_ID:**
   - Mirá la URL de tu admin de Tiendanube
   - La URL es algo como: `https://miecommerce.mitiendanube.com/admin/v2/6566743/...`
   - El número `6566743` es tu STORE_ID
   - Reemplazá el valor

**EJEMPLO:**
```env
TN_STORE_ID=1234567
```

2. **TN_ACCESS_TOKEN:**
   - Copiá tu token de Tiendanube
   - Reemplazá TODO lo que está después del `=`

**EJEMPLO:**
```env
TN_ACCESS_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

**⚠️ IMPORTANTE:**
- NO pongas comillas
- NO dejes espacios
- El token es largo (40-50 caracteres)

---

### 📍 SECCIÓN 3: CATEGORÍA "NEW IN"

**BUSCÁ estas líneas:**

```env
# ID específico de la categoría (si lo conoces)
NEWIN_CATEGORY_ID=34799819
```

**OPCIONES:**

**Opción A: Si conocés el ID de tu categoría NEW IN**
```env
NEWIN_CATEGORY_ID=12345678
```

**Opción B: Si NO conocés el ID (recomendado al principio)**
```env
NEWIN_CATEGORY_ID=
```
(Dejalo vacío y el robot la buscará por nombre)

**Opción C: Para que el robot cree la categoría si no existe**
```env
NEWIN_ALLOW_CREATE=true
```

---

## 💾 PASO 3: GUARDAR EL ARCHIVO

1. En Notepad, hacé click en: **Archivo → Guardar** (o presiona `Ctrl + S`)
2. Cerrá el Notepad

---

## ✅ PASO 4: VERIFICAR QUE QUEDÓ BIEN

Abrí CMD y ejecutá:

```cmd
cd "C:\Users\santiago\NEW IN"
bin\who.cmd
```

**Si todo está bien, vas a ver:**
```
[OK] Python encontrado
[TN] STORE_ID=1234567
[TN] Categorías: 227
[OK] Conexión exitosa
```

**Si hay error, vas a ver:**
```
[ERROR] ...
```

---

## 📋 EJEMPLO COMPLETO DE ARCHIVO config.env EDITADO

Así debería verse tu archivo **DESPUÉS de editarlo**:

```env
# ============================================================
# DRAGONFISH (ZOOLOGIC)
# ============================================================
DF_BASE_URL=http://localhost:8009/api.Dragonfish
DF_IDCLIENTE=WEB
DF_JWTOKEN=eyJtuTokenLarguisimoAquiConMuchasLetrasYNumeros123456789
DF_BASEDEDATOS=MIBASEDEDATOS
DF_ORIGENDESTINO=STOCK
DF_TIPO=1
DF_MOTIVO=ING

# ============================================================
# TIENDANUBE
# ============================================================
TN_BASE_URL=https://api.tiendanube.com/v1
TN_STORE_ID=1234567
TN_ACCESS_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901

# ============================================================
# CATEGORÍA "NEW IN"
# ============================================================
NEWIN_CATEGORY_NAME=NEW IN
NEWIN_HANDLE=new-in67
NEWIN_CATEGORY_ID=12345678
NEWIN_ALLOW_CREATE=true

# ============================================================
# COMPORTAMIENTO
# ============================================================
CATCHUP_DAYS=7
```

---

## ❓ PREGUNTAS FRECUENTES

### ¿Dónde encuentro mi token JWT de Dragonfish?

**Versión 15 o superior:**
1. Abrí Dragonfish
2. Ir a: **Configuración → Parámetros del sistema → Cliente REST API**
3. Click en: **Acciones → Obtener Token**
4. Ingresar usuario y fecha de expiración
5. Copiar el token que aparece

**Versión anterior:**
- Contactar a Mesa de Ayuda de Zoologic
- Proporcionar: IdCliente, Clave Privada, Usuario y Contraseña

---

### ¿Dónde encuentro mi token de Tiendanube?

1. Ir a: [partners.tiendanube.com](https://partners.tiendanube.com)
2. Crear una app privada (si no tenés una)
3. Instalar la app en tu tienda
4. Copiar el **Access Token**

**IMPORTANTE:** El token debe tener permisos de:
- ✅ Lectura de productos
- ✅ Escritura de productos
- ✅ Lectura de categorías
- ✅ Escritura de categorías

---

### ¿Qué pasa si me equivoco al editar?

No hay problema, podés:
1. Volver a descargar el archivo `config.env` original
2. O copiar el ejemplo de arriba y editarlo

---

### ¿Puedo poner comillas alrededor de los valores?

**NO** - Las comillas causan problemas.

**❌ MAL:**
```env
TN_STORE_ID="1234567"
TN_ACCESS_TOKEN="abc123..."
```

**✅ BIEN:**
```env
TN_STORE_ID=1234567
TN_ACCESS_TOKEN=abc123...
```

---

### ¿Puedo dejar espacios?

**NO** - Los espacios causan problemas.

**❌ MAL:**
```env
TN_STORE_ID = 1234567
TN_ACCESS_TOKEN =abc123...
```

**✅ BIEN:**
```env
TN_STORE_ID=1234567
TN_ACCESS_TOKEN=abc123...
```

---

### ¿Qué líneas DEBO editar obligatoriamente?

**MÍNIMO NECESARIO:**
1. `DF_JWTOKEN` - Token de Dragonfish
2. `DF_BASEDEDATOS` - Nombre de tu base de datos
3. `TN_STORE_ID` - ID de tu tienda
4. `TN_ACCESS_TOKEN` - Token de Tiendanube

**El resto puede quedar con valores por defecto.**

---

### ¿Cómo sé si mi ID de categoría es correcto?

Ejecutá:
```cmd
bin\check_category.cmd
```

Si existe, vas a ver:
```
[CHECK] ✓ Existe: id=12345678 name.es='NEW IN'
```

Si no existe:
```
[CHECK] ✗ Categoría NO existe
```

---

## 🆘 ¿NECESITÁS MÁS AYUDA?

Si seguís con dudas:
1. Ejecutá: `bin\check_health.cmd`
2. Copiá TODO el output
3. Enviámelo para ayudarte

---

**¡Listo! Ahora ya sabés cómo configurar config.env** 🎉
