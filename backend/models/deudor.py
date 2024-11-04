from typing import TypedDict

class Deudor(TypedDict):
    id = int
    nombre = str
    valor_deuda = float
    creacion_deuda = str