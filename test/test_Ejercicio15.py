import json
import os
import tempfile
import pytest
from Ejercicios.Ejercicio15 import (
    cargar_biblioteca,
    guardar_biblioteca,
    prestar_libro,
    devolver_libro,
    buscar_libro,
    ver_libros_prestados,
    mostrar_tabla
)

# FIXTURES
@pytest.fixture
def biblioteca_temporal(monkeypatch):
    """Crea un archivo JSON temporal con libros de ejemplo."""
    datos = [
        {"libro_id": "1", "titulo": "Python Básico", "prestado_a": None},
        {"libro_id": "2", "titulo": "Git y GitHub", "prestado_a": "Laura"},
    ]
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="utf-8") as tmp:
        json.dump(datos, tmp)
        tmp_path = tmp.name
    monkeypatch.setattr("Ejercicios.Ejercicio15.ARCHIVO_BIBLIOTECA", tmp_path)
    yield tmp_path
    os.remove(tmp_path)


# PRUEBAS DE PERSISTENCIA
def test_cargar_biblioteca_correctamente(biblioteca_temporal):
    libros = cargar_biblioteca()
    assert isinstance(libros, list)
    assert len(libros) == 2
    assert libros[0]["titulo"] == "Python Básico"


def test_cargar_biblioteca_no_existente(monkeypatch, capsys):
    monkeypatch.setattr("Ejercicios.Ejercicio15.ARCHIVO_BIBLIOTECA", "archivo_inexistente.json")
    libros = cargar_biblioteca()
    salida = capsys.readouterr().out
    assert libros == []
    assert "No existe el archivo biblioteca.json" in salida


def test_cargar_biblioteca_json_danado(monkeypatch, capsys):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp.write(b"{no valido json}")
        tmp_path = tmp.name
    monkeypatch.setattr("Ejercicios.Ejercicio15.ARCHIVO_BIBLIOTECA", tmp_path)

    libros = cargar_biblioteca()
    salida = capsys.readouterr().out
    assert libros == []
    assert "archivo JSON está dañado" in salida
    os.remove(tmp_path)


def test_guardar_biblioteca(biblioteca_temporal):
    libros = cargar_biblioteca()
    libros.append({"libro_id": "3", "titulo": "Django Pro", "prestado_a": None})
    guardar_biblioteca(libros)
    with open(biblioteca_temporal, encoding="utf-8") as f:
        data = json.load(f)
    assert any(libro["titulo"] == "Django Pro" for libro in data)


# PRUEBAS FUNCIONALES
def test_prestar_libro_exitoso(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    prestar_libro(libros, "1", "Carlos")
    salida = capsys.readouterr().out
    assert "prestado a Carlos" in salida
    assert any(libro["prestado_a"] == "Carlos" for libro in libros)


def test_prestar_libro_ya_prestado(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    prestar_libro(libros, "2", "Pedro")
    salida = capsys.readouterr().out
    assert "ya está prestado" in salida


def test_prestar_libro_no_existente(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    prestar_libro(libros, "99", "Pedro")
    salida = capsys.readouterr().out
    assert "No se encontró un libro" in salida


def test_devolver_libro_exitoso(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    devolver_libro(libros, "2")
    salida = capsys.readouterr().out
    assert "devuelto correctamente" in salida
    assert any(libro["prestado_a"] is None for libro in libros)


def test_devolver_libro_ya_disponible(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    devolver_libro(libros, "1")
    salida = capsys.readouterr().out
    assert "ya estaba disponible" in salida


def test_buscar_libro(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    resultados = buscar_libro(libros, "Python")
    salida = capsys.readouterr().out
    assert len(resultados) == 1
    assert "Python Básico" in resultados[0]["titulo"]
    assert "Resultados de búsqueda" in salida


def test_ver_libros_prestados(capsys, biblioteca_temporal):
    libros = cargar_biblioteca()
    prestados = ver_libros_prestados(libros)
    salida = capsys.readouterr().out
    assert len(prestados) == 1
    assert prestados[0]["prestado_a"] == "Laura"
    assert "Libros Prestados" in salida


# VISUALIZACIÓN
def test_mostrar_tabla_vacia(capsys):
    mostrar_tabla([], "Sin libros")
    salida = capsys.readouterr().out
    assert "No hay libros para mostrar" in salida


def test_mostrar_tabla_con_datos(capsys):
    libros = [
        {"libro_id": "1", "titulo": "Python Básico", "prestado_a": None},
        {"libro_id": "2", "titulo": "Git y GitHub", "prestado_a": "Laura"},
    ]
    mostrar_tabla(libros, "Biblioteca")
    salida = capsys.readouterr().out
    assert "Python Básico" in salida
    assert "Git y GitHub" in salida

