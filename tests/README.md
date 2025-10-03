# Tests para Red Social - Sistema de Grafos

Este directorio está destinado a contener las pruebas unitarias del proyecto.

## Estructura Propuesta

```
tests/
├── __init__.py
├── test_usuario.py          # Tests del modelo Usuario
├── test_red_social_service.py  # Tests del servicio principal
├── test_data_manager.py     # Tests de persistencia
├── test_recomendador.py     # Tests del sistema de recomendaciones
└── test_analizador_red.py   # Tests del analizador de red
```

## Ejecutar Tests

Para ejecutar los tests cuando estén implementados:

```bash
# Instalar pytest
pip install pytest

# Ejecutar todos los tests
pytest tests/

# Ejecutar con cobertura
pip install pytest-cov
pytest --cov=src tests/
```

## Ejemplo de Test

```python
import unittest
from src.models.usuario import Usuario

class TestUsuario(unittest.TestCase):
    def test_crear_usuario(self):
        usuario = Usuario(1, "Juan", 25, "juan@email.com", ["Python", "AI"])
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.edad, 25)
```
