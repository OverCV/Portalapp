from dataclasses import dataclass
from backend.models.base_model import BaseModel


@dataclass
class Producto(BaseModel):
    nombre = str
    precio = int
    stock = int
