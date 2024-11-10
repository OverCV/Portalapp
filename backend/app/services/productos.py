from backend.data.managers.manager import Manager
from backend.models.producto import Producto


def get_producto_by_id(data_manager: Manager, id_producto: int) -> Producto:
    return data_manager.get_data(Producto, id_producto)


def put_producto(
    data_manager: Manager,
    id_producto: Producto,
    nuevo_producto: Producto,
) -> None:
    return data_manager.put_data(
        Producto,
        id_producto,
        nuevo_producto,
    )
