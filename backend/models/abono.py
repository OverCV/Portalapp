from datetime import datetime
from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Abono(BaseModel):
    id_deudor: int
    valor_abono: int
    fecha_abono: datetime