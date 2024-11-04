from typing import TypedDict

class Deudor(TypedDict):
    id = int
    id_venta = int
    nombre = str
    valor_deuda = float
    creacion_deuda = str