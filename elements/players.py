from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    def __init__(self):
        self._health = 100
        self._position = (0, 0)
        self._size = 50

    def move(self, axis: str, direction: str, distance: int) -> None:
        if axis == "x":
            self.position = (self.position[0] + distance, self.position[1]) if direction == "right" else (self.position[0] - distance, self.position[1])
        elif axis == "y":
            self.position = (self.position[0], self.position[1] + distance) if direction == "down" else (self.position[0], self.position[1] - distance)

    def jump(self, distance: int = 50) -> None:
        self.position = (self.position[0], self.position[1] - distance)

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


class Player(AbstractPlayer):
    def attack(self):
        print("Player attacks")


if __name__ == "__main__":
    player = Player()
    player.attack()
    print(player.position)
    player.move("x", "right", 10)
    print(player.position)
    player.jump(20)
    print(player.position)
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



