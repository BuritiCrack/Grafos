# 🌐 Red Social - Sistema de Grafos

Una aplicación de escritorio desarrollada en Python que implementa una **red social basada en grafos** utilizando NetworkX, Tkinter y Matplotlib. Este sistema permite gestionar usuarios, crear conexiones automáticas basadas en intereses comunes y generar recomendaciones inteligentes de nuevas conexiones.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionalidades Principales](#funcionalidades-principales)
- [Algoritmos Implementados](#algoritmos-implementados)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Contribución](#contribución)
- [Licencia](#licencia)

## ✨ Características

### 🎯 **Gestión de Usuarios**
- ➕ Agregar nuevos usuarios con información personal (nombre, edad, email, intereses)
- 📊 Visualizar lista de usuarios con estadísticas de conectividad
- 🔍 Búsqueda de usuarios por nombre
- 🗑️ Interfaz intuitiva con validación de datos

### 🔗 **Sistema de Conexiones**
- 🤖 **Conexiones Automáticas**: Se crean automáticamente entre usuarios con intereses comunes
- 🔧 **Conexiones Manuales**: Permite crear conexiones específicas entre usuarios
- 📈 Visualización de conexiones existentes con intereses compartidos
- 🎨 Diferentes tipos de layouts de visualización

### 💡 **Sistema de Recomendaciones Inteligentes**
- 🧠 Algoritmo de recomendaciones basado en:
  - **Intereses comunes** (factor principal)
  - **Similitud de edad** (±5 años)
  - **Diversidad de intereses**
- ⭐ Puntuación de compatibilidad (0-100%)
- 📊 Top 10 recomendaciones ordenadas por relevancia
- 🔗 Creación rápida de conexiones recomendadas

### 📊 **Análisis de Red**
- 📈 **Métricas de Centralidad**: Grado y cercanía
- 🎯 **Detección de Comunidades**: Algoritmo de Louvain
- 📋 Estadísticas detalladas del grafo (densidad, grado promedio, conectividad)
- 👁️ Visualización de redes personales (Ego Networks)

### 🎨 **Visualización Avanzada**
- 🖼️ Gráficos interactivos con Matplotlib
- 🔵 Nodos con colores según nivel de conectividad
- 📏 Aristas con grosor variable
- 🏷️ Etiquetas optimizadas para evitar superposición
- 🔍 Zoom y navegación con toolbar integrado

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje de programación principal
- **NetworkX** - Biblioteca para análisis y manipulación de grafos
- **Tkinter** - Interfaz gráfica de usuario (GUI)
- **Matplotlib** - Visualización de grafos y gráficos
- **NumPy** - Cálculos matemáticos y manejo de arrays
- **JSON** - Persistencia de datos

## 💻 Requisitos del Sistema

### Dependencias Python:
```bash
networkx >= 2.8
matplotlib >= 3.5.0
numpy >= 1.21.0
tkinter (incluido en Python estándar)
json (incluido en Python estándar)
```

### Sistema Operativo:
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/red-social-grafos.git
cd red-social-grafos
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install networkx matplotlib numpy
```

### 4. Ejecutar la aplicación
```bash
python red_social_gui.py
```

## 🎮 Uso

### Inicio Rápido

1. **Ejecuta la aplicación**:
   ```bash
   python red_social_gui.py
   ```

2. **Agrega usuarios**:
   - Ve a la pestaña "👤 Personas"
   - Completa el formulario (nombre, edad, email, intereses)
   - Haz clic en "➕ Agregar Persona"

3. **Explora conexiones**:
   - Las conexiones se crean automáticamente por intereses comunes
   - Ve a "🔗 Conexiones" para crear conexiones manuales

4. **Obtén recomendaciones**:
   - Ve a "👁️ Recomendaciones"
   - Ingresa un ID de usuario o busca por nombre
   - Revisa las sugerencias inteligentes de conexión

5. **Analiza la red**:
   - Ve a "⚙️ Configuración" para análisis avanzados
   - Calcula centralidad y detecta comunidades

### Datos de Ejemplo

La aplicación incluye archivos de datos de ejemplo:
- `usuarios.json` - Usuarios predefinidos con información completa
- `conexiones.json` - Conexiones existentes entre usuarios

## 📁 Estructura del Proyecto

```
red-social-grafos/
├── red_social_gui.py          # Aplicación principal
├── usuarios.json              # Datos de usuarios
├── conexiones.json           # Datos de conexiones
├── README.md                 # Documentación
└── requirements.txt          # Dependencias (opcional)
```

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `red_social_gui.py` | Interfaz gráfica principal y lógica de la aplicación |
| `usuarios.json` | Base de datos JSON con información de usuarios |
| `conexiones.json` | Base de datos JSON con las conexiones entre usuarios |

## 🔧 Funcionalidades Principales

### 📱 Interfaz por Pestañas

#### 1. **👤 Personas**
- Formulario para agregar nuevos usuarios
- Lista interactiva de usuarios existentes
- Doble clic para ver red personal

#### 2. **🔗 Conexiones**
- Creación manual de conexiones
- Lista de conexiones con intereses comunes
- Selección por nombre o ID

#### 3. **👁️ Recomendaciones**
- Búsqueda de usuarios (ID o nombre)
- Sistema de recomendaciones inteligentes
- Creación rápida de conexiones

#### 4. **📊 Información**
- Estadísticas generales de la red
- Información detallada de usuarios
- Modo red personal (Ego Network)

#### 5. **⚙️ Configuración**
- Gestión de datos (guardar/cargar)
- Análisis de centralidad
- Detección de comunidades

## 🧮 Algoritmos Implementados

### Sistema de Recomendaciones
```python
def calcular_score_recomendacion(usuario, candidato):
    score = len(intereses_comunes)           # Base: intereses compartidos
    score += 0.5 if diversidad_intereses    # Bonus: diversidad
    score += 0.3 if edad_similar            # Bonus: edad ±5 años
    return score
```

### Layouts de Visualización
- **Shell Layout**: Organiza nodos por grado de conectividad
- **Spring Layout**: Simulación física para ego networks
- **Circular Layout**: Distribución circular para redes pequeñas

### Métricas de Red
- **Centralidad de Grado**: `nx.degree_centrality()`
- **Centralidad de Cercanía**: `nx.closeness_centrality()`
- **Detección de Comunidades**: `nx_comm.greedy_modularity_communities()`

## 📊 Capturas de Pantalla

### Interfaz Principal
La aplicación cuenta con una interfaz moderna dividida en pestañas:
- Panel izquierdo: Controles y opciones
- Panel derecho: Visualización interactiva del grafo

### Visualización de Red
- Nodos coloreados por nivel de conectividad:
  - 🔴 Rojo: Muy conectado (>8 conexiones)
  - 🟡 Verde-azul: Bien conectado (4-8 conexiones)  
  - 🔵 Azul: Pocas conexiones (1-4)
  - 🟡 Amarillo: Aislado (0 conexiones)

### Sistema de Recomendaciones
Muestra sugerencias detalladas con:
- Información del usuario
- Intereses comunes destacados
- Puntuación de compatibilidad
- Estadísticas del análisis

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas de Mejora
- [ ] Base de datos SQLite en lugar de JSON
- [ ] Interfaz web con Flask/Django
- [ ] Algoritmos de recomendación más sofisticados
- [ ] Exportación de grafos a diferentes formatos
- [ ] Análisis temporal de la evolución de la red

## 🐛 Reporte de Errores

Si encuentras algún error, por favor:
1. Verifica que tengas todas las dependencias instaladas
2. Revisa la versión de Python (3.8+ requerido)
3. Abre un issue con descripción detallada del problema


## 📧 Contacto

**Desarrollador**: [Tu Nombre]
- Email: tu.email@example.com
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

## 🙏 Agradecimientos

- **NetworkX Team** - Por la excelente biblioteca de análisis de grafos
- **Matplotlib Community** - Por las herramientas de visualización
- **Python Software Foundation** - Por el lenguaje y ecosistema

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐

*Desarrollado con ❤️ en Python*