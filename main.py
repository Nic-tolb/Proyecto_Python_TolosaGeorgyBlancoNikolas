"""
main.py - Punto de entrada y controlador principal
"""
from models import RegistroGastos
from storage import Storage
from analytics import Analizador
from ui import UI

class SimuladorGastos:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        self.storage = Storage()
        self.registro = self.storage.cargar()
        self.analizador = Analizador(self.registro)
        self.ui = UI()
    
    def ejecutar(self):
        """Loop principal de la aplicación"""
        while True:
            self.ui.mostrar_menu_principal()
            opcion = input("\nSeleccione una opción (1-5): ").strip()
            
            if opcion == '1':
                self.opcion_registrar_gasto()
            elif opcion == '2':
                self.opcion_listar_gastos()
            elif opcion == '3':
                self.opcion_calcular_total()
            elif opcion == '4':
                self.opcion_generar_reporte()
            elif opcion == '5':
                if self.opcion_salir():
                    break
            else:
                print("\n⚠ Opción inválida. Intente nuevamente.")
            
            input("\nPresione enter para seguir ")
    
    def opcion_registrar_gasto(self):
        """Maneja el registro de un nuevo gasto"""
        categorias = self.registro.obtener_categorias()
        resultado = self.ui.registrar_gasto(categorias)
        
        if resultado:
            monto, categoria, descripcion = resultado
            categoria_lower = categoria.lower().strip()
            
            # Si la categoría no existe, preguntar si desea crearla
            if categoria_lower not in self.registro.obtener_categorias():
                print(f"\n⚠ La categoría '{categoria}' no existe.")
                crear = input("¿Desea crear esta nueva categoría? (S/N): ").strip().upper()
                
                if crear == 'S':
                    if self.registro.agregar_categoria(categoria):
                        self.storage.guardar(self.registro)
                        print(f"✓ Categoría '{categoria}' creada exitosamente!")
                    else:
                        print("\n⚠ Error: No se pudo crear la categoría.")
                        return
                else:
                    print("\n✗ Registro cancelado.")
                    return
            
            # Registrar el gasto
            if self.registro.agregar_gasto(categoria, monto, descripcion):
                self.storage.guardar(self.registro)
                print("\n✓ Gasto registrado exitosamente!")
            else:
                print("\n⚠ Error: No se pudo registrar el gasto.")
        else:
            print("\n✗ Registro cancelado.")
    
    def opcion_listar_gastos(self):
        """Maneja el listado de gastos con filtros"""
        while True:
            self.ui.mostrar_menu_listar()
            opcion = input("\nSeleccione una opción (1-4): ").strip()
            
            if opcion == '1':
                self.ui.mostrar_gastos(self.registro.obtener_gastos(), "Todos los gastos")
            elif opcion == '2':
                categorias = self.registro.obtener_categorias()
                print("\nCategorías disponibles:", ", ".join(categorias))
                categoria = input("Ingrese la categoría: ").strip()
                gastos = self.analizador.filtrar_por_categoria(categoria)
                self.ui.mostrar_gastos(gastos, f"Gastos en {categoria}")
            elif opcion == '3':
                print("\nIngrese el rango de fechas (formato: YYYY-MM-DD)")
                fecha_inicio = input("Fecha inicio: ").strip()
                fecha_fin = input("Fecha fin: ").strip()
                try:
                    gastos = self.analizador.filtrar_por_fechas(fecha_inicio, fecha_fin)
                    self.ui.mostrar_gastos(gastos, f"Gastos del {fecha_inicio} al {fecha_fin}")
                except ValueError:
                    print("\n⚠ Error: Formato de fecha inválido.")
            elif opcion == '4':
                break
            else:
                print("\n⚠ Opción inválida.")
            
            if opcion in ['1', '2', '3']:
                input("\nPresione enter para seguir")
    
    def opcion_calcular_total(self):
        """Maneja el cálculo de totales"""
        self.ui.mostrar_menu_calcular()
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        if opcion == '1':
            total = self.analizador.calcular_total_diario()
            print(f"\n💰 Total gastado HOY: ${total:,.2f}")
        elif opcion == '2':
            total = self.analizador.calcular_total_semanal()
            print(f"\n💰 Total gastado en los últimos 7 días: ${total:,.2f}")
        elif opcion == '3':
            total = self.analizador.calcular_total_mensual()
            print(f"\n💰 Total gastado en los últimos 30 días: ${total:,.2f}")
        elif opcion == '4':
            return
        else:
            print("\n⚠ Opción inválida.")
    
    def opcion_generar_reporte(self):
        """Maneja la generación de reportes"""
        self.ui.mostrar_menu_reporte()
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        periodo_map = {'1': 'diario', '2': 'semanal', '3': 'mensual'}
        
        if opcion in periodo_map:
            reporte = self.analizador.generar_reporte(periodo_map[opcion])
            self.ui.mostrar_reporte(reporte)
            
            if self.ui.preguntar_guardar_reporte():
                self.ui.guardar_reporte_json(reporte)
        elif opcion == '4':
            return
        else:
            print("\n⚠ Opción inválida.")
    
    def opcion_salir(self) -> bool:
        """Confirma la salida del programa"""
        confirmacion = input("\n¿Desea salir del programa? (S/N): ").strip().upper()
        if confirmacion == 'S':
            print("\n¡Gracias por usar el Simulador de Gasto Diario!")
            return True
        return False

if __name__ == "__main__":
    app = SimuladorGastos()
    app.ejecutar()