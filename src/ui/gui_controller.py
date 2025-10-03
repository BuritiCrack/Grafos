# -*- coding: utf-8 -*-
# gui_controller.py
"""
Controlador principal que conecta la l�gica de negocio con la interfaz
Implementa el patr�n MVC (Model-View-Controller)
"""
from typing import Optional, List
import tkinter as tk
from tkinter import messagebox
from services.red_social_service import RedSocialService
from models.usuario import Usuario
from utils.visualizador import VisualizadorGrafo, ShellLayout

class GUIController:
    """Controlador principal de la aplicaci�n"""
    
    def __init__(self):
        self.service = RedSocialService()
        self.visualizador = VisualizadorGrafo()
        self.view = None  # Se asignar� cuando se cree la vista
        
        # Estado de la aplicaci�n
        self.ego_mode = False
        self.ego_user_id = None
    
    def inicializar(self):
        """Inicializar el controlador"""
        self.service.cargar_datos()
    
    def set_view(self, view):
        """Asignar la vista al controlador"""
        self.view = view
    
    # === GESTI�N DE USUARIOS ===
    
    def agregar_usuario(self, nombre: str, edad_str: str, email: str, intereses_str: str) -> bool:
        """Agregar un nuevo usuario"""
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return False
        
        try:
            edad = int(edad_str) if edad_str.strip() else 0
        except ValueError:
            edad = 0
        
        intereses = [i.strip() for i in intereses_str.split(',') if i.strip()] if intereses_str else []
        
        usuario, conexiones_creadas = self.service.agregar_usuario(
            nombre=nombre.strip(),
            edad=edad,
            email=email.strip(),
            intereses=intereses
        )
        
        # Mensaje de �xito
        mensaje = f"Persona '{usuario.nombre}' agregada con ID {usuario.id}"
        if conexiones_creadas > 0:
            mensaje += f"\n{conexiones_creadas} conexiones autom�ticas creadas"
        
        messagebox.showinfo("�xito", mensaje)
        
        # Notificar a la vista para actualizar
        if self.view:
            self.view.actualizar_tras_cambio()
        
        return True
    
    def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtener lista de todos los usuarios"""
        return self.service.obtener_todos_usuarios()
    
    def buscar_usuarios_por_nombre(self, nombre: str) -> List[Usuario]:
        """Buscar usuarios por nombre"""
        if not nombre.strip():
            messagebox.showerror("Error", "Por favor, ingresa un nombre para buscar")
            return []
        
        usuarios_encontrados = self.service.buscar_usuarios_por_nombre(nombre.strip())
        
        if not usuarios_encontrados:
            messagebox.showinfo("Sin resultados", 
                               f"No se encontraron usuarios con el nombre '{nombre}'")
            return []
        
        return usuarios_encontrados
    
    # === GESTI�N DE CONEXIONES ===
    
    def crear_conexion_manual(self, id1_str: str, id2_str: str) -> bool:
        """Crear conexi�n manual entre dos usuarios"""
        try:
            id1 = int(id1_str)
            id2 = int(id2_str)
        except ValueError:
            messagebox.showerror("Error", "Los IDs deben ser n�meros v�lidos")
            return False
        
        # Validaciones
        if id1 == id2:
            messagebox.showerror("Error", "No puedes conectar una persona consigo misma")
            return False
        
        usuario1 = self.service.obtener_usuario(id1)
        usuario2 = self.service.obtener_usuario(id2)
        
        if not usuario1 or not usuario2:
            messagebox.showerror("Error", "Una o ambas personas no existen")
            return False
        
        if id2 in usuario1.amigos:
            messagebox.showwarning("Advertencia", "Estas personas ya est�n conectadas")
            return False
        
        # Crear conexi�n
        if self.service.crear_conexion(id1, id2):
            messagebox.showinfo("�xito", f"Conexi�n creada entre {usuario1.nombre} y {usuario2.nombre}")
            
            # Actualizar vista
            if self.view:
                self.view.actualizar_tras_cambio()
            return True
        
        return False
    
    def obtener_conexiones(self):
        """Obtener todas las conexiones"""
        return self.service.obtener_conexiones()
    
    # === RECOMENDACIONES ===
    
    def mostrar_ego_network(self, usuario_id_str: str) -> bool:
        """Mostrar red personal de un usuario"""
        if not usuario_id_str.strip():
            messagebox.showerror("Error", "Por favor, ingresa un ID de usuario")
            return False
        
        try:
            usuario_id = int(usuario_id_str)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un n�mero v�lido")
            return False
        
        if not self.service.obtener_usuario(usuario_id):
            messagebox.showerror("Error", f"No existe un usuario con ID {usuario_id}")
            return False
        
        # Cambiar a modo ego network
        self.ego_mode = True
        self.ego_user_id = usuario_id
        
        # Actualizar vista
        if self.view:
            self.view.actualizar_visualizacion()
            self.view.mostrar_recomendaciones(usuario_id)
            self.view.cambiar_a_pestana_informacion()
        
        return True
    
    def buscar_y_mostrar_usuario(self, nombre: str) -> bool:
        """Buscar usuario por nombre y mostrar su red"""
        usuarios = self.buscar_usuarios_por_nombre(nombre)
        
        if len(usuarios) == 1:
            return self.mostrar_ego_network(str(usuarios[0].id))
        elif len(usuarios) > 1:
            opciones = "\n".join([f"ID {u.id}: {u.nombre}" for u in usuarios])
            messagebox.showinfo("M�ltiples resultados", 
                               f"Se encontraron varios usuarios:\n\n{opciones}\n\n"
                               f"Ingresa el ID espec�fico del usuario que deseas ver.")
        
        return False
    
    def obtener_recomendaciones(self, usuario_id: int):
        """Obtener recomendaciones para un usuario"""
        return self.service.obtener_recomendaciones(usuario_id)
    
    def crear_conexion_recomendada(self, usuario_origen_id: int, usuario_destino_str: str) -> bool:
        """Crear conexi�n con usuario recomendado"""
        try:
            usuario_destino_id = int(usuario_destino_str.strip())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un ID v�lido")
            return False
        
        return self.crear_conexion_manual(str(usuario_origen_id), str(usuario_destino_id))
    
    def mostrar_red_completa(self):
        """Volver a mostrar la red completa"""
        self.ego_mode = False
        self.ego_user_id = None
        
        if self.view:
            self.view.limpiar_campos_ego()
            self.view.actualizar_visualizacion()
        
        messagebox.showinfo("Red Completa", "Ahora se muestra la red social completa")
    
    # === AN�LISIS ===
    
    def obtener_estadisticas(self):
        """Obtener estad�sticas de la red"""
        return self.service.obtener_estadisticas()
    
    def calcular_centralidad(self):
        """Calcular m�tricas de centralidad"""
        if not self.service.obtener_todos_usuarios():
            messagebox.showwarning("Advertencia", "No hay datos para analizar")
            return None
        
        return self.service.calcular_centralidad()
    
    def detectar_comunidades(self):
        """Detectar comunidades en la red"""
        if not self.service.obtener_todos_usuarios():
            messagebox.showwarning("Advertencia", "No hay datos para analizar")
            return None
        
        return self.service.detectar_comunidades()
    
    # === PERSISTENCIA ===
    
    def guardar_datos(self) -> bool:
        """Guardar datos"""
        if self.service.guardar_datos():
            usuarios = self.service.obtener_todos_usuarios()
            conexiones = self.service.obtener_conexiones()
            
            messagebox.showinfo("�xito", 
                               f"Datos guardados exitosamente:\n"
                               f"� {len(usuarios)} usuarios\n"
                               f"� {len(conexiones)} conexiones")
            return True
        else:
            messagebox.showerror("Error", "Error al guardar los datos")
            return False
    
    def recargar_datos(self) -> bool:
        """Recargar datos desde archivos"""
        # Limpiar estado
        self.ego_mode = False
        self.ego_user_id = None
        
        # Recargar
        self.service = RedSocialService()
        self.service.cargar_datos()
        
        # Actualizar vista
        if self.view:
            self.view.actualizar_tras_recarga()
        
        messagebox.showinfo("�xito", "Datos recargados correctamente")
        return True
    
    # === VISUALIZACI�N ===
    
    def renderizar_grafo(self, ax, usuarios_data=None):
        """Renderizar el grafo en el axis dado"""
        if self.ego_mode and self.ego_user_id:
            # Renderizar ego network
            self.visualizador.renderizar_ego_network(
                self.service.grafo, self.ego_user_id, ax, usuarios_data
            )
        else:
            # Renderizar grafo completo
            self.visualizador.renderizar_grafo(
                self.service.grafo, ax, usuarios_data, "Red Social"
            )
    
    def esta_en_modo_ego(self) -> bool:
        """Verificar si est� en modo ego network"""
        return self.ego_mode and self.ego_user_id is not None
    
    def obtener_usuario_ego(self) -> Optional[Usuario]:
        """Obtener usuario del ego network actual"""
        if self.ego_user_id:
            return self.service.obtener_usuario(self.ego_user_id)
        return None
