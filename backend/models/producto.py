from dataclasses import dataclass
from backend.models.base_model import BaseModel
from typing import Optional


@dataclass
class Producto(BaseModel):
    nombre: str
    precio: int
    stock: int
    coste: int
    imagen_ruta: Optional[str] = None
