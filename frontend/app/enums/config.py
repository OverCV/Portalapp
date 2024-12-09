from .operative_system import OS
from .dimensions import Dim
from .app import AppParams


class AppConfig:
    """Clase que maneja la configuración de la aplicación según el sistema operativo.

    Esta clase proporciona métodos para obtener el nombre de la aplicación y las
    dimensiones de la ventana según la plataforma en la que se está ejecutando.

    Attributes:
        __APP_NAME (str): Nombre de la aplicación definido en AppParams.
        __APP_OS (str): Sistema operativo actual, por defecto ANDROID.
    """

    def __init__(self):
        """Inicializa la configuración con valores predeterminados."""
        self.__APP_NAME: str = AppParams.APP_NAME
        self.__APP_OS: str = OS.ANDROID

    def get_name(self) -> str:
        """Obtiene el nombre de la aplicación.

        Returns:
            str: Nombre de la aplicación definido en la configuración.
        """
        return self.__APP_NAME

    def get_window_width(self) -> int:
        """Obtiene el ancho de la ventana según el sistema operativo.

        Returns:
            int: Ancho de la ventana en píxeles correspondiente al sistema
                operativo actual.

        Note:
            Los valores de ancho están definidos en la clase Dim para cada
            plataforma (ANDROID, WINDOWS, IOS).
        """
        options: dict[str, int] = {
            OS.ANDROID: Dim.ANDROID_WIDTH,
            OS.WINDOWS: Dim.WINDOWS_WIDTH,
            OS.IOS: Dim.IOS_WIDTH,
        }
        return options[self.__APP_OS]

    def get_window_height(self) -> int:
        """Obtiene el alto de la ventana según el sistema operativo.

        Returns:
            int: Alto de la ventana en píxeles correspondiente al sistema
                operativo actual.

        Note:
            Los valores de alto están definidos en la clase Dim para cada
            plataforma (ANDROID, WINDOWS, IOS).
        """
        options: dict[str, int] = {
            OS.ANDROID: Dim.ANDROID_HEIGHT,
            OS.WINDOWS: Dim.WINDOWS_HEIGHT,
            OS.IOS: Dim.IOS_HEIGHT,
        }
        return options[self.__APP_OS]


conf = AppConfig()
