"""
storage.py - Manejo de persistencia de datos en JSON
"""
import json
import os
from models import RegistroGastos

class Storage:
    """Maneja el guardado y carga de datos en JSON"""
    
    def __init__(self, archivo: str = "gastos.json"):
        self.archivo = archivo
    
    def guardar(self, registro: RegistroGastos) -> bool:
        """Guarda el registro de gastos en archivo JSON"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(registro.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def cargar(self) -> RegistroGastos:
        """Carga el registro de gastos desde archivo JSON"""
        registro = RegistroGastos()
        
        if not os.path.exists(self.archivo):
            return registro
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                registro.from_dict(data)
        except Exception as e:
            print(f"Error al cargar: {e}")
        
        return registro