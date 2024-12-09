from dataclasses import dataclass
from backend.models.base_model import BaseModel

from datetime import datetime


@dataclass
class VentaProducto(BaseModel):
    """Clase que representa la relación entre una venta y un producto vendido.

    Esta clase actúa como una tabla intermedia que registra los productos
    individuales incluidos en una venta, heredando de BaseModel y utilizando
    dataclass para la gestión de atributos.

    Args:
        id_venta (int): Identificador único de la venta a la que pertenece.
        fecha (datetime): Fecha y hora en que se registró la venta del producto.
        id_producto (int): Identificador único del producto vendido.
        cantidad (int): Cantidad de unidades vendidas del producto.

    Note:
        - Esta clase permite rastrear el detalle de productos por cada venta.
        - Al ser un dataclass, se generan automáticamente los métodos básicos
        como __init__, __repr__, __eq__.
    """

    id_venta: int
    fecha: datetime
    id_producto: int
    cantidad: int
