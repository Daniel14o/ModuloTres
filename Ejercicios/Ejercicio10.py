"""
Ejercicio 10: Explorador de Estructuras de Datos Recursivo.
Autor: Daniel Cáceres

Objetivo:
Explorar de forma recursiva cualquier estructura de datos anidada (listas, diccionarios,
tuplas, etc.) e imprimir los valores no iterables junto a su nivel de profundidad.

Conceptos aplicados:
- Recursividad
- isinstance()
- Tipado dinámico con Any
- Interfaz visual con rich
"""

from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

console = Console()

def explorar_estructura(elemento: Any, profundidad: int = 1, arbol: Tree | None = None) -> Tree:
    """
    Explora una estructura de datos recursivamente e imprime cada valor no iterable
    junto con su profundidad.

    Args:
        elemento (Any): Estructura de datos a explorar (lista, diccionario, etc.).
        profundidad (int): Nivel de profundidad actual (por defecto 1).
        arbol (Tree | None): Nodo del árbol de rich para visualización recursiva.

    Returns:
        Tree: Objeto Tree de rich representando la estructura.
    """
    # Si es la primera llamada, creamos el árbol principal
    if arbol is None:
        arbol = Tree(f"Explorando estructura (nivel {profundidad})", guide_style="bright_blue")

    # Caso base: elemento no iterable (valor final)
    if isinstance(elemento, (int, float, str, bool, type(None))):
        arbol.add(f"[cyan]Valor:[/cyan] {elemento!r} [magenta](Profundidad: {profundidad})[/magenta]")
        return arbol

    # Caso recursivo: si es lista o tupla
    if isinstance(elemento, (list, tuple)):
        nodo = arbol.add(f"[green]Lista/Tupla (nivel {profundidad})[/green]")
        for item in elemento:
            explorar_estructura(item, profundidad + 1, nodo)

    # Si es diccionario
    elif isinstance(elemento, dict):
        nodo = arbol.add(f"[yellow]Diccionario (nivel {profundidad})[/yellow]")
        for clave, valor in elemento.items():
            subnodo = nodo.add(f"[bold]{clave}[/bold] →")
            explorar_estructura(valor, profundidad + 1, subnodo)

    # Si es conjunto
    elif isinstance(elemento, set):
        nodo = arbol.add(f"[blue]Conjunto (nivel {profundidad})[/blue]")
        for item in elemento:
            explorar_estructura(item, profundidad + 1, nodo)

    # Si es un tipo no reconocido (por ejemplo, objeto personalizado)
    else:
        arbol.add(f"[red]Tipo no soportado:[/red] {type(elemento).__name__}")

    return arbol

if __name__ == "__main__":
    console.print(Panel("Ejercicio 10: Explorador de Estructuras de Datos Recursivo", style="green bold"))

    estructura_prueba = [
        1,
        [2, 3, [4, 5]],
        {"a": 6, "b": {"c": 7, "d": [8, 9]}},
        (10, 11),
        {12, 13, 14},
    ]

    console.print(Panel("Estructura inicial de prueba:", style="cyan"))
    console.print(estructura_prueba)

    console.print("\n🌲 Resultado del recorrido:\n", style="bold green")
    arbol = explorar_estructura(estructura_prueba)
    console.print(arbol)
