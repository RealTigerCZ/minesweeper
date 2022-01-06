from dataclasses import dataclass, field
import pygame

class Tile:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.hasBomb = False
        self.bombMembersCount = None

    def find_neighbours(self):
        dirs = [(1,0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for dir in dirs:
            x = dir[0] + self.__x
            y = dir[1] + self.__y
            if x < glo.sizeX and x >= 0 and y < glo.SizeY and y >= 0:
                self.neighbours.append(glo.board[y][x]) 


@dataclass
class Glo:
    sizeX: int
    sizeY: int
    bombsCount: int
    board: list[list[Tile]] = field(default_factory=list)


glo = Glo()
