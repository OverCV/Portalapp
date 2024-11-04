import flet as fl

from frontend.app.enums.routes import Routes


def mostrar_deudores(page: fl.Page):
    view = fl.View(
        Routes.DEUDORES,
        [
            fl.AppBar(
                title=fl.Text('Deudores'),
                center_title=True,
            ),
        ],
    )
    page.update()
    return view