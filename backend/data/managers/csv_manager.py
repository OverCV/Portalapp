
import csv
from pathlib import Path
from typing import List, Dict, Any
from backend.data.manager import Manager

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

        # Inicializar archivos CSV con columnas si no existen
        self._init_files()

    def _init_files(self):
        default_columns = {
            self.productos_file: ['id', 'nombre', 'precio', 'stock'],
            self.ventas_file: ['id', 'fecha', 'ganancia'],
            self.deudas_file: ['id', 'id_venta', 'id_deudor', 'valor_deuda', 'creacion_deuda'],
            self.venta_productos_file: ['id', 'id_venta', 'id_producto', 'cantidad'],
            self.deudores_file: ['id', 'nombre', 'telefono'],
        }
        for file, columns in default_columns.items():
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
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

    def get_data(self, source: str) -> List[Dict]:
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            return self._read_file(file_path)
        raise ValueError(f"Source '{source}' not recognized.")

    def add_data(self, source: str, item: Dict):
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            last_id: int = data[-1]['id'] if data else 0
            item['id'] = int(last_id) + 1
            data.append(item)
            self._write_file(file_path, data)
            return item
        raise ValueError(f"Source '{source}' not recognized.")

    def put_data(self, source: str, id_source: int, new_source: dict):
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            for row in data:
                if row['id'] == id_source:
                    row.update(new_source)
                    self._write_file(file_path, data)
                    return row
        raise ValueError(f"Source '{source}' not recognized.")

    def delete_data(self, source: str, id_source: int):
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            data = [row for row in data if row['id'] != id_source]
            self._write_file(file_path, data)
            return True
        raise ValueError(f"Source '{source}' not recognized.")
