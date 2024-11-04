from typing import TypedDict
from datetime import datetime

class Deuda(TypedDict):
    id = int
    id_venta = int
    id_deudor = int
    valor_deuda = int
    creacion_deuda = datetime