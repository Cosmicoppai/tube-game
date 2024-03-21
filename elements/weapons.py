from abc import ABC, abstractmethod


class Weapon(ABC):
    @abstractmethod
    def attack(self):
        ...

    @abstractmethod
    def damage(self, damage: int):
        ...

    @abstractmethod
    def durability(self, durability: int):
        ...

    @abstractmethod
    def position(self, x: int, y: int):
        ...

    @abstractmethod
    def size(self, size: int):
        ...

    @abstractmethod
    def weight(self, weight: int):
        ...
