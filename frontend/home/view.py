import flet as fl

from frontend.app.enums.app import AppRoutes
from backend.data.managers.csv_manager import CSVManager


def mostrar_inicio(page: fl.Page, sql_manager: CSVManager):
    view = fl.View(
        AppRoutes.HOME,
        [
            fl.AppBar(
                title=fl.Text('Bienvenido a Portalapp 🧰'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view
