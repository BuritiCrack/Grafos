# -*- coding: utf-8 -*-
# recomendador.py
"""
Sistema de recomendaciones - Implementa Strategy Pattern
"""
from typing import List, Dict
from abc import ABC, abstractmethod
from models.usuario import Usuario

class EstrategiaRecomendacion(ABC):
    """Interfaz para estrategias de recomendacion"""
    
    @abstractmethod
    def calcular_score(self, usuario_origen: Usuario, usuario_candidato: Usuario) -> float:
        """Calcular puntuacion de compatibilidad entre usuarios"""
        pass

class RecomendacionPorIntereses(EstrategiaRecomendacion):
    """Estrategia de recomendacion basada en intereses comunes"""
    
    def calcular_score(self, usuario_origen: Usuario, usuario_candidato: Usuario) -> float:
        """Calcular score basado en intereses comunes y otros factores"""
        # Score base por intereses comunes
        intereses_comunes = usuario_origen.intereses_comunes(usuario_candidato)
        score = len(intereses_comunes)
        
        # Bonus por diversidad de intereses del candidato
        if len(usuario_candidato.intereses) > 2:
            score += 0.5
        
        # Bonus por edad similar (+/- 5 anos)
        if (usuario_origen.edad > 0 and usuario_candidato.edad > 0 and
            abs(usuario_origen.edad - usuario_candidato.edad) <= 5):
            score += 0.3
        
        return score

class RecomendadorConexiones:
    """Recomendador principal que utiliza diferentes estrategias"""
    
    def __init__(self, estrategia: EstrategiaRecomendacion = None):
        self.estrategia = estrategia or RecomendacionPorIntereses()
    
    def cambiar_estrategia(self, estrategia: EstrategiaRecomendacion):
        """Cambiar estrategia de recomendacion"""
        self.estrategia = estrategia
    
    def generar_recomendaciones(self, usuario_origen: Usuario, 
                              candidatos: List[Usuario], 
                              limite: int = 10) -> List[Dict]:
        """Generar recomendaciones ordenadas por relevancia"""
        recomendaciones = []
        
        for candidato in candidatos:
            # Solo recomendar si hay intereses comunes
            intereses_comunes = usuario_origen.intereses_comunes(candidato)
            if not intereses_comunes:
                continue
            
            score = self.estrategia.calcular_score(usuario_origen, candidato)
            compatibilidad = min(100, int(score * 25))  # Convertir a porcentaje
            
            recomendacion = {
                'id': candidato.id,
                'nombre': candidato.nombre,
                'edad': candidato.edad,
                'email': candidato.email,
                'intereses': candidato.intereses,
                'intereses_comunes': intereses_comunes,
                'score': score,
                'compatibilidad': compatibilidad
            }
            recomendaciones.append(recomendacion)
        
        # Ordenar por score descendente
        recomendaciones.sort(key=lambda x: x['score'], reverse=True)
        
        return recomendaciones[:limite]
    
    def obtener_estadisticas_recomendaciones(self, usuario_origen: Usuario,
                                           candidatos: List[Usuario]) -> Dict:
        """Obtener estadisticas sobre las recomendaciones disponibles"""
        total_candidatos = len(candidatos)
        candidatos_con_intereses = sum(
            1 for c in candidatos 
            if usuario_origen.intereses_comunes(c)
        )
        
        return {
            'total_usuarios': total_candidatos,
            'usuarios_con_intereses_comunes': candidatos_con_intereses,
            'porcentaje_compatibles': (candidatos_con_intereses / total_candidatos * 100) 
                                    if total_candidatos > 0 else 0
        }
