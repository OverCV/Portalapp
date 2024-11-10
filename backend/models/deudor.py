from dataclasses import dataclass
from typing import Optional
from backend.models.base_model import BaseModel


@dataclass
class Deudor(BaseModel):
    nombre = str
    telfono = Optional[str]