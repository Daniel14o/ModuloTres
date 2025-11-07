import csv
import pytest
from Ejercicios.Ejercicio12 import analizar_csv, mostrar_resultados


@pytest.fixture
def archivo_csv_temporal(tmp_path):
    """
    Crea un archivo CSV temporal con datos de prueba.
    """
    ruta = tmp_path / "estudiantes.csv"
    with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "calificacion"])
        escritor.writerow(["Ana", 4.5])
        escritor.writerow(["Luis", 3.0])
        escritor.writerow(["Carla", 5.0])
        escritor.writerow(["Pedro", 2.5])
    return ruta


def test_analizar_csv_resultados_correctos(archivo_csv_temporal):
    """
    Verifica que el análisis CSV calcule correctamente los valores promedio, máximo y mínimo.
    """
    resultados = analizar_csv(str(archivo_csv_temporal), "calificacion")

    assert resultados["promedio"] == pytest.approx(3.75)
    assert resultados["maximo"] == 5.0
    assert resultados["minimo"] == 2.5
    assert resultados["mejor_estudiante"] == "Carla"
    assert resultados["peor_estudiante"] == "Pedro"


def test_analizar_csv_columna_invalida(archivo_csv_temporal):
    """
    Verifica que se lance un error si la columna no existe.
    """
    with pytest.raises(ValueError):
        analizar_csv(str(archivo_csv_temporal), "nota")


def test_analizar_csv_vacio(tmp_path):
    """
    Verifica que se lance un error si el archivo no tiene datos válidos.
    """
    ruta = tmp_path / "vacio.csv"
    with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
        archivo.write("nombre,calificacion\n")  # Solo encabezado

    with pytest.raises(ValueError):
        analizar_csv(str(ruta), "calificacion")


def test_mostrar_resultados_salida(capsys):
    """
    Verifica que la función mostrar_resultados imprima correctamente una tabla.
    """
    resultados = {
        "promedio": 4.25,
        "maximo": 5.0,
        "minimo": 3.5,
        "mejor_estudiante": "Ana",
        "peor_estudiante": "Luis",
    }

    mostrar_resultados(resultados)
    salida = capsys.readouterr().out

    # Normalizamos espacios y saltos de línea
    texto_normalizado = salida.replace("\n", " ").replace("  ", " ")

    assert "Resultados" in texto_normalizado
    assert "Análisis" in texto_normalizado
    assert "Promedio" in texto_normalizado
    assert "Ana" in texto_normalizado
    assert "Luis" in texto_normalizado

