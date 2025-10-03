# -*- coding: utf-8 -*-
"""
Script para remover tildes y ñ de archivos Python
"""
import os
import sys

def remove_accents(text):
    """Reemplaza caracteres con tildes y ñ"""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        'ü': 'u', 'Ü': 'U'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def process_file(filepath):
    """Procesar un archivo individual"""
    try:
        # Leer el archivo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene caracteres a reemplazar
        original_content = content
        content = remove_accents(content)
        
        if content != original_content:
            # Escribir el archivo modificado
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Procesado: {filepath}")
            return True
        else:
            print(f"- Sin cambios: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error en {filepath}: {e}")
        return False

def main():
    """Procesar todos los archivos Python en src/"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, 'src')
    
    if not os.path.exists(src_dir):
        print("Error: No se encontro el directorio src/")
        return
    
    print("Procesando archivos Python...")
    print("=" * 60)
    
    files_processed = 0
    files_modified = 0
    
    # Recorrer todos los archivos .py en src/
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                files_processed += 1
                if process_file(filepath):
                    files_modified += 1
    
    print("=" * 60)
    print(f"Archivos procesados: {files_processed}")
    print(f"Archivos modificados: {files_modified}")

if __name__ == "__main__":
    main()
