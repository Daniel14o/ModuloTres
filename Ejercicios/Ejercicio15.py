import json
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table

# Consola Rich para visualización colorida
console = Console()

# Archivo persistente del sistema
ARCHIVO_BIBLIOTECA = "biblioteca.json"



# FUNCIONES DE PERSISTENCIA
def cargar_biblioteca() -> List[Dict[str, Optional[str]]]:
    """
    Carga el estado de la biblioteca desde un archivo JSON.

    Returns:
        List[Dict[str, Optional[str]]]: Lista de libros con su información.
    """
    try:
        with open(ARCHIVO_BIBLIOTECA, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        console.print("[yellow] No existe el archivo biblioteca.json. Se creará uno nuevo.[/yellow]")
        return []
    except json.JSONDecodeError:
        console.print("[red] Error:[/] El archivo JSON está dañado. Se iniciará con una lista vacía.")
        return []


def guardar_biblioteca(libros: List[Dict[str, Optional[str]]]) -> None:
    """
    Guarda el estado actual de la biblioteca en un archivo JSON.

    Args:
        libros (List[Dict[str, Optional[str]]]): Lista de libros actualizada.
    """
    with open(ARCHIVO_BIBLIOTECA, "w", encoding="utf-8") as archivo:
        json.dump(libros, archivo, indent=4, ensure_ascii=False)



# FUNCIONES PRINCIPALES
def prestar_libro(libros: List[Dict[str, Optional[str]]], libro_id: str, nombre_aprendiz: str) -> None:
    """
    Marca un libro como prestado a un aprendiz.

    Args:
        libros (List[Dict[str, Optional[str]]]): Lista de libros.
        libro_id (str): ID del libro a prestar.
        nombre_aprendiz (str): Nombre del aprendiz que lo solicita.
    """
    for libro in libros:
        if libro["libro_id"] == libro_id:
            if libro["prestado_a"] is not None:
                console.print(f"[red] El libro '{libro['titulo']}' ya está prestado a {libro['prestado_a']}.[/red]")
                return
            libro["prestado_a"] = nombre_aprendiz
            guardar_biblioteca(libros)
            console.print(f"[green] Libro '{libro['titulo']}' prestado a {nombre_aprendiz}.[/green]")
            return
    console.print("[red] No se encontró un libro con ese ID.[/red]")


def devolver_libro(libros: List[Dict[str, Optional[str]]], libro_id: str) -> None:
    """
    Marca un libro como disponible (prestado_a = None).

    Args:
        libros (List[Dict[str, Optional[str]]]): Lista de libros.
        libro_id (str): ID del libro a devolver.
    """
    for libro in libros:
        if libro["libro_id"] == libro_id:
            if libro["prestado_a"] is None:
                console.print(f"[yellow] El libro '{libro['titulo']}' ya estaba disponible.[/yellow]")
                return
            libro["prestado_a"] = None
            guardar_biblioteca(libros)
            console.print(f"[green] Libro '{libro['titulo']}' devuelto correctamente.[/green]")
            return
    console.print("[red] No se encontró un libro con ese ID.[/red]")


def buscar_libro(libros: List[Dict[str, Optional[str]]], query: str) -> List[Dict[str, Optional[str]]]:
    """
    Busca libros cuyo título contenga la palabra clave indicada.

    Args:
        libros (List[Dict[str, Optional[str]]]): Lista de libros.
        query (str): Palabra o frase a buscar en los títulos.

    Returns:
        List[Dict[str, Optional[str]]]: Libros coincidentes.
    """
    resultados = [libro for libro in libros if query.lower() in libro["titulo"].lower()]
    mostrar_tabla(resultados, titulo=f"Resultados de búsqueda para '{query}'")
    return resultados


def ver_libros_prestados(libros: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
    """
    Muestra todos los libros que están actualmente prestados.

    Args:
        libros (List[Dict[str, Optional[str]]]): Lista de libros.

    Returns:
        List[Dict[str, Optional[str]]]: Libros prestados.
    """
    prestados = [libro for libro in libros if libro["prestado_a"] is not None]
    mostrar_tabla(prestados, titulo="Libros Prestados")
    return prestados



# FUNCIONES DE VISUALIZACIÓN
def mostrar_tabla(libros: List[Dict[str, Optional[str]]], titulo: str) -> None:
    """
    Muestra una lista de libros en formato tabla con Rich.

    Args:
        libros (List[Dict[str, Optional[str]]]): Lista de libros a mostrar.
        titulo (str): Título de la tabla.
    """
    if not libros:
        console.print("[yellow]No hay libros para mostrar.[/yellow]")
        return

    tabla = Table(title=titulo, header_style="bold magenta")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Título", style="green")
    tabla.add_column("Prestado a", style="yellow")

    for libro in libros:
        tabla.add_row(libro["libro_id"], libro["titulo"], libro["prestado_a"] or "Disponible")

    console.print(tabla)



# MENÚ PRINCIPAL

def menu_principal() -> None:
    """
    Muestra el menú principal de la aplicación de biblioteca.
    """
    libros = cargar_biblioteca()

    while True:
        console.print("\n[bold blue]=== SISTEMA DE BIBLIOTECA ===[/bold blue]")
        console.print("1. Ver libros prestados")
        console.print("2. Buscar libro por titulo")
        console.print("3. Prestar libro")
        console.print("4. Devolver libro")
        console.print("5. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            ver_libros_prestados(libros)
        elif opcion == "2":
            query = input("Ingrese palabra clave del titulo: ")
            buscar_libro(libros, query)
        elif opcion == "3":
            libro_id = input("ID del libro: ")
            aprendiz = input("Nombre del aprendiz: ")
            prestar_libro(libros, libro_id, aprendiz)
        elif opcion == "4":
            libro_id = input("ID del libro a devolver: ")
            devolver_libro(libros, libro_id)
        elif opcion == "5":
            console.print("[bold green]Saliendo del sistema...[/bold green]")
            break
        else:
            console.print("[red] Opción inválida. Intente nuevamente.[/red]")


if __name__ == "__main__":
    menu_principal()
