# 🌐 Red Social - Sistema de Grafos

Una aplicación de escritorio desarrollada en Python que implementa una **red social basada en grafos** utilizando NetworkX, Tkinter y Matplotlib.

## 📁 Estructura del Proyecto

```
Grafos/
├── src/                          # Código fuente
│   ├── models/                   # Modelos de datos
│   │   ├── __init__.py
│   │   └── usuario.py           # Modelo Usuario
│   ├── services/                 # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── red_social_service.py    # Servicio principal
│   │   ├── data_manager.py          # Persistencia de datos
│   │   ├── recomendador.py          # Sistema de recomendaciones
│   │   └── analizador_red.py        # Análisis de métricas
│   ├── ui/                       # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── red_social_gui_refactored.py  # Vista principal
│   │   └── gui_controller.py             # Controlador MVC
│   └── utils/                    # Utilidades
│       ├── __init__.py
│       └── visualizador.py      # Visualización de grafos
├── data/                         # Archivos de datos
│   ├── usuarios.json            # Base de datos de usuarios
│   └── Conexiones.json          # Conexiones entre usuarios
├── docs/                         # Documentación
│   ├── README.md
│   └── REFACTORING_GUIDE.md
├── tests/                        # Pruebas unitarias (pendiente)
└── launch_refactored.py         # Punto de entrada de la aplicación
```

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC (Model-View-Controller)** con separación de responsabilidades:

### 📦 Modelos (`src/models/`)
- **Usuario**: Entidad de dominio con información personal y métodos de negocio

### ⚙️ Servicios (`src/services/`)
- **RedSocialService**: Service Layer que coordina toda la lógica
- **DataManager**: Repository Pattern para persistencia
- **Recomendador**: Strategy Pattern para recomendaciones
- **AnalizadorRed**: Análisis de métricas y comunidades

### 🖥️ Interfaz (`src/ui/`)
- **RedSocialGUIRefactored**: Vista (solo presentación)
- **GUIController**: Controlador que conecta vista con servicios

### 🔧 Utilidades (`src/utils/`)
- **Visualizador**: Renderizado de grafos con diferentes layouts

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Dependencias
```bash
pip install networkx matplotlib
```

## 💻 Uso

Para ejecutar la aplicación:

```bash
python launch_refactored.py
```

## ✨ Características

### 🎯 Gestión de Usuarios
- Agregar nuevos usuarios
- Visualizar lista con estadísticas
- Búsqueda por nombre
- Validación de datos

### 🔗 Sistema de Conexiones
- Conexiones automáticas por intereses comunes
- Conexiones manuales
- Visualización interactiva

### 💡 Recomendaciones Inteligentes
- Basadas en intereses comunes
- Similitud de edad
- Puntuación de compatibilidad
- Top 10 recomendaciones

### 📊 Análisis de Red
- Métricas de centralidad
- Detección de comunidades (Louvain)
- Estadísticas del grafo
- Visualización de Ego Networks

## 🛠️ Tecnologías

- **Python 3**: Lenguaje principal
- **NetworkX**: Manipulación de grafos
- **Tkinter**: Interfaz gráfica
- **Matplotlib**: Visualización
- **JSON**: Persistencia de datos

## 📚 Patrones de Diseño

- **MVC**: Separación vista-controlador-modelo
- **Service Layer**: Encapsulación de lógica de negocio
- **Repository Pattern**: Abstracción de persistencia
- **Strategy Pattern**: Múltiples estrategias de visualización y recomendación

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como proyecto educativo para demostrar el uso de grafos en Python.
