from abc import ABC, abstractmethod
from . import colors
from .config import SCREEN_WIDTH, BULLET_SPEED
from pygame import sprite, Surface


class AbstractWeapon(ABC):
    def __init__(self):
        self._damage = 10
        self._durability = 100
        self._position = (0, 0)
        self._size = 50
        self._weight = 10
        self.owner: object = None
        self._has_hit = False

    @abstractmethod
    def attack(self, start_pos: tuple, direction: str = "right"):
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

    @property
    def has_hit(self):
        return self._has_hit

    @has_hit.setter
    def has_hit(self, value: bool):
        if self._has_hit:
            return
        self._has_hit = value


class Sword(AbstractWeapon):
    def __init__(self):
        super().__init__()
        self._damage = 20
        self._durability = 100
        self._size = 100
        self._weight = 20

    def attack(self, start_pos: tuple, direction: str = "right"):
        print("Sword attack")


class Gun(AbstractWeapon):
    def __init__(self):
        super().__init__()
        self._damage = 10
        self._durability = 100
        self._size = 100
        self._weight = 20

    def attack(self, start_pos: tuple, direction: str = "right") -> sprite.Sprite:
        bullet = Bullet(start_pos, BULLET_SPEED if direction == "right" else -BULLET_SPEED)
        bullet.owner = self.owner
        return bullet


class Bullet(sprite.Sprite):
    def __init__(self, start_pos, speed=BULLET_SPEED):
        super().__init__()
        self.surf = Surface((10, 5))
        self.surf.fill(colors.BLACK)
        self.rect = self.surf.get_rect(center=start_pos)
        self.speed = speed
        self.owner = None
        self.has_hit = False

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()