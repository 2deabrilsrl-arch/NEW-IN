#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
newin_robot.py (v12.2.0-REPORTES)
============================================================
CORRECCIONES CRÍTICAS v12.1.0:
- NUEVO: Genera reportes diarios individuales por fecha
- NUEVO: Reportes incluyen detalle por marca y producto
- NUEVO: Limpieza automática semanal (mantiene últimos 7 días)
- Archivos: logs/reportes_diarios/REPORTE_DAILY_YYYY-MM-DD.txt

CORRECCIONES PREVIAS v12.0.0:
- FIX CRÍTICO: Matching por CÓDIGO MADRE en vez de SKU completo
- NUEVO: Extrae T-1100 de T-1100#231#90 y busca CUALQUIER variante del producto
- NUEVO: Evita duplicados - agrega cada producto madre solo UNA vez
- MEJORA: Aumenta drásticamente el match rate (esperado 80%+ en vez de 6%)
- Mantiene todas las correcciones de v11.3.0

LÓGICA DE MATCHING:
1. Dragonfish dice: "Ingresó T-1100#231#90"
2. Robot extrae: "T-1100" (código madre)
3. Busca en TN: ¿Existe algún producto con ALGUNA variante que empiece con "T-1100"?
4. Si SÍ → Agrega el producto COMPLETO a NEW IN (solo una vez)
5. Cliente ve: Producto T-1100 con TODAS sus variantes disponibles

CORRECCIONES PREVIAS v11.3.0:
- FIX: Transforma espacios a "___" en SKUs para matchear con TN
- FIX: Filtra productos "CONTROL" (uso interno, no para venta)
- FIX: Paginación completa de Dragonfish
- HORARIO: Cambio recomendado a 18:30 (procesa todo el día laboral)
============================================================

FLUJO:
1. daily: Consulta ingresos desde último run, asigna categoría NEW IN
2. refresh: Limpia categoría NEW IN (ejecutar los lunes)
3. list_cats: Lista categorías de Tiendanube
4. check_cat: Verifica que la categoría configurada existe
5. who: Muestra info de conexión y test básico

