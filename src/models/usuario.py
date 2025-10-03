# -*- coding: utf-8 -*-
# usuario.py
"""
Modelo para representar un usuario en la red social
"""
from dataclasses import dataclass
from typing import List, Set

@dataclass
class Usuario:
    """Modelo de datos para un usuario"""
    id: int
    nombre: str
    edad: int = 0
    email: str = ""
    intereses: List[str] = None
    amigos: List[int] = None
    
    def __post_init__(self):
        if self.intereses is None:
            self.intereses = []
        if self.amigos is None:
            self.amigos = []
        # Normalizar intereses a minusculas
        self.intereses = [interes.lower() for interes in self.intereses]
    
    @property
    def intereses_set(self) -> Set[str]:
        """Retorna intereses como conjunto para operaciones de interseccion"""
        return set(self.intereses)
    
    def agregar_amigo(self, usuario_id: int):
        """Agregar un amigo evitando duplicados"""
        if usuario_id not in self.amigos:
            self.amigos.append(usuario_id)
    
    def remover_amigo(self, usuario_id: int):
        """Remover un amigo"""
        if usuario_id in self.amigos:
            self.amigos.remove(usuario_id)
    
    def tiene_interes_comun(self, otro_usuario: 'Usuario') -> bool:
        """Verificar si tiene intereses comunes con otro usuario"""
        return bool(self.intereses_set.intersection(otro_usuario.intereses_set))
    
    def intereses_comunes(self, otro_usuario: 'Usuario') -> Set[str]:
        """Obtener intereses comunes con otro usuario"""
        return self.intereses_set.intersection(otro_usuario.intereses_set)
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para serializacion"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "email": self.email,
            "intereses": self.intereses,
            "amigos": self.amigos
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Usuario':
        """Crear usuario desde diccionario"""
        return cls(
            id=data.get("id", 0),
            nombre=data.get("nombre", ""),
            edad=data.get("edad", 0),
            email=data.get("email", ""),
            intereses=data.get("intereses", []),
            amigos=data.get("amigos", [])
        )
