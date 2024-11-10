# backend/services/ventas.py

from datetime import datetime
from backend.data.managers.csv_manager import CSVManager
from backend.models.venta_producto import VentaProducto
from backend.models.producto import Producto
from backend.models.venta import Venta

from backend.app.services.productos import put_producto, get_producto_by_id

from icecream import ic


def get_ventas(data_manager: CSVManager):
    return data_manager.get_data(Venta)


def add_venta(
    data_manager: CSVManager,
    venta_productos: list[VentaProducto],
) -> dict:
    # Crear la venta principal
    # venta_id = len(data_manager.get_data('ventas')) + 1
    venta = Venta
    venta.fecha = datetime.now().isoformat()

    # Guardar la venta en la base de datos
    data_manager.add_data(Venta, venta)
    last_venta: Venta = data_manager.get_data(Venta)[-1]
    last_venta_id = last_venta.id

    # Registrar cada producto de la venta en 'venta_productos' y actualizar stock
    for venta_producto in venta_productos:
        venta_producto.id_venta = last_venta_id
        data_manager.add_data(VentaProducto, venta_producto)

        # Actualizar el stock del producto
        producto = get_producto_by_id(data_manager, venta_producto.id_producto)

        producto_actualizado = Producto(
            id=venta_producto.id_producto,
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock - venta_producto.cantidad,
        )
        put_producto(data_manager, venta_producto.id_producto, producto_actualizado)

    return venta


def calcular_total_venta(data_manager: CSVManager, venta_productos: list[VentaProducto]) -> float:
    """Calcula el total de la venta en base a la lista de productos."""
    total: int = 0
    for venta in venta_productos:
        producto: Producto = data_manager.get_data_by_id(venta.id_producto)
        total += producto.precio * venta.cantidad
    return total


def filtrar_productos_con_stock(productos: list[Producto]) -> list[Producto]:
    """Filtra productos con stock disponible."""
    return [producto for producto in productos if int(producto.stock) > 0]
