from typing import TypedDict, Optional

class Deudor(TypedDict):
    id = int
    nombre = str
    telfono = Optional[str]