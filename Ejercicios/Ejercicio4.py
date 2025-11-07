"""
Ejercicio 4 - Validador de Datos Genérico

Permite validar:
- Emails con formato correcto
- Números mayores a 10

Incluye funciones puras para pruebas unitarias.
"""

from typing import Callable, List
import re
from rich.console import Console
from rich.panel import Panel

# Inicializar consola Rich
console = Console()


# --- FUNCIONES DE VALIDACIÓN --- #
def es_email_valido(email: str) -> bool:
    """
    Valida si el email tiene formato correcto.
    """
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, email))


def es_mayor_a_10(valor: str) -> bool:
    """
    Valida si un número es mayor a 10.
    """
    try:
        return float(valor) > 10
    except ValueError:
        return False


# --- FUNCIÓN DE ORDEN SUPERIOR --- #
def aplicar_validador(datos: List[str], validador: Callable) -> List[bool]:
    """
    Aplica una función validadora a una lista de datos.
    Retorna una lista de booleanos.
    """
    return [validador(dato) for dato in datos]


# --- FUNCIÓN INTERACTIVA PRINCIPAL (NO SE TESTEA DIRECTAMENTE) --- #
def ejecutar_validador(opcion: str, datos: List[str]) -> List[bool]:
    """
    Ejecuta el validador según la opción dada ('Email' o 'Numero').
    Esta función puede ser llamada directamente en los tests.
    """
    if opcion.lower() == "email":
        return aplicar_validador(datos, es_email_valido)
    elif opcion.lower() == "numero":
        return aplicar_validador(datos, es_mayor_a_10)
    else:
        raise ValueError("Opción no válida. Usa 'Email' o 'Numero'.")


# --- MODO INTERACTIVO (solo si se ejecuta directamente) --- #
def main():
    console.print(Panel.fit("[bold cyan]Validador de Datos Genérico[/bold cyan]\n\n"
                            "Puedes validar dos tipos de datos:\n"
                            "- Emails usa formato correcto de correo.\n"
                            "- Números mayores a 10.\n\n"
                            "Escribe los datos separados por comas (ejemplo: dato1, dato2, dato3)."))

    opcion = console.input("\n¿Qué tipo de datos deseas validar? ('Email', 'Numero' o 'salir'): ")

    if opcion.lower() == "salir":
        console.print("[bold red]Saliendo del programa...[/bold red]")
        return

    datos = console.input("Ingresa los datos separados por coma: ").split(",")
    resultados = ejecutar_validador(opcion, [d.strip() for d in datos])

    for dato, valido in zip(datos, resultados):
        estado = "[green]Válido[/green]" if valido else "[red]Inválido[/red]"
        console.print(f"{dato.strip()}: {estado}")


if __name__ == "__main__":
    main()
