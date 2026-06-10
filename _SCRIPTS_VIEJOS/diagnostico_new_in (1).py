#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico Automático - Sistema New In
Verifica el estado completo del sistema y detecta problemas
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# Colores para terminal
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Color.BOLD}{Color.BLUE}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}{text.center(60)}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}{'='*60}{Color.END}\n")

def print_ok(text):
    print(f"{Color.GREEN}✓ {text}{Color.END}")

def print_warning(text):
    print(f"{Color.YELLOW}⚠ {text}{Color.END}")

def print_error(text):
    print(f"{Color.RED}✗ {text}{Color.END}")

def print_info(text):
    print(f"{Color.BLUE}ℹ {text}{Color.END}")

class DiagnosticoNewIn:
    def __init__(self):
        self.proyecto_root = Path.cwd()
        self.problemas = []
        self.warnings = []
        
    def verificar_estructura(self):
        """Verifica que exista la estructura esperada del proyecto"""
        print_header("VERIFICACIÓN DE ESTRUCTURA")
        
        directorios_esperados = ['scripts', 'data', 'logs', 'config']
        archivos_esperados = [
            'scripts/actualizar_new_in.py',
            'data/ultima_sincronizacion.txt',
            'data/productos_new_in.json'
        ]
        
        # Verificar directorios
        for dir_name in directorios_esperados:
            dir_path = self.proyecto_root / dir_name
            if dir_path.exists():
                print_ok(f"Directorio '{dir_name}' existe")
            else:
                print_error(f"Directorio '{dir_name}' NO EXISTE")
                self.problemas.append(f"Falta directorio: {dir_name}")
        
        # Verificar archivos clave
        for archivo in archivos_esperados:
            file_path = self.proyecto_root / archivo
            if file_path.exists():
                print_ok(f"Archivo '{archivo}' existe")
            else:
                print_error(f"Archivo '{archivo}' NO EXISTE")
                self.problemas.append(f"Falta archivo: {archivo}")
                
    def verificar_ultima_ejecucion(self):
        """Verifica cuándo fue la última ejecución exitosa"""
        print_header("ÚLTIMA EJECUCIÓN")
        
        sync_file = self.proyecto_root / 'data' / 'ultima_sincronizacion.txt'
        
        if not sync_file.exists():
            print_error("No hay registro de sincronización anterior")
            self.problemas.append("Sistema nunca se ha ejecutado o archivo de sincronización perdido")
            return
        
        try:
            with open(sync_file, 'r', encoding='utf-8') as f:
                ultima_fecha = f.read().strip()
            
            print_info(f"Última sincronización: {ultima_fecha}")
            
            # Intentar parsear la fecha
            try:
                fecha_sync = datetime.strptime(ultima_fecha, '%Y-%m-%d %H:%M:%S')
                ahora = datetime.now()
                dias_pasados = (ahora - fecha_sync).days
                horas_pasadas = (ahora - fecha_sync).seconds // 3600
                
                if dias_pasados == 0:
                    print_ok(f"Última ejecución hace {horas_pasadas} horas (HOY)")
                elif dias_pasados == 1:
                    print_warning(f"Última ejecución hace {dias_pasados} día")
                elif dias_pasados <= 3:
                    print_warning(f"Última ejecución hace {dias_pasados} días")
                else:
                    print_error(f"Última ejecución hace {dias_pasados} días - POSIBLE PROBLEMA")
                    self.problemas.append(f"Sistema no se ejecuta hace {dias_pasados} días")
                    
            except ValueError:
                print_warning("No se pudo parsear la fecha de última ejecución")
                
        except Exception as e:
            print_error(f"Error al leer archivo de sincronización: {e}")
            self.problemas.append("Error al leer última sincronización")
    
    def verificar_logs(self):
        """Analiza los logs más recientes"""
        print_header("ANÁLISIS DE LOGS")
        
        logs_dir = self.proyecto_root / 'logs'
        
        if not logs_dir.exists():
            print_error("Directorio de logs no existe")
            self.problemas.append("No hay logs disponibles")
            return
        
        # Buscar logs más recientes
        logs = sorted(logs_dir.glob('*.log'), key=os.path.getmtime, reverse=True)
        
        if not logs:
            print_error("No hay archivos de log")
            self.problemas.append("No se encontraron logs")
            return
        
        print_info(f"Logs encontrados: {len(logs)}")
        print_info(f"Log más reciente: {logs[0].name}")
        
        # Analizar el log más reciente
        try:
            with open(logs[0], 'r', encoding='utf-8') as f:
                contenido = f.read()
        except UnicodeDecodeError:
            # Intentar con encoding de Windows
            try:
                with open(logs[0], 'r', encoding='cp1252') as f:
                    contenido = f.read()
            except:
                # Último intento: ignorar errores
                with open(logs[0], 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
        
        # Buscar indicadores
        if 'ERROR' in contenido:
            errores = contenido.count('ERROR')
            print_error(f"Se encontraron {errores} errores en el último log")
            self.problemas.append(f"{errores} errores en última ejecución")
        
        if 'WARNING' in contenido:
            warnings = contenido.count('WARNING')
            print_warning(f"Se encontraron {warnings} advertencias en el último log")
            
        if 'exitosa' in contenido.lower() or 'completado' in contenido.lower():
            print_ok("Última ejecución se completó exitosamente")
        else:
            print_warning("No se encontró confirmación de ejecución exitosa")
            self.warnings.append("Última ejecución puede no haberse completado")
        
        # Mostrar últimas líneas
        lineas = contenido.strip().split('\n')
        print_info("\nÚltimas 5 líneas del log:")
        for linea in lineas[-5:]:
            print(f"  {linea}")
    
    def verificar_productos_actuales(self):
        """Verifica cuántos productos están actualmente en New In"""
        print_header("PRODUCTOS EN NEW IN")
        
        productos_file = self.proyecto_root / 'data' / 'productos_new_in.json'
        
        if not productos_file.exists():
            print_error("No hay archivo de productos")
            self.problemas.append("Archivo de productos no existe")
            return
        
        try:
            with open(productos_file, 'r', encoding='utf-8') as f:
                productos = json.load(f)
            
            if isinstance(productos, list):
                count = len(productos)
                if count == 0:
                    print_warning("La categoría New In está VACÍA")
                    self.warnings.append("No hay productos en New In")
                elif count < 5:
                    print_warning(f"Solo hay {count} productos en New In")
                    self.warnings.append(f"Pocos productos en New In: {count}")
                else:
                    print_ok(f"Hay {count} productos en New In")
            else:
                print_warning("Formato de archivo de productos inesperado")
                
        except json.JSONDecodeError:
            print_error("Error al leer JSON de productos")
            self.problemas.append("JSON de productos corrupto")
        except Exception as e:
            print_error(f"Error al leer productos: {e}")
            self.problemas.append("Error al leer productos")
    
    def verificar_tarea_programada(self):
        """Verifica si existe una tarea programada (Windows)"""
        print_header("TAREA PROGRAMADA")
        
        if os.name != 'nt':
            print_info("Sistema no es Windows, saltando verificación de Task Scheduler")
            return
        
        try:
            # Buscar tareas que contengan "new in" o nombres relacionados
            result = subprocess.run(
                ['schtasks', '/query', '/fo', 'LIST'],
                capture_output=True,
                text=True,
                encoding='cp1252'  # Windows encoding
            )
            
            tareas_relacionadas = []
            lineas = result.stdout.split('\n')
            
            for i, linea in enumerate(lineas):
                if 'TaskName:' in linea:
                    nombre_tarea = linea.split(':', 1)[1].strip()
                    if any(keyword in nombre_tarea.lower() for keyword in ['new', 'in', 'dragonfish', 'tiendanube']):
                        tareas_relacionadas.append(nombre_tarea)
            
            if tareas_relacionadas:
                print_ok(f"Se encontraron {len(tareas_relacionadas)} tareas relacionadas:")
                for tarea in tareas_relacionadas:
                    print(f"  • {tarea}")
                    
                # Verificar estado de la primera tarea
                result = subprocess.run(
                    ['schtasks', '/query', '/tn', tareas_relacionadas[0], '/fo', 'LIST', '/v'],
                    capture_output=True,
                    text=True,
                    encoding='cp1252'
                )
                
                if 'Disabled' in result.stdout:
                    print_error("La tarea está DESHABILITADA")
                    self.problemas.append("Tarea programada deshabilitada")
                else:
                    print_ok("La tarea está habilitada")
                    
                # Buscar última ejecución
                for linea in result.stdout.split('\n'):
                    if 'Last Run Time:' in linea:
                        ultima_ejecucion = linea.split(':', 1)[1].strip()
                        print_info(f"Última ejecución: {ultima_ejecucion}")
                    if 'Next Run Time:' in linea:
                        proxima_ejecucion = linea.split(':', 1)[1].strip()
                        print_info(f"Próxima ejecución: {proxima_ejecucion}")
            else:
                print_error("No se encontraron tareas programadas relacionadas")
                self.problemas.append("No hay tarea programada configurada")
                
        except Exception as e:
            print_warning(f"No se pudo verificar tareas programadas: {e}")
            self.warnings.append("No se pudo verificar Task Scheduler")
    
    def verificar_dependencias(self):
        """Verifica que estén instaladas las dependencias necesarias"""
        print_header("DEPENDENCIAS DE PYTHON")
        
        dependencias = ['requests', 'json']
        
        for dep in dependencias:
            try:
                __import__(dep)
                print_ok(f"Módulo '{dep}' instalado")
            except ImportError:
                print_error(f"Módulo '{dep}' NO INSTALADO")
                self.problemas.append(f"Falta dependencia: {dep}")
    
    def verificar_credenciales(self):
        """Verifica que existan archivos de credenciales"""
        print_header("CONFIGURACIÓN Y CREDENCIALES")
        
        config_dir = self.proyecto_root / 'config'
        
        if not config_dir.exists():
            print_error("Directorio de configuración no existe")
            self.problemas.append("No hay directorio de configuración")
            return
        
        archivos_config = ['credentials.json', 'config.json', 'settings.json']
        encontrado = False
        
        for archivo in archivos_config:
            config_file = config_dir / archivo
            if config_file.exists():
                print_ok(f"Archivo de configuración '{archivo}' existe")
                encontrado = True
                
                # Verificar que no esté vacío
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        if not config:
                            print_warning(f"El archivo {archivo} está vacío")
                        else:
                            print_info(f"Configuración contiene {len(config)} entradas")
                except json.JSONDecodeError:
                    print_error(f"El archivo {archivo} tiene formato JSON inválido")
                    self.problemas.append(f"JSON corrupto: {archivo}")
                except Exception as e:
                    print_warning(f"No se pudo leer {archivo}: {e}")
        
        if not encontrado:
            print_error("No se encontraron archivos de configuración")
            self.problemas.append("Faltan archivos de configuración")
    
    def generar_reporte(self):
        """Genera un reporte final con recomendaciones"""
        print_header("RESUMEN Y RECOMENDACIONES")
        
        if not self.problemas and not self.warnings:
            print_ok("¡No se detectaron problemas! El sistema parece estar correctamente configurado.")
            print_info("\nSi aún no está funcionando, intenta:")
            print("  1. Ejecutar manualmente: python scripts/actualizar_new_in.py")
            print("  2. Verificar los logs generados")
            print("  3. Revisar conectividad a internet")
        else:
            if self.problemas:
                print_error(f"\nSe detectaron {len(self.problemas)} PROBLEMAS CRÍTICOS:")
                for i, problema in enumerate(self.problemas, 1):
                    print(f"  {i}. {problema}")
            
            if self.warnings:
                print_warning(f"\nSe detectaron {len(self.warnings)} ADVERTENCIAS:")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
            
            print("\n" + "="*60)
            print_info("\nPRÓXIMOS PASOS RECOMENDADOS:\n")
            
            # Recomendaciones específicas basadas en problemas
            if any('tarea programada' in p.lower() for p in self.problemas):
                print("  📌 Configurar tarea programada en Task Scheduler")
                print("     Ver guía: Sección 3.1 del documento de diagnóstico\n")
            
            if any('log' in p.lower() for p in self.problemas):
                print("  📌 Ejecutar script manualmente para generar logs")
                print("     Comando: python scripts/actualizar_new_in.py\n")
            
            if any('sincronización' in p.lower() or 'días' in p.lower() for p in self.problemas):
                print("  📌 El sistema no se está ejecutando automáticamente")
                print("     1. Verificar tarea programada")
                print("     2. Ejecutar manualmente para probar\n")
            
            if any('configuración' in p.lower() or 'credenciales' in p.lower() for p in self.problemas):
                print("  📌 Verificar credenciales de API")
                print("     1. Revisar config/credentials.json")
                print("     2. Regenerar tokens si es necesario\n")
            
            if any('dependencia' in p.lower() for p in self.problemas):
                print("  📌 Instalar dependencias faltantes")
                print("     Comando: pip install requests\n")
        
        print("="*60)
        print_info(f"\nDiagnóstico completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_info("Para más ayuda, consulta: guia_diagnostico_new_in.md\n")
    
    def ejecutar_diagnostico_completo(self):
        """Ejecuta todos los chequeos de diagnóstico"""
        print("\n" + "="*60)
        print(f"{Color.BOLD}DIAGNÓSTICO DEL SISTEMA NEW IN{Color.END}".center(70))
        print(f"Directorio: {self.proyecto_root}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        self.verificar_estructura()
        self.verificar_ultima_ejecucion()
        self.verificar_logs()
        self.verificar_productos_actuales()
        self.verificar_tarea_programada()
        self.verificar_dependencias()
        self.verificar_credenciales()
        self.generar_reporte()

def main():
    diagnostico = DiagnosticoNewIn()
    diagnostico.ejecutar_diagnostico_completo()

if __name__ == "__main__":
    main()
