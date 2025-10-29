import pytest
from Ejercicios.Ejercicio1 import calcular_imc, interpretar_imc

# PRUEBAS UNITARIAS PARA calcular_imc()

def test_calcular_imc_valores_validos():
    """Debe calcular correctamente el IMC con valores válidos"""
    resultado = calcular_imc(70.0, 1.75)  # ambos floats válidos
    assert resultado == pytest.approx(22.86, 0.01)

def test_calcular_imc_redondeo_dos_decimales():
    """Debe redondear el resultado a dos decimales."""
    resultado = calcular_imc(80.0, 1.80)
    assert resultado == 24.69  # 80 / (1.8**2) = 24.6913

def test_calcular_imc_altura_cero():
    """Debe lanzar ValueError si la altura es cero."""
    with pytest.raises(ValueError, match="La altura debe ser un valor positivo"):
        calcular_imc(70.0, 0.0)

def test_calcular_imc_altura_negativa():
    """Debe lanzar ValueError si la altura es negativa."""
    with pytest.raises(ValueError):
        calcular_imc(70.0, -1.75)


# PRUEBAS UNITARIAS PARA interpretar_imc()


@pytest.mark.parametrize(
    "imc, esperado",
    [
        (17.9, "Bajo peso"),
        (22.0, "Peso Normal"),
        (27.0, "Sobrepeso"),
        (32.0, "Obesidad Grado I"),
        (37.0, "Obesidad Grado II"),
        (42.0, "Obesidad Grado III (Mórbida)"),
    ]
)
def test_interpretar_imc_valores(imc, esperado):
    """Debe devolver la categoría correcta según el IMC."""
    assert interpretar_imc(imc) == esperado
