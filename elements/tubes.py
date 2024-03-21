from abc import ABC, abstractmethod


class AbstractTube(ABC):
    def __init__(self, length: int, position: tuple, alignment: str):
        self._position = position
        self._length = length
        self._alignment = alignment

    @property
    def position(self):
        return self._position

    @property
    def length(self):
        return self._length

    @property
    def alignment(self):
        return self._alignment


class VerticalTube(AbstractTube):
    def __init__(self, length: int, position: tuple):
        super().__init__(length, position, "y")


class HorizontalTube(AbstractTube):
    def __init__(self, length: int, position: tuple):
        super().__init__(length, position, "x")


if __name__ == "__main__":
    ...
