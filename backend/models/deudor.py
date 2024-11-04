from dataclasses import dataclass
from typing import Optional


@dataclass
class Deudor:
    id = int
    nombre = str
    telfono = Optional[str]
