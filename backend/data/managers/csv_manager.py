import csv
from pathlib import Path
from typing import Type, TypeVar, List, Dict, Any, Optional

from backend.app.enums.application import Portalapp
from backend.app.enums.reports import Reports
from backend.app.enums.manager import CSVModels
from datetime import datetime

from backend.models.base_model import T
from backend.models.deuda import Deuda
from backend.models.producto import Producto
from backend.models.venta_producto import VentaProducto
from backend.models.deudor import Deudor
from backend.models.venta import Venta
from backend.models.abono import Abono

from dataclasses import asdict, fields


class CSVManager:
    """
    Clase utilitaria para gestionar operaciones de archivos CSV para diferentes modelos de datos.

    Esta clase proporciona métodos para crear, leer, actualizar y eliminar datos en archivos CSV,
    con soporte para varios modelos de datos a través de registro dinámico y análisis de tipos.

    Atributos:
        __data_dir (Path): Ruta del directorio donde se almacenarán los archivos CSV.
        file_map (dict): Mapea clases de modelos con sus rutas de archivos CSV correspondientes.
        column_map (dict): Mapea clases de modelos con sus nombres de columnas.
    """

    def __init__(self):
        self.__data_dir = Path(Portalapp.DATABASE_PATH)
        self.__data_dir.mkdir(exist_ok=True)

        self.file_map = {}
        self.column_map = {}

        self.register_model(Producto, 'productos')
        self.register_model(VentaProducto, 'ventas_productos')
        self.register_model(Venta, 'ventas')
        self.register_model(Deuda, 'deudas')
        self.register_model(Deudor, 'deudores')
        self.register_model(Abono, 'abonos')

    def register_model(self, model_class: Type[T], file_name: str):
        """
        Lee datos de un archivo CSV y los convierte en una lista de instancias de modelo.

        Este método realiza los siguientes pasos:
        - Obtiene la ruta del archivo para la clase de modelo
        - Abre el archivo CSV con la codificación especificada
        - Lee los datos utilizando un DictReader
        - Convierte cada fila en una instancia del modelo
        - Parsea los valores de cada campo para garantizar el tipo correcto

        Args:
            model_class (Type[T]): La clase de modelo utilizada para crear instancias.

        Returns:
            List[T]: Una lista de instancias de modelo parseadas desde el archivo CSV.

        Raises:
            IOError: Si hay un problema al leer el archivo.
            ValueError: Si los datos no pueden ser convertidos al modelo.
        """
        file_path = self.__data_dir / f'{file_name}.csv'
        self.file_map[model_class] = file_path
        self.column_map[model_class] = [field.name for field in fields(model_class)]
        self.__init_file(file_path, self.column_map[model_class])

    def __init_file(self, file_path: Path, columns: List[str]):
        """
        Inicializa un archivo CSV con columnas especificadas si el archivo no existe.

        Este método realiza las siguientes tareas:
        - Verifica si el archivo CSV ya existe
        - Si no existe, crea un nuevo archivo
        - Escribe los encabezados de columnas en el archivo

        Args:
            file_path (Path): Ruta completa del archivo CSV.
            columns (List[str]): Nombres de columnas para escribir en el encabezado del CSV.

        Comportamiento:
        - Si el archivo no existe, se crea con los encabezados especificados
        - Utiliza la codificación definida en Reports.ENCODING
        - Escribe una sola fila de encabezados
        - No genera errores si el archivo ya existe
        """
        if not file_path.exists():
            with open(file_path, 'w', newline='', encoding=Reports.ENCODING) as f:
                writer = csv.writer(f)
                writer.writerow(columns)

    def __read_file(self, model_class: Type[T]) -> List[T]:
        """
        Lee datos de un archivo CSV y los convierte en una lista de instancias de modelo.

        Realiza un proceso de lectura y transformación de datos:
        - Obtiene la ruta del archivo para la clase de modelo
        - Lee el archivo CSV utilizando DictReader
        - Convierte cada fila en una instancia del modelo correspondiente
        - Parsea los valores de cada campo para garantizar el tipo correcto

        Args:
            model_class (Type[T]): Clase de modelo utilizada para crear instancias.

        Returns:
            List[T]: Lista de instancias de modelo parseadas desde el archivo CSV.

        Raises:
            IOError: Si existe un problema de lectura del archivo.
            ValueError: Si los datos no pueden convertirse al modelo especificado.
        """
        file_path = self.file_map[model_class]
        with open(file_path, 'r', encoding=Reports.ENCODING) as f:
            reader = csv.DictReader(f)
            return [
                model_class(
                    **{
                        field.name: self.__parse_value(field.type, row[field.name])
                        for field in fields(model_class)
                    }
                )
                for row in reader
            ]

    def __write_file(self, model_class: Type[T], data: List[T]):
        """
        Escribe una lista de instancias de modelo en un archivo CSV.

        Proceso de escritura:
        - Obtiene la ruta del archivo para la clase de modelo
        - Recupera las columnas correspondientes al modelo
        - Abre el archivo en modo escritura
        - Escribe los encabezados de columnas
        - Convierte las instancias de modelo a diccionarios
        - Escribe los datos en el archivo CSV

        Args:
            model_class (Type[T]): Clase de modelo de los datos a escribir.
            data (List[T]): Lista de instancias de modelo para escribir en el CSV.

        Comportamiento:
        - Sobrescribe completamente el archivo existente
        - Utiliza la codificación definida en Reports.ENCODING
        - Mantiene el formato CSV con encabezados

        Raises:
            IOError: Si existe un problema de escritura en el archivo.
        """
        file_path = self.file_map[model_class]
        columns = self.column_map[model_class]
        with open(file_path, 'w', newline='', encoding=Reports.ENCODING) as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows([asdict(item) for item in data])

    def __parse_value(self, field_type: Any, value: str) -> Any:
        """
        Convierte un valor de cadena a un tipo de datos apropiado según el tipo de campo.

        Método robusto de conversión de tipos que soporta:
        - Manejo de valores vacíos
        - Conversión para tipos int, float, datetime, str
        - Soporte para tipos Optional
        - Conversión recursiva de tipos anidados

        Args:
            field_type (Any): Tipo esperado del campo.
            value (str): Valor de cadena a convertir.

        Returns:
            Any: Valor convertido o None si la entrada está vacía.

        Conversiones soportadas:
        - int: Convierte cadena a entero
        - float: Convierte cadena a número de punto flotante
        - datetime: Convierte cadena en formato ISO a objeto datetime
        - str: Devuelve el valor de cadena original
        - Tipos Optional: Analiza recursivamente el tipo subyacente
        """
        if not value:  # Manejo de valores vacíos
            return None

        if field_type is int:
            return int(value)
        elif field_type is float:
            return float(value)
        elif field_type is datetime:
            return datetime.fromisoformat(value)
        elif field_type is str:
            return value  # Retorno sin conversión si es cadena
        elif hasattr(field_type, '__origin__') and field_type.__origin__ is Optional:
            # Si el tipo es Optional (ejemplo: Optional[int]), procesamos el sub-tipo
            return self.__parse_value(field_type.__args__[0], value)

        return value

    def add_data(self, item: T) -> T:
        """
        Agrega un nuevo elemento a un archivo CSV, asignando un ID único.

        Este método realiza las siguientes operaciones:
        - Determina la clase del modelo del elemento
        - Lee los datos existentes del archivo CSV
        - Calcula el próximo ID disponible
        - Asigna el nuevo ID al elemento
        - Agrega el elemento a la lista de datos
        - Escribe los datos actualizados en el archivo CSV

        Args:
            item (T): El elemento del modelo de datos a agregar.

        Returns:
            T: El elemento agregado con un ID recién asignado.

        Proceso:
        - Si no hay datos existentes, el ID inicial es 0
        - Incrementa el último ID en 1
        - Agrega el elemento al final de la lista de datos
        - Guarda todos los datos en el archivo CSV
        """
        model_class = type(item)
        data = self.__read_file(model_class)
        last_id = int(data[-1].id) if data else 0
        item.id = last_id + 1
        data.append(item)
        self.__write_file(model_class, data)
        return item

    def get_data(self, model_class: Type[T]) -> List[T]:
        """
        Recupera todos los datos de un modelo específico desde su archivo CSV.

        Método que lee y devuelve todos los elementos de un tipo de modelo
        almacenados en el archivo CSV correspondiente.

        Args:
            model_class (Type[T]): La clase de modelo cuyos datos se desean recuperar.

        Returns:
            List[T]: Una lista con todos los elementos del modelo especificado.

        Comportamiento:
        - Utiliza el método privado __read_file para leer los datos
        - Devuelve todos los elementos sin modificación
        - Si no hay datos, devuelve una lista vacía

        Ejemplo:
            productos = csv_manager.get_data(Producto)  # Recupera todos los productos
        """
        return self.__read_file(model_class)

    def get_data_by_id(self, model_class: Type[T], id_value: int) -> T:
        """
        Recupera un elemento específico por su ID desde el archivo CSV correspondiente.

        Busca y devuelve un elemento único basándose en su identificador único.

        Args:
            model_class (Type[T]): La clase de modelo donde se buscará el elemento.
            id_value (int): El ID del elemento a recuperar.

        Returns:
             T: El elemento con el ID coincidente.

         Raises:
             ValueError: Si no se encuentra ningún elemento con el ID proporcionado.

         Proceso:
         - Lee todos los datos del modelo
         - Itera sobre los elementos buscando coincidencia de ID
         - Lanza una excepción si no se encuentra el elemento
        """
        data = self.__read_file(model_class)
        for item in data:
            if item.id == id_value:
                return item
        raise ValueError(f'Item with id {id_value} not found in {model_class.__name__}')

    def put_data(self, model_class: Type[T], id_value: int, updates: Dict[str, Any]) -> T:
        """
        Actualiza un elemento existente en el archivo CSV.

        Busca un elemento por su ID y aplica las actualizaciones especificadas.

        Args:
            model_class (Type[T]): La clase de modelo del elemento a actualizar.
            id_value (int): El ID del elemento a modificar.
            updates (Dict[str, Any]): Un diccionario con los campos y valores a actualizar.

        Returns:
            T: El elemento actualizado.

        Raises:
            ValueError: Si no se encuentra ningún elemento con el ID proporcionado.

        Proceso:
        - Lee todos los datos del modelo
        - Busca el elemento con el ID especificado
        - Actualiza los campos indicados en el diccionario de actualizaciones
        - Escribe los datos modificados en el archivo CSV

        Ejemplo:
            csv_manager.put_data(Producto, 5, {'precio': 1200, 'stock': 50})
        """
        data = self.__read_file(model_class)
        updated_item = None
        for item in data:
            if item.id == id_value:
                for field, value in updates.items():
                    setattr(item, field, value)
                updated_item = item
                break
        if updated_item:
            self.__write_file(model_class, data)
            return updated_item
        raise ValueError(f'Item with id {id_value} not found in {model_class.__name__}')

    def delete_data(self, model_class: Type[T], id_value: int) -> bool:
        """
        Elimina un elemento de un archivo CSV según su ID.

        Busca y elimina un elemento específico basándose en su identificador único.

        Args:
            model_class (Type[T]): La clase de modelo del elemento a eliminar.
            id_value (int): El ID del elemento a eliminar.

        Returns:
            bool: True si se eliminó un elemento, False si no se encontró.

        Proceso:
        - Lee todos los datos del modelo
        - Crea una nueva lista sin el elemento con el ID especificado
        - Si la lista cambia de tamaño, significa que se eliminó un elemento
        - Escribe los datos actualizados en el archivo CSV

        Ejemplo:
            eliminado = csv_manager.delete_data(Producto, 5)  # Retorna True/False
        """
        data = self.__read_file(model_class)
        new_data = [item for item in data if item.id != id_value]
        if len(new_data) != len(data):
            self.__write_file(model_class, new_data)
            return True
        return False
