import flet as fl
from typing import Callable

from frontend.app.enums.routes import Routes
from frontend.app.enums.config import conf

from frontend.home.view import mostrar_inicio
from frontend.deudores.view import mostrar_deudores
from frontend.productos.view import mostrar_productos
from frontend.ventas.view import mostrar_ventas

class Portalapp:
    def __init__(self):
        pass

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
                    icon=fl.icons.HOME_OUTLINED,
                    selected_icon=fl.icons.HOME_FILLED,
                    label='Inicio',
                ),fl.NavigationBarDestination(
                    icon=fl.icons.INVENTORY_2_OUTLINED,
                    selected_icon=fl.icons.INVENTORY_2,
                    label='Productos',
                ),
                fl.NavigationBarDestination(
                    icon=fl.icons.SHOPPING_CART_OUTLINED,
                    selected_icon=fl.icons.SHOPPING_CART,
                    label='Ventas',
                ),
                fl.NavigationBarDestination(
                    icon=fl.icons.PEOPLE_OUTLINED,
                    selected_icon=fl.icons.PEOPLE,
                    label='Deudores',
                ),
            ],
            on_change=self.navigation_changed,
        )

        # Router
        async def route_change(e: fl.RouteChangeEvent):
            page.views.clear()
            route = e.route

            print(f'{route=}')

            all_routes: dict[str, Callable] = {
                Routes.HOME: mostrar_inicio,
                Routes.PRODUCTOS: mostrar_productos,
                Routes.VENTAS: mostrar_ventas,
                Routes.DEUDORES: mostrar_deudores,
            }

            page.views.append(
                all_routes[route](
                    page,
                )
                if route in all_routes
                else mostrar_inicio(page)
            )

            # Agregar la barra de navegación a todas las vistas
            page.views[-1].navigation_bar = nav_rail
            page.update()

        page.on_route_change = route_change
        #! Ruta inicial !#
        page.go(Routes.HOME)

    async def navigation_changed(self, e: fl.Page):
        added_routes = [
            Routes.HOME,
            Routes.PRODUCTOS,
            Routes.VENTAS,
            Routes.DEUDORES
        ]
        e.page.go(added_routes[e.control.selected_index])
        
