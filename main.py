# main.py
import flet as fl
from flet_core.types import AppView


from frontend.app.portalapp import Portalapp
from backend.constants.application import __MAIN__


def main() -> None:
    """
    Función principal de inicialización de la aplicación.

    Responsabilidades:
    - Crea una instancia de la aplicación Portal
    - Lanza la aplicación utilizando el framework Flet
    - Configura la vista de la aplicación como una aplicación Flet nativa
    """
    app: Portalapp = Portalapp()
    fl.app(
        target=app.main,
        view=AppView.FLET_APP,
    )


if __name__ == __MAIN__:
    main()
