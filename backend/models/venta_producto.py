from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class VentaProducto(BaseModel):
    id_venta = int
    id_producto = int
    cantidad = int