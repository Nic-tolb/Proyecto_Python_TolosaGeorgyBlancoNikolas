"""
models.py - Modelos de datos para el simulador de gastos
Define las estructuras de datos principales
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

@dataclass
class Gasto:
    """Representa un gasto individual"""
    categoria: str
    monto: float
    descripcion: str
    fecha: str
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict):
        return Gasto(**data)

class RegistroGastos:
    """Maneja la colección de gastos"""
    CATEGORIAS_BASE = ["comida", "transporte", "entretenimiento", "salud", "servicios", "otros"]
    
    def __init__(self):
        self.gastos: List[Gasto] = []
        self.categorias_personalizadas: List[str] = []
    
    def obtener_categorias(self) -> List[str]:
        """Retorna todas las categorías (base + personalizadas)"""
        return self.CATEGORIAS_BASE + self.categorias_personalizadas
    
    def agregar_categoria(self, categoria: str) -> bool:
        """Agrega una nueva categoría personalizada"""
        categoria = categoria.lower().strip()
        if not categoria or categoria in self.obtener_categorias():
            return False
        self.categorias_personalizadas.append(categoria)
        return True
    
    def agregar_gasto(self, categoria: str, monto: float, descripcion: str = "") -> bool:
        if monto <= 0:
            return False
        
        categoria = categoria.lower().strip()
        if categoria not in self.obtener_categorias():
            return False
        
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gasto = Gasto(categoria, monto, descripcion, fecha)
        self.gastos.append(gasto)
        return True
    
    def obtener_gastos(self) -> List[Gasto]:
        return self.gastos
    
    def to_dict(self) -> dict:
        return {
            "gastos": [g.to_dict() for g in self.gastos],
            "categorias_personalizadas": self.categorias_personalizadas
        }
    
    def from_dict(self, data: dict):
        self.gastos = [Gasto.from_dict(g) for g in data.get("gastos", [])]
        self.categorias_personalizadas = data.get("categorias_personalizadas", [])