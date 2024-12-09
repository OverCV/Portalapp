# frontend\app\portalapp.py
import flet as fl
from typing import Callable

from frontend.app.enums.config import conf
from frontend.app.enums.app import AppRoutes
from frontend.app.enums.app import AppLabels

from backend.data.managers.csv_manager import CSVManager

from frontend.deudores.view import mostrar_deudores
from frontend.home.view import mostrar_inicio
from frontend.productos.view import mostrar_productos
from frontend.ventas.view import mostrar_ventas


class Portalapp:
    """Clase principal que implementa la aplicación del portal usando Flet.

    Esta clase maneja la configuración inicial, el enrutamiento y la navegación
    de la aplicación. Define la estructura base de la interfaz gráfica incluyendo
    la barra de navegación inferior.

    Attributes:
        __sql_manager (CSVManager): Instancia del manejador de datos CSV.
        __app_routes (dict[str, Callable]): Diccionario que mapea rutas a funciones
            que generan las vistas correspondientes.
    """

    def __init__(self):
        """Inicializa la aplicación configurando el manejador de datos y las rutas."""
        self.__sql_manager = CSVManager()
        self.__app_routes: dict[str, Callable] = {
            AppRoutes.HOME: mostrar_inicio,
            AppRoutes.PRODUCTOS: mostrar_productos,
            AppRoutes.VENTAS: mostrar_ventas,
            AppRoutes.DEUDORES: mostrar_deudores,
        }

    async def main(self, page: fl.Page):
        """Método principal que configura y arranca la aplicación.

        Configura la página inicial, el tema, dimensiones de la ventana y
        establece la barra de navegación y el sistema de enrutamiento.

        Args:
            page (fl.Page): Instancia de la página principal de Flet donde
                se renderizará toda la aplicación.

        Example:
            >>> app = Portalapp()
            >>> fl.app(target=app.main)
        """
        page.title = conf.get_name()
        page.theme_mode = fl.ThemeMode.LIGHT
        page.window.height = conf.get_window_height()
        page.window.width = conf.get_window_width()

        nav_rail = fl.NavigationBar(
            selected_index=0,
            destinations=[
                fl.NavigationBarDestination(
                    label=AppLabels.HOME,
                    icon=fl.icons.HOME_OUTLINED,
                    selected_icon=fl.icons.HOME_FILLED,
                ),
                fl.NavigationBarDestination(
                    label=AppLabels.PRODUCTOS,
                    icon=fl.icons.INVENTORY_2_OUTLINED,
                    selected_icon=fl.icons.INVENTORY_2,
                ),
                fl.NavigationBarDestination(
                    label=AppLabels.VENTAS,
                    icon=fl.icons.SHOPPING_CART_OUTLINED,
                    selected_icon=fl.icons.SHOPPING_CART,
                ),
                fl.NavigationBarDestination(
                    label=AppLabels.DEUDORES,
                    icon=fl.icons.PEOPLE_OUTLINED,
                    selected_icon=fl.icons.PEOPLE,
                ),
            ],
            on_change=self.navigation_changed,
        )

        async def route_change(e: fl.RouteChangeEvent):
            page.views.clear()
            route = e.route
            page.views.append(
                self.__app_routes[route](page, self.__sql_manager)
                if route in self.__app_routes
                else mostrar_inicio(page, self.__sql_manager)
            )

            page.views[-1].navigation_bar = nav_rail
            page.update()

        page.on_route_change = route_change

        page.go(AppRoutes.HOME)

    async def navigation_changed(self, e: fl.Page):
        """Maneja los cambios en la barra de navegación.

        Este método se ejecuta cuando el usuario selecciona un destino diferente
        en la barra de navegación, actualizando la ruta actual de la aplicación.

        Args:
            e (fl.Page): Evento que contiene la información de la página y
                el nuevo índice seleccionado.

        Note:
            La navegación se realiza usando las rutas definidas en __app_routes
            correspondientes al índice seleccionado en la barra de navegación.
        """
        added_routes = list(self.__app_routes.keys())
        e.page.go(added_routes[e.control.selected_index])
