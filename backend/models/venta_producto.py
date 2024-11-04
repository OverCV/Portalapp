from typing import TypedDict

class VentaProducto(TypedDict):
    id = int
    id_venta = int
    id_producto = int
    cantidad = int