import csv
from typing import Dict
from rich.console import Console
from rich.table import Table


def analizar_csv(nombre_archivo: str, columna: str) -> Dict[str, float | str]:
    """
    Analiza una columna numérica en un archivo CSV y calcula su promedio,
    valor máximo, mínimo y quién los obtuvo.

    Args:
        nombre_archivo (str): Ruta o nombre del archivo CSV a analizar.
        columna (str): Nombre de la columna numérica a analizar.

    Returns:
        Dict[str, float | str]: Diccionario con promedio, máximo, mínimo y los nombres
        de los estudiantes con esos valores.
    """
    datos: list[dict[str, str]] = []

    with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                valor = float(fila[columna])
                datos.append({"nombre": fila["nombre"], "valor": valor})
            except (ValueError, KeyError):
                continue

    if not datos:
        raise ValueError(f"No se encontraron valores válidos en la columna '{columna}'.")

    valores = [d["valor"] for d in datos]
    promedio = round(sum(valores) / len(valores), 2)
    maximo = max(valores)
    minimo = min(valores)

    # Buscar los nombres correspondientes
    nombre_max = next(d["nombre"] for d in datos if d["valor"] == maximo)
    nombre_min = next(d["nombre"] for d in datos if d["valor"] == minimo)

    return {
        "promedio": promedio,
        "maximo": maximo,
        "minimo": minimo,
        "mejor_estudiante": nombre_max,
        "peor_estudiante": nombre_min,
    }


def mostrar_resultados(resultados: Dict[str, float | str]) -> None:
    """
    Muestra los resultados del análisis en una tabla usando rich.

    Args:
        resultados (Dict[str, float | str]): Diccionario con las métricas calculadas.

    Returns:
        None
    """
    console = Console()
    table = Table(title="Resultados del Análisis CSV")

    table.add_column("Métrica", justify="center", style="bold cyan")
    table.add_column("Valor", justify="center", style="bold green")

    table.add_row("Promedio", str(resultados["promedio"]))
    table.add_row("Máximo", f"{resultados['maximo']} ({resultados['mejor_estudiante']})")
    table.add_row("Mínimo", f"{resultados['minimo']} ({resultados['peor_estudiante']})")

    console.print(table)


if __name__ == "__main__":
    archivo = "estudiantes.csv"

    try:
        resultados = analizar_csv(archivo, "calificacion")
        mostrar_resultados(resultados)
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no existe.")
    except ValueError as e:
        print(f"Error: {e}")
