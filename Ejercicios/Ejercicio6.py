from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import re

console = Console()


def validar_precio(valor: str) -> float | None:
    """
    Valida que el precio ingresado sea un número válido.

    Args:
        valor: Cadena ingresada por el usuario.

    Returns:
        El valor convertido a float si es válido, de lo contrario None.
    """
    try:
        # Elimina espacios y valida que no contenga emojis ni letras
        valor = valor.strip()
        if not re.match(r"^\d+(\.\d+)?$", valor):
            raise ValueError("El precio debe contener solo números.")
        return float(valor)
    except ValueError:
        console.print(
            Panel.fit(
                f"[bold red]Error:[/bold red] El valor '{valor}' no es un precio válido. "
                "Asegúrate de ingresar solo números.",
                title="[red]Error de entrada[/red]",
                border_style="red",
            )
        )
        return None


def aplicar_descuento(productos: List[Dict[str, Any]], porcentaje: float) -> List[float]:
    """
    Aplica un descuento a cada producto.

    Args:
        productos: Lista de diccionarios con 'nombre' y 'precio'.
        porcentaje: Porcentaje de descuento.

    Returns:
        Lista con los precios con descuento.
    """
    return list(
        map(lambda p: p["precio"] * (1 - porcentaje / 100), productos)
    )


def mostrar_tabla(productos: List[Dict[str, Any]], precios_descuento: List[float]) -> None:
    """
    Muestra una tabla con los productos y precios aplicando rich.

    Args:
        productos: Lista de productos originales.
        precios_descuento: Lista de precios con descuento.
    """
    tabla = Table(title="Lista de Productos con Descuento", show_lines=True)
    tabla.add_column("Producto", style="bold cyan")
    tabla.add_column("Precio Original", justify="right", style="yellow")
    tabla.add_column("Precio con Descuento", justify="right", style="green")

    for producto, nuevo_precio in zip(productos, precios_descuento):
        tabla.add_row(
            producto["nombre"],
            f"$ {producto['precio']:,.0f}",
            f"$ {nuevo_precio:,.0f}",
        )

    console.print(tabla)


def main() -> None:
    """
    Permite al usuario ingresar productos y muestra los descuentos.
    """
    productos: List[Dict[str, Any]] = []

    console.print(
        Panel.fit(
            "[bold cyan] Ingreso de productos[/bold cyan]\n"
            "Escribe 'fin' cuando quieras terminar.",
            border_style="cyan",
        )
    )

    while True:
        nombre = console.input("[bold green]Nombre del producto:[/bold green] ").strip()
        if nombre.lower() == "fin":
            break
        precio_str = console.input("[bold yellow]Precio del producto:[/bold yellow] ").strip()

        precio = validar_precio(precio_str)
        if precio is not None:
            productos.append({"nombre": nombre, "precio": precio})

    if not productos:
        console.print("[red]No se ingresaron productos válidos.[/red]")
        return

    porcentaje = 10.0
    precios_descuento = aplicar_descuento(productos, porcentaje)
    mostrar_tabla(productos, precios_descuento)


if __name__ == "__main__":
    main()

