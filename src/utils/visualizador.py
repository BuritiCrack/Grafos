# -*- coding: utf-8 -*-
# visualizador.py
"""
Componente para manejo de visualizaci�n de grafos
Implementa Strategy Pattern para diferentes tipos de layouts
"""
import networkx as nx
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class LayoutStrategy(ABC):
    """Estrategia abstracta para layouts de grafos"""
    
    @abstractmethod
    def calcular_posiciones(self, grafo: nx.Graph) -> Dict[int, Tuple[float, float]]:
        """Calcular posiciones de los nodos"""
        pass
    
    @abstractmethod
    def get_parametros_visualizacion(self, num_nodos: int) -> Dict[str, Any]:
        """Obtener par�metros de visualizaci�n seg�n el tama�o"""
        pass

class ShellLayout(LayoutStrategy):
    """Layout Shell - organiza nodos por grado de conectividad"""
    
    def calcular_posiciones(self, grafo: nx.Graph) -> Dict[int, Tuple[float, float]]:
        # Agrupar nodos por grado de conectividad
        nodes_by_degree = {}
        for node in grafo.nodes():
            degree = grafo.degree(node)
            if degree not in nodes_by_degree:
                nodes_by_degree[degree] = []
            nodes_by_degree[degree].append(node)
        
        # Crear shells ordenados por grado (m�s conectados en el centro)
        shells = [nodes_by_degree[degree] 
                 for degree in sorted(nodes_by_degree.keys(), reverse=True)]
        
        if len(shells) > 1:
            pos = nx.shell_layout(grafo, nlist=shells)
        else:
            pos = nx.circular_layout(grafo)
        
        # Aplicar escalado si hay muchos nodos
        num_nodos = grafo.number_of_nodes()
        if num_nodos > 30:
            scale_factor = min(2.0, num_nodos * 0.02)
            for node in pos:
                pos[node] = (pos[node][0] * scale_factor, pos[node][1] * scale_factor)
        
        return pos
    
    def get_parametros_visualizacion(self, num_nodos: int) -> Dict[str, Any]:
        if num_nodos > 50:
            return {
                'node_size': max(200, 800 - num_nodos * 5),
                'font_size': max(6, 10 - num_nodos * 0.03),
                'edge_width_factor': 0.1
            }
        elif num_nodos > 20:
            return {
                'node_size': 600,
                'font_size': 7,
                'edge_width_factor': 0.15
            }
        else:
            return {
                'node_size': 1000,
                'font_size': 8,
                'edge_width_factor': 0.2
            }

class EgoNetworkLayout(LayoutStrategy):
    """Layout especializado para ego networks"""
    
    def __init__(self, ego_node_id: int):
        self.ego_node_id = ego_node_id
    
    def calcular_posiciones(self, grafo: nx.Graph) -> Dict[int, Tuple[float, float]]:
        num_nodos = grafo.number_of_nodes()
        
        if num_nodos == 2:
            # Solo ego y un vecino
            neighbor_id = list(grafo.neighbors(self.ego_node_id))[0]
            return {
                self.ego_node_id: (-0.8, 0),
                neighbor_id: (0.8, 0)
            }
        elif num_nodos <= 8:
            # Layout circular con ego en el centro
            neighbors = list(grafo.neighbors(self.ego_node_id))
            pos = {self.ego_node_id: (0, 0)}
            
            angle_step = 2 * np.pi / len(neighbors)
            radius = 1.2
            
            for i, neighbor in enumerate(neighbors):
                angle = i * angle_step
                pos[neighbor] = (radius * np.cos(angle), radius * np.sin(angle))
            
            return pos
        else:
            # Spring layout para redes m�s grandes
            return nx.spring_layout(grafo, k=1.5, iterations=100, seed=42)
    
    def get_parametros_visualizacion(self, num_nodos: int) -> Dict[str, Any]:
        return {
            'node_size': 1200,
            'font_size': 11,
            'edge_width': 3,
            'ego_node_size': 1800
        }

