from datetime import datetime
from dataclasses import dataclass


@dataclass
class Venta:
    id = int
    fecha = datetime
    ganancia = int
