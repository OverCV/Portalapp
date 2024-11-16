# productos/presenter.py #
from typing import List, Optional
from backend.models.producto import Producto
from backend.data.managers.csv_manager import CSVManager

import flet as fl


class ProductosPresenter:
    def __init__(self, view: fl.View, sql_manager: CSVManager):
        self.__view = view
        self.__search_term: str = ''  # Término de búsqueda actual
        self.__all_productos: List[Producto] = []
        self.__sql_manager = sql_manager

    def load_productos(self) -> List[Producto]:
        # TODO: Integrar con backend
        self.__all_productos = self.__sql_manager.get_data(Producto)
        return (
            self.__all_productos
            if not self.__search_term
            else [p for p in self.__all_productos if p.nombre.lower() in self.__search_term.lower()]
        )

    def search_productos(self, term: str):
        self.__search_term = term.strip()
        self.__view.refresh_productos()  # Actualiza la vista con productos filtrados

    def validate_product(
        self, nombre: str, precio: str, coste: str, stock: str, imagen_ruta: str = None
    ) -> tuple[bool, Optional[Producto]]:
        try:
            if not nombre:
                raise ValueError('El nombre es requerido')

            precio_val = self.__validate_precio(precio)
            stock_val = self.__validate_stock(stock)
            coste_val = precio_val if coste == '' else int(coste)

            return True, Producto(
                id=-1, nombre=nombre, precio=precio_val, coste=coste_val, stock=stock_val, imagen_ruta=imagen_ruta
            )
        except ValueError as e:
            self.__view.show_error(str(e))
            return False, None

    def __validate_precio(self, precio: str) -> int:
        try:
            precio_val = int(precio)
            if precio_val <= 0:
                raise ValueError()
            return precio_val
        except ValueError:
            raise ValueError('Precio debe ser un número mayor a 0')

    def __validate_stock(self, stock: str) -> int:
        try:
            stock_val = int(stock)
            if stock_val < 0:
                raise ValueError()
            return stock_val
        except ValueError:
            raise ValueError('Stock debe ser un número positivo')

    def save_producto(
        self, nombre: str, precio: str, coste: str, stock: str, imagen_ruta: str = None, id_producto: int = None
    ) -> bool:
        is_valid, nuevo_producto = self.validate_product(nombre, precio, coste, stock, imagen_ruta)
        if not is_valid:
            return False

        datos_producto = {
            'nombre': nombre,
            'precio': precio,
            'coste': coste,
            'stock': stock,
            'imagen_ruta': imagen_ruta,
        }

        if id_producto:
            # Actualización
            nuevo_producto.id = id_producto
            self.__sql_manager.put_data(
                Producto,
                id_producto,
                datos_producto,
            )
        else:
            # Creación
            self.__sql_manager.add_data(nuevo_producto)

        return True

    def delete_producto(self, producto: Producto):
        # TODO: Eliminar en backend
        self.__sql_manager.delete_data(Producto, producto.id)
