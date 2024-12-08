from typing import List
from backend.data.managers.csv_manager import CSVManager
from backend.models.producto import Producto


class ProductoService:
    def __init__(self, data_manager: CSVManager):
        self.data_manager = data_manager

    def get_productos_disponibles(self) -> List[Producto]:
        productos = self.data_manager.get_data(Producto)
        return [p for p in productos if p.stock > 0]

    def get_producto(self, producto_id: int) -> Producto:
        return self.data_manager.get_data(Producto, producto_id)