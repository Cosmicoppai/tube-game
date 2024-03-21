from abc import ABC, abstractmethod


class Tube(ABC):
    @abstractmethod
    def position(self, x: int, y: int):
        ...

    @abstractmethod
    def length(self, length: int):
        ...

    @abstractmethod
    def alignment(self, alignment: str):
        # whether tube is aligned in x or y direction
        ...
