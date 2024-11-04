import flet as fl

from frontend.app.enums.routes import Routes


def mostrar_productos(page: fl.Page):
    view = fl.View(
        Routes.PRODUCTOS,
        [
            fl.AppBar(
                title=fl.Text('Mis productos'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view