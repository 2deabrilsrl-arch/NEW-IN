#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_semana_26_31.py
============================================================
Script especial para sincronizar manualmente toda la semana
del lunes 26/01/2026 al sábado 31/01/2026

Este script:
1. Consulta Dragonfish para todos los ingresos (ING) del 26/01 al 31/01
2. Extrae códigos madre únicos
3. Busca productos en Tiendanube que matcheen
4. Agrega todos los productos encontrados a la categoría NEW IN
5. Genera reporte detallado

USO:
    python sync_semana_26_31.py

IMPORTANTE:
- Ejecutar ANTES de la sincronización automática del lunes 02/02
- Este script NO modifica el archivo state.json para no interferir con el robot diario
- Genera un reporte en logs/SYNC_SEMANA_26_31_REPORTE.txt
============================================================
"""
import os
import sys
import json
import datetime as dt
import time
from typing import List, Dict, Set

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
except ImportError:
    print("[FATAL] Falta 'requests'. Instala: pip install requests", file=sys.stderr)
    sys.exit(1)

# ============================================================
# CONFIGURACIÓN
# ============================================================

# Fechas de la semana a sincronizar
FECHA_INICIO = dt.date(2026, 1, 26)  # Lunes
FECHA_FIN = dt.date(2026, 1, 31)     # Sábado

DEFAULT_BASE_DIR = r"C:\Users\santiago\NEW IN"
CONFIG_FILE = os.path.join(DEFAULT_BASE_DIR, "config.env")
LOG_DIR = os.path.join(DEFAULT_BASE_DIR, "logs")

# ============================================================
# UTILIDADES
# ============================================================

def load_env_file(path: str) -> Dict[str, str]:
    """Carga variables de entorno desde archivo .env"""
    d = {}
    if not os.path.isfile(path):
        print(f"[ERROR] No se encuentra config.env en: {path}")
        return d
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if "=" in s:
                k, v = s.split("=", 1)
                d[k.strip()] = v.strip()
    
    print(f"[ENV] Cargadas {len(d)} variables desde {path}")
    return d


def env(k: str, default: str = "") -> str:
    """Obtiene variable de entorno"""
    return ENV_VARS.get(k, os.environ.get(k, default)).strip()


def extract_madre_code(sku: str) -> str:
    """Extrae código madre del SKU"""
    if not sku:
        return ""
    if "#" in sku:
        return sku.split("#")[0]
    return sku


# ============================================================
# API HELPERS
# ============================================================

def tn_headers() -> Dict[str, str]:
    """Headers para Tiendanube"""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authentication": f"bearer {env('TN_ACCESS_TOKEN')}",
        "User-Agent": "NewInRobot/SyncSemana"
    }


def tn_base() -> str:
    """URL base Tiendanube"""
    return env("TN_BASE_URL", "https://api.tiendanube.com/v1").rstrip("/")


def tn_store_id() -> str:
    """ID de tienda"""
    return env("TN_STORE_ID")


def df_headers() -> Dict[str, str]:
    """Headers para Dragonfish"""
    h = {
        "IdCliente": env("DF_IDCLIENTE", "WEB"),
        "BaseDeDatos": env("DF_BASEDEDATOS"),
        "accept": "application/json"
    }
    t = env("DF_JWTOKEN")
    if t:
        h["Authorization"] = t
    return h


# Alias de campos para SKU
ART_KEYS = ["Articulo", "CodArticulo", "CodigoArticulo", "Codigo"]
COLOR_KEYS = ["Color", "CodColor", "CodigoColor"]
TALLE_KEYS = ["Talle", "CodTalle", "CodigoTalle"]


def _pick_first(d: Dict, keys: List[str]) -> str:
    """Busca el primer campo con valor"""
    for k in keys:
        if k in d and str(d[k]).strip():
            return str(d[k]).strip()
    return ""


def build_sku(it: Dict) -> str:
    """Construye SKU desde item de Dragonfish"""
    a = _pick_first(it, ART_KEYS)
    c = _pick_first(it, COLOR_KEYS)
    t = _pick_first(it, TALLE_KEYS)
    
    if not a or not c or not t:
        return ""
    
    # Filtrar CONTROL
    if "CONTROL" in a.upper():
        return ""
    
    # Transformar espacios
    a = a.replace(" ", "___")
    c = c.replace(" ", "___")
    t = t.replace(" ", "___")
    
    return f"{a}#{c}#{t}"


# ============================================================
# CONSULTA DRAGONFISH
# ============================================================

def consultar_dragonfish_rango(fecha_desde: dt.date, fecha_hasta: dt.date) -> List[str]:
    """
    Consulta Dragonfish para todos los movimientos ING en el rango de fechas.
    Retorna lista de SKUs únicos.
    """
    base = env("DF_BASE_URL").rstrip("/")
    url = f"{base}/Movimientodestock/"
    
    todos_skus = []
    fecha_actual = fecha_desde
    
    print(f"\n{'='*60}")
    print(f"CONSULTANDO DRAGONFISH: {fecha_desde} -> {fecha_hasta}")
    print(f"{'='*60}\n")
    
    while fecha_actual <= fecha_hasta:
        print(f"[DF] Consultando {fecha_actual}...")
        
        params = {
            "OrigenDestino": env("DF_ORIGENDESTINO", "STOCK"),
            "Tipo": env("DF_TIPO", "1"),
            "Motivo": env("DF_MOTIVO", "ING"),
            "Fecha": fecha_actual.strftime("%Y-%m-%d"),
            "limit": "200",
            "page": "1"
        }
        
        page = 1
        items_dia = []
        
        while page <= 50:  # max páginas
            params["page"] = str(page)
            
            try:
                resp = requests.get(url, headers=df_headers(), params=params, timeout=30)
            except Exception as e:
                print(f"[DF] Error en {fecha_actual} page={page}: {e}")
                break
            
            if resp.status_code == 404:
                if page == 1:
                    print(f"[DF] {fecha_actual}: Sin movimientos (404)")
                break
            
            if resp.status_code != 200:
                print(f"[DF] {fecha_actual}: HTTP {resp.status_code}")
                break
            
            try:
                js = resp.json()
            except:
                print(f"[DF] {fecha_actual}: Respuesta no JSON")
                break
            
            # Extraer items
            items = []
            if isinstance(js, dict) and "Resultados" in js:
                for mov in js["Resultados"]:
                    det = mov.get("MovimientoDetalle", [])
                    if isinstance(det, list):
                        items.extend(det)
            
            if not items:
                break
            
            items_dia.extend(items)
            print(f"[DF] {fecha_actual} page={page}: {len(items)} items")
            
            if len(items) < 200:
                break
            
            page += 1
        
        # Construir SKUs del día
        skus_dia = []
        for item in items_dia:
            sku = build_sku(item)
            if sku:
                skus_dia.append(sku)
        
        print(f"[DF] {fecha_actual}: {len(skus_dia)} SKUs válidos de {len(items_dia)} items")
        todos_skus.extend(skus_dia)
        
        fecha_actual += dt.timedelta(days=1)
    
    # Deduplicar
    skus_unicos = list(dict.fromkeys(todos_skus))
    print(f"\n[DF] TOTAL: {len(skus_unicos)} SKUs únicos de {len(todos_skus)} totales")
    
    return skus_unicos


# ============================================================
# CONSULTA TIENDANUBE
# ============================================================

def listar_productos_tiendanube() -> List[Dict]:
    """Lista todos los productos de Tiendanube"""
    print(f"\n{'='*60}")
    print("LISTANDO PRODUCTOS DE TIENDANUBE")
    print(f"{'='*60}\n")
    
    productos = []
    page = 1
    
    while True:
        url = f"{tn_base()}/{tn_store_id()}/products"
        params = {"per_page": 100, "page": page}
        
        try:
            resp = requests.get(url, headers=tn_headers(), params=params, timeout=30)
        except Exception as e:
            print(f"[TN] Error page={page}: {e}")
            break
        
        if resp.status_code != 200:
            print(f"[TN] HTTP {resp.status_code} page={page}")
            break
        
        try:
            data = resp.json()
        except:
            print(f"[TN] No JSON page={page}")
            break
        
        if not data or not isinstance(data, list):
            break
        
        productos.extend(data)
        print(f"[TN] Página {page}: {len(data)} productos (acumulado={len(productos)})")
        
        if len(data) < 100:
            break
        
        page += 1
    
    print(f"[TN] Total productos: {len(productos)}")
    return productos


def construir_indice_madre(productos: List[Dict]) -> Dict[str, Dict]:
    """
    Construye índice de código madre -> info del producto
    """
    print(f"\n{'='*60}")
    print("CONSTRUYENDO ÍNDICE DE CÓDIGOS MADRE")
    print(f"{'='*60}\n")
    
    indice = {}
    
    for prod in productos:
        pid = int(prod.get("id"))
        cats = prod.get("categories", [])
        nombre = (prod.get("name") or {}).get("es", "") if isinstance(prod.get("name"), dict) else ""
        
        # Normalizar categorías
        cat_ids = []
        for c in cats:
            if isinstance(c, dict):
                cid = c.get("id")
                if cid:
                    cat_ids.append(int(cid))
            else:
                try:
                    cat_ids.append(int(c))
                except:
                    pass
        
        # Indexar por código madre de cada variante
        for var in prod.get("variants", []):
            sku = (var.get("sku") or "").strip()
            if sku:
                madre = extract_madre_code(sku)
                if madre and madre not in indice:
                    indice[madre] = {
                        "product_id": pid,
                        "nombre": nombre,
                        "categories": cat_ids
                    }
    
    print(f"[MAP] Códigos madre indexados: {len(indice)}")
    return indice


# ============================================================
# ASIGNACIÓN DE CATEGORÍA
# ============================================================

def obtener_categoria_newin() -> int:
    """Obtiene el ID de la categoría NEW IN"""
    cat_id = env("NEWIN_CATEGORY_ID")
    if cat_id and cat_id.isdigit():
        return int(cat_id)
    
    # Buscar por handle
    url = f"{tn_base()}/{tn_store_id()}/categories"
    try:
        resp = requests.get(url, headers=tn_headers(), params={"per_page": 200}, timeout=30)
        if resp.status_code == 200:
            cats = resp.json()
            handle = env("NEWIN_HANDLE", "new-in1")
            for c in cats:
                h = c.get("handle", {})
                h_es = h.get("es") if isinstance(h, dict) else h
                if h_es and h_es.lower() == handle.lower():
                    return int(c.get("id"))
    except:
        pass
    
    print("[ERROR] No se pudo obtener categoría NEW IN")
    return 0


def asignar_categoria(product_ids: List[int], categoria_id: int, indice: Dict[str, Dict]) -> Dict:
    """
    Asigna la categoría NEW IN a los productos.
    Retorna estadísticas de la operación.
    """
    print(f"\n{'='*60}")
    print(f"ASIGNANDO CATEGORÍA {categoria_id} A {len(product_ids)} PRODUCTOS")
    print(f"{'='*60}\n")
    
    exitosos = 0
    fallidos = 0
    ya_tenian = 0
    
    for i, pid in enumerate(product_ids, 1):
        # Buscar info del producto
        prod_info = None
        for madre, info in indice.items():
            if info["product_id"] == pid:
                prod_info = info
                break
        
        if not prod_info:
            print(f"[{i}/{len(product_ids)}] pid={pid}: Sin info, saltando")
            fallidos += 1
            continue
        
        cats_actuales = prod_info["categories"]
        
        # Ya tiene la categoría?
        if categoria_id in cats_actuales:
            print(f"[{i}/{len(product_ids)}] pid={pid}: Ya tiene categoría, salto")
            ya_tenian += 1
            continue
        
        # Agregar categoría
        nuevas_cats = sorted(set(cats_actuales + [categoria_id]))
        url = f"{tn_base()}/{tn_store_id()}/products/{pid}"
        body = {"categories": nuevas_cats}
        
        try:
            resp = requests.put(url, headers=tn_headers(), data=json.dumps(body), timeout=60)
            if resp.status_code in (200, 201):
                print(f"[{i}/{len(product_ids)}] pid={pid}: OK ({prod_info['nombre'][:40]})")
                exitosos += 1
            else:
                print(f"[{i}/{len(product_ids)}] pid={pid}: HTTP {resp.status_code}")
                fallidos += 1
        except Exception as e:
            print(f"[{i}/{len(product_ids)}] pid={pid}: Error {e}")
            fallidos += 1
        
        time.sleep(0.3)  # Rate limiting
    
    return {
        "exitosos": exitosos,
        "fallidos": fallidos,
        "ya_tenian": ya_tenian,
        "total": len(product_ids)
    }


# ============================================================
# REPORTE
# ============================================================

def generar_reporte(
    fecha_desde: dt.date,
    fecha_hasta: dt.date,
    skus: List[str],
    codigos_madre: List[str],
    matched: List[str],
    missed: List[str],
    stats: Dict
) -> str:
    """Genera reporte de la sincronización"""
    
    fecha_reporte = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    reporte = f"""
{'='*80}
REPORTE DE SINCRONIZACIÓN MANUAL - SEMANA 26/01 AL 31/01
{'='*80}

