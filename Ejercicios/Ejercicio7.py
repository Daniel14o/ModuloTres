from typing import List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import re

console = Console()

def validar_nombre(nombre: str) -> str | None:
    """
    Valida que el nombre contenga solo letras y espacios (sin números, emojis ni caracteres especiales).

    Args:
        nombre: Cadena ingresada por el usuario.

    Returns:
        El nombre limpio si es válido, de lo contrario None.
    """
    nombre = nombre.strip()
    # Permitir letras con tildes y espacios, pero no números ni símbolos
    if re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        return nombre
    console.print(
        Panel.fit(
            f"[bold red]Error:[/bold red] El nombre '{nombre}' no es válido. "
            "No se permiten números, emojis ni caracteres especiales.",
            title="[red]Error de entrada[/red]",
            border_style="red",
        )
    )
    return None

def validar_nota(valor: str) -> float | None:
    """
    Valida que la nota sea un número entre 0.0 y 5.0, sin letras ni símbolos.

    Args:
        valor: Cadena ingresada por el usuario.

    Returns:
        La nota como float si es válida, de lo contrario None.
    """
    valor = valor.strip()
    # Verifica que contenga solo números y punto decimal
    if not re.fullmatch(r"\d+(\.\d+)?", valor):
        console.print(
            Panel.fit(
                f"[bold red]Error:[/bold red] El valor '{valor}' no es una nota válida. "
                "Debe contener solo números entre 0 y 5.",
                title="[red]Error de entrada[/red]",
                border_style="red",
            )
        )
        return None

    try:
        nota = float(valor)
        if 0.0 <= nota <= 5.0:
            return nota
        raise ValueError
    except ValueError:
        console.print(
            Panel.fit(
                f"[bold red]Error:[/bold red] La nota '{valor}' debe estar entre 0 y 5.",
                title="[red]Error de entrada[/red]",
                border_style="red",
            )
        )
        return None

def filtrar_aprobados(estudiantes: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    """
    Filtra la lista de estudiantes para obtener solo los que aprobaron (nota >= 3.0).

    Args:
        estudiantes: Lista de tuplas (nombre, nota).

    Returns:
        Nueva lista con los estudiantes que aprobaron.
    """
    return list(filter(lambda e: e[1] >= 3.0, estudiantes))

def mostrar_tabla(estudiantes: List[Tuple[str, float]]) -> None:
    """
    Muestra una tabla con los estudiantes que aprobaron usando rich.

    Args:
        estudiantes: Lista de tuplas (nombre, nota).
    """
    tabla = Table(title="Estudiantes que aprobaron", show_lines=True)
    tabla.add_column("Nombre", style="bold cyan")
    tabla.add_column("Nota", justify="center", style="green")

    for nombre, nota in estudiantes:
        tabla.add_row(nombre, f"{nota:.1f}")

    console.print(tabla)

def main() -> None:
    """
    Permite ingresar estudiantes, valida los datos y muestra los aprobados.
    """
    estudiantes: List[Tuple[str, float]] = []

    console.print(
        Panel.fit(
            "[bold cyan] Ingreso de estudiantes[/bold cyan]\n"
            "Escribe 'fin' cuando quieras terminar.",
            border_style="cyan",
        )
    )

    while True:
        nombre_input = console.input("[bold green]Nombre del estudiante:[/bold green] ").strip()
        if nombre_input.lower() == "fin":
            break

        nombre = validar_nombre(nombre_input)
        if nombre is None:
            continue  # vuelve a pedir el nombre

        nota_input = console.input("[bold yellow]Nota del estudiante (0-5):[/bold yellow] ").strip()
        nota = validar_nota(nota_input)
        if nota is None:
            continue  # vuelve a pedir la nota

        estudiantes.append((nombre, nota))

    if not estudiantes:
        console.print("[red]No se ingresaron estudiantes válidos.[/red]")
        return

    aprobados = filtrar_aprobados(estudiantes)

    if aprobados:
        mostrar_tabla(aprobados)
    else:
        console.print(
            Panel.fit(
                "Ningún estudiante aprobó.",
                title="[yellow]Resultado[/yellow]",
                border_style="yellow",
            )
        )

if __name__ == "__main__":
    main()
