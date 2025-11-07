import os
import json
import tempfile
import pytest
from Ejercicios.Ejercicio14 import (
    leer_csv,
    leer_json,
    generar_reporte,
)

# FIXTURES

@pytest.fixture
def archivo_csv_tmp():
    """
    Crea un archivo CSV temporal con datos de ejemplo.
    """
    contenido = "nombre,edad\nAna,20\nLuis,22\n"
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".csv") as tmp:
        tmp.write(contenido)
        ruta = tmp.name
    yield ruta
    try:
        os.remove(ruta)
    except OSError:
        pass


@pytest.fixture
def archivo_json_tmp():
    """
    Crea un archivo JSON temporal con datos de ejemplo.
    """
    data = {"Ana": ["Python", "Git"], "Luis": ["HTML", "CSS"]}
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".json") as tmp:
        json.dump(data, tmp)
        ruta = tmp.name
    yield ruta
    try:
        os.remove(ruta)
    except OSError:
        pass


# PRUEBAS DE LECTURA CSV

def test_leer_csv_exitoso(archivo_csv_tmp):
    """Debe leer correctamente un archivo CSV existente."""
    resultado = leer_csv(archivo_csv_tmp)
    assert isinstance(resultado, list)
    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Ana"
    assert resultado[1]["edad"] == "22"


def test_leer_csv_inexistente(capsys):
    """Debe manejar el error de archivo CSV no encontrado."""
    resultado = leer_csv("no_existe.csv")
    salida = capsys.readouterr().out
    assert resultado == []
    assert "No se encontró el archivo" in salida


#PRUEBAS DE LECTURA JSON

def test_leer_json_exitoso(archivo_json_tmp):
    """Debe leer correctamente un archivo JSON existente."""
    resultado = leer_json(archivo_json_tmp)
    assert isinstance(resultado, dict)
    assert "Ana" in resultado
    assert "Python" in resultado["Ana"]


def test_leer_json_inexistente(capsys):
    """Debe manejar el error de archivo JSON no encontrado."""
    resultado = leer_json("no_existe.json")
    salida = capsys.readouterr().out
    assert resultado == {}
    assert "No se encontró el archivo" in salida


def test_leer_json_invalido(capsys):
    """Debe manejar errores de formato JSON inválido."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".json") as tmp:
        tmp.write("{malformado}")
        ruta = tmp.name

    resultado = leer_json(ruta)
    salida = capsys.readouterr().out
    assert resultado == {}
    assert "formato JSON inválido" in salida

    try:
        os.remove(ruta)
    except OSError:
        pass


# PRUEBAS DE GENERAR REPORTE

def test_generar_reporte_exitoso(capsys, archivo_csv_tmp, archivo_json_tmp):
    """Debe generar correctamente el reporte y guardarlo."""
    estudiantes = leer_csv(archivo_csv_tmp)
    cursos = leer_json(archivo_json_tmp)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        ruta_reporte = tmp.name

    # ejecutar y capturar salida
    generar_reporte(estudiantes, cursos, ruta_reporte)
    salida = capsys.readouterr().out  # <-- corregido: .out

    # Verifica que se haya mostrado el panel y el mensaje final
    assert "Reporte Generado" in salida
    assert "guardado correctamente" in salida

    # Verifica que el archivo se haya creado y contenga información
    with open(ruta_reporte, encoding="utf-8") as f:
        contenido = f.read()

    # Normalizamos contenido para evitar problemas de mayúsculas/espacios
    contenido_normalizado = contenido.upper()
    assert "REPORTE" in contenido_normalizado
    assert "ANA" in contenido_normalizado
    assert "PYTHON" in contenido_normalizado

    try:
        os.remove(ruta_reporte)
    except OSError:
        pass


def test_generar_reporte_sin_datos(capsys):
    """Si faltan datos, muestra advertencia y no crea archivo."""
    ruta = "salida_prueba.txt"
    # asegurar que no exista antes
    try:
        os.remove(ruta)
    except OSError:
        pass

    generar_reporte([], {}, ruta)
    salida = capsys.readouterr().out
    assert "No hay datos suficientes" in salida
    assert not os.path.exists(ruta)

