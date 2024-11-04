from .operative_system import OS
from .dimensions import Dim


class AppConfig:
    def __init__(self):
        self.__APP_NAME: str = 'Portalapp'
        self.__APP_OS: str = OS.ANDROID

    def get_name(self) -> str:
        return self.__APP_NAME

    def get_window_width(self) -> int:
        options: dict[str, int] = {
            OS.ANDROID: Dim.ANDROID_WIDTH,
            OS.WINDOWS: Dim.WINDOWS_WIDTH,
            OS.IOS: Dim.IOS_WIDTH,
        }
        return options[self.__APP_OS]

    def get_window_height(self) -> int:
        options: dict[str, int] = {
            OS.ANDROID: Dim.ANDROID_HEIGHT,
            OS.WINDOWS: Dim.WINDOWS_HEIGHT,
            OS.IOS: Dim.IOS_HEIGHT,
        }
        return options[self.__APP_OS]


conf = AppConfig()
