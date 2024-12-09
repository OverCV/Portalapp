import flet as fl

from frontend.app.enums.app import AppRoutes
from backend.data.managers.csv_manager import CSVManager


def mostrar_deudores(page: fl.Page, sql_manager: CSVManager):
    """Función que construye y muestra la vista principal de deudores.

    Esta función crea una vista básica con una barra de navegación superior
    que muestra el título de la sección de deudores.

    Args:
        page (fl.Page): Instancia de la página de Flet donde se renderizará la vista.
        sql_manager (CSVManager): Instancia del manejador de datos CSV que gestiona
            la persistencia de información.

    Returns:
        fl.View: Vista construida con la barra de navegación y título de deudores.
    """
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
