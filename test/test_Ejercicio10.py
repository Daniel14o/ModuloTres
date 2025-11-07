import sys
import os
from io import StringIO
from rich.console import Console

# Aseguramos que se pueda importar el módulo
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Ejercicios.Ejercicio10 import explorar_estructura
from rich.tree import Tree


def render_tree(tree: Tree) -> str:
    """Convierte un objeto Tree en texto plano usando Rich Console."""
    console = Console(file=StringIO(), force_terminal=False, color_system=None)
    console.print(tree)
    return console.file.getvalue()


def test_explorar_estructura_valor_simple():
    """Prueba que un valor simple (int) sea agregado correctamente al árbol."""
    resultado = explorar_estructura(42)
    assert isinstance(resultado, Tree)
    texto = render_tree(resultado)
    assert "Valor:" in texto
    assert "42" in texto


def test_explorar_estructura_lista_anidada():
    """Prueba que una lista anidada sea explorada completamente."""
    estructura = [1, [2, 3]]
    resultado = explorar_estructura(estructura)
    texto = render_tree(resultado)
    assert "1" in texto
    assert "2" in texto
    assert "3" in texto
    assert "Lista/Tupla" in texto


def test_explorar_estructura_diccionario():
    """Prueba que un diccionario se explore correctamente."""
    estructura = {"a": 1, "b": {"c": 2}}
    resultado = explorar_estructura(estructura)
    texto = render_tree(resultado)
    assert "Diccionario" in texto
    assert "a" in texto
    assert "b" in texto
    assert "c" in texto
    assert "1" in texto
    assert "2" in texto


def test_explorar_estructura_conjunto():
    """Prueba que un conjunto se explore correctamente."""
    estructura = {1, 2, 3}
    resultado = explorar_estructura(estructura)
    texto = render_tree(resultado)
    assert "Conjunto" in texto
    assert "1" in texto
    assert "2" in texto
    assert "3" in texto


def test_explorar_estructura_tipo_no_soportado():
    """Prueba que se maneje un tipo no iterable ni conocido."""
    class ObjetoPersonalizado:
        pass

    objeto = ObjetoPersonalizado()
    resultado = explorar_estructura(objeto)
    texto = render_tree(resultado)
    assert "Tipo no soportado" in texto
    assert "ObjetoPersonalizado" in texto
