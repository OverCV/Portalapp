from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T', bound='BaseModel')


@dataclass
class BaseModel:
    """
    Clase base para modelos de datos utilizada como una estructura fundamental.

    Attributes:
        id (int): Identificador único para cada instancia del modelo.
            Permite identificar y distinguir diferentes objetos de la clase.

    Esta clase utiliza el decorador @dataclass de Python para generar
    automáticamente métodos como __init__, __repr__ y __eq__ basados
    en los atributos definidos.
    """

    id: int
