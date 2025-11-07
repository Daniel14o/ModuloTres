import os
import tempfile
import pytest

from Ejercicios.Ejercicio11 import (
    validar_tarea,
    agregar_tarea,
)

#FIXTURES

import Ejercicios.Ejercicio11

@pytest.fixture
def archivo_temporal(monkeypatch):
    """
    Crea un archivo temporal para pruebas sin afectar tareas.txt real.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tmp:
        ruta = tmp.name

    # Aquí usamos la referencia directa al módulo
    monkeypatch.setattr(Ejercicios.Ejercicio11, "ARCHIVO_TAREAS", ruta)
    yield ruta
    os.remove(ruta)



# TESTS

def test_validar_tarea_valida():
    """Debe aceptar una tarea con texto y signos básicos."""
    assert validar_tarea("Comprar leche") is True
    assert validar_tarea("Hacer la cama!") is True


def test_validar_tarea_invalida():
    """Debe rechazar tareas vacías o con emojis."""
    assert validar_tarea("") is False
    assert validar_tarea("   ") is False
    assert validar_tarea("Estudiar 😎") is False


def test_agregar_y_ver_tareas(archivo_temporal):
    """Debe agregar y luego leer correctamente las tareas."""
    agregar_tarea("Lavar los platos")
