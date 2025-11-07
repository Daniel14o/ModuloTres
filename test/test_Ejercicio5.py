import pytest
from Ejercicios.Ejercicio5 import calcular_iva, actualizar_tasa_iva, TASA_IVA


def test_calcular_iva_correcto():
    """Debe calcular correctamente el IVA con la tasa global."""
    precio = 1000
    resultado = calcular_iva(precio)
    assert resultado == pytest.approx(precio * TASA_IVA)


def test_calcular_iva_tipo_invalido():
    """Debe lanzar TypeError si el precio no es numérico."""
    with pytest.raises(TypeError):
        calcular_iva("abc")


def test_calcular_iva_negativo():
    """Debe lanzar ValueError si el precio es negativo."""
    with pytest.raises(ValueError):
        calcular_iva(-500)


def test_actualizar_tasa_valida():
    """Debe actualizar correctamente la tasa global."""
    actualizar_tasa_iva(0.25)
    from Ejercicios import Ejercicio5
    assert Ejercicio5.TASA_IVA == 0.25


def test_actualizar_tasa_fuera_de_rango():
    """Debe lanzar ValueError si la tasa no está entre 0 y 1."""
    with pytest.raises(ValueError):
        actualizar_tasa_iva(1.5)
    with pytest.raises(ValueError):
        actualizar_tasa_iva(-0.1)


def test_actualizar_tasa_tipo_invalido():
    """Debe lanzar TypeError si la tasa no es numérica."""
    with pytest.raises(TypeError):
        actualizar_tasa_iva("abc")


def test_calculo_con_tasa_actualizada(monkeypatch):
    """Verifica que el cambio de tasa afecta el cálculo."""
    actualizar_tasa_iva(0.10)
    assert calcular_iva(100) == 10.0
