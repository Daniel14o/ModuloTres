from rich.console import Console
from rich.panel import Panel

# Inicializar consola Rich
console = Console()

# VARIABLE GLOBAL
TASA_IVA = 0.19  # 19% de IVA inicial


# FUNCIONES PRINCIPALES
def calcular_iva(precio_base: float) -> float:
    """
    Calcula el valor del IVA a partir del precio base.
    Utiliza la variable global TASA_IVA.
    """
    if not isinstance(precio_base, (int, float)):
        raise TypeError("El precio debe ser un número.")
    if precio_base < 0:
        raise ValueError("El precio no puede ser negativo.")
    return precio_base * TASA_IVA


def actualizar_tasa_iva(nueva_tasa: float) -> None:
    """
    Actualiza la tasa de IVA global.
    Usa la palabra clave 'global' para modificar la variable global.
    Incluye validaciones para que la tasa esté entre 0 y 1.
    """
    global TASA_IVA
    if not isinstance(nueva_tasa, (int, float)):
        raise TypeError("La tasa debe ser un número.")
    if 0 <= nueva_tasa <= 1:
        TASA_IVA = nueva_tasa
    else:
        raise ValueError("La tasa debe estar entre 0 y 1 (por ejemplo, 0.19 para 19%).")


# PROGRAMA PRINCIPAL (solo se ejecuta si se corre directamente)
if __name__ == "__main__":
    console.print(
        Panel.fit(
            "[bold cyan] Calculadora de Impuestos con Scope Global[/bold cyan]\n\n"
            "Este programa simula el cálculo del IVA usando una variable global.\n"
            "Puedes actualizar la tasa de IVA (entre 0 y 1) y ver cómo cambia el resultado.",
            title="Descripción",
            border_style="bright_blue",
        )
    )

    while True:
        console.print("\n[bold yellow]Opciones:[/bold yellow]\n"
                      "1. Calcular IVA\n"
                      "2. Actualizar tasa de IVA\n"
                      "3. Mostrar tasa actual\n"
                      "4. Salir")

        opcion = console.input("[bold cyan] Elige una opción (1-4): [/bold cyan]").strip()

        if opcion == "1":
            try:
                precio_str = console.input("[bold yellow] Ingresa el precio base: [/bold yellow] ").strip()
                precio = float(precio_str)
                valor_iva = calcular_iva(precio)
                console.print(
                    Panel.fit(
                        f"[bold white]Precio base:[/bold white] {precio}\n"
                        f"[bold white]Tasa de IVA actual:[/bold white] {TASA_IVA * 100:.1f}%\n"
                        f"[bold green]IVA calculado:[/bold green] {valor_iva:.2f}\n"
                        f"[bold cyan]Precio total:[/bold cyan] {precio + valor_iva:.2f}",
                        title="Resultado del Cálculo",
                        border_style="green",
                    )
                )
            except ValueError:
                console.print(
                    Panel.fit("[bold red]Error:[/bold red] Ingresa un número válido.", border_style="red")
                )

        elif opcion == "2":
            try:
                nueva_str = console.input("[bold magenta] Ingresa la nueva tasa de IVA (ejemplo: 0.15): [/bold magenta] ").strip()
                nueva = float(nueva_str)
                actualizar_tasa_iva(nueva)
                console.print(
                    Panel.fit(
                        f"[bold green] La tasa de IVA se ha actualizado correctamente a {TASA_IVA * 100:.1f}%[/bold green]",
                        title="Actualización Exitosa",
                        border_style="bright_green",
                    )
                )
            except ValueError as e:
                console.print(Panel.fit(f"[bold red] Error: {str(e)}[/bold red]", border_style="red"))

        elif opcion == "3":
            console.print(
                Panel.fit(
                    f"[bold cyan] Tasa de IVA actual: {TASA_IVA * 100:.1f}%[/bold cyan]",
                    title="Información Global",
                    border_style="cyan",
                )
            )

        elif opcion == "4":
            console.print(
                Panel.fit(
                    "[bold green] Programa finalizado correctamente.[/bold green]\n",
                    border_style="bright_green",
                )
            )
            break

        else:
            console.print(
                Panel.fit("[bold red] Opción no válida. Intenta nuevamente.[/bold red]", border_style="red")
            )

