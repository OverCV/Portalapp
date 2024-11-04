from typing import TypedDict
from datetime import datetime

class Venta(TypedDict):
    id = int
    fecha = datetime
    ganancia = int
    