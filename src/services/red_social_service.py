# -*- coding: utf-8 -*-
# red_social_service.py
"""
Servicio principal para manejar la l�gica de negocio de la red social
Implementa el patr�n Service Layer
"""
import networkx as nx
from typing import List, Dict, Tuple, Optional, Set
from models.usuario import Usuario
from services.data_manager import DataManager
from services.recomendador import RecomendadorConexiones
from services.analizador_red import AnalizadorRed

class RedSocialService:
    """Servicio principal que maneja toda la l�gica de negocio"""
    
    def __init__(self):
        self.grafo = nx.Graph()
        self.usuarios: Dict[int, Usuario] = {}
        self.data_manager = DataManager()
        self.recomendador = RecomendadorConexiones()
        self.analizador = AnalizadorRed()
        self._siguiente_id = 1
    
    def cargar_datos(self) -> None:
        """Cargar datos desde archivos"""
        usuarios_data, conexiones_data = self.data_manager.cargar_datos()
        
        # Cargar usuarios
        for user_data in usuarios_data:
            usuario = Usuario.from_dict(user_data)
            self.usuarios[usuario.id] = usuario
            self.grafo.add_node(usuario.id, **usuario.to_dict())
            self._siguiente_id = max(self._siguiente_id, usuario.id + 1)
        
        # Cargar conexiones
        for conexion in conexiones_data:
            if conexion['origen'] in self.usuarios and conexion['destino'] in self.usuarios:
                self.crear_conexion(conexion['origen'], conexion['destino'])
    
    def guardar_datos(self) -> bool:
        """Guardar datos a archivos"""
        usuarios_data = [usuario.to_dict() for usuario in self.usuarios.values()]
        conexiones_data = [
            {"origen": origen, "destino": destino}
            for origen, destino in self.grafo.edges()
        ]
        return self.data_manager.guardar_datos(usuarios_data, conexiones_data)
    
    def agregar_usuario(self, nombre: str, edad: int = 0, email: str = "", 
                       intereses: List[str] = None) -> Tuple[Usuario, int]:
        """
        Agregar un nuevo usuario al sistema
        Retorna: (usuario_creado, cantidad_conexiones_automaticas)
        """
        if intereses is None:
            intereses = []
        
        # Crear usuario
        usuario = Usuario(
            id=self._siguiente_id,
            nombre=nombre,
            edad=edad,
            email=email,
            intereses=intereses
        )
        
        # Agregar al sistema
        self.usuarios[usuario.id] = usuario
        self.grafo.add_node(usuario.id, **usuario.to_dict())
        self._siguiente_id += 1
        
        # Crear conexiones autom�ticas
        conexiones_creadas = self._crear_conexiones_automaticas(usuario.id)
        
        return usuario, conexiones_creadas
    
    def crear_conexion(self, usuario1_id: int, usuario2_id: int) -> bool:
        """Crear conexi�n entre dos usuarios"""
        if (usuario1_id not in self.usuarios or 
            usuario2_id not in self.usuarios or
            usuario1_id == usuario2_id or
            self.grafo.has_edge(usuario1_id, usuario2_id)):
            return False
        
        # Crear conexi�n en el grafo
        self.grafo.add_edge(usuario1_id, usuario2_id)
        
        # Actualizar listas de amigos
        self.usuarios[usuario1_id].agregar_amigo(usuario2_id)
        self.usuarios[usuario2_id].agregar_amigo(usuario1_id)
        
        # Actualizar atributos del grafo
        self.grafo.nodes[usuario1_id]['amigos'] = self.usuarios[usuario1_id].amigos
        self.grafo.nodes[usuario2_id]['amigos'] = self.usuarios[usuario2_id].amigos
        
        return True
    
    def obtener_usuario(self, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return self.usuarios.get(usuario_id)
    
    def buscar_usuarios_por_nombre(self, nombre: str) -> List[Usuario]:
        """Buscar usuarios por nombre (b�squeda parcial)"""
        nombre_lower = nombre.lower()
        return [
            usuario for usuario in self.usuarios.values()
            if nombre_lower in usuario.nombre.lower()
        ]
    
    def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtener lista de todos los usuarios"""
        return list(self.usuarios.values())
    
    def obtener_conexiones(self) -> List[Tuple[Usuario, Usuario, Set[str]]]:
        """Obtener todas las conexiones con intereses comunes"""
        conexiones = []
        for origen_id, destino_id in self.grafo.edges():
            usuario1 = self.usuarios[origen_id]
            usuario2 = self.usuarios[destino_id]
            intereses_comunes = usuario1.intereses_comunes(usuario2)
            conexiones.append((usuario1, usuario2, intereses_comunes))
        return conexiones
    
    def obtener_red_personal(self, usuario_id: int) -> Optional[nx.Graph]:
        """Obtener ego network de un usuario"""
        if usuario_id not in self.usuarios:
            return None
        return nx.ego_graph(self.grafo, usuario_id, radius=1)
    
    def obtener_recomendaciones(self, usuario_id: int) -> List[Dict]:
        """Obtener recomendaciones de conexiones para un usuario"""
        if usuario_id not in self.usuarios:
            return []
        
        usuario = self.usuarios[usuario_id]
        candidatos = [
            u for u in self.usuarios.values() 
            if u.id != usuario_id and u.id not in usuario.amigos
        ]
        
        return self.recomendador.generar_recomendaciones(usuario, candidatos)
    
    def obtener_estadisticas(self) -> Dict:
        """Obtener estad�sticas generales de la red"""
        return self.analizador.calcular_estadisticas_generales(self.grafo)
    
    def calcular_centralidad(self) -> Dict:
        """Calcular m�tricas de centralidad"""
        return self.analizador.calcular_centralidad(self.grafo, self.usuarios)
    
    def detectar_comunidades(self) -> List[List[Usuario]]:
        """Detectar comunidades en la red"""
        return self.analizador.detectar_comunidades(self.grafo, self.usuarios)
    
    def _crear_conexiones_automaticas(self, usuario_id: int) -> int:
        """Crear conexiones autom�ticas basadas en intereses comunes"""
        usuario = self.usuarios[usuario_id]
        conexiones_creadas = 0
        
        for otro_usuario in self.usuarios.values():
            if (otro_usuario.id != usuario_id and 
                not self.grafo.has_edge(usuario_id, otro_usuario.id) and
                usuario.tiene_interes_comun(otro_usuario)):
                
                self.crear_conexion(usuario_id, otro_usuario.id)
                conexiones_creadas += 1
        
        return conexiones_creadas
