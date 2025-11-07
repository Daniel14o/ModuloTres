import pytest
from rich.console import Console
from io import StringIO
from contextlib import redirect_stdout

from Ejercicios.Ejercicio7 import (
    validar_nombre,
    validar_nota,
    filtrar_aprobados,
    mostrar_tabla,
)

# Simulamos una consola de rich
console = Console(file=StringIO())


# TESTS PARA validar_nombre

def test_validar_nombre_valido():
    """Debe aceptar nombres válidos con letras y espacios."""
    assert validar_nombre("Juan Pérez") == "Juan Pérez"
    assert validar_nombre("María José") == "María José"


def test_validar_nombre_invalido_numeros(monkeypatch):
    """Debe devolver None si el nombre contiene números."""
    f = StringIO()
    with redirect_stdout(f):
        resultado = validar_nombre("Juan123")
    assert resultado is None
    assert "no es válido" in f.getvalue()


def test_validar_nombre_invalido_caracteres_especiales(monkeypatch):
    """Debe devolver None si el nombre contiene símbolos o emojis."""
    f = StringIO()
    with redirect_stdout(f):
        resultado = validar_nombre("Pepe 😁")
    assert resultado is None


def test_validar_nombre_espacios_extremos():
    """Debe eliminar espacios al inicio y al final."""
    assert validar_nombre("  Ana María  ") == "Ana María"


# TESTS PARA validar_nota

@pytest.mark.parametrize("entrada,esperado", [
    ("0", 0.0),
    ("3", 3.0),
    ("5", 5.0),
    ("4.5", 4.5),
])
def test_validar_nota_valida(entrada, esperado):
    """Debe aceptar notas válidas entre 0 y 5."""
    assert validar_nota(entrada) == esperado


@pytest.mark.parametrize("entrada", ["-1", "5.1", "6", "abc", "3,5", "😄"])
def test_validar_nota_invalida(entrada):
    """Debe devolver None si la nota no es válida o está fuera de rango."""
    f = StringIO()
    with redirect_stdout(f):
        resultado = validar_nota(entrada)
    assert resultado is None
    assert "Error" in f.getvalue()


def test_validar_nota_con_espacios():
    """Debe limpiar espacios antes de validar."""
    assert validar_nota(" 4 ") == 4.0


# TESTS PARA filtrar_aprobados

def test_filtrar_aprobados_mixto():
    """Debe retornar solo los estudiantes con nota >= 3.0."""
    estudiantes = [("Juan", 2.5), ("Ana", 3.0), ("Luis", 4.5)]
    resultado = filtrar_aprobados(estudiantes)
    assert resultado == [("Ana", 3.0), ("Luis", 4.5)]


def test_filtrar_aprobados_todos_aprueban():
    """Si todos aprueban, debe devolver la lista completa."""
    estudiantes = [("Pedro", 3.5), ("Laura", 4.0)]
    assert filtrar_aprobados(estudiantes) == estudiantes


def test_filtrar_aprobados_ninguno_aprueba():
    """Si ninguno aprueba, debe devolver lista vacía."""
    estudiantes = [("A", 1.0), ("B", 2.9)]
    assert filtrar_aprobados(estudiantes) == []


# TESTS PARA mostrar_tabla

def test_mostrar_tabla_salida_rich(capsys):
    """Debe mostrar correctamente la tabla con los aprobados."""
    estudiantes = [("Carlos", 4.0), ("Lucía", 5.0)]
    mostrar_tabla(estudiantes)
    salida = capsys.readouterr().out

    # Normalizamos el texto: quitamos saltos de línea y dobles espacios
    salida_normalizada = " ".join(salida.split())

    assert "Carlos" in salida_normalizada
    assert "Lucía" in salida_normalizada
    assert "Estudiantes" in salida_normalizada
    assert "aprobaron" in salida_normalizada

