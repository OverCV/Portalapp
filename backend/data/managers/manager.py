# data/manager.py
from abc import ABC, abstractmethod

class Manager(ABC):
    @abstractmethod
    def get_data(self, source: str):
        pass

    @abstractmethod
    def add_data(self, source: str, data: dict):
        pass

    @abstractmethod
    def put_data(self, source: str, id_source: int, new_source: dict):
        pass

    @abstractmethod
    def delete_data(self, source: str, id_source: int):
        pass
