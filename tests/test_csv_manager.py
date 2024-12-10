# tests/test_csv_manager.py

import pytest
from pathlib import Path
from backend.app.enums.application import Portalapp
from backend.app.enums.reports import Reports
from backend.models.producto import Producto
from backend.models.venta_producto import VentaProducto
from backend.models.venta import Venta
from backend.models.deuda import Deuda
from backend.models.deudor import Deudor
from backend.models.abono import Abono
from backend.data.managers.csv_manager import CSVManager

@pytest.fixture
def csv_manager():
    """
    Fixture para configurar y limpiar el entorno de pruebas para CSVManager.
    
    Configuración:
    - Crea una instancia de CSVManager.
    - Configura el directorio de datos de prueba.
    
    Limpieza:
    - Elimina el directorio de datos de prueba después de las pruebas.
    """
    Portalapp.DATABASE_PATH = 'test_data'
    Reports.ENCODING = 'utf-8'
    manager = CSVManager()
    yield manager
    for file_path in Path('test_data').glob('*.csv'):
        file_path.unlink()
    Path('test_data').rmdir()

def test_register_model(csv_manager):
    """
    Prueba para verificar que los modelos se registren correctamente en CSVManager.
    """
    assert Producto in csv_manager.file_map
    assert VentaProducto in csv_manager.file_map
    assert Venta in csv_manager.file_map
    assert Deuda in csv_manager.file_map
    assert Deudor in csv_manager.file_map
    assert Abono in csv_manager.file_map

def test_add_data(csv_manager):
    """
    Prueba para agregar datos a un archivo CSV y verificar que se asigna un ID único.
    """
    producto = Producto(id=None, nombre='Producto de Prueba', precio=100, stock=10, coste=50)
    added_producto = csv_manager.add_data(producto)
    assert added_producto.id == 1
    data = csv_manager.get_data(Producto)
    assert len(data) == 1
    assert data[0].nombre == 'Producto de Prueba'

def test_get_data_by_id(csv_manager):
    """
    Prueba para recuperar datos de un archivo CSV por ID.
    """
    producto = Producto(id=None, nombre='Producto de Prueba', precio=100, stock=10, coste=50)
    csv_manager.add_data(producto)
    retrieved_producto = csv_manager.get_data_by_id(Producto, 1)
    assert retrieved_producto.nombre == 'Producto de Prueba'

def test_put_data(csv_manager):
    """
    Prueba para actualizar datos en un archivo CSV.
    """
    producto = Producto(id=None, nombre='Producto de Prueba', precio=100, stock=10, coste=50)
    csv_manager.add_data(producto)
    updated_producto = csv_manager.put_data(Producto, 1, {'precio': 150})
    assert updated_producto.precio == 150

def test_delete_data(csv_manager):
    """
    Prueba para eliminar datos de un archivo CSV por ID.
    """
    producto = Producto(id=None, nombre='Producto de Prueba', precio=100, stock=10, coste=50)
    csv_manager.add_data(producto)
    assert csv_manager.delete_data(Producto, 1) is True
    assert len(csv_manager.get_data(Producto)) == 0