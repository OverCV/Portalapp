import flet as fl

from frontend.app.enums.app import AppRoutes
from backend.data.managers.csv_manager import CSVManager


def mostrar_productos(page: fl.Page, sql_manager: CSVManager):
    view = fl.View(
        AppRoutes.PRODUCTOS,
        [
            fl.AppBar(
                title=fl.Text('Mis productos 📦'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view
