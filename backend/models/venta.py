from datetime import datetime
from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Venta(BaseModel):
    fecha: datetime
    total: int
    ganancia: int
