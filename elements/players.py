from abc import ABC, abstractmethod
from .tubes import HorizontalTube, VerticalTube, AbstractTube
from .config import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT
from .weapons import AbstractWeapon, Gun
from pygame.sprite import Sprite


class AbstractPlayer(ABC):
    def __init__(self, player_id: str, weapon: AbstractWeapon = None):
        self.id: str = player_id
        self._health = 100
        self._position = (0, 0)
        self._size = 50
        self.on_ground = True
        self.velocity_y = 0
        self.jump_velocity = 15
        self.weapon = weapon
        self.last_direction = "right"

    def move(self, axis: str, direction: str, distance: int) -> None:
        if axis == "x":
            if direction == "right":
                self.position = (min(self.position[0] + distance, SCREEN_WIDTH - self._size), self.position[1])
            else:
                self.position = max(self.position[0] - distance, 0), self.position[1]
            self.last_direction = direction

        elif axis == "y":
            if direction == "up":
                self.position = (self.position[0], min(self.position[1] - distance, 0))
            else:
                self.position = (self.position[0], min(self.position[1] + distance, SCREEN_HEIGHT))

    def jump(self):
        if self.on_ground:
            self.velocity_y = - self.jump_velocity
            self.on_ground = False

    def update_position(self):
        self.velocity_y += GRAVITY
        self.move('y', 'down', int(self.velocity_y))

        if self.position[1] >= SCREEN_HEIGHT - FLOOR_HEIGHT - self.size:
            self.position = (self.position[0], SCREEN_HEIGHT - FLOOR_HEIGHT - self.size)
            self.velocity_y = 0
            self.on_ground = True

        if self.position[0] < 0:
            self.position = (0, self.position[1])
        if self.position[1] > SCREEN_WIDTH:
            self.position = (SCREEN_WIDTH, self.position[1])

    def enter_tube(self, tube: AbstractTube):
        if isinstance(tube, HorizontalTube):
            self.position = (tube.position[0], self.position[1])
        elif isinstance(tube, VerticalTube):
            self.position = (self.position[0], tube.position[1])

    @abstractmethod
    def attack(self):
        ...

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: tuple):
        self._position = position

    def damage(self, damage: int):
        damage = abs(damage)
        if damage > self._health:
            self._health = 0
            return

        self._health -= damage

    def heal(self, heal: int):
        heal = abs(heal)
        if self._health + heal > 100:
            self._health = 100
            return
        self._health += heal

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value


class Player(AbstractPlayer):

    def __init__(self, player_id: str, weapon: AbstractWeapon = None):
        super().__init__(player_id, weapon)
        if self.weapon is None:
            self.weapon = Gun()
        self.weapon.owner = self

    def attack(self) -> Sprite:
        pos = (self.position[0], self.position[1] + self.size // 2)
        return self.weapon.attack(pos, self.last_direction)


if __name__ == "__main__":
    player = Player("player1")
    player.attack()
    print(player.position)
    player.move("x", "right", 10)
    print(player.position)
    player.jump()
    print(player.position, "position after jump")
    player.size = 100
    print(player.size)
    print(player.health, "health")
    player.damage(10)
    print(player.health, "health after damage")
    player.heal(20)
    print(player.health, "health after healing")
    player.position = (100, 100)
    print(player.position)
    player.move("y", "down", 10)
    print(player.position)
    player.move("y", "up", 10)
    print(player.position)
    player.move("x", "left", 10)
    print(player.position)