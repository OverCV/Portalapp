from backend.data.manager import Manager


def put_producto(data_manager: Manager, id_producto: dict, nuevo_producto: dict):
    return data_manager.put_data(
        'productos',
        id_producto,
        nuevo_producto,
    )