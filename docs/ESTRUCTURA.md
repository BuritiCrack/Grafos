# Estructura del Proyecto - Red Social con Grafos

## Organizacion Completa

```
Grafos/
├── src/                                    # Codigo fuente principal
│   ├── __init__.py                        # Paquete principal
│   │
│   ├── models/                            # Modelos de datos
│   │   ├── __init__.py
│   │   └── usuario.py                     # Clase Usuario (dataclass)
│   │
│   ├── services/                          # Logica de negocio
│   │   ├── __init__.py
│   │   ├── red_social_service.py         # Servicio principal (Service Layer)
│   │   ├── data_manager.py               # Persistencia (Repository Pattern)
│   │   ├── recomendador.py               # Sistema de recomendaciones
│   │   └── analizador_red.py             # Analisis de metricas
│   │
│   ├── ui/                                # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── red_social_gui_refactored.py  # Vista (Tkinter GUI)
│   │   └── gui_controller.py             # Controlador (MVC)
│   │
│   └── utils/                             # Utilidades
│       ├── __init__.py
│       └── visualizador.py               # Visualizacion de grafos
│
├── data/                                  # Datos persistentes
│   ├── usuarios.json                     # Base de datos de usuarios
│   └── Conexiones.json                   # Conexiones entre usuarios
│
├── docs/                                  # Documentacion
│   ├── README.md                         # Documentacion del proyecto
│   ├── ESTRUCTURA.md                     # Este archivo
│   └── REFACTORING_GUIDE.md              # Guia de refactorizacion
│
├── tests/                                 # Pruebas unitarias
│   └── README.md                         # Documentacion de tests
│
├── launch_refactored.py                   # Punto de entrada
├── verify_structure.py                    # Script de verificacion
├── fix_encoding.py                        # Script para corregir encoding
├── requirements.txt                       # Dependencias
└── README.md                              # README principal

```

## Descripcion de Componentes

### Modelos (src/models/)

**usuario.py**
- Clase `Usuario` usando dataclass
- Propiedades: id, nombre, edad, email, intereses, amigos
- Metodos de negocio: agregar_amigo, tiene_interes_comun, to_dict, from_dict

### Servicios (src/services/)

**red_social_service.py**
- `RedSocialService`: Servicio principal
- Maneja el grafo de NetworkX
- Coordina todas las operaciones de negocio
- CRUD de usuarios y conexiones

**data_manager.py**
- `DataManager`: Manejo de persistencia
- Carga y guarda datos en JSON
- Patron Repository para abstraer almacenamiento

**recomendador.py**
- `RecomendadorConexiones`: Sistema de recomendaciones
- Calcula compatibilidad entre usuarios
- Basado en intereses comunes y edad

**analizador_red.py**
- `AnalizadorRed`: Analisis de metricas
- Centralidad, comunidades, estadisticas
- Algoritmo de Louvain para deteccion de comunidades

### Interfaz (src/ui/)

**red_social_gui_refactored.py**
- `RedSocialGUIRefactored`: Vista principal
- Solo maneja presentacion (Tkinter)
- Pestanas: Personas, Conexiones, Recomendaciones, Informacion, Configuracion

**gui_controller.py**
- `GUIController`: Controlador MVC
- Conecta la vista con los servicios
- Maneja eventos y actualizaciones

### Utilidades (src/utils/)

**visualizador.py**
- `VisualizadorGrafo`: Renderizado de grafos
- `ShellLayout`, `SpringLayout`, `CircularLayout`
- Patron Strategy para diferentes layouts

## Patrones de Diseno Implementados

1. **MVC (Model-View-Controller)**
   - Model: Usuario, RedSocialService
   - View: RedSocialGUIRefactored
   - Controller: GUIController

2. **Service Layer**
   - RedSocialService encapsula logica de negocio
   - Desacopla UI de la logica

3. **Repository Pattern**
   - DataManager abstrae persistencia
   - Facilita cambiar el almacenamiento

4. **Strategy Pattern**
   - Diferentes layouts de visualizacion
   - Diferentes estrategias de recomendacion

## Flujo de Datos

```
Usuario interactua con GUI
         ↓
    GUIController
         ↓
  RedSocialService
         ↓
    ┌─────┴─────┬──────────┬──────────┐
    ↓           ↓          ↓          ↓
DataManager  Recomendador  AnalizadorRed  Visualizador
    ↓
archivos JSON
```

## Dependencias entre Modulos

```
ui/
├── gui_controller.py
│   ├── → services/red_social_service.py
│   ├── → models/usuario.py
│   └── → utils/visualizador.py
│
└── red_social_gui_refactored.py
    └── → ui/gui_controller.py

services/
├── red_social_service.py
│   ├── → models/usuario.py
│   ├── → services/data_manager.py
│   ├── → services/recomendador.py
│   └── → services/analizador_red.py
│
├── recomendador.py
│   └── → models/usuario.py
│
└── analizador_red.py
    └── → models/usuario.py
```

## Configuracion de Imports

Todos los imports usan rutas relativas desde src/:
```python
from models.usuario import Usuario
from services.red_social_service import RedSocialService
from ui.gui_controller import GUIController
from utils.visualizador import VisualizadorGrafo
```

El archivo `launch_refactored.py` agrega src/ al path:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
```

## Archivos de Configuracion

**requirements.txt**
```
networkx>=3.0
matplotlib>=3.5
```

## Buenas Practicas Implementadas

- Separacion de responsabilidades
- Sin codigo duplicado
- Nombres descriptivos en ingles
- Sin tildes ni ñ en el codigo
- Docstrings en todas las clases y metodos
- Type hints en funciones principales
- Encoding UTF-8 declarado
- Manejo de errores

## Como Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicacion
python launch_refactored.py
```

## Proximos Pasos

1. Agregar tests unitarios en tests/
2. Implementar logging
3. Agregar validacion de datos mas robusta
4. Crear API REST (opcional)
5. Dockerizar la aplicacion (opcional)
