from datetime import datetime
from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Abono(BaseModel):
    """Representa un abono (pago) realizado por un deudor.

    Esta clase hereda de ModeloBase y utiliza dataclass para una definición
    de clase compacta y con tipos de datos claros.

    Atributos:
        id_deudor (int): Identificador único del deudor que realiza el abono.
        valor_abono (int): Monto del abono realizado.
        fecha_abono (datetime): Fecha y hora en que se realizó el abono.
    """

    id_deudor: int
    valor_abono: int
    fecha_abono: datetime
