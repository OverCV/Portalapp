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
    def __init__(self):
        self.__sql_manager = CSVManager()
        self.__app_routes: dict[str, Callable] = {
            AppRoutes.HOME: mostrar_inicio,
            AppRoutes.PRODUCTOS: mostrar_productos,
            AppRoutes.VENTAS: mostrar_ventas,
            AppRoutes.DEUDORES: mostrar_deudores,
        }

    async def main(self, page: fl.Page):
        page.title = conf.get_name()
        page.theme_mode = fl.ThemeMode.LIGHT
        page.window.height = conf.get_window_height()
        page.window.width = conf.get_window_width()

        # Bottom Navigation #
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

        # Router #
        async def route_change(e: fl.RouteChangeEvent):
            page.views.clear()
            route = e.route
            page.views.append(
                self.__app_routes[route](page, self.__sql_manager)
                if route in self.__app_routes
                else mostrar_inicio(page, self.__sql_manager)
            )
            # Agregar barra de navegación a todas las vistas #
            page.views[-1].navigation_bar = nav_rail
            page.update()

        page.on_route_change = route_change
        #! Ruta inicial !#
        page.go(AppRoutes.HOME)

    async def navigation_changed(self, e: fl.Page):
        added_routes = list(self.__app_routes.keys())
        e.page.go(added_routes[e.control.selected_index])
