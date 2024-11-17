# productos/presenter.py #
from typing import List, Optional
from backend.models.producto import Producto
from backend.data.managers.csv_manager import CSVManager

import flet as fl


class ProductosPresenter:
    """Maneja la lógica de negocio y la interacción entre la vista y el modelo para productos.

    Esta clase actúa como el intermediario entre la vista (UI) y el backend
    (administrado por `CSVManager` en este caso). Se encarga de cargar, filtrar,
    validar, guardar y eliminar productos.
    
    Args:
        view (fl.View): La vista que presenta los datos al usuario.
        sql_manager (CSVManager): Administrador para interactuar con la base de datos (en este caso, CSV).
    """
    def __init__(self, view: fl.View, sql_manager: CSVManager):
        """Inicializa el presentador con la vista y el administrador SQL.

        Args:
            view (fl.View): Vista que será actualizada o manipulada.
            sql_manager (CSVManager): Objeto para manejar las operaciones de datos.
        """
        self.__view = view
        self.__search_term: str = ''  # Término de búsqueda actual
        self.__all_productos: List[Producto] = []
        self.__sql_manager = sql_manager

    def load_productos(self) -> List[Producto]:
        """Carga y retorna la lista de productos desde el backend, con un filtro opcional.

        Si hay un término de búsqueda activo, devuelve solo los productos que coincidan.

        Returns:
            List[Producto]: Lista de productos cargados y filtrados.
        """
        # TODO: Integrar con backend
        self.__all_productos = self.__sql_manager.get_data(Producto)
        return (
            self.__all_productos
            if not self.__search_term
            else [p for p in self.__all_productos if p.nombre.lower() in self.__search_term.lower()]
        )

    def search_productos(self, term: str):
        """Actualiza el término de búsqueda y refresca la vista con productos filtrados.

        Args:
            term (str): Término de búsqueda ingresado por el usuario.
        """
        self.__search_term = term.strip()
        self.__view.refresh_productos()  # Actualiza la vista con productos filtrados

    def validate_product(
        self, nombre: str, precio: str, coste: str, stock: str, imagen_ruta: str = None
    ) -> tuple[bool, Optional[Producto]]:
        """Valida los datos de un producto antes de guardarlo o actualizarlo.

        Args:
            nombre (str): Nombre del producto.
            precio (str): Precio en formato de cadena (se convierte a entero).
            stock (str): Stock en formato de cadena (se convierte a entero).
            imagen_ruta (str, optional): Ruta a la imagen del producto. Por defecto, None.

        Returns:
            tuple[bool, Optional[Producto]]: 
                - Un booleano indicando si la validación fue exitosa.
                - El objeto `Producto` validado o None si falló.
        """
        try:
            if not nombre:
                raise ValueError('El nombre es requerido')

            precio_val = self.__validate_precio(precio)
            stock_val = self.__validate_stock(stock)
            coste_val = self.__validate_coste(coste, precio_val)
            self.__validate_imagen(imagen_ruta)

            return True, Producto(
                id=-1, nombre=nombre, precio=precio_val, coste=coste_val, stock=stock_val, imagen_ruta=imagen_ruta
            )
        except ValueError as e:
            self.__view.show_error(str(e))
            return False, None

    def __validate_precio(self, precio: str) -> int:
        """Valida que el precio sea un número entero positivo.

        Args:
            precio (str): Precio ingresado como cadena.

        Returns:
            int: Precio validado como entero.

        Raises:
            ValueError: Si el precio no es un número válido mayor a 0.
        """
        try:
            precio_val = int(precio)
            if precio_val <= 0:
                raise ValueError()
            return precio_val
        except ValueError:
            raise ValueError('Precio debe ser un número entero mayor a 0')

    def __validate_imagen(self, imagen_ruta: str):
        if imagen_ruta:
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
            if not imagen_ruta.lower().endswith(valid_extensions):
                raise ValueError('La imagen debe ser un archivo con formato de imagen válido (jpg, jpeg, png, gif, bmp)')

    def __validate_stock(self, stock: str) -> int:
        """Valida que el stock sea un número entero no negativo.

        Args:
            stock (str): Stock ingresado como cadena.

        Returns:
            int: Stock validado como entero.

        Raises:
            ValueError: Si el stock no es un número válido o es negativo.
        """
        try:
            stock_val = int(stock)
            if stock_val < 0:
                raise ValueError()
            return stock_val
        except ValueError:
            raise ValueError('Stock debe ser un número entero positivo')

    def __validate_coste(self, coste: str, precio: int) -> int:
        try:
            coste_val = int(coste)
            if coste_val < 0 or coste_val >= precio:
                raise ValueError()
            return coste_val
        except ValueError:
            raise ValueError('Coste debe ser un número entero entre 0 y el precio')

    def save_producto(
        self, nombre: str, precio: str, coste: str, stock: str, imagen_ruta: str = None, id_producto: int = None
    ) -> bool:
        """Guarda o actualiza un producto en la base de datos.

        Args:
            nombre (str): Nombre del producto.
            precio (str): Precio del producto.
            stock (str): Cantidad de stock.
            imagen_ruta (str, optional): Ruta a la imagen del producto. Por defecto, None.
            id_producto (int, optional): ID del producto a actualizar. Por defecto, None.

        Returns:
            bool: True si la operación fue exitosa, False si falló.
        """
        is_valid, nuevo_producto = self.validate_product(nombre, precio, stock, imagen_ruta)
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
        """Elimina un producto de la base de datos.

        Args:
            producto (Producto): El producto a eliminar.
        """
        # TODO: Eliminar en backend
        self.__sql_manager.delete_data(Producto, producto.id)
