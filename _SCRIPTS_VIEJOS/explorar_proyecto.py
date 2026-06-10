#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Explorador de Proyecto - Descubre la estructura real del sistema New In
"""

import os
import json
from pathlib import Path
from datetime import datetime

def explorar_directorio():
    """Explora y muestra la estructura completa del proyecto"""
    proyecto_root = Path.cwd()
    
    print("="*70)
    print("EXPLORACIÓN DEL PROYECTO NEW IN")
    print("="*70)
    print(f"\nDirectorio actual: {proyecto_root}\n")
    
    # Recolectar información
    archivos_python = []
    archivos_json = []
    archivos_txt = []
    archivos_log = []
    directorios = []
    
    print("Escaneando archivos...\n")
    
    for item in proyecto_root.rglob('*'):
        if item.is_file():
            nombre = item.name
            ruta_relativa = item.relative_to(proyecto_root)
            
            if nombre.endswith('.py'):
                archivos_python.append(ruta_relativa)
            elif nombre.endswith('.json'):
                archivos_json.append(ruta_relativa)
            elif nombre.endswith('.txt'):
                archivos_txt.append(ruta_relativa)
            elif nombre.endswith('.log'):
                archivos_log.append(ruta_relativa)
        elif item.is_dir() and item != proyecto_root:
            ruta_relativa = item.relative_to(proyecto_root)
            # Ignorar directorios de sistema
            if not any(p in str(ruta_relativa) for p in ['.git', '__pycache__', 'venv', 'node_modules']):
                directorios.append(ruta_relativa)
    
    # Mostrar resultados
    print("📁 DIRECTORIOS ENCONTRADOS:")
    print("-" * 70)
    if directorios:
        for d in sorted(directorios):
            print(f"  📂 {d}")
    else:
        print("  (No se encontraron subdirectorios)")
    
    print("\n🐍 ARCHIVOS PYTHON (.py):")
    print("-" * 70)
    if archivos_python:
        for f in sorted(archivos_python):
            print(f"  🐍 {f}")
    else:
        print("  ⚠ No se encontraron archivos Python")
    
    print("\n📄 ARCHIVOS JSON (.json):")
    print("-" * 70)
    if archivos_json:
        for f in sorted(archivos_json):
            tamaño = (proyecto_root / f).stat().st_size
            print(f"  📄 {f} ({tamaño:,} bytes)")
    else:
        print("  ⚠ No se encontraron archivos JSON")
    
    print("\n📝 ARCHIVOS DE TEXTO (.txt):")
    print("-" * 70)
    if archivos_txt:
        for f in sorted(archivos_txt):
            print(f"  📝 {f}")
    else:
        print("  ⚠ No se encontraron archivos TXT")
    
    print("\n📋 ARCHIVOS DE LOG (.log):")
    print("-" * 70)
    if archivos_log:
        for f in sorted(archivos_log):
            log_path = proyecto_root / f
            tamaño = log_path.stat().st_size
            modificado = datetime.fromtimestamp(log_path.stat().st_mtime)
            print(f"  📋 {f}")
            print(f"      Tamaño: {tamaño:,} bytes | Modificado: {modificado.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("  ⚠ No se encontraron logs")
    
    # Análisis especial de logs
    if archivos_log:
        print("\n" + "="*70)
        print("ANÁLISIS DE LOGS")
        print("="*70)
        
        log_mas_reciente = max(archivos_log, key=lambda f: (proyecto_root / f).stat().st_mtime)
        print(f"\n📋 Log más reciente: {log_mas_reciente}")
        
        log_path = proyecto_root / log_mas_reciente
        print(f"   Tamaño: {log_path.stat().st_size:,} bytes")
        print(f"   Última modificación: {datetime.fromtimestamp(log_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n   Últimas 20 líneas del log:")
        print("   " + "-"*66)
        
        try:
            # Intentar múltiples encodings
            encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
            contenido = None
            
            for encoding in encodings:
                try:
                    with open(log_path, 'r', encoding=encoding) as f:
                        contenido = f.read()
                    print(f"   (Leído con encoding: {encoding})")
                    break
                except UnicodeDecodeError:
                    continue
            
            if contenido is None:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                print("   (Leído ignorando errores de encoding)")
            
            lineas = contenido.strip().split('\n')
            for linea in lineas[-20:]:
                print(f"   {linea}")
                
        except Exception as e:
            print(f"   ⚠ Error al leer log: {e}")
    
    # Buscar archivos de configuración
    print("\n" + "="*70)
    print("BÚSQUEDA DE ARCHIVOS CLAVE")
    print("="*70)
    
    archivos_clave = [
        'actualizar_new_in.py',
        'sync.py',
        'main.py',
        'credentials.json',
        'config.json',
        'ultima_sincronizacion.txt',
        'productos_new_in.json'
    ]
    
    encontrados = []
    for archivo in archivos_clave:
        for item in proyecto_root.rglob(archivo):
            encontrados.append((archivo, item.relative_to(proyecto_root)))
    
    if encontrados:
        print("\n✓ Archivos clave encontrados:")
        for nombre, ruta in encontrados:
            print(f"  ✓ {nombre} → {ruta}")
    else:
        print("\n⚠ No se encontraron archivos clave del sistema")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"\n  Total de archivos Python: {len(archivos_python)}")
    print(f"  Total de archivos JSON: {len(archivos_json)}")
    print(f"  Total de archivos de log: {len(archivos_log)}")
    print(f"  Total de directorios: {len(directorios)}")
    
    if len(archivos_python) == 0:
        print("\n⚠ ADVERTENCIA: No hay archivos Python en este proyecto")
        print("  ¿Estás en el directorio correcto?")
    
    if len(archivos_log) > 0 and len(archivos_python) == 0:
        print("\n⚠ Hay logs pero no hay scripts Python")
        print("  Los archivos del sistema pueden estar en otro lugar")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    explorar_directorio()
