from rich.console import Console
from rich.panel import Panel

# Inicializar la consola de Rich
console = Console()

def crear_contador():
    """
    Crea una función contador usando un closure.
    Retorna una función interna que incrementa un valor
    cada vez que se llama.
    """
    conteo = 0  # Variable local de la función externa

    def incrementar():
        """
        Incrementa y devuelve el valor del conteo.
        Usa 'nonlocal' para modificar la variable 'conteo'
        del ámbito de la función externa.
        """
        nonlocal conteo
        conteo += 1
        return conteo

    return incrementar


# ---------------------------------------------------------
# 🔹 Bloque principal protegido para evitar ejecución al importar
# ---------------------------------------------------------
if __name__ == "__main__":
    contador_a = crear_contador()
    contador_b = crear_contador()

    total_a = 0
    total_b = 0

    console.print(
        Panel.fit(
            "[bold cyan] Bienvenido al Contador de Llamadas con Closure[/bold cyan]\n\n"
            "[white] Puedes elegir qué contador incrementar:[/white]\n"
            "- Escribe [bold green]'A'[/bold green] para incrementar el Contador A\n"
            "- Escribe [bold magenta]'B'[/bold magenta] para incrementar el Contador B\n"
            "- Escribe [bold red]'salir'[/bold red] para finalizar\n",
            title="Instrucciones",
            border_style="bright_blue",
        )
    )

    while True:
        opcion = console.input("[bold yellow] Elige un contador (A/B o 'salir'):[/bold yellow] ").strip().lower()

        if opcion == "a":
            total_a = contador_a()
            console.print(Panel.fit(f"[bold cyan]Contador A:[/bold cyan] {total_a}", border_style="cyan"))

        elif opcion == "b":
            total_b = contador_b()
            console.print(Panel.fit(f"[bold magenta]Contador B:[/bold magenta] {total_b}", border_style="magenta"))

        elif opcion == "salir":
            resumen = (
                f"[bold cyan]Contador A finalizó en:[/bold cyan] {total_a}\n"
                f"[bold magenta]Contador B finalizó en:[/bold magenta] {total_b}"
            )
            console.print(
                Panel.fit(
                    f"[bold green] Programa finalizado correctamente.[/bold green]\n\n{resumen}",
                    title="Resumen Final",
                    border_style="bright_green",
                )
            )
            break

        else:
            console.print(
                Panel.fit("[bold red] Opción no válida. Intenta nuevamente.[/bold red]", border_style="red")
            )




