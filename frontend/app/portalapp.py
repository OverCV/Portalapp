# from typing import Callable
import flet as fl
from typing import Callable

from frontend.app.enums.routes import Routes

from frontend.home.view import mostrar_inicio

from frontend.app.enums.config import conf


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
        ]
        e.page.go(added_routes[e.control.selected_index])
