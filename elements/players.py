from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def jump(self):
        ...

    @abstractmethod
    def attack(self):
        ...

    @abstractmethod
    def size(self, size: int):
        ...

    @abstractmethod
    def position(self, x: int, y: int):
        ...
