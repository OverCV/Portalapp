import csv
from pathlib import Path
from typing import List, Dict, Any
from backend.data.managers.manager import Manager

from backend.app.enums.application import Portalapp
from backend.app.enums.reports import Reports
from backend.app.enums.manager import CSVModels


class CSVManager(Manager):
    def __init__(self):
        # Directorio base para los archivos
        self.data_dir = Path(Portalapp.DATABASE_PATH)
        self.data_dir.mkdir(exist_ok=True)

        # Rutas de los archivos
        self.productos_file = self.data_dir / CSVModels.PRODUCTOS
        self.ventas_file = self.data_dir / CSVModels.VENTAS
        self.deudas_file = self.data_dir / CSVModels.DEUDAS
        self.deudores_file = self.data_dir / CSVModels.DEUDORES
        self.venta_productos_file = self.data_dir / CSVModels.VENTA_PRODUCTOS

        # Mapeo de columnas de cada archivo CSV
        self.column_map = {
            self.productos_file: ['id', 'nombre', 'precio', 'stock'],
            self.ventas_file: ['id', 'fecha', 'ganancia'],
            self.deudas_file: ['id', 'id_venta', 'id_deudor', 'valor_deuda', 'creacion_deuda'],
            self.venta_productos_file: ['id', 'id_venta', 'id_producto', 'cantidad'],
            self.deudores_file: ['id', 'nombre', 'telefono'],
        }

        # Inicializar archivos CSV con columnas si no existen
        self._init_files()

    def _init_files(self):
        for file, columns in self.column_map.items():
            if not file.exists():
                with open(file, 'w', newline='', encoding=Reports.ENCODING) as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)

    def _read_file(self, file_path: Path) -> List[Dict[str, Any]]:
        with open(file_path, 'r', encoding=Reports.ENCODING) as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def _write_file(self, file_path: Path, data: List[Dict[str, Any]]):
        with open(file_path, 'w', newline='', encoding=Reports.ENCODING) as f:
            columns = self.column_map[file_path]
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)

    def get_data(self, source: str) -> List[Dict[str, Any]]:
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            return self._read_file(file_path)
        raise ValueError(f"Source '{source}' not recognized.")

    def add_data(self, source: str, item: Dict[str, Any]) -> Dict[str, Any]:
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            last_id = int(data[-1]['id']) if data else 0
            item['id'] = last_id + 1
            data.append(item)
            self._write_file(file_path, data)
            return item
        raise ValueError(f"Source '{source}' not recognized.")

    def put_data(self, source: str, id_source: int, new_source: Dict[str, Any]) -> Dict[str, Any]:
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            for row in data:
                if int(row['id']) == id_source:
                    row.update(new_source)
                    self._write_file(file_path, data)
                    return row
        raise ValueError(f"Source '{source}' not recognized.")

    def delete_data(self, source: str, id_source: int) -> bool:
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            data = [row for row in data if int(row['id']) != id_source]
            self._write_file(file_path, data)
            return True
        raise ValueError(f"Source '{source}' not recognized.")
