# -*- coding: utf-8 -*-
# red_social_gui_refactored.py
"""
Interfaz grafica refactorizada usando el patron MVC
Solo maneja la presentacion, delegando la logica al controlador
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from ui.gui_controller import GUIController

class RedSocialGUIRefactored:
    
    
    def __init__(self, root):
        self.root = root
        self.controller = GUIController()
        self.controller.set_view(self)
        
        # Configurar ventana
        self.configurar_ventana()
        
        # Crear elementos de UI
        self.crear_interfaz()
        
        # Inicializar controlador y datos
        self.controller.inicializar()
        self.actualizar_tras_recarga()
    
    def configurar_ventana(self):
        """Configurar propiedades de la ventana principal"""
        self.root.title("Red Social - Sistema de Grafos (Refactorizado)")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        self.root.state('zoomed')
    
    def crear_interfaz(self):
        """Crear la interfaz grafica principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de las columnas y filas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel de control (izquierda)
        self.crear_panel_control(main_frame)
        
        # Panel de visualizacion (derecha)
        self.crear_panel_visualizacion(main_frame)
    
    def crear_panel_control(self, parent):
        """Crear panel de control con pestanas"""
        control_container = ttk.Frame(parent)
        control_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        control_container.columnconfigure(0, weight=1)
        control_container.rowconfigure(0, weight=1)
        
        # Notebook con pestanas
        self.notebook = ttk.Notebook(control_container)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Crear pestanas
        self.crear_tab_personas()
        self.crear_tab_conexiones() 
        self.crear_tab_recomendaciones()
        self.crear_tab_informacion()
        self.crear_tab_configuracion()
        
        # Vincular eventos
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def crear_tab_personas(self):
        """Pestana de gestion de personas"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="👤 Personas")
        
        # Formulario de agregar persona
        form_frame = ttk.LabelFrame(frame, text="Agregar Nueva Persona", padding="10")
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Campos
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = ttk.Entry(form_frame, width=25)
        self.nombre_entry.grid(row=0, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Edad:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.edad_entry = ttk.Entry(form_frame, width=25)
        self.edad_entry.grid(row=1, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(form_frame, width=25)
        self.email_entry.grid(row=2, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Intereses:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(form_frame, text="(separar con comas)", font=("Arial", 8)).grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        self.intereses_entry = ttk.Entry(form_frame, width=25)
        self.intereses_entry.grid(row=4, column=0, columnspan=2, pady=2, sticky=(tk.W, tk.E))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botones
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Button(buttons_frame, text="➕ Agregar Persona", 
                  command=self.on_agregar_persona).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="🗑️ Limpiar", 
                  command=self.limpiar_formulario_persona).pack(side=tk.LEFT)
        
        # Lista de personas
        lista_frame = ttk.LabelFrame(frame, text="Personas en la Red", padding="10")
        lista_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        columns = ('ID', 'Nombre', 'Edad', 'Conexiones')
        self.personas_tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.personas_tree.heading(col, text=col)
        
        self.personas_tree.column('ID', width=50, anchor='center')
        self.personas_tree.column('Nombre', width=120)
        self.personas_tree.column('Edad', width=60, anchor='center')
        self.personas_tree.column('Conexiones', width=80, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.personas_tree.yview)
        self.personas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.personas_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Doble clic para ver red personal
        self.personas_tree.bind('<Double-1>', self.on_persona_double_click)
    
    def crear_tab_conexiones(self):
        """Pestana de gestion de conexiones"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="🔗 Conexiones")
        
        # Formulario de conexion manual
        conn_frame = ttk.LabelFrame(frame, text="Crear Conexion Manual", padding="10")
        conn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(conn_frame, text="ID Persona 1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.persona1_entry = ttk.Entry(conn_frame, width=10)
        self.persona1_entry.grid(row=0, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(conn_frame, text="ID Persona 2:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.persona2_entry = ttk.Entry(conn_frame, width=10)
        self.persona2_entry.grid(row=1, column=1, pady=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        conn_frame.columnconfigure(1, weight=1)
        
        ttk.Button(conn_frame, text="🔗 Crear Conexion", 
                  command=self.on_crear_conexion).grid(row=2, column=0, columnspan=2, pady=15)
        
        # Lista de conexiones
        lista_frame = ttk.LabelFrame(frame, text="Conexiones Existentes", padding="10")
        lista_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        conn_columns = ('Persona 1', 'Persona 2', 'Intereses Comunes')
        self.conexiones_tree = ttk.Treeview(lista_frame, columns=conn_columns, show='headings', height=12)
        
        for col in conn_columns:
            self.conexiones_tree.heading(col, text=col)
            self.conexiones_tree.column(col, width=120)
        
        conn_scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.conexiones_tree.yview)
        self.conexiones_tree.configure(yscrollcommand=conn_scrollbar.set)
        
        self.conexiones_tree.pack(side=tk.LEFT, fill='both', expand=True)
        conn_scrollbar.pack(side=tk.RIGHT, fill='y')
    
    def crear_tab_recomendaciones(self):
        """Pestana de recomendaciones"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="👁️ Recomendaciones")
        
        # Seccion ego network
        ego_frame = ttk.LabelFrame(frame, text="Red Personal de Usuario", padding="10")
        ego_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(ego_frame, text="Ver red de usuario (ID):").pack(anchor="w")
        
        input_frame = ttk.Frame(ego_frame)
        input_frame.pack(fill="x", pady=5)
        
        self.ego_user_entry = ttk.Entry(input_frame, width=10)
        self.ego_user_entry.pack(side="left", padx=(0, 5))
        self.ego_user_entry.bind('<Return>', lambda e: self.on_mostrar_ego_network())
        
        ttk.Button(input_frame, text="🔍 Ver Red", 
                  command=self.on_mostrar_ego_network).pack(side="left", padx=(5, 0))
        
        # Buscar por nombre
        ttk.Label(ego_frame, text="O buscar por nombre:").pack(anchor="w", pady=(10, 0))
        search_frame = ttk.Frame(ego_frame)
        search_frame.pack(fill="x", pady=5)
        
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.on_buscar_usuario())
        
        ttk.Button(search_frame, text="🔍 Buscar", 
                  command=self.on_buscar_usuario).pack(side="left")
        
        ttk.Button(ego_frame, text="🌐 Ver Red Completa", 
                  command=self.on_mostrar_red_completa).pack(fill="x", pady=(15, 0))
        
        # Recomendaciones
        recom_frame = ttk.LabelFrame(frame, text="💡 Recomendaciones de Conexiones", padding="10")
        recom_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        ttk.Label(recom_frame, 
                 text="Las recomendaciones apareceran aqui cuando veas la red personal de un usuario.",
                 font=("Arial", 9, "italic"), foreground="gray").pack(anchor="w", pady=(0, 10))
        
        self.recomendaciones_text = scrolledtext.ScrolledText(recom_frame, height=12, width=50, wrap=tk.WORD)
        self.recomendaciones_text.pack(fill="both", expand=True)
        
        # Frame para crear conexion recomendada
        self.crear_recom_frame = ttk.Frame(recom_frame)
        
        ttk.Label(self.crear_recom_frame, text="Crear conexion con usuario ID:").pack(side="left")
        self.recom_id_entry = ttk.Entry(self.crear_recom_frame, width=8)
        self.recom_id_entry.pack(side="left", padx=(5, 5))
        
        self.btn_crear_recom = ttk.Button(self.crear_recom_frame, text="🔗 Conectar", 
                                         command=self.on_crear_conexion_recomendada, state="disabled")
        self.btn_crear_recom.pack(side="left", padx=(5, 0))
    
    def crear_tab_informacion(self):
        """Pestana de informacion"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="📊 Informacion")
        
        # Estadisticas
        stats_frame = ttk.LabelFrame(frame, text="Estadisticas del Grafo", padding="10")
        stats_frame.pack(fill="x", pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack(anchor="w")
        
        self.info_adicional_label = ttk.Label(stats_frame, text="", font=("Arial", 9))
        self.info_adicional_label.pack(anchor="w", pady=(5, 0))
        
        # Informacion detallada
        ttk.Label(frame, text="Informacion Detallada:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        self.info_text = scrolledtext.ScrolledText(frame, height=15, width=40, wrap=tk.WORD)
        self.info_text.pack(fill="both", expand=True)
    
    def crear_tab_configuracion(self):
        """Pestana de configuracion"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="⚙️ Configuracion")
        
        # Gestion de datos
        datos_frame = ttk.LabelFrame(frame, text="Gestion de Datos", padding="10")
        datos_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(datos_frame, text="💾 Guardar Datos", 
                  command=self.controller.guardar_datos).pack(fill="x", pady=2)
        ttk.Button(datos_frame, text="📂 Recargar Datos", 
                  command=self.controller.recargar_datos).pack(fill="x", pady=2)
        
        # Analisis
        analisis_frame = ttk.LabelFrame(frame, text="Analisis de Red", padding="10")
        analisis_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(analisis_frame, text="📈 Calcular Centralidad", 
                  command=self.on_calcular_centralidad).pack(fill="x", pady=2)
        ttk.Button(analisis_frame, text="🎯 Detectar Comunidades", 
                  command=self.on_detectar_comunidades).pack(fill="x", pady=2)
        
        # Resultados
        self.analisis_text = scrolledtext.ScrolledText(frame, height=12, width=40, wrap=tk.WORD)
        self.analisis_text.pack(fill="both", expand=True, pady=(10, 0))
    
    def crear_panel_visualizacion(self, parent):
        """Crear panel de visualizacion"""
        viz_frame = ttk.LabelFrame(parent, text="Visualizacion del Grafo", padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Figura de matplotlib
        self.fig = Figure(figsize=(14, 10), dpi=120, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        self.fig.tight_layout(pad=3.0)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar_frame = ttk.Frame(viz_frame)
        toolbar_frame.pack(fill="x", pady=(5, 0))
        
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
    
    # === EVENTOS DE UI ===
    
    def on_agregar_persona(self):
        """Manejar agregar persona"""
        if self.controller.agregar_usuario(
            self.nombre_entry.get(),
            self.edad_entry.get(), 
            self.email_entry.get(),
            self.intereses_entry.get()
        ):
            self.limpiar_formulario_persona()
    
    def on_crear_conexion(self):
        """Manejar crear conexion manual"""
        self.controller.crear_conexion_manual(
            self.persona1_entry.get(),
            self.persona2_entry.get()
        )
        
        # Limpiar campos
        self.persona1_entry.delete(0, tk.END)
        self.persona2_entry.delete(0, tk.END)
    
    def on_mostrar_ego_network(self):
        """Manejar mostrar ego network"""
        if self.controller.mostrar_ego_network(self.ego_user_entry.get()):
            self.mostrar_recomendaciones(int(self.ego_user_entry.get()))
    
    def on_buscar_usuario(self):
        """Manejar busqueda de usuario"""
        self.controller.buscar_y_mostrar_usuario(self.search_entry.get())
    
    def on_mostrar_red_completa(self):
        """Manejar mostrar red completa"""
        self.controller.mostrar_red_completa()
        self.crear_recom_frame.pack_forget()
        self.recomendaciones_text.delete(1.0, tk.END)
        self.recomendaciones_text.insert(tk.END, "Selecciona un usuario para ver recomendaciones.")
    
    def on_crear_conexion_recomendada(self):
        """Manejar crear conexion recomendada"""
        if self.controller.ego_user_id:
            if self.controller.crear_conexion_recomendada(
                self.controller.ego_user_id,
                self.recom_id_entry.get()
            ):
                self.recom_id_entry.delete(0, tk.END)
                self.actualizar_visualizacion()
                self.mostrar_recomendaciones(self.controller.ego_user_id)
    
    def on_persona_double_click(self, event):
        """Manejar doble clic en persona"""
        selection = self.personas_tree.selection()
        if selection:
            item = self.personas_tree.item(selection[0])
            user_id = item['values'][0]
            
            self.notebook.select(2)  # Pestana recomendaciones
            self.ego_user_entry.delete(0, tk.END)
            self.ego_user_entry.insert(0, str(user_id))
            
            if self.controller.mostrar_ego_network(str(user_id)):
                self.mostrar_recomendaciones(user_id)
    
    def on_tab_changed(self, event):
        """Manejar cambio de pestana"""
        selected_tab = event.widget.tab('current')['text']
        
        if "Personas" in selected_tab:
            self.actualizar_lista_personas()
        elif "Conexiones" in selected_tab:
            self.actualizar_lista_conexiones()
        elif "Informacion" in selected_tab:
            self.actualizar_informacion()
    
    def on_calcular_centralidad(self):
        """Manejar calcular centralidad"""
        resultados = self.controller.calcular_centralidad()
        if resultados:
            self.mostrar_resultados_centralidad(resultados)
    
    def on_detectar_comunidades(self):
        """Manejar detectar comunidades"""
        comunidades = self.controller.detectar_comunidades()
        if comunidades:
            self.mostrar_resultados_comunidades(comunidades)
    
    # === METODOS DE ACTUALIZACION ===
    
    def actualizar_tras_cambio(self):
        """Actualizar despues de un cambio en los datos"""
        self.actualizar_visualizacion()
        self.actualizar_lista_personas()
        self.actualizar_lista_conexiones()
        self.actualizar_informacion()
    
    def actualizar_tras_recarga(self):
        """Actualizar despues de recargar datos"""
        self.limpiar_campos_ego()
        self.actualizar_tras_cambio()
    
    def actualizar_visualizacion(self):
        """Actualizar visualizacion del grafo"""
        usuarios_data = {u.id: {'label': u.nombre} for u in self.controller.obtener_todos_usuarios()}
        self.controller.renderizar_grafo(self.ax, usuarios_data)
        self.canvas.draw()
    
    def actualizar_lista_personas(self):
        """Actualizar lista de personas"""
        # Limpiar
        for item in self.personas_tree.get_children():
            self.personas_tree.delete(item)
        
        # Agregar usuarios actuales
        for usuario in self.controller.obtener_todos_usuarios():
            self.personas_tree.insert('', 'end', values=(
                usuario.id, usuario.nombre, usuario.edad, len(usuario.amigos)
            ))
    
    def actualizar_lista_conexiones(self):
        """Actualizar lista de conexiones"""
        # Limpiar
        for item in self.conexiones_tree.get_children():
            self.conexiones_tree.delete(item)
        
        # Agregar conexiones actuales
        for usuario1, usuario2, intereses_comunes in self.controller.obtener_conexiones():
            comunes_str = ', '.join(intereses_comunes) if intereses_comunes else 'Ninguno'
            self.conexiones_tree.insert('', 'end', values=(
                usuario1.nombre, usuario2.nombre, comunes_str
            ))
    
    def actualizar_informacion(self):
        """Actualizar panel de informacion"""
        self.info_text.delete(1.0, tk.END)
        
        if self.controller.esta_en_modo_ego():
            self.mostrar_info_ego_network()
        else:
            self.mostrar_info_general()
    
    def mostrar_info_general(self):
        """Mostrar informacion general de la red"""
        stats = self.controller.obtener_estadisticas()
        
        stats_text = (f"Personas: {stats['num_personas']} | Conexiones: {stats['num_conexiones']}\n"
                     f"Densidad: {stats['densidad']:.3f} | Grado promedio: {stats['grado_promedio']:.1f}")
        
        additional_info = (f"Componentes conectados: {stats['componentes_conectados']}\n"
                          f"¿Red conectada?: {'Si' if stats['es_conectado'] else 'No'}")
        
        self.stats_label.config(text=stats_text)
        self.info_adicional_label.config(text=additional_info)
        
        # Informacion detallada de usuarios
        usuarios = sorted(self.controller.obtener_todos_usuarios(), 
                         key=lambda u: len(u.amigos), reverse=True)
        
        for usuario in usuarios:
            intereses = ", ".join(usuario.intereses)
            amigos_count = len(usuario.amigos)
            
            # Icono segun conectividad
            if amigos_count > 8:
                icono = "🔴"
            elif amigos_count > 4:
                icono = "🟡"
            elif amigos_count > 0:
                icono = "🔵"
            else:
                icono = "⚪"
            
            info = f"{icono} {usuario.nombre} (ID: {usuario.id})\n"
            info += f"   Edad: {usuario.edad} | Email: {usuario.email}\n"
            info += f"   Conexiones: {amigos_count}\n"
            info += f"   Intereses: [{intereses}]\n\n"
            
            self.info_text.insert(tk.END, info)
    
    def mostrar_info_ego_network(self):
        """Mostrar informacion del ego network"""
        usuario = self.controller.obtener_usuario_ego()
        if not usuario:
            return
        
        stats_text = f"Red de: {usuario.nombre} | Conexiones: {len(usuario.amigos)}"
        self.stats_label.config(text=stats_text)
        self.info_adicional_label.config(text="Modo: Red Personal (Ego Network)")
        
        # Informacion detallada del usuario central
        intereses = ", ".join(usuario.intereses)
        
        info = f"👤 USUARIO CENTRAL:\n"
        info += f"━━━━━━━━━━━━━━━━━━━━\n"
        info += f"• {usuario.nombre} (ID: {usuario.id})\n"
        info += f"  Edad: {usuario.edad}\n"
        info += f"  Email: {usuario.email}\n"
        info += f"  Intereses: [{intereses}]\n"
        info += f"  Total de conexiones: {len(usuario.amigos)}\n\n"
        
        # Informacion de conexiones
        info += f"🔗 CONEXIONES DIRECTAS ({len(usuario.amigos)}):\n"
        info += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if usuario.amigos:
            todos_usuarios = {u.id: u for u in self.controller.obtener_todos_usuarios()}
            
            conexiones_info = []
            for amigo_id in usuario.amigos:
                if amigo_id in todos_usuarios:
                    amigo = todos_usuarios[amigo_id]
                    comunes = usuario.intereses_comunes(amigo)
                    conexiones_info.append((amigo, comunes))
            
            # Ordenar por intereses comunes
            conexiones_info.sort(key=lambda x: len(x[1]), reverse=True)
            
            for amigo, comunes in conexiones_info:
                amigo_intereses = ", ".join(amigo.intereses)
                
                # Icono segun intereses comunes
                if len(comunes) >= 3:
                    icono = "🌟"
                elif len(comunes) >= 2:
                    icono = "⭐"
                elif len(comunes) >= 1:
                    icono = "✨"
                else:
                    icono = "⚪"
                
                info += f"{icono} {amigo.nombre} (ID: {amigo.id})\n"
                info += f"    Edad: {amigo.edad}\n"
                info += f"    Intereses: [{amigo_intereses}]\n"
                
                if comunes:
                    info += f"    💫 Intereses comunes: {', '.join(comunes)}\n"
                else:
                    info += f"    ⚪ Sin intereses comunes\n"
                info += "\n"
        else:
            info += "  No tiene conexiones directas.\n"
        
        self.info_text.insert(tk.END, info)
    
    def mostrar_recomendaciones(self, usuario_id: int):
        """Mostrar recomendaciones para un usuario"""
        recomendaciones = self.controller.obtener_recomendaciones(usuario_id)
        
        self.recomendaciones_text.delete(1.0, tk.END)
        
        if recomendaciones:
            usuario = self.controller.obtener_usuario(usuario_id)
            self.recomendaciones_text.insert(tk.END, f"💡 RECOMENDACIONES PARA: {usuario.nombre}\n")
            self.recomendaciones_text.insert(tk.END, "="*50 + "\n\n")
            
            for i, recom in enumerate(recomendaciones[:10], 1):
                # Icono segun puntuacion
                if recom['score'] >= 3:
                    icono = "🌟"
                elif recom['score'] >= 2:
                    icono = "⭐"
                else:
                    icono = "✨"
                
                self.recomendaciones_text.insert(tk.END, f"{icono} {i}. {recom['nombre']} (ID: {recom['id']})\n")
                self.recomendaciones_text.insert(tk.END, f"     Edad: {recom['edad']}\n")
                self.recomendaciones_text.insert(tk.END, f"     Email: {recom['email']}\n")
                
                if recom['intereses_comunes']:
                    comunes_str = ', '.join(recom['intereses_comunes'])
                    self.recomendaciones_text.insert(tk.END, f"     💫 Intereses comunes: {comunes_str}\n")
                
                todos_intereses = ', '.join(recom['intereses'])
                self.recomendaciones_text.insert(tk.END, f"     🏷️ Todos sus intereses: {todos_intereses}\n")
                
                self.recomendaciones_text.insert(tk.END, f"     📊 Compatibilidad: {recom['compatibilidad']}%\n\n")
            
            if len(recomendaciones) > 10:
                self.recomendaciones_text.insert(tk.END, f"... y {len(recomendaciones) - 10} recomendaciones mas.\n")
            
            # Mostrar frame para crear conexion
            self.crear_recom_frame.pack(fill="x", pady=(10, 0))
            self.btn_crear_recom.config(state="normal")
        else:
            usuario = self.controller.obtener_usuario(usuario_id)
            self.recomendaciones_text.insert(tk.END, f"🤔 NO HAY RECOMENDACIONES PARA: {usuario.nombre}\n")
            self.recomendaciones_text.insert(tk.END, "="*50 + "\n\n")
            self.recomendaciones_text.insert(tk.END, "No se encontraron usuarios con intereses similares\n")
            self.crear_recom_frame.pack_forget()
    
    def mostrar_resultados_centralidad(self, resultados):
        """Mostrar resultados del analisis de centralidad"""
        self.notebook.select(4)  # Pestana configuracion
        
        self.analisis_text.delete(1.0, tk.END)
        self.analisis_text.insert(tk.END, "📈 ANALISIS DE CENTRALIDAD\n" + "="*40 + "\n\n")
        
        # Centralidad de grado
        self.analisis_text.insert(tk.END, "🎯 CENTRALIDAD DE GRADO:\n")
        for i, item in enumerate(resultados['grado'], 1):
            self.analisis_text.insert(tk.END, f"{i}. {item['usuario']} (ID: {item['id']}): {item['centralidad']:.3f}\n")
        
        # Centralidad de cercania
        if resultados['cercania']:
            self.analisis_text.insert(tk.END, "\n🎯 CENTRALIDAD DE CERCANIA:\n")
            for i, item in enumerate(resultados['cercania'], 1):
                self.analisis_text.insert(tk.END, f"{i}. {item['usuario']} (ID: {item['id']}): {item['centralidad']:.3f}\n")
        else:
            self.analisis_text.insert(tk.END, "\n⚠️ El grafo no esta completamente conectado para calcular centralidad de cercania.\n")
    
    def mostrar_resultados_comunidades(self, comunidades):
        """Mostrar resultados de deteccion de comunidades"""
        self.notebook.select(4)  # Pestana configuracion
        
        self.analisis_text.delete(1.0, tk.END)
        self.analisis_text.insert(tk.END, "🎯 DETECCION DE COMUNIDADES\n" + "="*40 + "\n\n")
        
        self.analisis_text.insert(tk.END, f"Se encontraron {len(comunidades)} comunidades:\n\n")
        
        for i, comunidad in enumerate(comunidades, 1):
            self.analisis_text.insert(tk.END, f"📍 COMUNIDAD {i} ({len(comunidad)} miembros):\n")
            for usuario in comunidad:
                self.analisis_text.insert(tk.END, f"  • {usuario.nombre} (ID: {usuario.id})\n")
            self.analisis_text.insert(tk.END, "\n")
    
    # === METODOS AUXILIARES ===
    
    def limpiar_formulario_persona(self):
        """Limpiar formulario de persona"""
        self.nombre_entry.delete(0, tk.END)
        self.edad_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.intereses_entry.delete(0, tk.END)
    
    def limpiar_campos_ego(self):
        """Limpiar campos de ego network"""
        self.ego_user_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        if hasattr(self, 'crear_recom_frame'):
            self.crear_recom_frame.pack_forget()
    
    def cambiar_a_pestana_informacion(self):
        """Cambiar a la pestana de recomendaciones"""
        self.notebook.select(2)  # Indice 2 = Pestana de Recomendaciones

if __name__ == "__main__":
    root = tk.Tk()
    app = RedSocialGUIRefactored(root)
    root.mainloop()
