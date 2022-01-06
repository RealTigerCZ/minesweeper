from dataclasses import dataclass, field
import pygame, sys, os

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

    def render(self, screen):
        pass


@dataclass
class Textures:
    path: str
    extension: str = "png"

    bomb_tile: str = "bomb_tile"
    bomb_tile_red: str = "bomb_tile_red"
    flag_tile: str = "flag_tile"
    uncovered_tile: str = "uncovered_tile"


@dataclass
class Glo:
    sizeX: int
    sizeY: int
    sizeTile: int
    bombsCount: int
    textures: Textures
    board: list[list[Tile]] = field(default_factory=list)

run = True
screen = pygame.display.set_mode((350, 250), pygame.RESIZABLE)
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0,255,255))
    clock.tick(20)
    print(screen.get_width(), screen.get_height())
    pygame.display.flip()
