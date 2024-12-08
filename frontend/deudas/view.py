import flet as fl

from frontend.app.enums.app import AppRoutes
from backend.data.managers.csv_manager import CSVManager


def mostrar_deudores(page: fl.Page, sql_manager: CSVManager):
    view = fl.View(
        AppRoutes.DEUDORES,
        [
            fl.AppBar(
                title=fl.Text('Mis deudores 💸'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view
