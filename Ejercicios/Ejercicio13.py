import json
from typing import List, Dict
from rich.console import Console
from rich.table import Table

console = Console()
ARCHIVO_INVENTARIO = "inventario.json"


def cargar_inventario() -> List[Dict[str, str | int | float]]:
    """
    Carga el inventario desde un archivo JSON.

    Si el archivo no existe, devuelve una lista vacía.

    Returns:
        List[Dict[str, str | int | float]]: Lista de productos en el inventario.
    """
    try:
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []  # No existe el archivo, se empieza con inventario vacío
    except json.JSONDecodeError:
        console.print("[red]Error:[/] El archivo JSON está dañado. Se usará un inventario vacío.")
        return []


def guardar_inventario(inventario: List[Dict[str, str | int | float]]) -> None:
    """
    Guarda el inventario actual en el archivo JSON.

    Args:
        inventario (List[Dict[str, str | int | float]]): Lista de productos a guardar.
    """
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


def agregar_producto(inventario: List[Dict[str, str | int | float]]) -> None:
    """
    Agrega un nuevo producto al inventario y guarda los cambios.

    Args:
        inventario (List[Dict[str, str | int | float]]): Lista de productos existente.
    """
    console.print("\n[bold cyan]Agregar nuevo producto[/bold cyan]")
    nombre = input("Nombre del producto: ").strip()
    precio = float(input("Precio del producto: "))
    cantidad = int(input("Cantidad disponible: "))

    # Verifica si ya existe el producto
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            console.print("[yellow]El producto ya existe. Actualizando cantidad...[/yellow]")
            producto["cantidad"] += cantidad
            guardar_inventario(inventario)
            return

    inventario.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
    guardar_inventario(inventario)
    console.print("[green] Producto agregado correctamente.[/green]")


def vender_producto(inventario: List[Dict[str, str | int | float]]) -> None:
    """
    Realiza una venta de un producto, actualiza la cantidad y guarda los cambios.

    Args:
        inventario (List[Dict[str, str | int | float]]): Lista de productos existente.
    """
    console.print("\n[bold cyan]Vender producto[/bold cyan]")
    nombre = input("Nombre del producto a vender: ").strip()
    cantidad_vendida = int(input("Cantidad a vender: "))

    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            if producto["cantidad"] >= cantidad_vendida:
                producto["cantidad"] -= cantidad_vendida
                guardar_inventario(inventario)
                console.print(f"[green] Venta realizada. Quedan {producto['cantidad']} unidades.[/green]")
                return
            else:
                console.print("[red] No hay suficiente stock para realizar la venta.[/red]")
                return

    console.print("[red] Producto no encontrado en el inventario.[/red]")


def mostrar_inventario(inventario: List[Dict[str, str | int | float]]) -> None:
    """
    Muestra el inventario en una tabla con la librería Rich.

    Args:
        inventario (List[Dict[str, str | int | float]]): Lista de productos existente.
    """
    console.print("\n[bold magenta] Inventario Actual[/bold magenta]")
    if not inventario:
        console.print("[yellow]El inventario está vacío.[/yellow]")
        return

    tabla = Table(title="Inventario de Productos")
    tabla.add_column("Nombre", style="cyan", justify="left")
    tabla.add_column("Precio", style="green", justify="right")
    tabla.add_column("Cantidad", style="yellow", justify="center")

    for producto in inventario:
        tabla.add_row(
            producto["nombre"],
            f"${producto['precio']:.2f}",
            str(producto["cantidad"])
        )

    console.print(tabla)


def menu_principal() -> None:
    """
    Muestra el menu principal y gestiona las opciones del usuario.
    """
    inventario = cargar_inventario()

    while True:
        console.print("\n[bold blue] GESTOR DE INVENTARIO [/bold blue]")
        console.print("1. Mostrar inventario")
        console.print("2. Agregar producto")
        console.print("3. Vender producto")
        console.print("4. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            mostrar_inventario(inventario)
        elif opcion == "2":
            agregar_producto(inventario)
        elif opcion == "3":
            vender_producto(inventario)
        elif opcion == "4":
            console.print("[bold green]Saliendo del programa...[/bold green]")
            break
        else:
            console.print("[red] Opción no válida. Intenta nuevamente.[/red]")


if __name__ == "__main__":
    menu_principal()
