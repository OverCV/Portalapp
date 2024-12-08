from typing import List
from backend.models.producto import Producto
from backend.app.services.productos import ProductoService

class ProductoRoutes:
    def __init__(self, service: ProductoService):
        self.service = service

    def get_productos_disponibles(self) -> List[Producto]:
        return self.service.get_productos_disponibles()

    def get_producto(self, producto_id: int) -> Producto:
        return self.service.get_producto(producto_id)
