import flet as fl

from frontend.app.enums.routes import Routes


def mostrar_inicio(page: fl.Page):
    view = fl.View(
        Routes.HOME,
        [
            fl.AppBar(
                title=fl.Text('Inicio'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view
