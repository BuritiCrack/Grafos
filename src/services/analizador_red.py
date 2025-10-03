# -*- coding: utf-8 -*-
# analizador_red.py
"""
Analizador de m�tricas y propiedades de la red social
"""
import networkx as nx
from typing import Dict, List
from models.usuario import Usuario

class AnalizadorRed:
    """Analiza m�tricas y propiedades de la red social"""
    
    def calcular_estadisticas_generales(self, grafo: nx.Graph) -> Dict:
        """Calcular estad�sticas generales de la red"""
        num_nodos = grafo.number_of_nodes()
        num_aristas = grafo.number_of_edges()
        
        if num_nodos == 0:
            return {
                'num_personas': 0,
                'num_conexiones': 0,
                'densidad': 0,
                'grado_promedio': 0,
                'componentes_conectados': 0,
                'es_conectado': False
            }
        
        densidad = nx.density(grafo)
        grado_promedio = sum(dict(grafo.degree()).values()) / num_nodos
        componentes = nx.number_connected_components(grafo)
        es_conectado = nx.is_connected(grafo)
        
        return {
            'num_personas': num_nodos,
            'num_conexiones': num_aristas,
            'densidad': densidad,
            'grado_promedio': grado_promedio,
            'componentes_conectados': componentes,
            'es_conectado': es_conectado
        }
    
    def calcular_centralidad(self, grafo: nx.Graph, usuarios: Dict[int, Usuario]) -> Dict:
        """Calcular m�tricas de centralidad"""
        if not grafo.nodes:
            return {'grado': [], 'cercania': []}
        
        # Centralidad de grado
        centralidad_grado = nx.degree_centrality(grafo)
        top_grado = sorted(centralidad_grado.items(), 
                          key=lambda x: x[1], reverse=True)[:5]
        
        grado_resultado = [
            {
                'usuario': usuarios[node_id].nombre,
                'id': node_id,
                'centralidad': centralidad
            }
            for node_id, centralidad in top_grado
        ]
        
        # Centralidad de cercan�a (solo si el grafo est� conectado)
        cercania_resultado = []
        if nx.is_connected(grafo):
            centralidad_cercania = nx.closeness_centrality(grafo)
            top_cercania = sorted(centralidad_cercania.items(), 
                                key=lambda x: x[1], reverse=True)[:5]
            
            cercania_resultado = [
                {
                    'usuario': usuarios[node_id].nombre,
                    'id': node_id,
                    'centralidad': centralidad
                }
                for node_id, centralidad in top_cercania
            ]
        
        return {
            'grado': grado_resultado,
            'cercania': cercania_resultado
        }
    
    def detectar_comunidades(self, grafo: nx.Graph, 
                           usuarios: Dict[int, Usuario]) -> List[List[Usuario]]:
        """Detectar comunidades en la red"""
        if not grafo.nodes:
            return []
        
        try:
            import networkx.algorithms.community as nx_comm
            comunidades = list(nx_comm.greedy_modularity_communities(grafo))
            
            resultado = []
            for comunidad in comunidades:
                usuarios_comunidad = [usuarios[node_id] for node_id in comunidad]
                resultado.append(usuarios_comunidad)
            
            return resultado
            
        except Exception:
            # Fallback: usar componentes conectados
            componentes = list(nx.connected_components(grafo))
            resultado = []
            
            for componente in componentes:
                usuarios_componente = [usuarios[node_id] for node_id in componente]
                resultado.append(usuarios_componente)
            
            return resultado
    
    def analizar_usuario(self, grafo: nx.Graph, usuario_id: int, 
                        usuarios: Dict[int, Usuario]) -> Dict:
        """An�lisis detallado de un usuario espec�fico"""
        if usuario_id not in grafo.nodes:
            return {}
        
        usuario = usuarios[usuario_id]
        grado = grafo.degree(usuario_id)
        vecinos = list(grafo.neighbors(usuario_id))
        
        # An�lisis de conexiones por intereses
        conexiones_por_interes = {}
        for vecino_id in vecinos:
            vecino = usuarios[vecino_id]
            intereses_comunes = usuario.intereses_comunes(vecino)
            for interes in intereses_comunes:
                if interes not in conexiones_por_interes:
                    conexiones_por_interes[interes] = 0
                conexiones_por_interes[interes] += 1
        
        return {
            'usuario': usuario,
            'grado': grado,
            'num_conexiones': len(vecinos),
            'conexiones_por_interes': conexiones_por_interes,
            'centralidad_local': grado / (grafo.number_of_nodes() - 1) if grafo.number_of_nodes() > 1 else 0
        }
