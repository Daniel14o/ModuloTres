"""
Objetivo:
1. Calcular la suma total de una lista de números usando functools.reduce.
2. Concatenar una lista de strings en una sola frase usando reduce.

Conceptos aplicados:
- functools.reduce
- Funciones lambda
- Programación funcional
"""

from functools import reduce
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def validar_lista_numeros(lista: List[str]) -> bool:
    """
    Valida que todos los elementos de la lista sean números válidos.

    Args:
        lista (List[str]): Lista de elementos ingresados por el usuario.

    Returns:
        bool: True si todos los elementos son numéricos, False en caso contrario.
    """
    try:
        for elemento in lista:
            float(elemento)
        return True
    except ValueError:
        return False


def validar_lista_texto(lista: List[str]) -> bool:
    """
    Valida que los elementos del texto no contengan emojis ni caracteres especiales raros.

    Args:
        lista (List[str]): Lista de palabras o frases.

    Returns:
        bool: True si todos los textos son válidos, False en caso contrario.
    """
    for texto in lista:
        if any(not (char.isalpha() or char.isspace() or char in ".,!?¡¿") for char in texto):
            return False
    return True


def calcular_suma(lista_numeros: List[float]) -> float:
    """
    Calcula la suma total de los números usando reduce.
    """
    return reduce(lambda a, b: a + b, lista_numeros)


def concatenar_texto(lista_textos: List[str]) -> str:
    """
    Concatena una lista de strings usando reduce.
    """
    return reduce(lambda a, b: a + b, lista_textos)


def mostrar_resultados(suma_total: float, texto_final: str) -> None:
    """
    Muestra los resultados en tablas con rich.
    """
    tabla = Table(title="Resultados del Ejercicio 9", show_lines=True)
    tabla.add_column("Operación", style="cyan", justify="center")
    tabla.add_column("Resultado", style="magenta", justify="center")

    tabla.add_row("Suma Total", f"{suma_total}")
    tabla.add_row("Texto Concatenado", texto_final)

    # ✅ Se imprime directamente la tabla, sin envolver en Panel para compatibilidad con los tests
    console.print(tabla)


if __name__ == "__main__":
    console.print(Panel("Ejercicio 9: Sumatoria con reduce", style="green bold"))

    # --- Parte 1: Lista de números ---
    entrada_numeros = console.input("[yellow]Ingrese una lista de números separados por comas:[/yellow]\n> ")
    lista_numeros_str = [x.strip() for x in entrada_numeros.split(",")]

    if not validar_lista_numeros(lista_numeros_str):
        console.print(Panel("Error: Solo se permiten números válidos (sin letras ni emojis).", style="red"))
    else:
        lista_numeros = [float(x) for x in lista_numeros_str]
        suma_total = calcular_suma(lista_numeros)

        # --- Parte 2: Lista de strings ---
        entrada_texto = console.input("\n[yellow]Ingrese palabras o frases separadas por comas para concatenar:[/yellow]\n> ")
        lista_textos = [x.strip() for x in entrada_texto.split(",")]

        if not validar_lista_texto(lista_textos):
            console.print(Panel("Error: El texto contiene caracteres no permitidos.", style="red"))
        else:
            texto_final = concatenar_texto(lista_textos)
            mostrar_resultados(suma_total, texto_final)
