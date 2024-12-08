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
    def __init__(self):
        # Directorio de datos
        self.__data_dir = Path(Portalapp.DATABASE_PATH)
        self.__data_dir.mkdir(exist_ok=True)

        # Mapeo de archivos y columnas para cada modelo (basado en el nombre del modelo)
        self.file_map = {}
        self.column_map = {}

        self.register_model(Producto, 'productos')
        self.register_model(VentaProducto, 'ventas_productos')
        self.register_model(Venta, 'ventas')
        self.register_model(Deuda, 'deudas')
        self.register_model(Deudor, 'deudores')
        self.register_model(Abono, 'abonos')


    def register_model(self, model_class: Type[T], file_name: str):
        """Registra un modelo para que sea manejado por CSVManager."""
        file_path = self.__data_dir / f'{file_name}.csv'
        self.file_map[model_class] = file_path
        self.column_map[model_class] = [field.name for field in fields(model_class)]
        self.__init_file(file_path, self.column_map[model_class])

    def __init_file(self, file_path: Path, columns: List[str]):
        """Inicializa el archivo CSV con las columnas especificadas si no existe."""
        if not file_path.exists():
            with open(file_path, 'w', newline='', encoding=Reports.ENCODING) as f:
                writer = csv.writer(f)
                writer.writerow(columns)

    def __read_file(self, model_class: Type[T]) -> List[T]:
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
        file_path = self.file_map[model_class]
        columns = self.column_map[model_class]
        with open(file_path, 'w', newline='', encoding=Reports.ENCODING) as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows([asdict(item) for item in data])

    def __parse_value(self, field_type: Any, value: str) -> Any:
        """Convierte el valor de string a un tipo adecuado."""
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
        model_class = type(item)
        data = self.__read_file(model_class)
        last_id = int(data[-1].id) if data else 0
        item.id = last_id + 1
        data.append(item)
        self.__write_file(model_class, data)
        return item

    def get_data(self, model_class: Type[T]) -> List[T]:
        return self.__read_file(model_class)

    def get_data_by_id(self, model_class: Type[T], id_value: int) -> T:
        data = self.__read_file(model_class)
        for item in data:
            if item.id == id_value:
                return item
        raise ValueError(f'Item with id {id_value} not found in {model_class.__name__}')

    def put_data(self, model_class: Type[T], id_value: int, updates: Dict[str, Any]) -> T:
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
        data = self.__read_file(model_class)
        new_data = [item for item in data if item.id != id_value]
        if len(new_data) != len(data):
            self.__write_file(model_class, new_data)
            return True
        return False
