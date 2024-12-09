from dataclasses import dataclass
from backend.models.base_model import BaseModel
from typing import Optional


@dataclass
class Producto(BaseModel):
    """Clase que representa un producto en el inventario.
    Esta clase hereda de BaseModel y utiliza dataclass para definir un producto
    con sus características básicas como nombre, precio, stock y costes.

    Args:
        nombre (str): Nombre o descripción del producto.
        precio (int): Precio de venta del producto en la moneda local.
        stock (int): Cantidad de unidades disponibles en inventario.
        coste (int): Costo de adquisición o producción del producto.
        imagen_ruta (Optional[str], optional): Ruta al archivo de imagen del
            producto. Por defecto es None.

    Note:
        - La ganancia por producto se puede calcular como precio - coste
        - Al ser un dataclass, los métodos __init__, __repr__, __eq__ y otros
            se generan automáticamente
    """

    nombre: str
    precio: int
    stock: int
    coste: int
    imagen_ruta: Optional[str] = None
