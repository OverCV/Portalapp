import flet as fl

from frontend.app.enums.app import AppRoutes
from backend.data.managers.csv_manager import CSVManager


def mostrar_ventas(page: fl.Page, sql_manager: CSVManager):
    view = fl.View(
        AppRoutes.VENTAS,
        [
            fl.AppBar(
                title=fl.Text('Realizar venta 🛒'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view
