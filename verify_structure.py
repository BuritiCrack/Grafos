# -*- coding: utf-8 -*-
"""
Script de verificación de la estructura del proyecto
"""
import sys
import os

# Add src directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

print("=" * 70)
print("VERIFICACIÓN DE LA ESTRUCTURA DEL PROYECTO")
print("=" * 70)

# Test 1: Verificar estructura de carpetas
print("\n1. Verificando estructura de carpetas...")
folders = ['src', 'src/models', 'src/services', 'src/ui', 'src/utils', 'data', 'docs', 'tests']
for folder in folders:
    path = os.path.join(project_root, folder)
    status = "✓" if os.path.exists(path) else "✗"
    print(f"   {status} {folder}")

# Test 2: Verificar archivos principales
print("\n2. Verificando archivos principales...")
files = [
    'launch_refactored.py',
    'README.md',
    'requirements.txt',
    'src/__init__.py',
    'src/models/usuario.py',
    'src/services/red_social_service.py',
    'src/services/data_manager.py',
    'src/services/recomendador.py',
    'src/services/analizador_red.py',
    'src/ui/gui_controller.py',
    'src/ui/red_social_gui_refactored.py',
    'src/utils/visualizador.py',
    'data/usuarios.json',
    'data/Conexiones.json'
]
for file in files:
    path = os.path.join(project_root, file)
    status = "✓" if os.path.exists(path) else "✗"
    print(f"   {status} {file}")

# Test 3: Verificar imports
print("\n3. Verificando imports...")
try:
    from src.models.usuario import Usuario
    print("   ✓ models.usuario importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar models.usuario: {e}")

try:
    from src.services.red_social_service import RedSocialService
    print("   ✓ services.red_social_service importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar services.red_social_service: {e}")

try:
    from src.services.data_manager import DataManager
    print("   ✓ services.data_manager importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar services.data_manager: {e}")

try:
    from src.services.recomendador import RecomendadorConexiones
    print("   ✓ services.recomendador importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar services.recomendador: {e}")

try:
    from src.services.analizador_red import AnalizadorRed
    print("   ✓ services.analizador_red importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar services.analizador_red: {e}")

try:
    from src.utils.visualizador import VisualizadorGrafo
    print("   ✓ utils.visualizador importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar utils.visualizador: {e}")

try:
    from src.ui.gui_controller import GUIController
    print("   ✓ ui.gui_controller importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar ui.gui_controller: {e}")

# Test 4: Verificar datos
print("\n4. Verificando datos JSON...")
import json
try:
    with open(os.path.join(project_root, 'data', 'usuarios.json'), 'r', encoding='utf-8') as f:
        usuarios = json.load(f)
    print(f"   ✓ usuarios.json cargado ({len(usuarios)} usuarios)")
except Exception as e:
    print(f"   ✗ Error al cargar usuarios.json: {e}")

try:
    with open(os.path.join(project_root, 'data', 'Conexiones.json'), 'r', encoding='utf-8') as f:
        conexiones = json.load(f)
    print(f"   ✓ Conexiones.json cargado ({len(conexiones)} conexiones)")
except Exception as e:
    print(f"   ✗ Error al cargar Conexiones.json: {e}")

print("\n" + "=" * 70)
print("VERIFICACIÓN COMPLETADA")
print("=" * 70)
print("\nSi todos los tests muestran ✓, la estructura está correcta.")
print("Para ejecutar la aplicación: python launch_refactored.py")
print("=" * 70)
