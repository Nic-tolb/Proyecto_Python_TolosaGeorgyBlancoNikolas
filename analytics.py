"""
analytics.py - Análisis y reportes de gastos
"""
from datetime import datetime, timedelta
from collections import defaultdict
from models import RegistroGastos, Gasto
from typing import List

class Analizador:
    """Realiza análisis y cálculos sobre los gastos"""
    
    def __init__(self, registro: RegistroGastos):
        self.registro = registro
    
    def filtrar_por_categoria(self, categoria: str) -> List[Gasto]:
        """Filtra gastos por categoría"""
        return [g for g in self.registro.gastos if g.categoria == categoria.lower()]
    
    def filtrar_por_fechas(self, fecha_inicio: str, fecha_fin: str) -> List[Gasto]:
        """Filtra gastos por rango de fechas (formato: YYYY-MM-DD)"""
        gastos_filtrados = []
        for gasto in self.registro.gastos:
            fecha_gasto = datetime.strptime(gasto.fecha.split()[0], "%Y-%m-%d")
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            if inicio <= fecha_gasto <= fin:
                gastos_filtrados.append(gasto)
        
        return gastos_filtrados
    
    def calcular_total_diario(self) -> float:
        """Calcula el total de gastos del día actual"""
        hoy = datetime.now().strftime("%Y-%m-%d")
        return sum(g.monto for g in self.registro.gastos if g.fecha.startswith(hoy))
    
    def calcular_total_semanal(self) -> float:
        """Calcula el total de gastos de los últimos 7 días"""
        hace_7_dias = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        hoy = datetime.now().strftime("%Y-%m-%d")
        gastos = self.filtrar_por_fechas(hace_7_dias, hoy)
        return sum(g.monto for g in gastos)
    
    def calcular_total_mensual(self) -> float:
        """Calcula el total de gastos de los últimos 30 días"""
        hace_30_dias = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        hoy = datetime.now().strftime("%Y-%m-%d")
        gastos = self.filtrar_por_fechas(hace_30_dias, hoy)
        return sum(g.monto for g in gastos)
    
    def generar_reporte(self, periodo: str) -> dict:
        """Genera un reporte detallado por categorías para el periodo especificado"""
        if periodo == "diario":
            hoy = datetime.now().strftime("%Y-%m-%d")
            gastos = [g for g in self.registro.gastos if g.fecha.startswith(hoy)]
        elif periodo == "semanal":
            hace_7 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            hoy = datetime.now().strftime("%Y-%m-%d")
            gastos = self.filtrar_por_fechas(hace_7, hoy)
        else:  # mensual
            hace_30 = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            hoy = datetime.now().strftime("%Y-%m-%d")
            gastos = self.filtrar_por_fechas(hace_30, hoy)
        
        # Agrupar por categoría
        categorias = defaultdict(float)
        for gasto in gastos:
            categorias[gasto.categoria] += gasto.monto
        
        total = sum(categorias.values())
        
        return {
            "periodo": periodo,
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_gastos": total,
            "por_categoria": dict(categorias),
            "cantidad_transacciones": len(gastos)
        }