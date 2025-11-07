from io import StringIO
from rich.console import Console
from rich.panel import Panel

def test_simulacion_salida_rich_panel():
    """Verifica que el uso de Rich no genere errores al imprimir."""
    buffer = StringIO()
    console = Console(file=buffer)  # Escribir directamente en el buffer
    console.print(Panel("Prueba de panel", title="Test"))

    output = buffer.getvalue()
    assert isinstance(output, str)
    assert "Prueba de panel" in output or len(output.strip()) > 0, "Debe generar alguna salida en consola"
