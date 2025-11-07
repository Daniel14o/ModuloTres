from Ejercicios.Ejercicio4 import (
    es_email_valido,
    es_mayor_a_10
)


# --- TESTS DE VALIDADORES INDIVIDUALES --- #

def test_es_email_valido_correctos():
    assert es_email_valido("a@a.com") is True
    assert es_email_valido("user@mail.co") is True


def test_es_email_valido_incorrectos():
    assert es_email_valido("a@") is False
    assert es_email_valido("correo.com") is False
    assert es_email_valido("") is False


def test_es_mayor_a_10_correctos():
    assert es_mayor_a_10("11") is True
    assert es_mayor_a_10("15.5") is True


def test_es_mayor_a_10_incorrectos():
    assert es_mayor_a_10("10") is False
    assert es_mayor_a_10("0") is False
    assert es_mayor_a_10("texto") is False


# --- TESTS