Fecha del reporte: {fecha_reporte}
Rango sincronizado: {fecha_desde} -> {fecha_hasta}

{'='*80}
ESTADÍSTICAS DE DRAGONFISH
{'='*80}

SKUs ingresados (con talle/color):  {len(skus)}
Códigos madre únicos:                {len(codigos_madre)}

{'='*80}
ESTADÍSTICAS DE MATCHING
{'='*80}

Códigos madre encontrados en TN:     {len(matched)} ({len(matched)*100//len(codigos_madre) if codigos_madre else 0}%)
Códigos madre NO encontrados:        {len(missed)} ({len(missed)*100//len(codigos_madre) if codigos_madre else 0}%)

{'='*80}
ESTADÍSTICAS DE ASIGNACIÓN
{'='*80}

Productos procesados:                {stats['total']}
Exitosos (nuevos):                   {stats['exitosos']}
Ya tenían la categoría:              {stats['ya_tenian']}
Fallidos:                            {stats['fallidos']}

{'='*80}
CÓDIGOS MADRE CON MATCH (primeros 50)
{'='*80}

{chr(10).join('  - ' + m for m in matched[:50])}

{'='*80}
CÓDIGOS MADRE SIN MATCH (primeros 50)
{'='*80}

{chr(10).join('  - ' + m for m in missed[:50])}

{'='*80}
FIN DEL REPORTE
{'='*80}
"""
    
    return reporte


# ============================================================
# MAIN
# ============================================================

def main():
    """Función principal"""
    global ENV_VARS
    
    print(f"\n{'='*80}")
    print("SINCRONIZACIÓN MANUAL - SEMANA 26/01 AL 31/01")
    print(f"{'='*80}\n")
    
    # 1. Cargar configuración
    print("[1/7] Cargando configuración...")
    ENV_VARS = load_env_file(CONFIG_FILE)
    
    if not ENV_VARS:
        print("[ERROR] No se pudo cargar configuración")
        return 1
    
    # 2. Consultar Dragonfish
    print("\n[2/7] Consultando Dragonfish...")
    skus = consultar_dragonfish_rango(FECHA_INICIO, FECHA_FIN)
    
    if not skus:
        print("[WARN] No se encontraron SKUs para el rango")
        return 0
    
    # 3. Extraer códigos madre
    print("\n[3/7] Extrayendo códigos madre...")
    codigos_madre = []
    for sku in skus:
        madre = extract_madre_code(sku)
        if madre:
            codigos_madre.append(madre)
    
    codigos_madre_unicos = list(dict.fromkeys(codigos_madre))
    print(f"[MAP] Códigos madre únicos: {len(codigos_madre_unicos)}")
    
    # 4. Listar productos de Tiendanube
    print("\n[4/7] Listando productos de Tiendanube...")
    productos = listar_productos_tiendanube()
    
    if not productos:
        print("[ERROR] No se pudieron listar productos de TN")
        return 1
    
    # 5. Construir índice y matchear
    print("\n[5/7] Construyendo índice y matcheando...")
    indice = construir_indice_madre(productos)
    
    matched = []
    missed = []
    product_ids = []
    
    for madre in codigos_madre_unicos:
        if madre in indice:
            matched.append(madre)
            pid = indice[madre]["product_id"]
            if pid not in product_ids:
                product_ids.append(pid)
        else:
            missed.append(madre)
    
    print(f"\n[MATCH] Productos a categorizar: {len(product_ids)}")
    print(f"[MATCH] Match rate: {len(matched)*100//len(codigos_madre_unicos) if codigos_madre_unicos else 0}%")
    
    if not product_ids:
        print("[WARN] No hay productos para categorizar")
        return 0
    
    # 6. Asignar categoría
    print("\n[6/7] Asignando categoría...")
    categoria_id = obtener_categoria_newin()
    
    if not categoria_id:
        print("[ERROR] No se pudo obtener ID de categoría NEW IN")
        return 1
    
    stats = asignar_categoria(product_ids, categoria_id, indice)
    
    # 7. Generar reporte
    print("\n[7/7] Generando reporte...")
    reporte = generar_reporte(
        FECHA_INICIO,
        FECHA_FIN,
        skus,
        codigos_madre_unicos,
        matched,
        missed,
        stats
    )
    
    # Guardar reporte
    os.makedirs(LOG_DIR, exist_ok=True)
    reporte_path = os.path.join(LOG_DIR, "SYNC_SEMANA_26_31_REPORTE.txt")
    
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write(reporte)
    
    print(reporte)
    print(f"\n[SUCCESS] Reporte guardado en: {reporte_path}")
    
    return 0


if __name__ == "__main__":
    ENV_VARS = {}
    sys.exit(main())
