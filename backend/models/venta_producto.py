from dataclasses import dataclass
from backend.models.base_model import BaseModel

from datetime import datetime


@dataclass
class VentaProducto(BaseModel):
    id_venta: int
    fecha: datetime
    id_producto: int
    cantidad: int
