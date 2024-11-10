from dataclasses import dataclass


@dataclass
class VentaProducto:
    id = int
    id_venta = int
    id_producto = int
    cantidad = int
