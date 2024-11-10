import csv
from pathlib import Path
from typing import Type, TypeVar, List, Dict, Any
from backend.data.managers.manager import Manager
from backend.models.base_model import T

from backend.app.enums.application import Portalapp
from backend.app.enums.reports import Reports
from backend.app.enums.manager import CSVModels
from datetime import datetime

from dataclasses import asdict, fields


class CSVManager:
    def __init__(self):
        # Directorio de datos
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

        # Mapeo de archivos y columnas para cada modelo (basado en el nombre del modelo)
        self.file_map = {}
        self.column_map = {}

    def register_model(self, model_class: Type[T], file_name: str):
        """Registra un modelo para que sea manejado por CSVManager."""
        file_path = self.data_dir / f'{file_name}.csv'
        self.file_map[model_class] = file_path
        self.column_map[model_class] = [field.name for field in fields(model_class)]
        self._init_file(file_path, self.column_map[model_class])

    def _init_file(self, file_path: Path, columns: List[str]):
        """Inicializa el archivo CSV con las columnas especificadas si no existe."""
        if not file_path.exists():
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)

    def _read_file(self, model_class: Type[T]) -> List[T]:
        file_path = self.file_map[model_class]
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [
                model_class(
                    **{
                        field: self._parse_value(field_type, row[field])
                        for field, field_type in model_class.__annotations__.items()
                    }
                )
                for row in reader
            ]

    def _write_file(self, model_class: Type[T], data: List[T]):
        file_path = self.file_map[model_class]
        columns = self.column_map[model_class]
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows([asdict(item) for item in data])

    def add_data(self, item: T) -> T:
        model_class = type(item)
        data = self._read_file(model_class)
        last_id = data[-1].id if data else 0
        item.id = last_id + 1
        data.append(item)
        self._write_file(model_class, data)
        return item

    def get_data(self, model_class: Type[T]) -> List[T]:
        return self._read_file(model_class)

    def put_data(self, model_class: Type[T], id_value: int, updates: Dict[str, Any]) -> T:
        data = self._read_file(model_class)
        updated_item = None
        for item in data:
            if item.id == id_value:
                for field, value in updates.items():
                    setattr(item, field, value)
                updated_item = item
                break
        if updated_item:
            self._write_file(model_class, data)
            return updated_item
        raise ValueError(f'Item with id {id_value} not found in {model_class.__name__}')

    def delete_data(self, model_class: Type[T], id_value: int) -> bool:
        data = self._read_file(model_class)
        new_data = [item for item in data if item.id != id_value]
        if len(new_data) != len(data):
            self._write_file(model_class, new_data)
            return True
        return False

    def _parse_value(self, field_type: Any, value: str) -> Any:
        """Convierte el valor de string a un tipo adecuado."""
        if isinstance(field_type, int):
            return int(value)
        elif isinstance(field_type, float):
            return float(value)
        elif isinstance(field_type, datetime):
            return datetime.fromisoformat(value)
        return value
