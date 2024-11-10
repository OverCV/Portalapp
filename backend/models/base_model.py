from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T', bound='BaseModel')


@dataclass
class BaseModel:
    id: int
