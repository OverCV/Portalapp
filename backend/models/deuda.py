from datetime import datetime
from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Deuda(BaseModel):
    """Clase que representa una deuda en el sistema.

    Esta clase hereda de BaseModel y utiliza dataclass para registrar las deudas
    asociadas a ventas y deudores específicos.

    Args:
        id_venta (int): Identificador único de la venta asociada a la deuda.
        id_deudor (int): Identificador único del deudor al que corresponde la deuda.
        valor_deuda (int): Monto de la deuda en la moneda local.
        creacion_deuda (datetime): Fecha y hora en que se registró la deuda.

    Note:
        - Esta clase actúa como registro de las deudas pendientes en el sistema
        - La deuda está siempre asociada tanto a una venta como a un deudor
        - El valor de la deuda representa el monto pendiente de pago
    """

    id_venta: int
    id_deudor: int
    valor_deuda: int
    creacion_deuda: datetime
