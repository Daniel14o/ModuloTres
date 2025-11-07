import csv
import json
from typing import List, Dict
from rich.console import Console
from rich.panel import Panel

console = Console()


def leer_csv(nombre_archivo: str) -> List[Dict[str, str]]:
    """
    Lee los datos de un archivo CSV y devuelve una lista de diccionarios.

    Args:
        nombre_archivo (str): Ruta o nombre del archivo CSV.

    Returns:
        List[Dict[str, str]]: Lista de registros del archivo CSV.
    """
    try:
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    except FileNotFoundError:
        console.print(f"[red] Error:[/] No se encontró el archivo '{nombre_archivo}'.")
        return []


def leer_json(nombre_archivo: str) -> Dict[str, List[str]]:
    """
    Lee los datos de un archivo JSON y devuelve un diccionario.

    Args:
        nombre_archivo (str): Ruta o nombre del archivo JSON.

    Returns:
        Dict[str, List[str]]: Diccionario con los cursos de cada estudiante.
    """
    try:
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        console.print(f"[red] Error:[/] No se encontró el archivo '{nombre_archivo}'.")
        return {}
    except json.JSONDecodeError:
        console.print(f"[red] Error:[/] El archivo '{nombre_archivo}' tiene un formato JSON inválido.")
        return {}


def generar_reporte(estudiantes: List[Dict[str, str]], cursos: Dict[str, List[str]], nombre_salida: str) -> None:
    """
    Combina la información de estudiantes y cursos para generar un reporte en texto.

    Args:
        estudiantes (List[Dict[str, str]]): Lista de estudiantes con su información.
        cursos (Dict[str, List[str]]): Diccionario con los cursos que toma cada estudiante.
        nombre_salida (str): Nombre del archivo de salida (.txt).
    """
    if not estudiantes or not cursos:
        console.print("[yellow] No hay datos suficientes para generar el reporte.[/yellow]")
        return

    lineas_reporte = []
    lineas_reporte.append(" REPORTE DE ESTUDIANTES Y CURSOS \n")

    for estudiante in estudiantes:
        nombre = estudiante.get("nombre", "Desconocido")
        edad = estudiante.get("edad", "N/A")
        lista_cursos = cursos.get(nombre, [])

        lineas_reporte.append(f" Estudiante: {nombre} (Edad: {edad})")
        if lista_cursos:
            lineas_reporte.append(f" Cursos: {', '.join(lista_cursos)}\n")
        else:
            lineas_reporte.append(" No tiene cursos asignados.\n")

    reporte_final = "\n".join(lineas_reporte)

    # Mostrar en consola con Rich
    console.print(Panel.fit(reporte_final, title=" Reporte Generado", border_style="cyan"))

    # Guardar el reporte en un archivo de texto
    with open(nombre_salida, "w", encoding="utf-8") as archivo:
        archivo.write(reporte_final)

    console.print(f"[green] Reporte guardado correctamente en '{nombre_salida}'.[/green]")


def main() -> None:
    """
    Función principal del programa. Coordina la lectura y generación del reporte.
    """
    estudiantes = leer_csv("estudiantes.csv")
    cursos = leer_json("cursos.json")
    generar_reporte(estudiantes, cursos, "reporte.txt")


if __name__ == "__main__":
    main()
