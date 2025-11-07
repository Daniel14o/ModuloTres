from rich.console import Console
from Ejercicios.Ejercicio8 import validar_texto, procesar_texto, mostrar_resultados

console = Console()

def test_validar_texto_valido():
    assert validar_texto("Hola mundo, esto es una prueba.") is True

def test_validar_texto_invalido():
    assert validar_texto("Hola 😁 mundo") is False
    assert validar_texto("12345") is False

def test_procesar_texto_devuelve_correctamente():
    texto = "Programacion Python avanzada divertida"
    palabras, diccionario = procesar_texto(texto)
    assert "PROGRAMACION" in palabras
    assert diccionario["AVANZADA"] == 8
    assert len(palabras) == len(diccionario)

def test_procesar_texto_sin_palabras_largas():
    texto = "Sol mar pez luz"
    palabras, diccionario = procesar_texto(texto)
    assert palabras == []
    assert diccionario == {}

def test_mostrar_resultados_con_tabla(capsys):
    palabras = ["PROGRAMACION", "PYTHON"]
    diccionario = {"PROGRAMACION": 12, "PYTHON": 6}
    mostrar_resultados(palabras, diccionario)
    salida = capsys.readouterr().out
    assert "PROGRAMACION" in salida
    # Buscamos una parte del título en lugar de toda la frase
    assert "Palabras Filtradas" in salida

def test_mostrar_resultados_sin_palabras(capsys):
    mostrar_resultados([], {})
    salida = capsys.readouterr().out
    assert "No se encontraron palabras" in salida

