from dataclasses import dataclass
from typing import Optional
from backend.models.base_model import BaseModel


@dataclass
class Deudor(BaseModel):
    """Clase que representa a un deudor en el sistema.

    Esta clase hereda de BaseModel y utiliza dataclass para definir las
    características básicas de un deudor, como su nombre y número de contacto.

    Args:
        nombre (str): Nombre completo del deudor.
        telefono (Optional[str]): Número telefónico del deudor. Puede ser None
            si no se dispone del dato.

    Note:
        - Al ser un dataclass, los métodos __init__, __repr__, __eq__ y otros
            son generados automáticamente
        - El teléfono es opcional para permitir registrar deudores sin datos
            de contacto iniciales
    """

    nombre: str
    telefono: Optional[str]
