from datetime import datetime

from dataclasses import dataclass


@dataclass
class Deuda:
    id = int
    id_venta = int
    id_deudor = int
    valor_deuda = int
    creacion_deuda = datetime