IMPORTANTE:
- La API de Dragonfish limita a 200 items por página
- Este script implementa paginación completa
- Logs rotan automáticamente cada 10MB
"""
import os
import sys
import json
import argparse
import datetime as dt
import time
import traceback
from typing import List, Dict, Tuple, Optional, Any

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')
    except:
        pass

try:
    import requests
except ImportError as e:
    print("[FATAL] Falta 'requests'. Instala: pip install requests", file=sys.stderr)
    raise

# ============================================================
# CONFIGURACIÓN Y UTILIDADES
# ============================================================

MAIN_ENV = {}
VERSION = "12.3.0"

DEFAULT_BASE_DIR = r"C:\Users\santiago\NEW IN"
DEFAULT_DATA_DIR = os.path.join(DEFAULT_BASE_DIR, "data")
DEFAULT_LOG_DIR = os.path.join(DEFAULT_BASE_DIR, "logs")
STATE_FILENAME = "state.json"
CATEGORY_FILENAME = "newin_category.json"

# Configuración de retry
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def load_env_file(path: str) -> Dict[str, str]:
    """Carga variables de entorno desde archivo .env"""
    d = {}
    if not os.path.isfile(path):
        print(f"[WARN] Archivo .env no encontrado: {path}")
        return d
    
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if "=" in s:
                k, v = s.split("=", 1)
                d[k.strip()] = v.strip()
    
    print(f"[ENV] Cargadas {len(d)} variables desde {path}")
    return d


def env(k: str, default: Optional[str] = None) -> Optional[str]:
    """Obtiene variable de entorno (prioridad: os.environ > .env file)"""
    # Intentar obtener de os.environ
    if k in os.environ:
        val = os.environ[k]
        if val and val.strip():  # Si no está vacío
            return val.strip()
    
    # Intentar obtener de MAIN_ENV (archivo .env)
    val = MAIN_ENV.get(k)
    if val and val.strip():  # Si no está vacío
        return val.strip()
    
    # Usar default si no hay valor válido
    return default


def ensure_dir(p: str) -> None:
    """Crea directorio si no existe"""
    os.makedirs(p, exist_ok=True)


def log_error(msg: str, exc: Optional[Exception] = None) -> None:
    """Registra error con traceback completo"""
    print(f"[ERROR] {msg}", file=sys.stderr)
    if exc:
        print(f"[ERROR] Exception: {type(exc).__name__}: {exc}", file=sys.stderr)
        traceback.print_exc()


def safe_int(val: Any, default: int = 0) -> int:
    """Convierte a int de forma segura"""
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def extract_madre_code(sku: str) -> str:
    """
    Extrae el código madre del SKU completo.
    
    Ejemplos:
    - "T-1100#231#90" -> "T-1100"
    - "ACC-BOOB___TAPE#369#UNICO" -> "ACC-BOOB___TAPE"
    - "T-1100" -> "T-1100" (si no tiene #, devuelve el mismo)
    
    Returns:
        Código madre (todo antes del primer #)
    """
    if not sku:
        return ""
    
    # Si tiene #, extraer todo antes del primer #
    if "#" in sku:
        return sku.split("#")[0]
    
    # Si no tiene #, devolver el SKU completo
    return sku


# ============================================================
# API TIENDANUBE
# ============================================================

def tn_headers() -> Dict[str, str]:
    """Headers para requests a Tiendanube"""
    tok = env("TN_ACCESS_TOKEN", "")
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authentication": f"bearer {tok}" if tok else "",
        "User-Agent": f"NewInRobot/{VERSION}"
    }


def tn_base() -> str:
    """URL base de la API de Tiendanube"""
    return (env("TN_BASE_URL", "https://api.tiendanube.com/v1") or "https://api.tiendanube.com/v1").rstrip("/")


def tn_store_id() -> str:
    """ID de la tienda"""
    return (env("TN_STORE_ID", "") or "").strip()


def tn_list_categories_paginated(per_page: int = 200, max_pages: int = 200) -> List[Dict]:
    """Lista todas las categorías de Tiendanube con paginación"""
    out = []
    page = 1
    
    while page <= max_pages:
        url = f"{tn_base()}/{tn_store_id()}/categories"
        params = {"per_page": per_page, "page": page}
        
        try:
            resp = requests.get(url, headers=tn_headers(), params=params, timeout=30)
        except requests.RequestException as e:
            log_error(f"Error listando categorías (page={page})", e)
            break
        
        if resp.status_code == 404:
            print(f"[TN] Categorías: paginación cortada 404 page={page}")
            break
        
        if resp.status_code != 200:
            print(f"[TN] HTTP {resp.status_code} listando categorías page={page}: {resp.text[:200]}")
            break
        
        try:
            data = resp.json()
        except Exception as e:
            log_error(f"No JSON en categorías page={page}", e)
            break
        
        if not data or not isinstance(data, list):
            break
        
        out.extend(data)
        print(f"[TN] Categorías page {page}: {len(data)} elementos (acum={len(out)})")
        
        if len(data) < per_page:
            break
        
        page += 1
    
    print(f"[TN] Total categorías listadas: {len(out)}")
    return out


def _norm(s: Optional[str]) -> str:
    """Normaliza string para comparación"""
    return (s or "").strip().lower()


def _get_name_es(c: Dict) -> str:
    """Obtiene nombre en español de categoría"""
    nm = c.get("name") or {}
    return (nm.get("es") if isinstance(nm, dict) else nm) or ""


def _get_handle_es(c: Dict) -> str:
    """Obtiene handle en español de categoría"""
    h = c.get("handle") or {}
    return (h.get("es") if isinstance(h, dict) else h) or ""


def _category_persistence_path() -> str:
    """Path al archivo de persistencia de categoría"""
    data_dir = env("DATA_DIR", DEFAULT_DATA_DIR)
    ensure_dir(data_dir)
    return os.path.join(data_dir, CATEGORY_FILENAME)


def _persist_category_id(cid: int, handle: str, **extra) -> None:
    """Persiste el ID de categoría en archivo JSON"""
    path = _category_persistence_path()
    payload = {
        "category_id": int(cid),
        "handle": handle,
        "updated_at": dt.datetime.now().isoformat()
    }
    payload.update(extra)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    
    print(f"[CAT] Persistida categoría id={cid} en {path}")


def _load_persisted_category() -> Optional[int]:
    """Carga categoría persistida desde archivo"""
    p = _category_persistence_path()
    if os.path.isfile(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                j = json.load(f)
            return int(j.get("category_id"))
        except Exception as e:
            log_error("Error cargando categoría persistida", e)
            return None
    return None


def _validate_category_id(cid: int, cats: List[Dict]) -> bool:
    """Valida que el ID de categoría existe en la lista"""
    try:
        return any(int(c.get("id")) == int(cid) for c in cats)
    except Exception:
        return False


def tn_resolve_category_id(force_refresh: bool = False) -> Optional[int]:
    """
    Resuelve el ID de la categoría NEW IN.
    Orden de prioridad:
    1. NEWIN_CATEGORY_ID (ENV) si es válido
    2. Categoría persistida si es válida
    3. Búsqueda por handle
    4. Búsqueda por nombre
    5. Creación si NEWIN_ALLOW_CREATE=true
    """
    cats = tn_list_categories_paginated()
    handle = (env("NEWIN_HANDLE", "new-in1") or "new-in1").strip()
    name_es = (env("NEWIN_CATEGORY_NAME", "New In") or "New In").strip()
    
    # 1. Intentar con NEWIN_CATEGORY_ID del ENV
    fixed = (env("NEWIN_CATEGORY_ID", "") or "").strip()
    if fixed.isdigit() and _validate_category_id(int(fixed), cats):
        print(f"[CAT] OK: Usando categoría por ENV id={fixed} (handle esperado={handle})")
        _persist_category_id(int(fixed), handle, source="env")
        return int(fixed)
    
    if fixed.isdigit() and not force_refresh:
        print(f"[CAT] WARN: NEWIN_CATEGORY_ID={fixed} no existe en listado. Ignoramos override.")
    
    # 2. Intentar con categoría persistida
    if not force_refresh:
        persisted = _load_persisted_category()
        if persisted and _validate_category_id(persisted, cats):
            print(f"[CAT] OK: Usando categoría persistida id={persisted} (handle esperado={handle})")
            return persisted
        elif persisted:
            print("[CAT] WARN: ID persistido ya no existe. Ignorando persistencia.")
    
    # 3. Buscar por handle
    mh = _norm(handle)
    cand = [int(c.get("id")) for c in cats if _norm(_get_handle_es(c)) == mh]
    if cand:
        chosen = min(cand)
        print(f"[CAT] OK: Encontrada por handle. id={chosen} (candidatos={len(cand)})")
        _persist_category_id(chosen, handle, match_by="handle")
        return chosen
    
    # 4. Buscar por nombre
    mn = _norm(name_es)
    cand = [int(c.get("id")) for c in cats if _norm(_get_name_es(c)) == mn]
    if cand:
        chosen = min(cand)
        print(f"[CAT] OK: Encontrada por nombre. id={chosen} (candidatos={len(cand)})")
        _persist_category_id(chosen, handle, match_by="name")
        return chosen
    
    # 5. No existe, verificar si podemos crear
    print(f"[CAT] NOT FOUND: No existe handle={handle} ni nombre={name_es}")
    allow = _norm(env("NEWIN_ALLOW_CREATE", "false")) in ("true", "1", "yes", "y")
    
    if not allow:
        print("[CAT] SAFE MODE: no creamos (cambia NEWIN_ALLOW_CREATE=true para permitir)")
        return None
    
    # Crear categoría
    url = f"{tn_base()}/{tn_store_id()}/categories"
    body = {"name": {"es": name_es}, "handle": {"es": handle}}
    
    try:
        resp = requests.post(url, headers=tn_headers(), data=json.dumps(body), timeout=30)
    except requests.RequestException as e:
        log_error("Error creando categoría", e)
        return None
    
    if resp.status_code not in (200, 201):
        print(f"[TN] HTTP {resp.status_code} creando categoría: {resp.text[:200]}")
        return None
    
    try:
        data = resp.json()
        cid = data.get("id")
        if cid is None:
            print("[TN] No se recibió ID al crear categoría")
            return None
        cid = int(cid)
    except Exception as e:
        log_error("Error parseando respuesta al crear categoría", e)
        return None
    
    _persist_category_id(cid, handle, created=True)
    print(f"[CAT] OK: Creada categoría id={cid} (handle={handle})")
    return cid


# ============================================================
# API DRAGONFISH (ZOOLOGIC)
# ============================================================

def df_headers() -> Dict[str, str]:
    """Headers para requests a Dragonfish"""
    h = {
        "IdCliente": env("DF_IDCLIENTE", "WEB") or "WEB",
        "BaseDeDatos": env("DF_BASEDEDATOS", ""),
        "accept": "application/json"
    }
    t = env("DF_JWTOKEN", "")
    if t:
        h["Authorization"] = t
    return h


# Alias de campos para SKU
ART_KEYS = ["Articulo", "CodArticulo", "CodigoArticulo", "Codigo", "articulo", "codarticulo", "codigoarticulo"]
COLOR_KEYS = ["Color", "CodColor", "CodigoColor", "ColorCodigo", "ColorID", "ColorId", "color", "codcolor", "cod_color"]
TALLE_KEYS = ["Talle", "CodTalle", "TalleCodigo", "CodigoTalle", "TalleID", "TalleId", "talle", "codtalle", "cod_talle"]


def _pick_first(d: Dict, keys: List[str]) -> str:
    """Busca el primer campo que tenga valor en el diccionario"""
    for k in keys:
        if k in d and (str(d[k]).strip() != ""):
            return str(d[k]).strip()
    return ""


def build_sku(it: Dict) -> Optional[str]:
    """
    Construye SKU en formato Articulo#Color#Talle
    
    IMPORTANTE: 
    - Transforma espacios a triple guion bajo (___) para matchear con TN
    - Filtra productos de CONTROL (uso interno, no para venta)
    
    Ejemplo: "ACC-BOOB TAPE" -> "ACC-BOOB___TAPE"
    """
    a = _pick_first(it, ART_KEYS)
    c = _pick_first(it, COLOR_KEYS)
    t = _pick_first(it, TALLE_KEYS)
    
    if not a or not c or not t:
        return None
    
    # FILTRO: Excluir productos de CONTROL (uso interno, no para venta)
    # Los controles son para encargados, no son productos reales
    a_upper = a.upper()
    if "CONTROL" in a_upper:
        return None
    
    # Transformar espacios a triple guion bajo para matchear con Tiendanube
    a = a.replace(" ", "___")
    c = c.replace(" ", "___")
    t = t.replace(" ", "___")
    
    return f"{a}#{c}#{t}"


def _extract_items_from_df_json(js: Any) -> List[Dict]:
    """Extrae items de la respuesta JSON de Dragonfish"""
    out = []
    
    # Formato esperado: { Resultados: [ { MovimientoDetalle: [...] }, ... ] }
    if isinstance(js, dict) and "Resultados" in js and isinstance(js["Resultados"], list):
        for mov in js["Resultados"]:
            det = mov.get("MovimientoDetalle") or mov.get("detalle") or mov.get("Detalle") or []
            if isinstance(det, list):
                out.extend(det)
        
        print(f"[DF] Extraídos desde Resultados/MovimientoDetalle: {len(out)}")
        return out
    
    # Fallback: recorrer recursivamente
    def _walk(n):
        res = []
        if isinstance(n, list):
            res.extend(n)
        elif isinstance(n, dict):
            for v in n.values():
                res.extend(_walk(v))
        return res
    
    all_lists = [x for x in _walk(js) if isinstance(x, dict)]
    return all_lists


def df_get_movimientos_paginated(fecha: dt.date) -> Tuple[List[Dict], bool]:
    """
    Obtiene movimientos con paginación completa.
    Retorna: (items, network_error)
    network_error=True si hubo timeout o error de red (no avanzar last_run_date)
    network_error=False si la consulta fue exitosa (aunque no haya items)
    """
    base = (env("DF_BASE_URL", "") or "").rstrip("/")
    if not base:
        print("[DF] DF_BASE_URL no configurada.", file=sys.stderr)
        return [], False

    all_items = []
    page = 1
    max_pages = 50
    network_error = False

    params_base = {
        "OrigenDestino": env("DF_ORIGENDESTINO", "STOCK") or "STOCK",
        "Tipo": env("DF_TIPO", "1") or "1",
        "Motivo": env("DF_MOTIVO", "ING") or "ING",
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "limit": "200"
    }

    url = f"{base}/Movimientodestock/"

    print(f"[DF] Consultando {fecha} con paginación...")

    while page <= max_pages:
        params = params_base.copy()
        params["page"] = str(page)

        try:
            resp = requests.get(url, headers=df_headers(), params=params, timeout=30)
        except requests.RequestException as e:
            log_error(f"Error de red consultando DF page={page}", e)
            network_error = True
            break

        if resp.status_code == 404:
            if page == 1:
                print(f"[DF] {params_base['Fecha']}: 404 (sin movimientos)")
            break

        if resp.status_code != 200:
            print(f"[DF] {params_base['Fecha']}: HTTP {resp.status_code} page={page}")
            network_error = True
            break

        try:
            js = resp.json()
        except Exception as e:
            log_error(f"Respuesta no JSON page={page}", e)
            network_error = True
            break

        items = _extract_items_from_df_json(js)

        if not items:
            print(f"[DF] {fecha} page={page}: sin items, fin de paginación")
            break

        all_items.extend(items)
        print(f"[DF] {fecha} page={page}: {len(items)} items (acumulado={len(all_items)})")

        if len(items) < 200:
            print(f"[DF] {fecha}: fin de paginación (última página con {len(items)} items)")
            break

        page += 1

    print(f"[DF] {fecha}: Total items={len(all_items)} en {page} página(s)")
    return all_items, network_error


# ============================================================
# ESTADO Y PERSISTENCIA
# ============================================================

def _state_path() -> str:
    """Path al archivo de estado"""
    data_dir = env("DATA_DIR", DEFAULT_DATA_DIR)
    ensure_dir(data_dir)
    return os.path.join(data_dir, STATE_FILENAME)


def get_state() -> Dict:
    """Carga estado desde archivo"""
    p = _state_path()
    if os.path.isfile(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log_error("Error cargando state", e)
            pass
    return {}


def set_state(d: Dict) -> None:
    """Guarda estado en archivo"""
    with open(_state_path(), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def parse_date(s: str) -> dt.date:
    """Parsea fecha desde string YYYY-MM-DD"""
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def accumulate_since_last_run(today: Optional[dt.date] = None) -> Tuple[List[str], Dict[str, List[str]], bool]:
    """
    Acumula SKUs desde última ejecución exitosa hasta hoy.
    Retorna: (lista_skus_unicos, dict_por_dia, network_error)
    """
    if today is None:
        today = dt.date.today()
    
    try:
        catchup = int(env("CATCHUP_DAYS", "7") or "7")  # Aumentado a 7 días
    except Exception:
        catchup = 7
    
    st = get_state()
    last = st.get("last_run_date")
    last_date = parse_date(last) if last else None
    
    # Ventana: desde (último run + 1 día) o (hoy - catchup), hasta hoy
    if last_date:
        start = last_date + dt.timedelta(days=1)
    else:
        start = today - dt.timedelta(days=catchup)
    
    # No procesar fechas futuras
    if start > today:
        print(f"[ACC] Sin ventana (start={start} > today={today})")
        return [], {}
    
    print(f"[ACC] Ventana: {start} -> {today} (catchup={catchup}d, last_run={last_date})")
    
    uniq = []
    by_day = {}
    cur = start
    
    while cur <= today:
        items, net_err = df_get_movimientos_paginated(cur)
        if net_err:
            print(f"[ACC] Error de red en {cur}, abortando ventana")
            return [], {}, True
        day = []
        miss = 0
        sample_miss = []
        
        for it in items:
            s = build_sku(it)
            if s:
                day.append(s)
            else:
                miss += 1
                if len(sample_miss) < 3:
                    sample_miss.append(list(it.keys()))
        
        print(f"[DF] {cur}: SKUs armados={len(day)} sin_sku={miss}{' sample_keys='+str(sample_miss) if sample_miss else ''}")
        by_day[cur.strftime("%Y-%m-%d")] = day
        uniq.extend(day)
        cur += dt.timedelta(days=1)
    
    # Deduplicar manteniendo orden
    seen = set()
    dedup = []
    for s in uniq:
        if s not in seen:
            seen.add(s)
            dedup.append(s)
    
    print(f"[ACC] SKUs únicos: {len(dedup)}")
    return dedup, by_day, False


# ============================================================
# PRODUCTOS TIENDANUBE
# ============================================================

def tn_list_products_paginated() -> List[Dict]:
    """Lista todos los productos de Tiendanube con paginación"""
    page = 1
    out = []
    
    while True:
        url = f"{tn_base()}/{tn_store_id()}/products"
        params = {"per_page": 100, "page": page}
        
        try:
            resp = requests.get(url, headers=tn_headers(), params=params, timeout=30)
        except requests.RequestException as e:
            log_error(f"Error listando productos page={page}", e)
            break
        
        if resp.status_code == 404:
            print(f"[TN] Paginación cortada 404 page={page}")
            break
        
        if resp.status_code != 200:
            print(f"[TN] HTTP {resp.status_code} page={page}")
            break
        
        try:
            data = resp.json()
        except Exception as e:
            log_error(f"No JSON page={page}", e)
            break
        
        if not data or not isinstance(data, list):
            break
        
        out.extend(data)
        print(f"[TN] Página {page}: {len(data)} productos (acumulado={len(out)})")
        
        if len(data) < 100:
            break
        
        page += 1
    
    print(f"[TN] Productos listados: {len(out)}")
    return out


def tn_build_madre_index(products: List[Dict]) -> Tuple[Dict[str, int], Dict[int, List[int]]]:
    """
    NUEVA FUNCIÓN v12.0: Crea índice CÓDIGO MADRE -> ProductID
    
    En vez de indexar por SKU completo (T-1100#231#90), indexa por código madre (T-1100).
    Si un producto tiene múltiples variantes con el mismo código madre, todas apuntan al mismo ProductID.
    
    Returns:
        - madre_index: {codigo_madre -> product_id}
        - product_categories: {product_id -> [category_ids]}
    
    Ejemplo:
        Producto ID 12345 con variantes:
        - "T-1100#231#100"
        - "T-1100#231#105"
        - "T-1100#44#100"
        
        Genera entrada: {"T-1100": 12345}
    """
    madre_idx = {}
    prod_cats = {}
    
    for p in products:
        pid = int(p.get("id"))
        cats = p.get("categories") or []
        
        # Normalizar categorías a lista de ints
        norm = []
        for c in cats:
            if isinstance(c, dict):
                cid = c.get("id")
                if cid is not None:
                    try:
                        norm.append(int(cid))
                    except:
                        pass
            else:
                try:
                    norm.append(int(c))
                except:
                    pass
        
        prod_cats[pid] = sorted(set(norm))
        
        # Indexar por código madre de TODAS las variantes
        for v in (p.get("variants") or []):
            sku = (v.get("sku") or "").strip()
            if sku:
                # Extraer código madre
                madre = extract_madre_code(sku)
                if madre:
                    # Si ya existe, no sobreescribir (mantener el primer producto)
                    if madre not in madre_idx:
                        madre_idx[madre] = pid
    
    print(f"[MAP] Índice CÓDIGOS MADRE: {len(madre_idx)} entradas. Productos con categorías: {len(prod_cats)}")
    return madre_idx, prod_cats


def tn_add_category_to_products(
    category_id: int,
    product_ids: List[int],
    prod_cats: Dict[int, List[int]],
    sleep_ms: int = 250,
    retries: int = 3
) -> Tuple[bool, int, int]:
    """
    Agrega categoría a productos vía PUT /products/{id}
    
    Returns:
        (success, productos_nuevos, productos_ya_tenian)
    """
    ok_count = 0
    fail = 0
    ya_tenian = 0
    
    for pid in sorted(set(int(x) for x in product_ids)):
        current = prod_cats.get(pid, [])
        
        if category_id in current:
            print(f"[TN] pid={pid}: ya tiene categoría {category_id}, salto")
            ya_tenian += 1
            continue
        
        new_cats = sorted(set(current + [category_id]))
        url = f"{tn_base()}/{tn_store_id()}/products/{pid}"
        body = {"categories": new_cats}
        
        attempt = 0
        success = False
        
        while attempt <= retries:
            try:
                resp = requests.put(url, headers=tn_headers(), data=json.dumps(body), timeout=60)
                
                if resp.status_code in (200, 201):
                    ok_count += 1
                    success = True
                    break
                else:
                    attempt += 1
                    if attempt > retries:
                        print(f"[TN] pid={pid} PUT categorías HTTP {resp.status_code}: {resp.text[:200]}")
                        fail += 1
                        break
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
            
            except requests.RequestException as e:
                attempt += 1
                if attempt > retries:
                    log_error(f"pid={pid} error de red", e)
                    fail += 1
                    break
                time.sleep(RETRY_DELAY_SECONDS)
                continue
        
        if success:
            time.sleep(max(0, int(sleep_ms)) / 1000.0)
    
    print(f"[TN] PUT categorías resultado: ok={ok_count} fail={fail}")
    return (ok_count > 0 and fail == 0, ok_count, ya_tenian)


# ============================================================
# REPORTES DIARIOS
# ============================================================

def extract_marca_from_code(codigo: str) -> str:
    """
    Extrae la marca del código madre.
    Ejemplos:
    - "MK-10137" -> "MK (MARCELA KOURY)"
    - "T-1100" -> "T (TIENTO)"
    - "B-6085" -> "B (BOMBACHA)"
    - "CHI-BA105" -> "CHI (CHILL OUT)"
    """
    if not codigo:
        return "DESCONOCIDO"
    
    # Diccionario de marcas conocidas
    marcas = {
        "MK": "MARCELA KOURY",
        "T": "TIENTO",
        "B": "BOMBACHA",
        "CHI": "CHILL OUT",
        "AND": "ANDRESSA",
        "ACC": "ACCESORIOS",
        "VELLA": "VELLA BELLA",
        "TRENDA": "TRENDA"
    }
    
    # Extraer prefijo (todo antes del primer -)
    if "-" in codigo:
        prefijo = codigo.split("-")[0]
    else:
        prefijo = codigo.split("#")[0] if "#" in codigo else codigo
    
    # Buscar marca
    marca_nombre = marcas.get(prefijo.upper(), prefijo.upper())
    return f"{prefijo} ({marca_nombre})"


def generar_reporte_diario(
    fecha: dt.date,
    codigos_madre: List[str],
    matched: List[str],
    missed: List[str],
    productos_agregados: int,
    productos_ya_tenian: int
) -> str:
    """
    Genera reporte diario detallado con marcas y productos.
    
    Returns:
        Path del archivo generado
    """
    # Crear directorio de reportes
    log_dir = env("LOG_DIR", DEFAULT_LOG_DIR)
    reportes_dir = os.path.join(log_dir, "reportes_diarios")
    ensure_dir(reportes_dir)
    
    # Nombre del archivo
    fecha_str = fecha.strftime("%Y-%m-%d")
    reporte_path = os.path.join(reportes_dir, f"REPORTE_DAILY_{fecha_str}.txt")
    
    # Agrupar por marca
    marcas_matched = {}
    marcas_missed = {}
    
    for codigo in matched:
        marca = extract_marca_from_code(codigo)
        if marca not in marcas_matched:
            marcas_matched[marca] = []
        marcas_matched[marca].append(codigo)
    
    for codigo in missed:
        marca = extract_marca_from_code(codigo)
        if marca not in marcas_missed:
            marcas_missed[marca] = []
        marcas_missed[marca].append(codigo)
    
    # Match rate
    total = len(codigos_madre)
    match_rate = (len(matched) * 100 // total) if total > 0 else 0
    
    # Generar reporte
    reporte = f"""{'='*80}
REPORTE DIARIO NEW IN - {fecha_str}
{'='*80}

Fecha de generación: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
RESUMEN GENERAL
{'='*80}

Códigos madre procesados:       {total}
Productos encontrados en TN:    {len(matched)} ({match_rate}%)
Productos NO encontrados:        {len(missed)} ({100-match_rate}%)

Productos NUEVOS agregados:     {productos_agregados}
Productos que ya estaban:       {productos_ya_tenian}
Total productos en New In:      {productos_agregados + productos_ya_tenian}

{'='*80}
DETALLE POR MARCA - PRODUCTOS AGREGADOS
{'='*80}

"""
    
    # Detalle por marca (matched)
    if marcas_matched:
        for marca in sorted(marcas_matched.keys()):
            codigos = marcas_matched[marca]
            reporte += f"\n{marca}\n"
            reporte += f"  Cantidad: {len(codigos)}\n"
            reporte += f"  Códigos:\n"
            for codigo in sorted(codigos):
                reporte += f"    - {codigo}\n"
    else:
        reporte += "\n  (Ningún producto agregado)\n"
    
    # Productos NO encontrados
    if marcas_missed:
        reporte += f"\n{'='*80}\n"
        reporte += "PRODUCTOS NO ENCONTRADOS EN TIENDANUBE\n"
        reporte += f"{'='*80}\n"
        
        for marca in sorted(marcas_missed.keys()):
            codigos = marcas_missed[marca]
            reporte += f"\n{marca}\n"
            reporte += f"  Cantidad: {len(codigos)}\n"
            reporte += f"  Códigos:\n"
            for codigo in sorted(codigos):
                reporte += f"    - {codigo}\n"
        
        reporte += f"\nNOTA: Estos productos ingresaron en Dragonfish pero NO están\n"
        reporte += f"      cargados en Tiendanube todavía.\n"
    
    reporte += f"\n{'='*80}\n"
    reporte += "FIN DEL REPORTE\n"
    reporte += f"{'='*80}\n"
    
    # Guardar archivo
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write(reporte)
    
    print(f"[REPORTE] Generado: {reporte_path}")
    return reporte_path


def limpiar_reportes_viejos(dias_mantener: int = 7) -> None:
    """
    Elimina reportes diarios con más de N días de antigüedad.
    Llamado durante el refresh semanal.
    """
    log_dir = env("LOG_DIR", DEFAULT_LOG_DIR)
    reportes_dir = os.path.join(log_dir, "reportes_diarios")
    
    if not os.path.isdir(reportes_dir):
        print(f"[CLEANUP] No existe directorio de reportes: {reportes_dir}")
        return
    
    hoy = dt.date.today()
    limite = hoy - dt.timedelta(days=dias_mantener)
    
    eliminados = 0
    mantenidos = 0
    
    print(f"[CLEANUP] Limpiando reportes anteriores a {limite}")
    
    for filename in os.listdir(reportes_dir):
        if not filename.startswith("REPORTE_DAILY_"):
            continue
        
        # Extraer fecha del nombre: REPORTE_DAILY_2026-02-02.txt
        try:
            fecha_str = filename.replace("REPORTE_DAILY_", "").replace(".txt", "")
            fecha_reporte = dt.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            
            if fecha_reporte < limite:
                filepath = os.path.join(reportes_dir, filename)
                os.remove(filepath)
                print(f"[CLEANUP] Eliminado: {filename}")
                eliminados += 1
            else:
                mantenidos += 1
        
        except Exception as e:
            print(f"[CLEANUP] Error procesando {filename}: {e}")
    
    print(f"[CLEANUP] Reportes eliminados: {eliminados}, mantenidos: {mantenidos}")


# ============================================================
# FLUJOS PRINCIPALES
# ============================================================

def daily_update() -> int:
    """
    Flujo diario: consulta ingresos y asigna categoría NEW IN
    
    CORREGIDO v12.0: Usa matching por CÓDIGO MADRE en vez de SKU completo
    
    Retorna: 0=éxito, >0=error
    """
    print(f"\n{'='*60}")
    print(f"DAILY UPDATE - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 1. Resolver categoría
    cid = tn_resolve_category_id()
    if not cid:
        print("[ERROR] No se pudo resolver la categoría objetivo")
        return 2
    
    # 2. Listar productos y construir índice por CÓDIGO MADRE
    products = tn_list_products_paginated()
    madre_idx, prod_cats = tn_build_madre_index(products)
    
    # 3. Acumular SKUs desde último run
    today = dt.date.today()
    skus, by_day, network_error = accumulate_since_last_run(today=today)

    if network_error:
        print("[WARN] Error de red en Dragonfish — last_run_date NO actualizado, se reintentara mañana")
        return 1

    if not skus:
        print("[INFO] Sin SKUs para procesar en esta ventana")
        st = get_state()
        st["last_run_date"] = today.strftime("%Y-%m-%d")
        set_state(st)
        return 0
    
    # 4. Extraer códigos madre únicos de los SKUs
    codigos_madre = []
    for sku in skus:
        madre = extract_madre_code(sku)
        if madre:
            codigos_madre.append(madre)
    
    # Deduplicar códigos madre
    codigos_madre_unicos = list(dict.fromkeys(codigos_madre))  # Mantiene orden
    
    print(f"[MAP] SKUs ingresados: {len(skus)}")
    print(f"[MAP] Códigos madre únicos: {len(codigos_madre_unicos)}")
    
    # 5. Mapear códigos madre a ProductIDs
    pids = []
    matched_codes = []
    missed_codes = []
    
    for madre in codigos_madre_unicos:
        pid = madre_idx.get(madre)
        if pid:
            pids.append(int(pid))
            matched_codes.append(madre)
        else:
            missed_codes.append(madre)
    
    # Deduplicar product IDs (por si acaso)
    pids = sorted(set(pids))
    
    match_rate = (len(matched_codes)*100//len(codigos_madre_unicos)) if codigos_madre_unicos else 0
    print(f"[MAP] Códigos madre con match: {len(matched_codes)} / {len(codigos_madre_unicos)} ({match_rate}%)")
    
    # Mostrar códigos exitosos (primeros 20)
    if matched_codes:
        print(f"[MAP] + Códigos MADRE con MATCH ({len(matched_codes)} total, primeros 20): {matched_codes[:20]}")
    
    if missed_codes:
        print(f"[MAP] - Códigos MADRE SIN MATCH: {len(missed_codes)} (primeros 20): {missed_codes[:20]}")
    
    if not pids:
        print("[WARN] Ningún código madre matcheó con productos existentes")
        st = get_state()
        st["last_run_date"] = today.strftime("%Y-%m-%d")
        set_state(st)
        return 0
    
    # 6. Asignar categoría
    print(f"[INFO] Productos únicos a categorizar: {len(pids)}")
    success, productos_nuevos, productos_ya_tenian = tn_add_category_to_products(cid, pids, prod_cats)
    
    # 7. Generar reporte diario
    try:
        generar_reporte_diario(
            fecha=today,
            codigos_madre=codigos_madre_unicos,
            matched=matched_codes,
            missed=missed_codes,
            productos_agregados=productos_nuevos,
            productos_ya_tenian=productos_ya_tenian
        )
    except Exception as e:
        log_error("Error generando reporte diario", e)
        # No fallar la ejecución por error en reporte
    
    if success:
        print(f"[SUCCESS] Asignados {productos_nuevos} productos nuevos + {productos_ya_tenian} que ya estaban = {len(pids)} total")
        st = get_state()
        st["last_run_date"] = today.strftime("%Y-%m-%d")
        st["last_success_at"] = dt.datetime.now().isoformat()
        set_state(st)
        return 0
    
    print("[ERROR] Falló la asignación de categorías")
    return 3


def tn_clear_category_by_product_walk(category_id: int) -> bool:
    """
    Limpia la categoría de todos los productos que la tienen.
    Usado en el refresh semanal.
    """
    products = tn_list_products_paginated()
    _, prod_cats = tn_build_madre_index(products)
    
    holders = [pid for pid, cats in prod_cats.items() if category_id in cats]
    print(f"[TN] Productos que tienen la categoría {category_id}: {len(holders)}")
    
    if not holders:
        print("[TN] Ningún producto tiene esta categoría, nada que limpiar")
        return True
    
    ok_total = 0
    fail = 0
    
    for pid in holders:
        new_cats = [c for c in prod_cats[pid] if c != category_id]
        url = f"{tn_base()}/{tn_store_id()}/products/{pid}"
        body = {"categories": new_cats}
        
        try:
            resp = requests.put(url, headers=tn_headers(), data=json.dumps(body), timeout=60)
            if resp.status_code in (200, 201):
                ok_total += 1
            else:
                fail += 1
                print(f"[TN] pid={pid} limpiar cat HTTP {resp.status_code}: {resp.text[:200]}")
        except requests.RequestException as e:
            fail += 1
            log_error(f"pid={pid} limpiar cat error red", e)
        
        time.sleep(0.25)
    
    print(f"[TN] Limpieza por producto: ok={ok_total} fail={fail}")
    return fail == 0


def refresh_weekly() -> int:
    """
    Flujo semanal (lunes): limpia categoría NEW IN y resetea estado
    Retorna: 0=éxito, >0=error
    """
    print(f"\n{'='*60}")
    print(f"WEEKLY REFRESH - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 1. Resolver categoría
    cid = tn_resolve_category_id()
    if not cid:
        print("[ERROR] No se pudo resolver la categoría objetivo")
        return 2
    
    # 2. Limpiar categoría
    ok = tn_clear_category_by_product_walk(cid)
    if not ok:
        print("[ERROR] No se pudo limpiar la categoría por productos")
        return 3
    
    # 3. Limpiar reportes diarios viejos (mantener últimos 7 días)
    try:
        limpiar_reportes_viejos(dias_mantener=7)
    except Exception as e:
        log_error("Error limpiando reportes viejos", e)
        # No fallar la ejecución por error en limpieza de reportes
    
    # 4. Resetear estado
    # FIX v12.2.0: seteamos last_run_date=AYER en vez de borrarlo.
    # Al borrarlo, el daily posterior veia last_run=None y hacia catchup 7d.
    # Con esto: el daily ve last_run=ayer, arranca desde hoy, solo hoy.
    st = get_state()
    yesterday = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    st["last_run_date"] = yesterday
    st["last_refresh_at"] = dt.datetime.now().isoformat()
    set_state(st)
    
    print(f"[REFRESH] Estado: last_run_date={yesterday} (daily consultara solo hoy)")
    print("[SUCCESS] Refresh weekly OK. Estado reseteado y reportes limpiados")
    return 0


# ============================================================
# UTILIDADES
# ============================================================

def token_hash() -> str:
    """Hash del token para debugging"""
    t = (env("TN_ACCESS_TOKEN", "") or "").encode("utf-8")
    if not t:
        return "(vacio)"
    return (t[:4] + t[-4:]).hex()


def who() -> int:
    """Muestra información de conexión y test básico"""
    print(f"\n{'='*60}")
    print(f"WHO AM I - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    print(f"[TN] STORE_ID={tn_store_id()}")
    print(f"[TN] BASE={tn_base()}")
    print(f"[TN] TOKEN_HASH(first4+last4 hex)={token_hash()}")
    print(f"[DF] BASE_URL={env('DF_BASE_URL', '')}")
    print(f"[DF] IDCLIENTE={env('DF_IDCLIENTE', '')}")
    print(f"[DF] BASEDEDATOS={env('DF_BASEDEDATOS', '')}")
    
    cats = tn_list_categories_paginated(per_page=200)
    print(f"\n[TN] Categorías en esta tienda: {len(cats)}")
    
    for c in cats[:5]:
        def _get(d, k, default=""):
            v = d.get(k)
            if isinstance(v, dict):
                return v.get("es", "") or v.get("en", "") or v.get("pt", "")
            return v or default
        
        print(f"  - id={c.get('id')}  name.es='{_get(c,'name')}'  handle.es='{_get(c,'handle')}'")
    
    # Test de productos
    url = f"{tn_base()}/{tn_store_id()}/products"
    try:
        resp = requests.get(url, headers=tn_headers(), params={"per_page": 1, "page": 1}, timeout=30)
        if resp.status_code == 200:
            arr = resp.json()
            if isinstance(arr, list) and arr:
                nm = (arr[0].get('name') or {}).get('es', '') if isinstance(arr[0].get('name'), dict) else (arr[0].get('name') or '')
                print(f"\n[TN] Producto muestra: id={arr[0].get('id')} title.es='{nm}'")
            else:
                print("\n[TN] Sin productos o formato inesperado")
        else:
            print(f"\n[TN] HTTP {resp.status_code} consultando productos")
    except Exception as e:
        log_error("Error consultando productos", e)
    
    return 0


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    """Punto de entrada principal"""
    ap = argparse.ArgumentParser(
        description=f"New In Robot v{VERSION} (MATCHING POR CÓDIGO MADRE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos:
  daily       - Consulta ingresos y asigna categoría NEW IN (NUEVO: matching por código madre)
  refresh     - Limpia categoría NEW IN (ejecutar los lunes)
  list_cats   - Lista todas las categorías
  check_cat   - Verifica que la categoría configurada existe
  who         - Muestra info de conexión y test básico

Variables de entorno importantes:
  TN_ACCESS_TOKEN        - Token de acceso a Tiendanube
  TN_STORE_ID            - ID de la tienda
  DF_BASE_URL            - URL de la API de Dragonfish
  DF_JWTOKEN             - Token JWT de Dragonfish
  NEWIN_CATEGORY_ID      - ID de la categoría NEW IN
  NEWIN_ALLOW_CREATE     - Permitir crear categoría (true/false)

Archivos:
  config.env             - Variables de entorno
  data/state.json        - Estado de última ejecución
  data/newin_category.json - Categoría persistida
  logs/daily.log         - Log de ejecuciones diarias
  logs/refresh.log       - Log de refresh semanales

NUEVO EN v12.0.0:
  - Matching por CÓDIGO MADRE en vez de SKU completo
  - Aumenta drásticamente el match rate (80%+ esperado)
  - Evita duplicados automáticamente
        """
    )
    
    ap.add_argument(
        "cmd",
        choices=["daily", "refresh", "list_cats", "check_cat", "who"],
        help="Comando a ejecutar"
    )
    
    ap.add_argument(
        "--env",
        default="config.env",
        help="Ruta al archivo .env (default: config.env)"
    )
    
    args = ap.parse_args()
    
    # Cargar variables de entorno
    global MAIN_ENV
    MAIN_ENV = load_env_file(args.env)
    
    # Crear directorios necesarios
    ensure_dir(env("DATA_DIR", DEFAULT_DATA_DIR))
    ensure_dir(env("LOG_DIR", DEFAULT_LOG_DIR))
    
    # Mostrar configuración
    print(f"\n{'='*60}")
    print(f"New In Robot v{VERSION}")
    print(f"{'='*60}")
    print(f"[CFG] NEWIN_HANDLE={env('NEWIN_HANDLE', 'new-in1')}")
    print(f"[CFG] NEWIN_CATEGORY_ID={env('NEWIN_CATEGORY_ID', '(auto)')}")
    print(f"[CFG] NEWIN_ALLOW_CREATE={env('NEWIN_ALLOW_CREATE', 'false')}")
    print(f"[CFG] DATA_DIR={env('DATA_DIR', DEFAULT_DATA_DIR)}")
    print(f"[CFG] LOG_DIR={env('LOG_DIR', DEFAULT_LOG_DIR)}")
    print(f"{'='*60}\n")
    
    cmd = args.cmd.lower()
    
    try:
        if cmd == "daily":
            return daily_update()
        
        elif cmd == "refresh":
            return refresh_weekly()
        
        elif cmd == "list_cats":
            cats = tn_list_categories_paginated(per_page=200)
            print(f"\n[CATS] Total: {len(cats)}\n")
            for c in cats:
                print(f" - id={c.get('id')}  name.es='{_get_name_es(c)}'  handle.es='{_get_handle_es(c)}'")
            return 0
        
        elif cmd == "check_cat":
            cats = tn_list_categories_paginated(per_page=200)
            fixed = (env("NEWIN_CATEGORY_ID", "") or "").strip()
            
            if not fixed.isdigit():
                print("[CHECK] NEWIN_CATEGORY_ID no seteado o inválido")
                return 0
            
            cid = int(fixed)
            found = [c for c in cats if int(c.get('id')) == cid]
            
            if not found:
                print(f"[CHECK] ERROR: Categoría id={cid} NO existe en esta tienda (TN_STORE_ID={tn_store_id()})")
                return 0
            
            c = found[0]
            print(f"[CHECK] OK: Existe: id={cid} name.es='{_get_name_es(c)}' handle.es='{_get_handle_es(c)}'")
            return 0
        
        elif cmd == "who":
            return who()
        
        else:
            print(f"Comando inválido: {cmd}", file=sys.stderr)
            return 1
    
    except KeyboardInterrupt:
        print("\n[INFO] Interrumpido por usuario")
        return 130
    
    except Exception as e:
        log_error("Error inesperado", e)
        return 1


if __name__ == "__main__":
    MAIN_ENV = {}
    sys.exit(main())
