import pytest
from rich.console import Console
from Ejercicios.Ejercicio2 import validar_nombre, validar_edad, crear_perfil

console = Console()


def test_validar_nombre_valido():
    """Debe aceptar nombres válidos con letras y tildes."""
    assert validar_nombre("María López")
    assert validar_nombre("José Ñandú")


def test_validar_nombre_invalido():
    """Debe rechazar nombres con números, emojis o caracteres especiales."""
    assert not validar_nombre("Juan123")
    assert not validar_nombre("Ana 😊")
    assert not validar_nombre("Pepe@Casa")


def test_validar_edad_valida():
    """Debe aceptar edades enteras mayores que cero."""
    assert validar_edad(25)
    assert validar_edad(1)


def test_validar_edad_invalida():
    """Debe rechazar edades no enteras o menores/iguales a cero."""
    assert not validar_edad(0)
    assert not validar_edad(-5)
    assert not validar_edad("20")  # tipo incorrecto


def test_crear_perfil_valido(capsys):
    """Debe crear correctamente el perfil con datos válidos."""
    resultado = crear_perfil(
        "Carlos Pérez",
        30,
        "leer",
        "viajar",
        facebook="carlos.pz",
        instagram="carlospz_"
    )
    captured = capsys.readouterr()
    assert "Perfil de" in captured.out
    assert "Carlos Pérez" in resultado
    assert "leer" in resultado
    assert "facebook" in resultado.lower()


def test_crear_perfil_nombre_invalido():
    """Debe lanzar ValueError si el nombre es inválido."""
    with pytest.raises(ValueError):
        crear_perfil("Juan123", 25, "deporte", twitter="@juan")


def test_crear_perfil_edad_invalida():
    """Debe lanzar ValueError si la edad es inválida."""
    with pytest.raises(ValueError):
        crear_perfil("Sofía", -10, "leer", facebook="sofia.fb")


def test_crear_perfil_redes_duplicadas():
    """Debe lanzar ValueError si se repiten redes sociales."""
    with pytest.raises(ValueError):
        crear_perfil("Laura", 28, "bailar", facebook="laura.fb", FACEBOOK="otra")


def test_crear_perfil_sin_hobbies_y_sin_redes(capsys):
    """Debe manejar correctamente cuando no hay hobbies ni redes."""
    resultado = crear_perfil("Andrés", 22)
    captured = capsys.readouterr()
    assert "Sin redes registradas" in captured.out
    assert "No especificados" in resultado
