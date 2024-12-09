import flet as fl

from frontend.app.enums.app import AppRoutes
from backend.data.managers.csv_manager import CSVManager


def mostrar_inicio(page: fl.Page, sql_manager: CSVManager):
    """Crea y configura la vista inicial de la aplicación.

    Esta función genera la pantalla de inicio para la aplicación Portalapp,
    estableciendo una barra de aplicación con un título de bienvenida.

    Args:
        page (fl.Page): La página principal de la aplicación Flet donde se
                        renderizará la vista.
        sql_manager (CSVManager): Gestor de datos CSV para manejar
                            operaciones de datos si son necesarias.

    Returns:
        fl.View: La vista de la página de inicio configurada con una barra
                de aplicación que muestra un mensaje de bienvenida.

    Notas:
        - La función actualiza la página después de crear la vista.
        - Utiliza la ruta AppRoutes.HOME para identificar la vista.
        - Incluye un título de bienvenida centrado con un emoji de herramienta.
    """
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
