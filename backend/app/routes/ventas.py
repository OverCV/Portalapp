# backend/routes/ventas.py
from backend.data.managers.manager import Manager

from backend.models.producto import Producto
from backend.models.venta_producto import VentaProducto

from backend.app.services.ventas import (
    add_venta,
    get_ventas,
    calcular_total_venta,
    filtrar_productos_con_stock,
)


def registrar_venta(data_manager: Manager, venta_productos: list[VentaProducto]):
    """Función que maneja el registro de una venta completa."""
    return add_venta(data_manager, venta_productos)


def obtener_ventas(data_manager: Manager):
    return get_ventas(data_manager)


def obtener_total_venta(data_manager: Manager, venta_productos: list[VentaProducto]):
    return calcular_total_venta(data_manager, venta_productos)


def obtener_productos_disponibles(data_manager: Manager):
    productos = data_manager.get_data(Producto)
    return filtrar_productos_con_stock(productos)
