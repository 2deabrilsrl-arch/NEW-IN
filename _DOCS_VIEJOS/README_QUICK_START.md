# 🚀 QUICK START - NEW IN ROBOT

Guía rápida para poner en marcha el proyecto en 10 minutos.

---

## ⚡ INSTALACIÓN RÁPIDA

### 1. Ubicar archivos

Copiar todos los archivos descargados en:
```
C:\Users\santiago\NEW IN\
```

### 2. Instalar

Abrir **CMD** y ejecutar:
```cmd
cd "C:\Users\santiago\NEW IN"
bin\install.cmd
```

### 3. Configurar

Editar `config.env` con tus credenciales:
```cmd
notepad config.env
```

**Mínimo necesario:**
```env
# Dragonfish
DF_BASE_URL=http://localhost:8009/api.Dragonfish
DF_JWTOKEN=tu_token_jwt_aqui
DF_BASEDEDATOS=NADIN25

# Tiendanube
TN_STORE_ID=6566743
TN_ACCESS_TOKEN=tu_token_acceso_aqui

# Categoría
NEWIN_CATEGORY_ID=34799819
NEWIN_ALLOW_CREATE=true
```

### 4. Verificar

```cmd
bin\who.cmd
```

Deberías ver:
```
[OK] Conexión exitosa
```

### 5. Primera ejecución

```cmd
bin\daily.cmd
```

Verás:
```
[SUCCESS] ✓ Asignados X productos
```

### 6. Programar tareas

**CMD como Administrador:**
```cmd
bin\create_tasks.cmd
```

---

## 🎯 USO DIARIO

### Ver logs
```cmd
notepad logs\daily.log
```

### Ejecutar manualmente
```cmd
bin\daily.cmd         # Consultar ingresos
bin\refresh.cmd       # Limpiar categoría (lunes)
```

### Diagnóstico
```cmd
bin\check_health.cmd  # Ver estado completo
```

---

## ❓ PROBLEMAS COMUNES

### Python no encontrado
```cmd
# Instalar desde: https://www.python.org/
# Marcar: "Add Python to PATH"
```

### Error de conexión
```cmd
# Verificar credenciales en config.env
bin\who.cmd
```

### Bajo matching (<30%)
```cmd
# Ver logs para investigar
notepad logs\daily.log
# Buscar: [MAP] SKUs sin match
```

---

## 📚 DOCUMENTACIÓN COMPLETA

- **README.md** - Documentación detallada
- **INSTALL.md** - Guía de instalación paso a paso
- **RESUMEN_AUDITORIA.md** - Informe técnico completo
- **CHANGELOG.md** - Historial de cambios

---

## 🆘 AYUDA

**¿Algo no funciona?**

1. Ejecutar diagnóstico:
   ```cmd
   bin\check_health.cmd
   ```

2. Ver logs:
   ```cmd
   notepad logs\daily.log
   ```

3. Contactar soporte con:
   - Logs completos
   - Mensaje de error
   - Última modificación de archivos

---

**¡Listo en 10 minutos! 🎉**

Para más detalles, ver **README.md** o **INSTALL.md**.
