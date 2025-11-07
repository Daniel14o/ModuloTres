import pytest
from Ejercicios.Ejercicio13 import (
    cargar_inventario,
    guardar_inventario,
    agregar_producto,
    vender_producto,
)

# FIXTURE PARA ARCHIVO TEMPORAL
@pytest.fixture
def inventario_temporal(monkeypatch, tmp_path):
    """
    Crea un archivo JSON temporal para pruebas.
    """
    archivo = tmp_path / "inventario.json"
    monkeypatch.setattr("Ejercicios.Ejercicio13.ARCHIVO_INVENTARIO", str(archivo))
    return str(archivo)


# PRUEBAS DE CARGA Y GUARDADO
def test_cargar_inventario_vacio(inventario_temporal):
    """Debe devolver lista vacía si el archivo no existe."""
    inventario = cargar_inventario()
    assert inventario == []


def test_guardar_y_cargar_inventario(inventario_temporal):
    """Debe guardar y volver a cargar los datos correctamente."""
    datos = [{"nombre": "Manzanas", "precio": 2.5, "cantidad": 10}]
    guardar_inventario(datos)

    cargado = cargar_inventario()
    assert cargado == datos
    assert isinstance(cargado[0]["precio"], float)


#  PRUEBAS DE AGREGAR PRODUCTOS
def test_agregar_producto_nuevo(monkeypatch):
    """Agrega un producto nuevo correctamente."""
    inventario = []

    inputs = iter(["Manzanas", "2.5", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    agregar_producto(inventario)
    assert len(inventario) == 1
    producto = inventario[0]
    assert producto["nombre"] == "Manzanas"
    assert producto["cantidad"] == 5


def test_agregar_producto_existente(monkeypatch):
    """Si el producto existe, actualiza la cantidad."""
    inventario = [{"nombre": "Manzanas", "precio": 2.5, "cantidad": 5}]

    inputs = iter(["Manzanas", "2.5", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    agregar_producto(inventario)
    producto = inventario[0]
    assert producto["cantidad"] == 8


#  PRUEBAS DE VENTA DE PRODUCTOS
def test_vender_producto_existente(monkeypatch):
    """Debe reducir la cantidad al vender un producto."""
    inventario = [{"nombre": "Manzanas", "precio": 2.5, "cantidad": 10}]

    inputs = iter(["Manzanas", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    vender_producto(inventario)
    producto = inventario[0]
    assert producto["cantidad"] == 6


def test_vender_producto_insuficiente(monkeypatch, capsys):
    """Muestra error si no hay suficiente stock."""
    inventario = [{"nombre": "Manzanas", "precio": 2.5, "cantidad": 2}]

    inputs = iter(["Manzanas", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    vender_producto(inventario)
    salida = capsys.readouterr().out
    assert "No hay suficiente stock" in salida


def test_vender_producto_no_existente(monkeypatch, capsys):
    """Muestra mensaje si el producto no existe."""
    inventario = [{"nombre": "Peras", "precio": 3.0, "cantidad": 10}]

    inputs = iter(["Manzanas", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    vender_producto(inventario)
    salida = capsys.readouterr().out
    # Se ajusta el assert al mensaje real de la función
    assert "Producto no encontrado" in salida

