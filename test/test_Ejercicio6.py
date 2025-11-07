
from Ejercicios.Ejercicio6 import validar_precio


# PRUEBAS PARA validar_precio

def test_validar_precio_valido():
    """Debe retornar un float si el valor es un número válido."""
    assert validar_precio("2500") == 2500.0
    assert validar_precio("100.5") == 100.5


def test_validar_precio_invalido_letras():
    """Debe retornar None si el valor contiene letras."""
    resultado = validar_precio("abc")
    assert resultado is None


def test_validar_precio_invalido_emojis():
    """Debe retornar None si el valor contiene emojis o caracteres especiales."""
    resultado = validar_precio("300😁")
    assert resultado is None


def test_validar_precio_con_espacios():
    """Debe aceptar valores válidos con espacios al inicio o final."""
    assert validar_precio("  500  ") == 500.0



# PRUEBAS PARA aplicar_descuento


def test_aplicar_descuento_correcto():
    """Debe aplicar correctamente el porcentaje de descuento."""

