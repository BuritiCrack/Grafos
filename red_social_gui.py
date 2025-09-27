import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import numpy as np
from matplotlib.figure import Figure

class RedSocialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Social - Sistema de Grafos")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        # Maximizar ventana al inicio
        self.root.state('zoomed')
        
        # Inicializar el grafo
        self.grafo = nx.Graph()
        self.dir_actual = os.path.dirname(os.path.abspath(__file__))
        
        # Cargar datos iniciales
        self.cargar_datos()
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Actualizar visualización inicial
        self.actualizar_grafo()
        
    def cargar_datos(self):
        """Cargar usuarios y conexiones desde archivos JSON"""
        # Cargar usuarios
        ruta_usuarios = os.path.join(self.dir_actual, 'usuarios.json')
        try:
            with open(ruta_usuarios, 'r', encoding='utf-8') as f:
                users = json.load(f)
            for user in users['usuarios']:
                intereses_normalizados = [interes.lower() for interes in user.get('intereses', [])]
                self.grafo.add_node(user['id'], 
                              label=user['nombre'], 
                              edad=user.get('edad', 0),
                              email=user.get('email', ''),
                              intereses=intereses_normalizados,
                              amigos=[])
        except FileNotFoundError:
            pass
        
        # Cargar conexiones
        ruta_conexiones = os.path.join(self.dir_actual, 'conexiones.json')
        try:
            with open(ruta_conexiones, 'r', encoding='utf-8') as f:
                conexiones = json.load(f)
            for conn in conexiones['conexiones']:
                if conn['origen'] in self.grafo.nodes and conn['destino'] in self.grafo.nodes:
                    self.grafo.add_edge(conn['origen'], conn['destino'])
                    self.grafo.nodes[conn['origen']]['amigos'].append(conn['destino'])
                    self.grafo.nodes[conn['destino']]['amigos'].append(conn['origen'])
        except FileNotFoundError:
            pass
    
    def crear_interfaz(self):
        """Crear la interfaz gráfica principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de las columnas y filas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Panel de control (izquierda)
        self.crear_panel_control(main_frame)
        
        # Panel de visualización (derecha)
        self.crear_panel_visualizacion(main_frame)
        
        # Panel de información (abajo)
        self.crear_panel_informacion(main_frame)
    
    def crear_panel_control(self, parent):
        """Crear panel de controles"""
        control_frame = ttk.LabelFrame(parent, text="Panel de Control", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Sección: Agregar Persona
        persona_frame = ttk.LabelFrame(control_frame, text="Agregar Nueva Persona", padding="10")
        persona_frame.pack(fill="x", pady=(0, 10))
        
        # Campos de entrada
        ttk.Label(persona_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = ttk.Entry(persona_frame, width=25)
        self.nombre_entry.grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(persona_frame, text="Edad:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.edad_entry = ttk.Entry(persona_frame, width=25)
        self.edad_entry.grid(row=1, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(persona_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(persona_frame, width=25)
        self.email_entry.grid(row=2, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(persona_frame, text="Intereses:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(persona_frame, text="(separar con comas)", font=("Arial", 8)).grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        self.intereses_entry = ttk.Entry(persona_frame, width=25)
        self.intereses_entry.grid(row=4, column=0, columnspan=2, pady=2, sticky=(tk.W, tk.E))
        
        # Botón agregar persona
        btn_agregar = ttk.Button(persona_frame, text="Agregar Persona", command=self.agregar_persona)
        btn_agregar.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Sección: Conexiones Manuales
        conexion_frame = ttk.LabelFrame(control_frame, text="Agregar Conexión Manual", padding="10")
        conexion_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(conexion_frame, text="Persona 1 (ID):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.persona1_entry = ttk.Entry(conexion_frame, width=10)
        self.persona1_entry.grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(conexion_frame, text="Persona 2 (ID):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.persona2_entry = ttk.Entry(conexion_frame, width=10)
        self.persona2_entry.grid(row=1, column=1, pady=2, padx=(5, 0))
        
        btn_conectar = ttk.Button(conexion_frame, text="Crear Conexión", command=self.agregar_conexion_manual)
        btn_conectar.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Sección: Red Personal (Ego Network)
        ego_frame = ttk.LabelFrame(control_frame, text="Red Personal de Usuario", padding="10")
        ego_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(ego_frame, text="Ver red de usuario (ID):").pack(anchor="w")
        
        # Frame para entrada y botones
        ego_input_frame = ttk.Frame(ego_frame)
        ego_input_frame.pack(fill="x", pady=2)
        
        self.ego_user_entry = ttk.Entry(ego_input_frame, width=10)
        self.ego_user_entry.pack(side="left", padx=(0, 5))
        self.ego_user_entry.bind('<Return>', lambda e: self.mostrar_ego_network())
        
        btn_ver_red = ttk.Button(ego_input_frame, text="Ver Red", command=self.mostrar_ego_network)
        btn_ver_red.pack(side="left", padx=(5, 0))
        
        # Buscar por nombre
        ttk.Label(ego_frame, text="O buscar por nombre:").pack(anchor="w", pady=(10, 0))
        search_frame = ttk.Frame(ego_frame)
        search_frame.pack(fill="x", pady=2)
        
        self.search_entry = ttk.Entry(search_frame, width=15)
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.buscar_usuario_por_nombre())
        
        btn_buscar = ttk.Button(search_frame, text="Buscar", command=self.buscar_usuario_por_nombre)
        btn_buscar.pack(side="left")
        
        btn_ver_completa = ttk.Button(ego_frame, text="🔄 Ver Red Completa", command=self.mostrar_red_completa)
        btn_ver_completa.pack(fill="x", pady=(10, 0))
        
        # Variable para rastrear si estamos en modo ego network
        self.ego_mode = False
        self.ego_user_id = None
        
        # Sección: Acciones
        acciones_frame = ttk.LabelFrame(control_frame, text="Acciones", padding="10")
        acciones_frame.pack(fill="x", pady=(0, 10))
        
        btn_guardar = ttk.Button(acciones_frame, text="Guardar Datos", command=self.guardar_datos)
        btn_guardar.pack(fill="x", pady=2)
        
        btn_limpiar = ttk.Button(acciones_frame, text="Limpiar Formulario", command=self.limpiar_formulario)
        btn_limpiar.pack(fill="x", pady=2)
    
    def crear_panel_visualizacion(self, parent):
        """Crear panel de visualización del grafo"""
        viz_frame = ttk.LabelFrame(parent, text="Visualización del Grafo", padding="10")
        viz_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear figura de matplotlib con mayor resolución y tamaño
        self.fig = Figure(figsize=(12, 8), dpi=120, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        self.fig.tight_layout(pad=3.0)
        
        # Canvas para matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar de matplotlib
        toolbar_frame = ttk.Frame(viz_frame)
        toolbar_frame.pack(fill="x", pady=(5, 0))
        
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
    
    def crear_panel_informacion(self, parent):
        """Crear panel de información"""
        info_frame = ttk.LabelFrame(parent, text="Información del Grafo", padding="10")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(10, 0))
        
        # Estadísticas
        self.stats_label = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.stats_label.pack(anchor="w")
        
        # Lista de personas
        ttk.Label(info_frame, text="Personas en la red:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        self.personas_text = scrolledtext.ScrolledText(info_frame, height=8, width=40)
        self.personas_text.pack(fill="both", expand=True)
    
    def agregar_persona(self):
        """Agregar una nueva persona al grafo"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        try:
            edad = int(self.edad_entry.get()) if self.edad_entry.get().strip() else 0
        except ValueError:
            edad = 0
        
        email = self.email_entry.get().strip()
        intereses_input = self.intereses_entry.get().strip()
        intereses = [i.strip().lower() for i in intereses_input.split(',') if i.strip()] if intereses_input else []
        
        # Obtener próximo ID
        if self.grafo.nodes:
            nuevo_id = max(self.grafo.nodes) + 1
        else:
            nuevo_id = 1
        
        # Agregar nodo
        self.grafo.add_node(nuevo_id, 
                           label=nombre, 
                           edad=edad,
                           email=email,
                           intereses=intereses,
                           amigos=[])
        
        # Buscar conexiones automáticas
        conexiones_creadas = self.buscar_y_crear_conexiones_automaticas(nuevo_id)
        
        # Mostrar resultado
        mensaje = f"Persona '{nombre}' agregada con ID {nuevo_id}"
        if conexiones_creadas > 0:
            mensaje += f"\n{conexiones_creadas} conexiones automáticas creadas"
        
        messagebox.showinfo("Éxito", mensaje)
        
        # Limpiar formulario y actualizar
        self.limpiar_formulario()
        self.actualizar_grafo()
        self.actualizar_informacion()
    
    def buscar_y_crear_conexiones_automaticas(self, nuevo_id):
        """Buscar y crear conexiones automáticas"""
        conexiones_creadas = 0
        nueva_persona_intereses = set(self.grafo.nodes[nuevo_id]['intereses'])
        
        for persona_id, data in self.grafo.nodes(data=True):
            if persona_id == nuevo_id:
                continue
                
            persona_intereses = set(data.get('intereses', []))
            intereses_comunes = nueva_persona_intereses.intersection(persona_intereses)
            
            if intereses_comunes and not self.grafo.has_edge(nuevo_id, persona_id):
                self.grafo.add_edge(nuevo_id, persona_id)
                self.grafo.nodes[nuevo_id]['amigos'].append(persona_id)
                self.grafo.nodes[persona_id]['amigos'].append(nuevo_id)
                conexiones_creadas += 1
        
        return conexiones_creadas
    
    def agregar_conexion_manual(self):
        """Agregar una conexión manual entre dos personas"""
        try:
            persona1 = int(self.persona1_entry.get())
            persona2 = int(self.persona2_entry.get())
            
            if persona1 not in self.grafo.nodes or persona2 not in self.grafo.nodes:
                messagebox.showerror("Error", "Una o ambas personas no existen")
                return
            
            if persona1 == persona2:
                messagebox.showerror("Error", "No puedes conectar una persona consigo misma")
                return
            
            if self.grafo.has_edge(persona1, persona2):
                messagebox.showwarning("Advertencia", "Estas personas ya están conectadas")
                return
            
            # Crear conexión
            self.grafo.add_edge(persona1, persona2)
            self.grafo.nodes[persona1]['amigos'].append(persona2)
            self.grafo.nodes[persona2]['amigos'].append(persona1)
            
            nombre1 = self.grafo.nodes[persona1]['label']
            nombre2 = self.grafo.nodes[persona2]['label']
            
            messagebox.showinfo("Éxito", f"Conexión creada entre {nombre1} y {nombre2}")
            
            # Limpiar campos y actualizar
            self.persona1_entry.delete(0, tk.END)
            self.persona2_entry.delete(0, tk.END)
            self.actualizar_grafo()
            self.actualizar_informacion()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa números válidos para los IDs")
    
    def actualizar_grafo(self):
        """Actualizar la visualización del grafo con mejor separación de nodos"""
        # Si estamos en modo ego network, usar la función especializada
        if getattr(self, 'ego_mode', False) and getattr(self, 'ego_user_id', None):
            self.actualizar_ego_grafo()
            return
            
        self.ax.clear()
        
        if not self.grafo.nodes:
            self.ax.text(0.5, 0.2, 'No hay personas en la red', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=14, color='gray')
            self.canvas.draw()
            return
        
        num_nodes = self.grafo.number_of_nodes()
        
        # Usar layout shell como predeterminado
        layout_name = "shell"
        
        # Calcular parámetros según el tamaño de la red
        if num_nodes > 50:
            node_size = max(200, 800 - num_nodes * 5)  # Nodos más pequeños para redes grandes
            font_size = max(6, 10 - num_nodes * 0.03)  # Texto más pequeño
            k_value = max(3.0, num_nodes * 0.05)  # Separación dinámica
        elif num_nodes > 20:
            node_size = 600
            font_size = 7
            k_value = 2.5
        else:
            node_size = 1000
            font_size = 8
            k_value = 2.0
        
        # Crear layout según selección
        if layout_name == "spring":
            pos = nx.spring_layout(self.grafo, k=k_value, iterations=100, seed=42)
        elif layout_name == "circular":
            pos = nx.circular_layout(self.grafo)
        elif layout_name == "shell":
            # Agrupar nodos por grado de conectividad para shell layout
            shells = []
            nodes_by_degree = {}
            for node in self.grafo.nodes():
                degree = self.grafo.degree(node)
                if degree not in nodes_by_degree:
                    nodes_by_degree[degree] = []
                nodes_by_degree[degree].append(node)
            
            for degree in sorted(nodes_by_degree.keys(), reverse=True):
                shells.append(nodes_by_degree[degree])
            
            if len(shells) > 1:
                pos = nx.shell_layout(self.grafo, nlist=shells)
            else:
                pos = nx.circular_layout(self.grafo)
        else:  # random
            pos = nx.random_layout(self.grafo, seed=42)
        
        # Aplicar separación adicional si hay muchos nodos
        if num_nodes > 30:
            # Escalar posiciones para mayor separación
            scale_factor = min(2.0, num_nodes * 0.02)
            for node in pos:
                pos[node] = (pos[node][0] * scale_factor, pos[node][1] * scale_factor)
        
        # Dibujar nodos con colores variables según número de conexiones
        node_colors = []
        for node in self.grafo.nodes():
            degree = self.grafo.degree(node)
            if degree > 8:
                node_colors.append('#ff6b6b')  # Rojo para nodos muy conectados
            elif degree > 4:
                node_colors.append('#4ecdc4')  # Verde-azul para nodos bien conectados
            elif degree > 0:
                node_colors.append('#45b7d1')  # Azul para nodos con pocas conexiones
            else:
                node_colors.append('#f9ca24')  # Amarillo para nodos aislados
        
        nx.draw_networkx_nodes(self.grafo, pos, ax=self.ax, 
                              node_color=node_colors, 
                              node_size=node_size, 
                              alpha=0.8,
                              edgecolors='black',
                              linewidths=0.5)
        
        # Dibujar aristas con grosor variable
        edge_widths = []
        for edge in self.grafo.edges():
            # Aristas más gruesas para nodos más conectados
            degree_avg = (self.grafo.degree(edge[0]) + self.grafo.degree(edge[1])) / 2
            width = max(0.5, min(2.0, degree_avg * 0.2))
            edge_widths.append(width)
        
        nx.draw_networkx_edges(self.grafo, pos, ax=self.ax,
                              edge_color='#666666', 
                              width=edge_widths, 
                              alpha=0.6)
        
        # Etiquetas optimizadas para evitar superposición
        labels = {}
        for node, data in self.grafo.nodes(data=True):
            name = data['label']
            # Truncar nombres largos
            if len(name) > 12:
                name = name[:10] + "..."
            labels[node] = f"{name}\n({node})"
        
        # Dibujar etiquetas con mejor posicionamiento
        label_pos = {}
        for node, (x, y) in pos.items():
            # Desplazar ligeramente las etiquetas para evitar superposición con nodos
            label_pos[node] = (x, y - 0.05)
        
        nx.draw_networkx_labels(self.grafo, label_pos, labels, ax=self.ax,
                               font_size=font_size, 
                               font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", 
                                       facecolor='white', 
                                       edgecolor='none',
                                       alpha=0.8))
        
        self.ax.set_title(f"Red Social - {num_nodes} Personas, {self.grafo.number_of_edges()} Conexiones", 
                         fontsize=14, fontweight='bold', pad=20)
        self.ax.axis('off')
        
        # Ajustar márgenes para mejor visualización
        self.ax.margins(0.1)
        
        self.canvas.draw()
    
    def mostrar_ego_network(self):
        """Mostrar la red personal (ego network) de un usuario específico"""
        user_id_str = self.ego_user_entry.get().strip()
        
        if not user_id_str:
            messagebox.showerror("Error", "Por favor, ingresa un ID de usuario")
            return
        
        try:
            user_id = int(user_id_str)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número válido")
            return
        
        if user_id not in self.grafo.nodes:
            messagebox.showerror("Error", f"No existe un usuario con ID {user_id}")
            return
        
        # Activar modo ego network
        self.ego_mode = True
        self.ego_user_id = user_id
        
        # Actualizar la visualización
        self.actualizar_ego_grafo()
        self.actualizar_informacion()
    
    def mostrar_red_completa(self):
        """Volver a mostrar la red completa"""
        self.ego_mode = False
        self.ego_user_id = None
        self.ego_user_entry.delete(0, tk.END)
        
        # Actualizar la visualización
        self.actualizar_grafo()
        self.actualizar_informacion()
    
    def actualizar_ego_grafo(self):
        """Actualizar la visualización mostrando solo la red del usuario seleccionado"""
        if not self.ego_mode or self.ego_user_id is None:
            self.actualizar_grafo()
            return
        
        self.ax.clear()
        
        # Crear subgrafo con el usuario central y sus vecinos
        ego_graph = nx.ego_graph(self.grafo, self.ego_user_id, radius=1)
        
        if ego_graph.number_of_nodes() <= 1:
            # Usuario sin conexiones - mostrar solo el nodo central
            self.ax.clear()
            
            # Dibujar solo el nodo central
            pos = {self.ego_user_id: (0, 0)}
            
            nx.draw_networkx_nodes(ego_graph, pos, ax=self.ax, 
                                  node_color='#e74c3c', 
                                  node_size=2000, 
                                  alpha=0.9,
                                  edgecolors='black',
                                  linewidths=3)
            
            # Etiqueta para el usuario aislado
            user_data = self.grafo.nodes[self.ego_user_id]
            user_name = user_data['label']
            labels = {self.ego_user_id: f"★ {user_name}\n(ID: {self.ego_user_id})\nSin conexiones"}
            
            nx.draw_networkx_labels(ego_graph, pos, labels, ax=self.ax,
                                   font_size=12, 
                                   font_weight='bold',
                                   bbox=dict(boxstyle="round,pad=0.4", 
                                           facecolor='white', 
                                           edgecolor='red',
                                           alpha=0.9))
            
            self.ax.set_title(f"Red Personal de: {user_name} (ID: {self.ego_user_id})\n"
                             f"Usuario sin conexiones", 
                             fontsize=14, fontweight='bold', pad=20)
            self.ax.axis('off')
            self.ax.margins(0.2)
            self.canvas.draw()
            return
        
        num_nodes = ego_graph.number_of_nodes()
        
        # Posicionamiento mejorado para ego networks
        if num_nodes == 2:
            # Solo 2 nodos: usuario central y una conexión con más separación
            neighbor_id = list(ego_graph.neighbors(self.ego_user_id))[0]
            pos = {
                self.ego_user_id: (-0.8, 0),  # Central ligeramente a la izquierda
                neighbor_id: (0.8, 0)         # Vecino a la derecha con más espacio
            }
        elif num_nodes <= 8:
            # Redes pequeñas: layout circular con usuario central en el centro
            neighbors = list(ego_graph.neighbors(self.ego_user_id))
            pos = {self.ego_user_id: (0, 0)}
            
            # Distribuir vecinos en círculo alrededor del usuario central
            angle_step = 2 * np.pi / len(neighbors)
            radius = 1.2  # Aumentar radio para mejor separación
            
            for i, neighbor in enumerate(neighbors):
                angle = i * angle_step
                pos[neighbor] = (radius * np.cos(angle), radius * np.sin(angle))
        else:
            # Redes más grandes: usar spring layout con separación aumentada
            pos = nx.spring_layout(ego_graph, k=3.0, iterations=100, seed=42)
        
        # Colores y tamaños especiales para ego network
        node_colors = []
        node_sizes = []
        for node in ego_graph.nodes():
            if node == self.ego_user_id:
                # Usuario central en rojo destacado
                node_colors.append('#e74c3c')
                node_sizes.append(1800)
            else:
                # Conexiones en azul
                node_colors.append('#3498db')
                node_sizes.append(1200)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(ego_graph, pos, ax=self.ax, 
                              node_color=node_colors, 
                              node_size=node_sizes, 
                              alpha=0.9,
                              edgecolors='black',
                              linewidths=2)
        
        # Dibujar aristas con mayor grosor
        nx.draw_networkx_edges(ego_graph, pos, ax=self.ax,
                              edge_color='#2c3e50', 
                              width=4, 
                              alpha=0.8)
        
        # Crear etiquetas mejoradas
        labels = {}
        for node, data in ego_graph.nodes(data=True):
            name = data.get('label', f'Usuario {node}')
            if len(name) > 15:
                name = name[:12] + "..."
            
            if node == self.ego_user_id:
                # Etiqueta especial para el usuario central
                labels[node] = f"★ {name}\n(ID: {node})"
            else:
                labels[node] = f"{name}\n(ID: {node})"
        
        # Posicionar etiquetas con separación mejorada para ego networks
        label_pos = {}
        base_offset = 0.25  # Offset base más grande para ego networks
        
        for node, (x, y) in pos.items():
            if node == self.ego_user_id:
                # Usuario central: etiqueta siempre debajo con mayor separación
                label_pos[node] = (x, y - base_offset * 1.2)
            else:
                # Vecinos: posicionamiento inteligente según ubicación
                distance_from_center = np.sqrt(x*x + y*y)
                
                if num_nodes == 2:
                    # Para 2 nodos, posicionar etiquetas fuera de la línea
                    label_pos[node] = (x, y + base_offset if x > 0 else y - base_offset)
                elif distance_from_center > 0:
                    # Posicionar etiqueta hacia afuera del centro
                    factor = 1.3  # Factor para alejar más las etiquetas
                    label_pos[node] = (x * factor, y * factor)
                else:
                    # Fallback para casos especiales
                    label_pos[node] = (x, y - base_offset)
        
        # Dibujar etiquetas con estilo mejorado
        nx.draw_networkx_labels(ego_graph, label_pos, labels, ax=self.ax,
                               font_size=12,  # Tamaño más grande para ego networks
                               font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.4", 
                                       facecolor='white', 
                                       edgecolor='darkgray',
                                       alpha=0.98,
                                       linewidth=1))
        
        # Información del usuario central
        user_data = self.grafo.nodes[self.ego_user_id]
        user_name = user_data.get('label', f'Usuario {self.ego_user_id}')
        user_connections = len(list(ego_graph.neighbors(self.ego_user_id)))
        
        self.ax.set_title(f"Red Personal de: {user_name} (ID: {self.ego_user_id})\n"
                         f"{user_connections} Conexiones Directas", 
                         fontsize=14, fontweight='bold', pad=20)
        self.ax.axis('off')
        
        # Ajustar márgenes para mejor visualización
        self.ax.margins(0.2)
        
        self.canvas.draw()
    
    def actualizar_informacion(self):
        """Actualizar panel de información"""
        # Lista de personas
        self.personas_text.delete(1.0, tk.END)
        
        # Si estamos en modo ego network, mostrar información específica
        if getattr(self, 'ego_mode', False) and getattr(self, 'ego_user_id', None):
            self.mostrar_info_ego_network()
            return
        
        # Modo normal - mostrar estadísticas generales
        num_personas = self.grafo.number_of_nodes()
        num_conexiones = self.grafo.number_of_edges()
        self.stats_label.config(text=f"Personas: {num_personas} | Conexiones: {num_conexiones}")
        
        if self.grafo.nodes:
            for node_id, data in self.grafo.nodes(data=True):
                intereses = ", ".join(data.get('intereses', []))
                amigos_count = len(data.get('amigos', []))
                edad = data.get('edad', 0)
                
                info = f"• {data['label']} (ID: {node_id})\n"
                info += f"  Edad: {edad} | Amigos: {amigos_count}\n"
                info += f"  Intereses: [{intereses}]\n\n"
                
                self.personas_text.insert(tk.END, info)
        else:
            self.personas_text.insert(tk.END, "No hay personas en la red.")
    
    def mostrar_info_ego_network(self):
        """Mostrar información específica del ego network"""
        user_data = self.grafo.nodes[self.ego_user_id]
        ego_graph = nx.ego_graph(self.grafo, self.ego_user_id, radius=1)
        
        # Estadísticas del ego network
        num_conexiones_directas = len(list(self.grafo.neighbors(self.ego_user_id)))
        self.stats_label.config(text=f"Red de: {user_data['label']} | Conexiones: {num_conexiones_directas}")
        
        # Información detallada del usuario central
        intereses = ", ".join(user_data.get('intereses', []))
        edad = user_data.get('edad', 0)
        email = user_data.get('email', 'No especificado')
        
        info = f"👤 USUARIO CENTRAL:\n"
        info += f"• {user_data['label']} (ID: {self.ego_user_id})\n"
        info += f"  Edad: {edad}\n"
        info += f"  Email: {email}\n"
        info += f"  Intereses: [{intereses}]\n"
        info += f"  Total de conexiones: {num_conexiones_directas}\n\n"
        
        info += f"🔗 CONEXIONES DIRECTAS:\n"
        
        if num_conexiones_directas > 0:
            for neighbor_id in self.grafo.neighbors(self.ego_user_id):
                neighbor_data = self.grafo.nodes[neighbor_id]
                neighbor_intereses = ", ".join(neighbor_data.get('intereses', []))
                
                # Calcular intereses en común
                user_int = set(user_data.get('intereses', []))
                neighbor_int = set(neighbor_data.get('intereses', []))
                comunes = user_int.intersection(neighbor_int)
                
                info += f"• {neighbor_data['label']} (ID: {neighbor_id})\n"
                info += f"  Edad: {neighbor_data.get('edad', 0)}\n"
                info += f"  Intereses: [{neighbor_intereses}]\n"
                
                if comunes:
                    info += f"  ⭐ Intereses comunes: {', '.join(comunes)}\n"
                else:
                    info += f"  ⚪ Sin intereses comunes\n"
                info += "\n"
        else:
            info += "  No tiene conexiones directas.\n"
        
        self.personas_text.insert(tk.END, info)
    
    def buscar_usuario_por_nombre(self):
        """Buscar usuario por nombre y mostrar su red"""
        nombre_buscar = self.search_entry.get().strip().lower()
        
        if not nombre_buscar:
            messagebox.showerror("Error", "Por favor, ingresa un nombre para buscar")
            return
        
        # Buscar usuarios que coincidan con el nombre
        usuarios_encontrados = []
        for node_id, data in self.grafo.nodes(data=True):
            if nombre_buscar in data['label'].lower():
                usuarios_encontrados.append((node_id, data['label']))
        
        if not usuarios_encontrados:
            messagebox.showinfo("Sin resultados", f"No se encontraron usuarios con el nombre '{nombre_buscar}'")
            return
        
        if len(usuarios_encontrados) == 1:
            # Solo un usuario encontrado, mostrar directamente
            user_id = usuarios_encontrados[0][0]
            self.ego_user_entry.delete(0, tk.END)
            self.ego_user_entry.insert(0, str(user_id))
            self.mostrar_ego_network()
        else:
            # Múltiples usuarios encontrados, mostrar opciones
            opciones = "\n".join([f"ID {uid}: {nombre}" for uid, nombre in usuarios_encontrados])
            messagebox.showinfo("Múltiples resultados", 
                               f"Se encontraron varios usuarios:\n\n{opciones}\n\n"
                               f"Ingresa el ID específico del usuario que deseas ver.")
    
    def guardar_datos(self):
        """Guardar datos en archivos JSON"""
        try:
            # Guardar usuarios
            ruta_usuarios = os.path.join(self.dir_actual, 'usuarios.json')
            usuarios_data = {"usuarios": []}
            
            for node_id, data in self.grafo.nodes(data=True):
                usuario = {
                    "id": node_id,
                    "nombre": data.get('label', ''),
                    "edad": data.get('edad', 0),
                    "email": data.get('email', ''),
                    "intereses": data.get('intereses', []),
                    "amigos": data.get('amigos', [])
                }
                usuarios_data["usuarios"].append(usuario)
            
            with open(ruta_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios_data, f, ensure_ascii=False, indent=2)
            
            # Guardar conexiones
            ruta_conexiones = os.path.join(self.dir_actual, 'conexiones.json')
            conexiones_data = {"conexiones": []}
            
            aristas_procesadas = set()
            for origen, destino in self.grafo.edges():
                arista = tuple(sorted([origen, destino]))
                if arista not in aristas_procesadas:
                    conexiones_data["conexiones"].append({
                        "origen": arista[0],
                        "destino": arista[1]
                    })
                    aristas_procesadas.add(arista)
            
            with open(ruta_conexiones, 'w', encoding='utf-8') as f:
                json.dump(conexiones_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Éxito", 
                               f"Datos guardados exitosamente:\n"
                               f"• {len(usuarios_data['usuarios'])} usuarios\n"
                               f"• {len(conexiones_data['conexiones'])} conexiones")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos: {e}")
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.edad_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.intereses_entry.delete(0, tk.END)
    
    def __init_complete__(self):
        """Completar inicialización"""
        self.actualizar_informacion()

if __name__ == "__main__":
    root = tk.Tk()
    app = RedSocialGUI(root)
    app.actualizar_informacion()  # Actualizar información inicial
    root.mainloop()