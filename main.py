# main.py
import flet as fl
from flet_core.types import AppView


from frontend.app.portalapp import Portalapp
from backend.constants.application import __MAIN__


def main() -> None:
    """Application initializer."""
    app: Portalapp = Portalapp()
    fl.app(
        target=app.main,
        view=AppView.FLET_APP,
    )


if __name__ == __MAIN__:
    main()
