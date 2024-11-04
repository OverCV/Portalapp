from typing import TypedDict

class Venta_Producto(TypedDict):
    id = int
    id_venta = int
    id_producto = int
    cantidad = int