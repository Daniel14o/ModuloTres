"""
Ejercicio 11: Gestor de Tareas en Archivo de Texto (.txt)

Objetivo:
Crear una aplicación de consola que permita gestionar una lista de tareas almacenadas
en un archivo de texto. Incluye opciones para agregar y ver tareas, con una interfaz
visual mejorada usando la librería rich.

Conceptos aplicados:
- Funciones
- Manejo de archivos (with open)
- Modos de apertura ('r', 'a')
- readlines, writelines
- Menús de consola
"""

from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os

console = Console()
ARCHIVO_TAREAS = "tareas.txt"


def validar_tarea(tarea: str) -> bool:
    """
    Valida que la tarea no esté vacía ni contenga emojis o caracteres inválidos.

    Args:
        tarea (str): Texto de la tarea.

    Returns:
        bool: True si la tarea es válida, False en caso contrario.
    """
    if not tarea.strip():
        return False
    # No se permiten emojis ni caracteres especiales
    return all(char.isalnum() or char.isspace() or char in ",.!?-" for char in tarea)


def agregar_tarea(tarea: str) -> None:
    """
    Agrega una tarea al archivo de texto.

    Args:
        tarea (str): Descripción de la tarea.
    """
    with open(ARCHIVO_TAREAS, "a", encoding="utf-8") as archivo:
        archivo.write(tarea.strip() + "\n")


def ver_tareas() -> List[str]:
    """
    Lee todas las tareas del archivo y las devuelve como una lista.

    Returns:
        List[str]: Lista con las tareas almacenadas.
    """
    if not os.path.exists(ARCHIVO_TAREAS):
        return []

    with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as archivo:
        tareas = [linea.strip() for linea in archivo.readlines() if linea.strip()]
    return tareas


def mostrar_tareas(tareas: List[str]) -> None:
    """
    Muestra las tareas en formato de tabla usando rich.

    Args:
        tareas (List[str]): Lista de tareas.
    """
    if not tareas:
        console.print(Panel("No hay tareas registradas.", style="yellow"))
        return

    tabla = Table(title="Lista de Tareas", show_lines=True)
    tabla.add_column("N°", justify="center", style="cyan", no_wrap=True)
    tabla.add_column("Descripción", justify="left", style="magenta")

    for i, tarea in enumerate(tareas, 1):
        tabla.add_row(str(i), tarea)

    console.print(Panel(tabla, border_style="bright_blue"))


def menu() -> None:
    """
    Muestra el menú principal y gestiona las opciones del usuario.
    """
    while True:
        console.print(Panel("GESTOR DE TAREAS EN ARCHIVO .TXT", style="green bold"))
        console.print("[1] Agregar tarea")
        console.print("[2] Ver tareas")
        console.print("[3] Salir")

        opcion = console.input("\n[bold cyan]Selecciona una opción:[/bold cyan] ")

        if opcion == "1":
            tarea = console.input("\nIngrese la descripción de la tarea:\n> ")
            if not validar_tarea(tarea):
                console.print(Panel("Error: Tarea no válida. Evita emojis o dejarla vacía.", style="red"))
            else:
                agregar_tarea(tarea)
                console.print(Panel("Tarea agregada correctamente.", style="green"))

        elif opcion == "2":
            tareas = ver_tareas()
            mostrar_tareas(tareas)

        elif opcion == "3":
            console.print(Panel("Salida exitosa", style="yellow"))
            break

        else:
            console.print(Panel("Opción inválida. Intenta de nuevo.", style="red"))

if __name__ == "__main__":
    menu()
