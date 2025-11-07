import pytest
from Ejercicios.Ejercicio9 import (
    validar_lista_numeros,
    validar_lista_texto,
    calcular_suma,
    concatenar_texto,
    mostrar_resultados,
)


def test_validar_lista_numeros_valida():
    lista = ["10", "20.5", "30"]
    assert validar_lista_numeros(lista) is True


def test_validar_lista_numeros_invalida():
    lista = ["10", "abc", "30"]
    assert validar_lista_numeros(lista) is False


def test_validar_lista_texto_valida():
    lista = ["Hola", "Mundo", "Python es genial!"]
    assert validar_lista_texto(lista) is True


def test_validar_lista_texto_invalida():
    lista = ["Hola", "Mundo😁", "Python!"]
    assert validar_lista_texto(lista) is False


def test_calcular_suma_correcta():
    lista = [10, 20, 30]
    assert calcular_suma(lista) == 60


def test_concatenar_texto_correcto():
    lista = ["Hola ", "Mundo", "!"]
    assert concatenar_texto(lista) == "Hola Mundo!"


def test_mostrar_resultados_salida_rich(capsys):
    suma_total = 45.0
    texto_final = "Hola Mundo"
    mostrar_resultados(suma_total, texto_final)

    salida = capsys.readouterr().out
    # Verifica que aparezcan los textos clave
    assert "Resultados del Ejercicio 9" in salida
    assert "Suma Total" in salida
    assert "45.0" in salida
    assert "Texto Concatenado" in salida
    assert "Hola Mundo" in salida


@pytest.mark.parametrize(
    "lista,esperado",
    [
        (["1", "2", "3.5"], True),
        (["10", "veinte", "30"], False),
    ],
)
def test_validar_lista_numeros_parametrizado(lista, esperado):
    assert validar_lista_numeros(lista) == esperado


@pytest.mark.parametrize(
    "lista,esperado",
    [
        (["Python", "es", "increible!"], True),
        (["Hola", "😁"], False),
    ],
)
def test_validar_lista_texto_parametrizado(lista, esperado):
    assert validar_lista_texto(lista) == esperado
