from typing import NoReturn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import re
# Inicializar rich console
# Usamos console en lugar de print para aprovechar las funcionalidades de rich
console = Console()


def calcular_imc(peso: float, altura: float) -> float:
    """
    Calcula el Índice de Masa Corporal (IMC) a partir del peso y la altura.

    El IMC se calcula usando la fórmula: IMC = peso / (altura ** 2).
    La altura debe estar en metros y el peso en kilogramos.

    Args:
        peso: El peso de la persona en kilogramos (kg).
        altura: La altura de la persona en metros (m).

    Returns:
        El valor del IMC como un número flotante, redondeado a dos decimales.

    Raises:
        ValueError: Si la altura no es un valor positivo.
    """
    # Responsable del CÁLCULO
    if altura <= 0:
        raise ValueError("La altura debe ser un valor positivo y no cero.")

    imc = peso / (altura ** 2)
    return round(imc, 2)


def interpretar_imc(imc: float) -> str:
    """
    Interpreta el valor del Índice de Masa Corporal (IMC) y asigna una categoría de peso.

    Esta clasificación está basada en los estándares de la OMS.

    Args:
        imc: El valor del IMC calculado.

    Returns:
        Una cadena de texto que describe la categoría de peso.
    """
    # Responsable de la INTERPRETACIÓN/CLASIFICACIÓN
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 25.0:
        return "Peso Normal"
    elif 25.0 <= imc < 30.0:
        return "Sobrepeso"
    elif 30.0 <= imc < 35.0:
        return "Obesidad Grado I"
    elif 35.0 <= imc < 40.0:
        return "Obesidad Grado II"
    else:  # imc >= 40.0
        return "Obesidad Grado III (Mórbida)"


def validar_altura(altura: str) -> float:
    """
    Valida que la altura tenga el formato correcto X.XX (metros)
    y que esté dentro de un rango realista (1.00 - 2.50 m)
    """
    patron = r"^[1-2]\.\d{2}$"
    if not re.match(patron, altura):
        console.print(
            Panel.fit(
                "[bold red]Error:[/bold red] La altura debe estar en metros con formato X.XX (ejemplo: 1.70)",
                border_style="red"
            )
        )
        raise ValueError("Formato de altura inválido")

    altura_float = float(altura)
    if not (1.00 <= altura_float <= 2.50):
        console.print(
            Panel.fit(
                f"[bold red]Error:[/bold red] La altura debe estar entre 1.00 m y 2.15 m. (Ingresó: {altura_float} m)",
                border_style="red"
            )
        )
        raise ValueError("Altura fuera de rango")

    return altura_float


def main() -> NoReturn:
    """
    Orquesta el flujo principal del programa.
    Solicita datos al usuario, maneja errores y presenta los resultados
    de manera atractiva usando 'rich'.
    """
    # (Entrada/Salida) de datos

    # 1. Título con rich
    console.print(Panel("[bold yellow]CALCULADORA DE ÍNDICE DE MASA CORPORAL (IMC)[/bold yellow]", border_style="blue"))

    try:
        # Petición de datos con manejo de formato (reemplaza coma por punto)
        peso_str = console.input("[bold green]Ingrese su peso en kilogramos (kg): [/bold green]").replace(',', '.')
        altura_str = console.input("[bold green]Ingrese su altura en metros (m) y separe el primer numero por un ( . ): [/bold green]").replace(',', '.')

        peso_kg = float(peso_str)
        altura_m = validar_altura(altura_str)  # ← validación agregada aquí

        # Llamadas a las funciones
        imc_calculado = calcular_imc(peso_kg, altura_m)
        categoria = interpretar_imc(imc_calculado)

        # Impresión del resultado final con rich Panel
        resultado_panel = Panel(
            Text.from_markup(
                f"[bold cyan]IMC Calculado:[/bold cyan] {imc_calculado:.2f}\n"
                f"[bold cyan]Categoría:[/bold cyan] [bold magenta]{categoria}[/bold magenta]"
            ),
            title="[bold yellow]ANALISIS COMPLETO[/bold yellow]",
            border_style="green"
        )
        console.print(resultado_panel)

    except ValueError as e:
        # Manejo de errores de entrada (números no válidos, altura <= 0)
        console.print(f"[bold red]ERROR DE ENTRADA:[/bold red] Por favor, ingrese valores numéricos válidos. ({e})",
                      style="white on red")
    except Exception as e:
        # Manejo de otros errores inesperados
        console.print(f"[bold red]ERROR INESPERADO:[/bold red] {e}", style="white on red")


if __name__ == "__main__":
    main()

