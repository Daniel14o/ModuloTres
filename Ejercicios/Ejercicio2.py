from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import re

console = Console()


def validar_nombre(nombre: str) -> bool:
    """
    Valida que el nombre solo contenga letras, espacios y tildes.
    No se permiten números, emojis ni caracteres especiales.
    """
    patron = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$")
    return bool(patron.fullmatch(nombre.strip()))


def validar_edad(edad: int) -> bool:

# Valida que la edad sea un numero entero positivo mayor que cero.

    return isinstance(edad, int) and edad > 0


def crear_perfil(nombre: str, edad: int, *hobbies: str, **redes_sociales: str) -> str:
    """
    Genera un perfil de usuario con formato visual utilizando la librería Rich.
    Incluye validaciones de nombre, edad y redes sociales únicas.
    """
    #Validaciones
    if not validar_nombre(nombre):
        console.print("[red] ERROR: el nombre solo puede contener letras, espacios y tildes.[/red]")
        raise ValueError("Nombre inválido. Solo se permiten letras y tildes.")

    if not validar_edad(edad):
        console.print("[red] ERROR: la edad debe ser un número entero positivo mayor que cero.[/red]")
        raise ValueError("Edad invalida. Debe ser un número entero positivo.")

    #Validar redes sociales duplicadas
    nombres_redes = [red.lower() for red in redes_sociales.keys()]
    if len(nombres_redes) != len(set(nombres_redes)):
        console.print("[red] ERROR: no se pueden repetir las mismas redes sociales.[/red]")
        raise ValueError("Redes sociales duplicadas.")

    #Sección de hobbies
    hobbies_texto = ", ".join(hobbies) if hobbies else "No especificados"

    #Sección de redes sociales
    redes_texto = (
        "\n".join(
            [f"[cyan]{red.capitalize()}[/cyan]: [magenta]{usuario}[/magenta]" for red, usuario in redes_sociales.items()]
        )
        if redes_sociales
        else "[red]Sin redes registradas[/red]"
    )

    #Crear tabla visual
    tabla = Table(title=f"Perfil de [bold green]{nombre}[/bold green]", title_style="bold yellow")
    tabla.add_column("Campo", style="bold cyan", justify="right")
    tabla.add_column("Información", style="white", justify="left")

    tabla.add_row("Edad", f"[bold green]{edad} años[/bold green]")
    tabla.add_row("Hobbies", f"[italic]{hobbies_texto}[/italic]")
    tabla.add_row("Redes Sociales", redes_texto)

    #Mostrar panel con tabla
    panel = Panel(tabla, border_style="bright_blue", subtitle="Generado con éxito")
    console.print(panel)

    # Devolver texto plano (util para pruebas)
    return f"{nombre}, {edad}, {hobbies_texto}, {redes_texto}"


if __name__ == "__main__":
    console.print(
        Panel(
            "[bold yellow] Bienvenido al Generador de Perfiles de Usuario[/bold yellow]",
            border_style="bright_magenta",
            expand=False,
        )
    )

    #Solicitar nombre
    while True:
        nombre = Prompt.ask("[bold cyan]Ingrese su nombre[/bold cyan]")
        if validar_nombre(nombre):
            break
        console.print("[red] El nombre no puede contener números, emojis ni caracteres especiales.[/red]")

    #Solicitar edad
    while True:
        edad_str = Prompt.ask("[bold cyan]Ingrese su edad[/bold cyan]")
        if not edad_str.isdigit():
            console.print("[red] ERROR: Ingrese solo números enteros válidos.[/red]")
            continue

        edad = int(edad_str)
        if not validar_edad(edad):
            console.print("[red] La edad debe ser un número positivo mayor que cero.[/red]")
            continue

        break

    #Pedir hobbies
    console.print("[bold yellow]Ingrese sus hobbies separados por comas (o deje vacío si no tiene):[/bold yellow]")
    hobbies_input = Prompt.ask("Hobbies", default="")
    hobbies = tuple(h.strip() for h in hobbies_input.split(",") if h.strip())

    #Pedir redes sociales
    console.print(
        "[bold yellow]Ingrese sus redes sociales (por ejemplo: Facebook, Instagram, X, etc). Deje vacío para terminar.[/bold yellow]")
    redes: Dict[str, str] = {}

    while True:
        redes_input = Prompt.ask("Nombre(s) de red(es) social(es) separadas por comas (Enter para finalizar)",
                                 default="")
        if not redes_input.strip():
            break
        redes_lista = [r.strip() for r in redes_input.split(",") if r.strip()]
        for red in redes_lista:
            usuario = Prompt.ask(f"Usuario en [bold cyan]{red}[/bold cyan]")
            redes[red] = usuario

        #Validar redes sociales duplicadas
        if red.lower() in (r.lower() for r in redes.keys()):
            console.print(f"[red] La red social '{red}' ya fue registrada. Intente con otra.[/red]")
            continue

        usuario = Prompt.ask(f"Usuario en [bold cyan]{red}[/bold cyan]")
        redes[red] = usuario

    #Generar y mostrar perfil
    crear_perfil(nombre, edad, *hobbies, **redes)




