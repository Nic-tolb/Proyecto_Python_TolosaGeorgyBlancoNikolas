"""
ui.py - Interfaz de usuario en consola
"""
import json
from models import RegistroGastos
from analytics import Analizador

class UI:
    """Maneja toda la interfaz de usuario"""
    
    @staticmethod
    def limpiar_pantalla():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def mostrar_menu_principal():
        print("\n" + "=" * 45)
        print("         Simulador de Gasto Diario")
        print("=" * 45)
        print("Seleccione una opción:\n")
        print("1. Registrar nuevo gasto")
        print("2. Listar gastos")
        print("3. Calcular total de gastos")
        print("4. Generar reporte de gastos")
        print("5. Salir")
        print("=" * 45)
    
    @staticmethod
    def registrar_gasto(categorias_disponibles):
        print("\n" + "=" * 45)
        print("            Registrar Nuevo Gasto")
        print("=" * 45)
        print("Ingrese la información del gasto:\n")
        
        try:
            monto = float(input("- Monto del gasto: $"))
            print("\n- Categoría:")
            print(f"  Disponibles: {', '.join(categorias_disponibles)}")
            print("  (Puede ingresar una nueva categoría si lo desea)")
            categoria = input("  > ").strip()
            descripcion = input("- Descripción (opcional): ").strip()
            
            print("\nIngrese 'S' para guardar o 'C' para cancelar.")
            confirmacion = input("> ").strip().upper()
            
            return (monto, categoria, descripcion) if confirmacion == 'S' else None
        except ValueError:
            print("\n⚠ Error: El monto debe ser un número válido.")
            return None
    
    @staticmethod
    def mostrar_menu_listar():
        print("\n" + "=" * 45)
        print("                Listar Gastos")
        print("=" * 45)
        print("Seleccione una opción para filtrar los gastos:\n")
        print("1. Ver todos los gastos")
        print("2. Filtrar por categoría")
        print("3. Filtrar por rango de fechas")
        print("4. Regresar al menú principal")
        print("=" * 45)
    
    @staticmethod
    def mostrar_gastos(gastos, titulo="Gastos"):
        print(f"\n{titulo}:")
        print("-" * 80)
        if not gastos:
            print("No hay gastos registrados.")
            return
        
        for i, gasto in enumerate(gastos, 1):
            print(f"{i}. [{gasto.categoria.upper()}] ${gasto.monto:,.2f}")
            print(f"   Fecha: {gasto.fecha}")
            if gasto.descripcion:
                print(f"   Descripción: {gasto.descripcion}")
            print()
    
    @staticmethod
    def mostrar_menu_calcular():
        print("\n" + "=" * 45)
        print("          Calcular Total de Gastos")
        print("=" * 45)
        print("Seleccione el periodo de cálculo:\n")
        print("1. Calcular total diario")
        print("2. Calcular total semanal")
        print("3. Calcular total mensual")
        print("4. Regresar al menú principal")
        print("=" * 45)
    
    @staticmethod
    def mostrar_menu_reporte():
        print("\n" + "=" * 45)
        print("           Generar Reporte de Gastos")
        print("=" * 45)
        print("Seleccione el tipo de reporte:\n")
        print("1. Reporte diario")
        print("2. Reporte semanal")
        print("3. Reporte mensual")
        print("4. Regresar al menú principal")
        print("=" * 45)
    
    @staticmethod
    def mostrar_reporte(reporte: dict):
        print("\n" + "=" * 50)
        print(f"       REPORTE {reporte['periodo'].upper()}")
        print("=" * 50)
        print(f"Fecha de generación: {reporte['fecha_generacion']}")
        print(f"Total de transacciones: {reporte['cantidad_transacciones']}")
        print(f"\nTOTAL GASTADO: ${reporte['total_gastos']:,.2f}")
        print("\nDesglose por categoría:")
        print("-" * 50)
        
        for categoria, monto in reporte['por_categoria'].items():
            porcentaje = (monto / reporte['total_gastos'] * 100) if reporte['total_gastos'] > 0 else 0
            print(f"  {categoria.capitalize():15} ${monto:10,.2f}  ({porcentaje:5.1f}%)")
        
        print("=" * 50)
    
    @staticmethod
    def preguntar_guardar_reporte() -> bool:
        print("\n¿Desea guardar el reporte en un archivo? (S/N): ", end="")
        return input().strip().upper() == 'S'
    
    @staticmethod
    def guardar_reporte_json(reporte: dict):
        archivo = f"reporte_{reporte['periodo']}_{reporte['fecha_generacion'].split()[0]}.json"
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False)
            print(f"✓ Reporte guardado en: {archivo}")
        except Exception as e:
            print(f"⚠ Error al guardar reporte: {e}")