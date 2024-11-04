import flet as fl

from frontend.app.enums.routes import Routes


def mostrar_ventas(page: fl.Page):
    view = fl.View(
        Routes.VENTAS,
        [
            fl.AppBar(
                title=fl.Text('Ventas'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view