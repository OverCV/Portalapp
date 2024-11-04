from typing import TypeDict

class Producto(TypeDict):
    id = int
    nombre = str
    precio = int
    stock = int