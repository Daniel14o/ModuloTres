"""
Ejercicio 8:
- Crear una lista de palabras con más de 5 letras en mayúsculas.
- Crear un diccionario que asocie cada palabra con su longitud.

Conceptos aplicados:
- List Comprehensions
- Dictionary Comprehensions
- Métodos de string
- Validaciones y visualización con rich
"""

from typing import List, Dict, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import re

console = Console()


def validar_texto(texto: str) -> bool:
    """
    Valida que el texto no contenga emojis ni caracteres especiales excesivos.

    Args:
        texto (str): Texto ingresado por el usuario.

    Returns:
        bool: True si el texto es válido, False en caso contrario.
    """
    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ,.!?;:()¿¡]+$"
    return bool(re.match(patron, texto.strip()))


def procesar_texto(texto: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Procesa el texto para generar lista y diccionario según las condiciones del ejercicio.

    Args:
        texto (str): Texto a procesar.

    Returns:
        tuple[List[str], Dict[str, int]]: Lista de palabras y diccionario con su longitud.
    """
    palabras = texto.split()
    palabras_filtradas = [p.upper() for p in palabras if len(p) > 5]
    diccionario_palabras = {p: len(p) for p in palabras_filtradas}
    return palabras_filtradas, diccionario_palabras


def mostrar_resultados(palabras: List[str], diccionario: Dict[str, int]) -> None:
    """
    Muestra los resultados usando tablas de rich.

    Args:
        palabras (List[str]): Lista de palabras filtradas.
        diccionario (Dict[str, int]): Diccionario con longitud de cada palabra.
    """
    if not palabras:
        console.print(Panel("No se encontraron palabras con más de 5 letras.", style="yellow"))
        return

    tabla = Table(title="Palabras Filtradas y su Longitud", show_lines=True)
    tabla.add_column("Palabra", justify="center", style="cyan", no_wrap=True)
    tabla.add_column("Longitud", justify="center", style="magenta")

    for palabra, longitud in diccionario.items():
        tabla.add_row(palabra, str(longitud))

    console.print(Panel.fit(tabla, border_style="bright_blue"))


def main() -> None:
    """Punto de entrada del programa."""
    console.print(
        Panel("Ejercicio 8: Transformación de Datos con List y Dictionary Comprehensions",
              style="green bold")
    )

    texto_usuario = console.input("[yellow]Ingrese un texto largo para analizar:[/yellow]\n> ")

    if not validar_texto(texto_usuario):
        console.print(
            Panel(
                "Error: El texto contiene caracteres no permitidos. "
                "Solo se aceptan letras, espacios y signos básicos.",
                style="red",
            )
        )
        return

    palabras, diccionario = procesar_texto(texto_usuario)
    mostrar_resultados(palabras, diccionario)


if __name__ == "__main__":
    main()
