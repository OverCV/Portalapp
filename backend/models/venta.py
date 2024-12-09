from datetime import datetime
from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Venta(BaseModel):
    """Clase que representa una venta en el sistema.

    Esta clase hereda de BaseModel y utiliza el decorador dataclass para
    simplificar la creación de una clase de datos para ventas.

    Args:
        fecha (datetime): Fecha y hora en que se realizó la venta.
        total (int): Monto total de la venta en la moneda local.
        ganancia (int): Ganancia neta obtenida de la venta.

    Note:
        Al ser un dataclass, automáticamente se generan los métodos __init__,
        __repr__, __eq__ y otros métodos especiales.
    """

    fecha: datetime
    total: int
    ganancia: int
