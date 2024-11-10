from backend.app.services.ventas import (
    add_venta,
    get_ventas,
    calcular_total_venta,
    filtrar_productos_con_stock,
)

from datetime import datetime
from backend.data.managers.csv_manager import CSVManager
