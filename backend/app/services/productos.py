from backend.data.managers.csv_manager import CSVManager
from backend.models.producto import Producto


def get_producto_by_id(data_manager: CSVManager, id_producto: int) -> Producto:
    return data_manager.get_data(Producto, id_producto)


def put_producto(
    data_manager: CSVManager,
    id_producto: Producto,
    nuevo_producto: Producto,
) -> None:
    return data_manager.put_data(
        Producto,
        id_producto,
        nuevo_producto,
    )
