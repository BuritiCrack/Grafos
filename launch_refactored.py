# -*- coding: utf-8 -*-
"""
Launcher script for the refactored social network application
"""
import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

try:
    print("Iniciando Red Social - Sistema de Grafos (Version Refactorizada)")
    print("=" * 60)
    
    # Import and run the refactored application
    import tkinter as tk
    from ui.red_social_gui_refactored import RedSocialGUIRefactored
    
    print("Modulos importados correctamente")
    print("Creando interfaz...")
    
    # Create and run the application
    root = tk.Tk()
    app = RedSocialGUIRefactored(root)
    
    print("Aplicacion iniciada exitosamente")
    print("Arquitectura MVC implementada")
    print("Datos cargados desde archivos JSON")
    print("-" * 60)
    print("Funcionalidades disponibles:")
    print("   - Gestion de Personas")
    print("   - Conexiones Automaticas y Manuales") 
    print("   - Recomendaciones Inteligentes")
    print("   - Analisis de Red")
    print("   - Configuracion Avanzada")
    print("=" * 60)
    
    root.mainloop()
    
except ImportError as e:
    print(f"Error al importar modulos: {e}")
    print("Asegurate de que todos los archivos esten en el directorio actual")
    print("Archivos necesarios:")
    required_files = [
        "src/ui/red_social_gui_refactored.py",
        "src/ui/gui_controller.py", 
        "src/services/red_social_service.py",
        "src/models/usuario.py",
        "src/services/data_manager.py",
        "src/services/recomendador.py",
        "src/services/analizador_red.py", 
        "src/utils/visualizador.py",
        "data/usuarios.json",
        "data/Conexiones.json"
    ]
    for file in required_files:
        status = "OK" if os.path.exists(file) else "MISSING"
        print(f"   {status} {file}")

except Exception as e:
    print(f"Error inesperado: {e}")
    print("Por favor reporta este error")

finally:
    input("\nPresiona Enter para salir...")