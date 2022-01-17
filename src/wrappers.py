
from dataclasses import dataclass

@dataclass
class Window:
    w: int
    h: int


@dataclass
class V2i:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        if isinstance(other, V2i):
            x = self.x + other.x
            y = self.y + other.y
            return V2i(x, y)
        raise SystemExit(f"Cannot add {type(self)} to {type(other)}!")

