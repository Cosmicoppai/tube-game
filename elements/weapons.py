from abc import ABC, abstractmethod


class AbstractWeapon(ABC):
    def __init__(self):
        self._damage = 10
        self._durability = 100
        self._position = (0, 0)
        self._size = 50
        self._weight = 10

    @abstractmethod
    def attack(self):
        # WILL SHOW THE ANIMATION OF THE WEAPON ATTACKING
        ...

    @property
    def damage(self):
        return self._damage

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, durability: int):
        self._durability = durability

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: tuple):
        self._position = position

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight: int):
        self._weight = weight


class Sword(AbstractWeapon):
    def __init__(self):
        super().__init__()
        self._damage = 20
        self._durability = 100
        self._size = 100
        self._weight = 20

    def attack(self):
        print("Sword attack")


class Gun(AbstractWeapon):
    def __init__(self):
        super().__init__()
        self._damage = 30
        self._durability = 100
        self._size = 50
        self._weight = 10

    def attack(self):
        print("Gun attack")
