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
        main_frame.rowconfigure(0, weight=1)
        
        # Panel de control con navegación por pestañas (izquierda)
        self.crear_panel_control_navegacion(main_frame)
        
        # Panel de visualización (derecha)
        self.crear_panel_visualizacion(main_frame)
    
    def crear_panel_control_navegacion(self, parent):
        """Crear panel de control con navegación por pestañas"""
        # Frame contenedor para el panel de control
        control_container = ttk.Frame(parent)
        control_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        control_container.columnconfigure(0, weight=1)
        control_container.rowconfigure(0, weight=1)
        
        # Crear el Notebook (pestañas)
        self.notebook = ttk.Notebook(control_container)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Pestaña 1: Gestión de Personas
        self.crear_tab_personas()
        
        # Pestaña 2: Conexiones
        self.crear_tab_conexiones()
        
        # Pestaña 3: Visualización
        self.crear_tab_visualizacion()
        
        # Pestaña 4: Información del Grafo
        self.crear_tab_informacion()
        
        # Pestaña 5: Configuración
        self.crear_tab_configuracion()
        
        # Vincular evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def crear_tab_personas(self):
        """Crear pestaña de gestión de personas"""
        personas_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(personas_frame, text="👤 Personas")
        
        # Sección: Agregar Persona
        persona_frame = ttk.LabelFrame(personas_frame, text="Agregar Nueva Persona", padding="10")
        persona_frame.pack(fill="x", pady=(0, 10))
        
        # Campos de entrada en una grilla más organizada
        ttk.Label(persona_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = ttk.Entry(persona_frame, width=25)
        self.nombre_entry.grid(row=0, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(persona_frame, text="Edad:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.edad_entry = ttk.Entry(persona_frame, width=25)
        self.edad_entry.grid(row=1, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(persona_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(persona_frame, width=25)
        self.email_entry.grid(row=2, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(persona_frame, text="Intereses:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(persona_frame, text="(separar con comas)", font=("Arial", 8)).grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        self.intereses_entry = ttk.Entry(persona_frame, width=25)
        self.intereses_entry.grid(row=4, column=0, columnspan=2, pady=2, sticky=(tk.W, tk.E))
        
        # Configurar expansión de columnas
        persona_frame.columnconfigure(1, weight=1)
        
        # Botones de acción
        buttons_frame = ttk.Frame(persona_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        btn_agregar = ttk.Button(buttons_frame, text="➕ Agregar Persona", command=self.agregar_persona)
        btn_agregar.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_limpiar = ttk.Button(buttons_frame, text="🗑️ Limpiar", command=self.limpiar_formulario)
        btn_limpiar.pack(side=tk.LEFT)
        
        # Lista de personas existentes
        lista_frame = ttk.LabelFrame(personas_frame, text="Personas en la Red", padding="10")
        lista_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Crear Treeview para mostrar personas
        columns = ('ID', 'Nombre', 'Edad', 'Conexiones')
        self.personas_tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        self.personas_tree.heading('ID', text='ID')
        self.personas_tree.heading('Nombre', text='Nombre')
        self.personas_tree.heading('Edad', text='Edad')
        self.personas_tree.heading('Conexiones', text='Conexiones')
        
        self.personas_tree.column('ID', width=50, anchor='center')
        self.personas_tree.column('Nombre', width=120)
        self.personas_tree.column('Edad', width=60, anchor='center')
        self.personas_tree.column('Conexiones', width=80, anchor='center')
        
        # Scrollbar para el Treeview
        tree_scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.personas_tree.yview)
        self.personas_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.personas_tree.pack(side=tk.LEFT, fill='both', expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Vincular doble clic para ver red personal
        self.personas_tree.bind('<Double-1>', self.on_persona_double_click)
    
    def crear_tab_conexiones(self):
        """Crear pestaña de gestión de conexiones"""
        conexiones_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(conexiones_frame, text="🔗 Conexiones")
        
        # Sección: Conexiones Manuales
        conexion_frame = ttk.LabelFrame(conexiones_frame, text="Crear Conexión Manual", padding="10")
        conexion_frame.pack(fill="x", pady=(0, 10))
        
        # Usar comboboxes para seleccionar personas
        ttk.Label(conexion_frame, text="Persona 1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.persona1_combo = ttk.Combobox(conexion_frame, width=22, state="readonly")
        self.persona1_combo.grid(row=0, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(conexion_frame, text="Persona 2:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.persona2_combo = ttk.Combobox(conexion_frame, width=22, state="readonly")
        self.persona2_combo.grid(row=1, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # O usar IDs directamente
        ttk.Label(conexion_frame, text="O usar IDs directamente:", font=("Arial", 9, "italic")).grid(row=2, column=0, columnspan=2, pady=(10, 5))
        
        id_frame = ttk.Frame(conexion_frame)
        id_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(id_frame, text="ID 1:").pack(side=tk.LEFT)
        self.persona1_entry = ttk.Entry(id_frame, width=8)
        self.persona1_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(id_frame, text="ID 2:").pack(side=tk.LEFT)
        self.persona2_entry = ttk.Entry(id_frame, width=8)
        self.persona2_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        conexion_frame.columnconfigure(1, weight=1)
        
        btn_conectar = ttk.Button(conexion_frame, text="🔗 Crear Conexión", command=self.agregar_conexion_manual)
        btn_conectar.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Lista de conexiones existentes
        lista_conexiones_frame = ttk.LabelFrame(conexiones_frame, text="Conexiones Existentes", padding="10")
        lista_conexiones_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Treeview para conexiones
        conn_columns = ('Persona 1', 'Persona 2', 'Intereses Comunes')
        self.conexiones_tree = ttk.Treeview(lista_conexiones_frame, columns=conn_columns, show='headings', height=12)
        
        self.conexiones_tree.heading('Persona 1', text='Persona 1')
        self.conexiones_tree.heading('Persona 2', text='Persona 2')
        self.conexiones_tree.heading('Intereses Comunes', text='Intereses Comunes')
        
        self.conexiones_tree.column('Persona 1', width=100)
        self.conexiones_tree.column('Persona 2', width=100)
        self.conexiones_tree.column('Intereses Comunes', width=150)
        
        conn_scrollbar = ttk.Scrollbar(lista_conexiones_frame, orient=tk.VERTICAL, command=self.conexiones_tree.yview)
        self.conexiones_tree.configure(yscrollcommand=conn_scrollbar.set)
        
        self.conexiones_tree.pack(side=tk.LEFT, fill='both', expand=True)
        conn_scrollbar.pack(side=tk.RIGHT, fill='y')
    
    def crear_tab_visualizacion(self):
        """Crear pestaña de opciones de visualización"""
        viz_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(viz_frame, text="👁️ Visualización")
        
        # Sección: Red Personal (Ego Network)
        ego_frame = ttk.LabelFrame(viz_frame, text="Red Personal de Usuario", padding="10")
        ego_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(ego_frame, text="Ver red de usuario (ID):").pack(anchor="w")
        
        # Frame para entrada y botones
        ego_input_frame = ttk.Frame(ego_frame)
        ego_input_frame.pack(fill="x", pady=5)
        
        self.ego_user_entry = ttk.Entry(ego_input_frame, width=10)
        self.ego_user_entry.pack(side="left", padx=(0, 5))
        self.ego_user_entry.bind('<Return>', lambda e: self.mostrar_ego_network())
        
        btn_ver_red = ttk.Button(ego_input_frame, text="🔍 Ver Red", command=self.mostrar_ego_network)
        btn_ver_red.pack(side="left", padx=(5, 0))
        
        # Buscar por nombre
        ttk.Label(ego_frame, text="O buscar por nombre:").pack(anchor="w", pady=(10, 0))
        search_frame = ttk.Frame(ego_frame)
        search_frame.pack(fill="x", pady=5)
        
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.buscar_usuario_por_nombre())
        
        btn_buscar = ttk.Button(search_frame, text="🔍 Buscar", command=self.buscar_usuario_por_nombre)
        btn_buscar.pack(side="left")
        
        btn_ver_completa = ttk.Button(ego_frame, text="🌐 Ver Red Completa", command=self.mostrar_red_completa)
        btn_ver_completa.pack(fill="x", pady=(15, 0))
        
        # Variable para rastrear si estamos en modo ego network
        self.ego_mode = False
        self.ego_user_id = None
        
    def crear_tab_informacion(self):
        """Crear pestaña de información del grafo"""
        info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(info_frame, text="📊 Información")
        
        # Estadísticas generales
        stats_frame = ttk.LabelFrame(info_frame, text="Estadísticas del Grafo", padding="10")
        stats_frame.pack(fill="x", pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack(anchor="w")
        
        # Información adicional
        self.info_adicional_label = ttk.Label(stats_frame, text="", font=("Arial", 9))
        self.info_adicional_label.pack(anchor="w", pady=(5, 0))
        
        # Lista detallada de personas
        ttk.Label(info_frame, text="Información Detallada:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        self.personas_text = scrolledtext.ScrolledText(info_frame, height=15, width=40, wrap=tk.WORD)
        self.personas_text.pack(fill="both", expand=True)
    
    def crear_tab_configuracion(self):
        """Crear pestaña de configuración y acciones"""
        config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(config_frame, text="⚙️ Configuración")
        
        # Sección: Acciones de datos
        datos_frame = ttk.LabelFrame(config_frame, text="Gestión de Datos", padding="10")
        datos_frame.pack(fill="x", pady=(0, 10))
        
        btn_guardar = ttk.Button(datos_frame, text="💾 Guardar Datos", command=self.guardar_datos)
        btn_guardar.pack(fill="x", pady=2)
        
        btn_cargar = ttk.Button(datos_frame, text="📂 Recargar Datos", command=self.recargar_datos)
        btn_cargar.pack(fill="x", pady=2)
        
        # Sección: Análisis avanzado
        analisis_frame = ttk.LabelFrame(config_frame, text="Análisis de Red", padding="10")
        analisis_frame.pack(fill="x", pady=(10, 0))
        
        btn_centralidad = ttk.Button(analisis_frame, text="📈 Calcular Centralidad", command=self.calcular_centralidad)
        btn_centralidad.pack(fill="x", pady=2)
        
        btn_clusters = ttk.Button(analisis_frame, text="🎯 Detectar Comunidades", command=self.detectar_comunidades)
        btn_clusters.pack(fill="x", pady=2)
        
        # Área de resultados de análisis
        self.analisis_text = scrolledtext.ScrolledText(config_frame, height=12, width=40, wrap=tk.WORD)
        self.analisis_text.pack(fill="both", expand=True, pady=(10, 0))
    
    def on_tab_changed(self, event):
        """Manejar cambio de pestaña"""
        selected_tab = event.widget.tab('current')['text']
        
        # Actualizar datos específicos según la pestaña
        if "Personas" in selected_tab:
            self.actualizar_lista_personas()
        elif "Conexiones" in selected_tab:
            self.actualizar_comboboxes_personas()
            self.actualizar_lista_conexiones()
        elif "Información" in selected_tab:
            self.actualizar_informacion()
    
    def on_persona_double_click(self, event):
        """Manejar doble clic en la lista de personas"""
        selection = self.personas_tree.selection()
        if selection:
            item = self.personas_tree.item(selection[0])
            user_id = item['values'][0]
            
            # Cambiar a la pestaña de visualización
            self.notebook.select(2)  # Índice de la pestaña de visualización
            
            # Configurar y mostrar ego network
            self.ego_user_entry.delete(0, tk.END)
            self.ego_user_entry.insert(0, str(user_id))
            self.mostrar_ego_network()
    
    def actualizar_lista_personas(self):
        """Actualizar la lista de personas en el Treeview"""
        # Limpiar lista actual
        for item in self.personas_tree.get_children():
            self.personas_tree.delete(item)
        
        # Agregar personas actuales
        for node_id, data in self.grafo.nodes(data=True):
            nombre = data.get('label', f'Usuario {node_id}')
            edad = data.get('edad', 0)
            conexiones = len(data.get('amigos', []))
            
            self.personas_tree.insert('', 'end', values=(node_id, nombre, edad, conexiones))
    
    def actualizar_comboboxes_personas(self):
        """Actualizar los comboboxes de selección de personas"""
        personas = [f"{data['label']} (ID: {node_id})" 
                   for node_id, data in self.grafo.nodes(data=True)]
        
        self.persona1_combo['values'] = personas
        self.persona2_combo['values'] = personas
    
    def actualizar_lista_conexiones(self):
        """Actualizar la lista de conexiones"""
        # Limpiar lista actual
        for item in self.conexiones_tree.get_children():
            self.conexiones_tree.delete(item)
        
        # Agregar conexiones actuales
        for edge in self.grafo.edges():
            persona1_data = self.grafo.nodes[edge[0]]
            persona2_data = self.grafo.nodes[edge[1]]
            
            nombre1 = persona1_data.get('label', f'Usuario {edge[0]}')
            nombre2 = persona2_data.get('label', f'Usuario {edge[1]}')
            
            # Calcular intereses comunes
            int1 = set(persona1_data.get('intereses', []))
            int2 = set(persona2_data.get('intereses', []))
            comunes = int1.intersection(int2)
            intereses_comunes = ', '.join(comunes) if comunes else 'Ninguno'
            
            self.conexiones_tree.insert('', 'end', values=(nombre1, nombre2, intereses_comunes))
    
    def recargar_datos(self):
        """Recargar datos desde archivos"""
        self.grafo.clear()
        self.cargar_datos()
        self.actualizar_grafo()
        self.actualizar_informacion()
        messagebox.showinfo("Éxito", "Datos recargados correctamente")
    
    def calcular_centralidad(self):
        """Calcular y mostrar medidas de centralidad"""
        if not self.grafo.nodes:
            messagebox.showwarning("Advertencia", "No hay datos para analizar")
            return
        
        # Cambiar a la pestaña de configuración para mostrar resultados
        self.notebook.select(4)
        
        self.analisis_text.delete(1.0, tk.END)
        self.analisis_text.insert(tk.END, "📈 ANÁLISIS DE CENTRALIDAD\n" + "="*40 + "\n\n")
        
        # Centralidad de grado
        degree_centrality = nx.degree_centrality(self.grafo)
        self.analisis_text.insert(tk.END, "🎯 CENTRALIDAD DE GRADO:\n")
        sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        
        for i, (node, centrality) in enumerate(sorted_degree[:5], 1):
            nombre = self.grafo.nodes[node]['label']
            self.analisis_text.insert(tk.END, f"{i}. {nombre} (ID: {node}): {centrality:.3f}\n")
        
        # Centralidad de cercanía (si el grafo está conectado)
        if nx.is_connected(self.grafo):
            self.analisis_text.insert(tk.END, "\n🎯 CENTRALIDAD DE CERCANÍA:\n")
            closeness_centrality = nx.closeness_centrality(self.grafo)
            sorted_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
            
            for i, (node, centrality) in enumerate(sorted_closeness[:5], 1):
                nombre = self.grafo.nodes[node]['label']
                self.analisis_text.insert(tk.END, f"{i}. {nombre} (ID: {node}): {centrality:.3f}\n")
        else:
            self.analisis_text.insert(tk.END, "\n⚠️ El grafo no está completamente conectado para calcular centralidad de cercanía.\n")
    
    def detectar_comunidades(self):
        """Detectar comunidades en la red"""
        if not self.grafo.nodes:
            messagebox.showwarning("Advertencia", "No hay datos para analizar")
            return
        
        # Cambiar a la pestaña de configuración para mostrar resultados
        self.notebook.select(4)
        
        self.analisis_text.delete(1.0, tk.END)
        self.analisis_text.insert(tk.END, "🎯 DETECCIÓN DE COMUNIDADES\n" + "="*40 + "\n\n")
        
        try:
            # Usar algoritmo de Louvain para detección de comunidades
            import networkx.algorithms.community as nx_comm
            communities = list(nx_comm.greedy_modularity_communities(self.grafo))
            
            self.analisis_text.insert(tk.END, f"Se encontraron {len(communities)} comunidades:\n\n")
            
            for i, community in enumerate(communities, 1):
                self.analisis_text.insert(tk.END, f"📍 COMUNIDAD {i} ({len(community)} miembros):\n")
                for node in community:
                    nombre = self.grafo.nodes[node]['label']
                    self.analisis_text.insert(tk.END, f"  • {nombre} (ID: {node})\n")
                self.analisis_text.insert(tk.END, "\n")
                
        except Exception as e:
            self.analisis_text.insert(tk.END, f"Error al detectar comunidades: {e}\n")
            self.analisis_text.insert(tk.END, "Usando método alternativo basado en componentes conectados...\n\n")
            
            # Método alternativo: componentes conectados
            components = list(nx.connected_components(self.grafo))
            self.analisis_text.insert(tk.END, f"Componentes conectados encontrados: {len(components)}\n\n")
            
            for i, component in enumerate(components, 1):
                self.analisis_text.insert(tk.END, f"📍 COMPONENTE {i} ({len(component)} miembros):\n")
                for node in component:
                    nombre = self.grafo.nodes[node]['label']
                    self.analisis_text.insert(tk.END, f"  • {nombre} (ID: {node})\n")
                self.analisis_text.insert(tk.END, "\n")
    
    def crear_panel_visualizacion(self, parent):
        """Crear panel de visualización del grafo"""
        viz_frame = ttk.LabelFrame(parent, text="Visualización del Grafo", padding="10")
        self.notebook.add(viz_frame, text="👁️ Visualización")
        
        # Crear figura de matplotlib con mayor resolución y tamaño
        self.fig = Figure(figsize=(14, 10), dpi=120, facecolor='white')
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
        self.actualizar_lista_personas()
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
        # Primero intentar obtener IDs de los comboboxes
        persona1_id = None
        persona2_id = None
        
        # Obtener de comboboxes si están seleccionados
        if self.persona1_combo.get():
            try:
                # Extraer ID del formato "Nombre (ID: X)"
                persona1_id = int(self.persona1_combo.get().split("ID: ")[1].rstrip(")"))
            except (ValueError, IndexError):
                pass
        
        if self.persona2_combo.get():
            try:
                persona2_id = int(self.persona2_combo.get().split("ID: ")[1].rstrip(")"))
            except (ValueError, IndexError):
                pass
        
        # Si no se obtuvieron de comboboxes, usar campos de entrada
        if persona1_id is None:
            try:
                persona1_id = int(self.persona1_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Por favor, selecciona o ingresa un ID válido para la Persona 1")
                return
        
        if persona2_id is None:
            try:
                persona2_id = int(self.persona2_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Por favor, selecciona o ingresa un ID válido para la Persona 2")
                return
        
        if persona1_id not in self.grafo.nodes or persona2_id not in self.grafo.nodes:
            messagebox.showerror("Error", "Una o ambas personas no existen")
            return
        
        if persona1_id == persona2_id:
            messagebox.showerror("Error", "No puedes conectar una persona consigo misma")
            return
        
        if self.grafo.has_edge(persona1_id, persona2_id):
            messagebox.showwarning("Advertencia", "Estas personas ya están conectadas")
            return
        
        # Crear conexión
        self.grafo.add_edge(persona1_id, persona2_id)
        self.grafo.nodes[persona1_id]['amigos'].append(persona2_id)
        self.grafo.nodes[persona2_id]['amigos'].append(persona1_id)
        
        nombre1 = self.grafo.nodes[persona1_id]['label']
        nombre2 = self.grafo.nodes[persona2_id]['label']
        
        messagebox.showinfo("Éxito", f"Conexión creada entre {nombre1} y {nombre2}")
        
        # Limpiar campos y actualizar
        self.persona1_combo.set('')
        self.persona2_combo.set('')
        self.persona1_entry.delete(0, tk.END)
        self.persona2_entry.delete(0, tk.END)
        self.actualizar_grafo()
        self.actualizar_lista_conexiones()
        self.actualizar_informacion()
    
    def actualizar_grafo(self):
        """Actualizar la visualización del grafo con mejor separación de nodos"""
        # Si estamos en modo ego network, usar la función especializada
        if getattr(self, 'ego_mode', False) and getattr(self, 'ego_user_id', None):
            self.actualizar_ego_grafo()
            return
            
        self.ax.clear()
        
        if not self.grafo.nodes:
            self.ax.text(0.5, 0.5, 'No hay personas en la red\n\nUsa la pestaña "Personas" para agregar usuarios', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=14, color='gray',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.3))
            self.canvas.draw()
            return
        
        num_nodes = self.grafo.number_of_nodes()
        
        # Usar layout Shell por defecto
        layout_name = "shell"
        
        # Calcular parámetros según el tamaño de la red
        if num_nodes > 50:
            node_size = max(200, 800 - num_nodes * 5)
            font_size = max(6, 10 - num_nodes * 0.03)
            k_value = max(3.0, num_nodes * 0.05)
        elif num_nodes > 20:
            node_size = 600
            font_size = 7
            k_value = 2.5
        else:
            node_size = 1000
            font_size = 8
            k_value = 2.0
        
        # Crear layout Shell (agrupar nodos por grado de conectividad)
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
        
        # Aplicar separación adicional si hay muchos nodos
        if num_nodes > 30:
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
            if len(name) > 12:
                name = name[:10] + "..."
            labels[node] = f"{name}\n({node})"
        
        # Dibujar etiquetas con mejor posicionamiento
        label_pos = {}
        for node, (x, y) in pos.items():
            label_pos[node] = (x, y - 0.05)
        
        nx.draw_networkx_labels(self.grafo, label_pos, labels, ax=self.ax,
                               font_size=font_size, 
                               font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", 
                                       facecolor='white', 
                                       edgecolor='none',
                                       alpha=0.8))
        
        # Título con información del layout
        self.ax.set_title(f"Red Social - {num_nodes} Personas, {self.grafo.number_of_edges()} Conexiones\n"
                         f"Layout: Shell (Por conectividad)", 
                         fontsize=14, fontweight='bold', pad=20)
        self.ax.axis('off')
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
        # Cambiar automáticamente a la pestaña de información para ver detalles
        self.notebook.select(3)
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
        """Actualizar la visualización del ego graph con mejor separación de nodos"""
        if not self.ego_mode or self.ego_user_id is None:
            return
        
        self.ax.clear()
        
        ego_graph = nx.ego_graph(self.grafo, self.ego_user_id, radius=1)
        
        if not ego_graph.nodes:
            self.ax.text(0.5, 0.5, 'No hay datos para mostrar en la red personal', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=14, color='gray',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.3))
            self.canvas.draw()
            return
        
        num_nodes = ego_graph.number_of_nodes()
        
        pos = nx.spring_layout(ego_graph, k=0.5, iterations=50, seed=42)
        
        # Dibujar nodos with colores variables según número de conexiones
        node_colors = []
        for node in ego_graph.nodes():
            degree = ego_graph.degree(node)
            if degree > 8:
                node_colors.append('#ff6b6b')  # Rojo para nodos muy conectados
            elif degree > 4:
                node_colors.append('#4ecdc4')  # Verde-azul para nodos bien conectados
            elif degree > 0:
                node_colors.append('#45b7d1')  # Azul para nodos con pocas conexiones
            else:
                node_colors.append('#f9ca24')  # Amarillo para nodos aislados
        
        nx.draw_networkx_nodes(ego_graph, pos, ax=self.ax, 
                              node_color=node_colors, 
                              node_size=700, 
                              alpha=0.8,
                              edgecolors='black',
                              linewidths=0.5)
        
        # Dibujar aristas
        nx.draw_networkx_edges(ego_graph, pos, ax=self.ax,
                              edge_color='#666666', 
                              width=2.0, 
                              alpha=0.6)
        
        # Etiquetas optimizadas para evitar superposición
        labels = {}
        for node, data in ego_graph.nodes(data=True):
            name = data['label']
            if len(name) > 12:
                name = name[:10] + "..."
            labels[node] = f"{name}\n({node})"
        
        # Dibujar etiquetas con mejor posicionamiento
        label_pos = {}
        for node, (x, y) in pos.items():
            label_pos[node] = (x, y - 0.05)
        
        nx.draw_networkx_labels(ego_graph, label_pos, labels, ax=self.ax,
                               font_size=10, 
                               font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", 
                                       facecolor='white', 
                                       edgecolor='none',
                                       alpha=0.8))
        
        # Estadísticas del ego graph
        num_conexiones_directas = len(list(self.grafo.neighbors(self.ego_user_id)))
        stats_text = f"Red de: {self.grafo.nodes[self.ego_user_id]['label']} | Conexiones: {num_conexiones_directas}"
        
        self.ax.set_title(f"Red Personal - {num_nodes} Personas, {ego_graph.number_of_edges()} Conexiones\n"
                         f"Layout: Spring (Simulación física)", 
                         fontsize=14, fontweight='bold', pad=20)
        self.ax.axis('off')
        self.ax.margins(0.1)
        
        # Mostrar estadísticas en la gráfica
        self.ax.text(0.5, 1.05, stats_text, ha='center', va='center',
                    transform=self.ax.transAxes, fontsize=12, color='black')
        
        self.canvas.draw()
    
    def actualizar_informacion(self):
        """Actualizar panel de información"""
        # Si estamos en modo ego network, mostrar información específica
        if getattr(self, 'ego_mode', False) and getattr(self, 'ego_user_id', None):
            self.mostrar_info_ego_network()
            return
        
        # Modo normal - mostrar estadísticas generales
        num_personas = self.grafo.number_of_nodes()
        num_conexiones = self.grafo.number_of_edges()
        
        # Calcular estadísticas adicionales
        if num_personas > 0:
            densidad = nx.density(self.grafo)
            grado_promedio = sum(dict(self.grafo.degree()).values()) / num_personas
            componentes = nx.number_connected_components(self.grafo)
            
            stats_text = (f"Personas: {num_personas} | Conexiones: {num_conexiones}\n"
                         f"Densidad: {densidad:.3f} | Grado promedio: {grado_promedio:.1f}")
            
            additional_info = (f"Componentes conectados: {componentes}\n"
                             f"¿Red conectada?: {'Sí' if nx.is_connected(self.grafo) else 'No'}")
        else:
            stats_text = "No hay datos en la red"
            additional_info = "Usa la pestaña 'Personas' para agregar usuarios"
        
        self.stats_label.config(text=stats_text)
        if hasattr(self, 'info_adicional_label'):
            self.info_adicional_label.config(text=additional_info)
        
        # Actualizar información detallada
        self.personas_text.delete(1.0, tk.END)
        
        if self.grafo.nodes:
            # Ordenar por número de conexiones (más conectados primero)
            personas_ordenadas = sorted(self.grafo.nodes(data=True), 
                                      key=lambda x: len(x[1].get('amigos', [])), 
                                      reverse=True)
            
            for node_id, data in personas_ordenadas:
                intereses = ", ".join(data.get('intereses', []))
                amigos_count = len(data.get('amigos', []))
                edad = data.get('edad', 0)
                email = data.get('email', 'No especificado')
                
                # Indicador visual según conectividad
                if amigos_count > 8:
                    icono = "🔴"  # Muy conectado
                elif amigos_count > 4:
                    icono = "🟡"  # Bien conectado
                elif amigos_count > 0:
                    icono = "🔵"  # Pocas conexiones
                else:
                    icono = "⚪"  # Aislado
                
                info = f"{icono} {data['label']} (ID: {node_id})\n"
                info += f"   Edad: {edad} | Email: {email}\n"
                info += f"   Conexiones: {amigos_count}\n"
                info += f"   Intereses: [{intereses}]\n\n"
                
                self.personas_text.insert(tk.END, info)
        else:
            self.personas_text.insert(tk.END, "No hay personas en la red.\n\n")
            self.personas_text.insert(tk.END, "📝 Para comenzar:\n")
            self.personas_text.insert(tk.END, "1. Ve a la pestaña 'Personas'\n")
            self.personas_text.insert(tk.END, "2. Llena el formulario con los datos\n")
            self.personas_text.insert(tk.END, "3. Haz clic en 'Agregar Persona'\n")
            self.personas_text.insert(tk.END, "4. Las conexiones se crearán automáticamente\n")
            self.personas_text.insert(tk.END, "   según intereses comunes")
    
    def mostrar_info_ego_network(self):
        """Mostrar información específica del ego network"""
        user_data = self.grafo.nodes[self.ego_user_id]
        ego_graph = nx.ego_graph(self.grafo, self.ego_user_id, radius=1)
        
        # Estadísticas del ego network
        num_conexiones_directas = len(list(self.grafo.neighbors(self.ego_user_id)))
        stats_text = f"Red de: {user_data['label']} | Conexiones: {num_conexiones_directas}"
        
        if hasattr(self, 'info_adicional_label'):
            self.info_adicional_label.config(text=f"Modo: Red Personal (Ego Network)")
        
        self.stats_label.config(text=stats_text)
        
        # Limpiar área de información
        self.personas_text.delete(1.0, tk.END)
        
        # Información detallada del usuario central
        intereses = ", ".join(user_data.get('intereses', []))
        edad = user_data.get('edad', 0)
        email = user_data.get('email', 'No especificado')
        
        info = f"👤 USUARIO CENTRAL:\n"
        info += f"━━━━━━━━━━━━━━━━━━━━\n"
        info += f"• {user_data['label']} (ID: {self.ego_user_id})\n"
        info += f"  Edad: {edad}\n"
        info += f"  Email: {email}\n"
        info += f"  Intereses: [{intereses}]\n"
        info += f"  Total de conexiones: {num_conexiones_directas}\n\n"
        
        info += f"🔗 CONEXIONES DIRECTAS ({num_conexiones_directas}):\n"
        info += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if num_conexiones_directas > 0:
            # Ordenar conexiones por intereses comunes
            conexiones_info = []
            for neighbor_id in self.grafo.neighbors(self.ego_user_id):
                neighbor_data = self.grafo.nodes[neighbor_id]
                user_int = set(user_data.get('intereses', []))
                neighbor_int = set(neighbor_data.get('intereses', []))
                comunes = user_int.intersection(neighbor_int)
                conexiones_info.append((neighbor_id, neighbor_data, comunes))
            
            # Ordenar por número de intereses comunes
            conexiones_info.sort(key=lambda x: len(x[2]), reverse=True)
            
            for neighbor_id, neighbor_data, comunes in conexiones_info:
                neighbor_intereses = ", ".join(neighbor_data.get('intereses', []))
                
                # Icono según intereses comunes
                if len(comunes) >= 3:
                    icono = "🌟"  # Muchos intereses comunes
                elif len(comunes) >= 2:
                    icono = "⭐"   # Algunos intereses comunes
                elif len(comunes) >= 1:
                    icono = "✨"   # Pocos intereses comunes
                else:
                    icono = "⚪"   # Sin intereses comunes
                
                info += f"{icono} {neighbor_data['label']} (ID: {neighbor_id})\n"
                info += f"    Edad: {neighbor_data.get('edad', 0)}\n"
                info += f"    Intereses: [{neighbor_intereses}]\n"
                
                if comunes:
                    info += f"    💫 Intereses comunes: {', '.join(comunes)}\n"
                else:
                    info += f"    ⚪ Sin intereses comunes\n"
                info += "\n"
        else:
            info += "  No tiene conexiones directas.\n"
            info += "  💡 Sugerencia: Agrega intereses similares a otras personas\n"
            info += "     para crear conexiones automáticas.\n"
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = RedSocialGUI(root)
    app.actualizar_informacion()  # Actualizar información inicial
    root.mainloop()