class VisualizadorGrafo:
    """Componente principal para visualizaci�n de grafos"""
    
    def __init__(self):
        self.layout_strategy = ShellLayout()
    
    def cambiar_layout(self, strategy: LayoutStrategy):
        """Cambiar estrategia de layout"""
        self.layout_strategy = strategy
    
    def generar_colores_nodos(self, grafo: nx.Graph) -> list:
        """Generar colores para nodos seg�n grado de conectividad"""
        colores = []
        for node in grafo.nodes():
            degree = grafo.degree(node)
            if degree > 8:
                colores.append('#ff6b6b')  # Rojo - muy conectado
            elif degree > 4:
                colores.append('#4ecdc4')  # Verde-azul - bien conectado
            elif degree > 0:
                colores.append('#45b7d1')  # Azul - pocas conexiones
            else:
                colores.append('#f9ca24')  # Amarillo - aislado
        return colores
    
    def generar_anchos_aristas(self, grafo: nx.Graph, factor: float = 0.2) -> list:
        """Generar anchos variables para aristas"""
        anchos = []
        for edge in grafo.edges():
            degree_avg = (grafo.degree(edge[0]) + grafo.degree(edge[1])) / 2
            width = max(0.5, min(2.0, degree_avg * factor))
            anchos.append(width)
        return anchos
    
    def crear_etiquetas(self, grafo: nx.Graph, usuarios_data: dict) -> dict:
        """Crear etiquetas optimizadas para los nodos"""
        etiquetas = {}
        for node in grafo.nodes():
            nombre = usuarios_data.get(node, {}).get('label', f'Usuario {node}')
            if len(nombre) > 12:
                nombre = nombre[:10] + "..."
            etiquetas[node] = f"{nombre}\n({node})"
        return etiquetas
    
    def renderizar_grafo(self, grafo: nx.Graph, ax, usuarios_data: dict = None,
                        titulo: str = "Red Social") -> None:
        """Renderizar el grafo completo en el axis proporcionado"""
        if usuarios_data is None:
            usuarios_data = {}
        
        ax.clear()
        
        if not grafo.nodes:
            ax.text(0.5, 0.5, 'No hay datos en la red\n\nAgrega usuarios para comenzar',
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=14, color='gray',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.3))
            return
        
        # Calcular posiciones y par�metros
        pos = self.layout_strategy.calcular_posiciones(grafo)
        params = self.layout_strategy.get_parametros_visualizacion(grafo.number_of_nodes())
        
        # Dibujar nodos
        colores_nodos = self.generar_colores_nodos(grafo)
        nx.draw_networkx_nodes(grafo, pos, ax=ax,
                              node_color=colores_nodos,
                              node_size=params['node_size'],
                              alpha=0.8, edgecolors='black', linewidths=0.5)
        
        # Dibujar aristas
        anchos_aristas = self.generar_anchos_aristas(grafo, params.get('edge_width_factor', 0.2))
        nx.draw_networkx_edges(grafo, pos, ax=ax,
                              edge_color='#666666', width=anchos_aristas, alpha=0.6)
        
        # Dibujar etiquetas
        etiquetas = self.crear_etiquetas(grafo, usuarios_data)
        label_pos = {node: (x, y - 0.05) for node, (x, y) in pos.items()}
        nx.draw_networkx_labels(grafo, label_pos, etiquetas, ax=ax,
                               font_size=params['font_size'], font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", facecolor='white',
                                       edgecolor='none', alpha=0.8))
        
        # Configurar axis
        ax.set_title(f"{titulo} - {grafo.number_of_nodes()} Personas, "
                    f"{grafo.number_of_edges()} Conexiones",
                    fontsize=14, fontweight='bold', pad=10)
        ax.axis('off')
        ax.margins(0.1)
    
    def renderizar_ego_network(self, grafo: nx.Graph, ego_node_id: int, ax,
                              usuarios_data: dict = None) -> None:
        """Renderizar ego network especifico"""
        if usuarios_data is None:
            usuarios_data = {}
        
        # Cambiar temporalmente a layout de ego network
        layout_anterior = self.layout_strategy
        self.cambiar_layout(EgoNetworkLayout(ego_node_id))
        
        try:
            ego_graph = nx.ego_graph(grafo, ego_node_id, radius=1)
            
            if not ego_graph.nodes:
                ax.clear()
                ax.text(0.5, 0.5, 'No hay datos para la red personal',
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=14, color='gray')
                return
            
            ax.clear()
            pos = self.layout_strategy.calcular_posiciones(ego_graph)
            params = self.layout_strategy.get_parametros_visualizacion(ego_graph.number_of_nodes())
            
            # Colores y tama�os especiales para ego network
            colores = []
            tamanos = []
            for node in ego_graph.nodes():
                if node == ego_node_id:
                    colores.append('#e74c3c')  # Rojo para ego
                    tamanos.append(params.get('ego_node_size', 1800))
                else:
                    colores.append('#3498db')  # Azul para vecinos
                    tamanos.append(params.get('node_size', 1200))
            
            # Dibujar nodos y aristas
            nx.draw_networkx_nodes(ego_graph, pos, ax=ax,
                                  node_color=colores, node_size=tamanos,
                                  alpha=0.9, edgecolors='black', linewidths=2)
            
            nx.draw_networkx_edges(ego_graph, pos, ax=ax,
                                  edge_color='#2c3e50', width=params.get('edge_width', 3),
                                  alpha=0.8)
            
            # Etiquetas especiales para ego network
            etiquetas = {}
            for node in ego_graph.nodes():
                nombre = usuarios_data.get(node, {}).get('label', f'Usuario {node}')
                if len(nombre) > 15:
                    nombre = nombre[:12] + "..."
                
                if node == ego_node_id:
                    etiquetas[node] = f"? {nombre}\n(ID: {node})"
                else:
                    etiquetas[node] = f"{nombre}\n(ID: {node})"
            
            # Posicionamiento optimizado de etiquetas
            label_pos = {}
            for node, (x, y) in pos.items():
                if node == ego_node_id:
                    label_pos[node] = (x, y - 0.2)
                else:
                    distance = np.sqrt(x*x + y*y)
                    if distance > 0:
                        factor = 1.3
                        label_pos[node] = (x * factor, y * factor)
                    else:
                        label_pos[node] = (x, y - 0.2)
            
            nx.draw_networkx_labels(ego_graph, label_pos, etiquetas, ax=ax,
                                   font_size=params['font_size'], font_weight='bold',
                                   bbox=dict(boxstyle="round,pad=0.4", facecolor='white',
                                           edgecolor='darkgray', alpha=0.95, linewidth=1))
            
            # Titulo
            user_name = usuarios_data.get(ego_node_id, {}).get('label', f'Usuario {ego_node_id}')
            num_conexiones = len(list(ego_graph.neighbors(ego_node_id)))
            ax.set_title(f"Red Personal de: {user_name} (ID: {ego_node_id})\n"
                        f"{num_conexiones} Conexiones Directas",
                        fontsize=14, fontweight='bold', pad=10)
            ax.axis('off')
            ax.margins(0.2)  # Ajuste de margenes para mejor visualizacion
            
        finally:
            # Restaurar layout anterior
            self.cambiar_layout(layout_anterior)
