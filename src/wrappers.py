
from dataclasses import dataclass

@dataclass
class Window:
    w: int
    h: int


@dataclass
class V2i:
    x: int = 0
    y: int = 0