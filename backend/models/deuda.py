from datetime import datetime
from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Deuda(BaseModel):
    id_venta: int
    id_deudor: int
    valor_deuda: int
    creacion_deuda: datetime
