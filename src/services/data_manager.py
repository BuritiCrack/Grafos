# -*- coding: utf-8 -*-
# data_manager.py
"""
Manejo de persistencia de datos - Implementa Repository Pattern
"""
import json
import os
from typing import List, Dict, Tuple

class DataManager:
    """Maneja la persistencia de datos en archivos JSON"""
    
    def __init__(self, directorio: str = None):
        # Get the project root directory (3 levels up from services folder)
        if directorio is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            self.directorio = os.path.join(project_root, 'data')
        else:
            self.directorio = directorio
        self.archivo_usuarios = os.path.join(self.directorio, 'usuarios.json')
        self.archivo_conexiones = os.path.join(self.directorio, 'conexiones.json')
    
    def cargar_datos(self) -> Tuple[List[Dict], List[Dict]]:
        """Cargar usuarios y conexiones desde archivos JSON"""
        usuarios = self._cargar_usuarios()
        conexiones = self._cargar_conexiones()
        return usuarios, conexiones
    
    def guardar_datos(self, usuarios: List[Dict], conexiones: List[Dict]) -> bool:
        """Guardar usuarios y conexiones en archivos JSON"""
        try:
            self._guardar_usuarios(usuarios)
            self._guardar_conexiones(conexiones)
            return True
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False
    
    def _cargar_usuarios(self) -> List[Dict]:
        """Cargar usuarios desde archivo JSON"""
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('usuarios', [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error al leer {self.archivo_usuarios}")
            return []
    
    def _cargar_conexiones(self) -> List[Dict]:
        """Cargar conexiones desde archivo JSON"""
        try:
            with open(self.archivo_conexiones, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('conexiones', [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error al leer {self.archivo_conexiones}")
            return []
    
    def _guardar_usuarios(self, usuarios: List[Dict]) -> None:
        """Guardar usuarios en archivo JSON"""
        data = {"usuarios": usuarios}
        with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _guardar_conexiones(self, conexiones: List[Dict]) -> None:
        """Guardar conexiones en archivo JSON"""
        # Evitar duplicados
        conexiones_unicas = []
        aristas_procesadas = set()
        
        for conexion in conexiones:
            arista = tuple(sorted([conexion['origen'], conexion['destino']]))
            if arista not in aristas_procesadas:
                conexiones_unicas.append({
                    "origen": arista[0],
                    "destino": arista[1]
                })
                aristas_procesadas.add(arista)
        
        data = {"conexiones": conexiones_unicas}
        with open(self.archivo_conexiones, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
