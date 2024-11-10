from backend.data.managers.manager import Manager
from backend.models.producto import Producto


def put_producto(
    data_manager: Manager,
    id_producto: Producto,
    nuevo_producto: Producto,
) -> None:
    return data_manager.put_data(
        'productos',
        id_producto,
        nuevo_producto,
    )