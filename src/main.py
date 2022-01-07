from dataclasses import dataclass, field
from typing import Tuple
import pygame, sys, os, random

# not used: sysm field!

@dataclass
class Texture:
    """
    - represents one texture -> holds inportant values
    - no need to store every texture image in each 'Tile' separately
    """

    def __init__(self, name: str, ext: str, size: Tuple[int, int], path: os.path):
        self.name = name
        self.name_with_ext = name + "." + ext
        self.path = os.path.join(path, self.name_with_ext)
        self.size = size
        self.image = None


@dataclass
class Textures:
    """Data class Textures which holds path and 'Texture' objects"""

    def __init__(self, path: str):
        self.path = path

        # textures
        self.bomb_tile      = Texture("bomb_tile", "png", (15, 15), path)
        self.bomb_tile_red  = Texture("bomb_tile_red", "png", (15, 15), path)
        self.flag_tile      = Texture("flag_tile", "png", (512, 512), path)
        self.uncovered_tile = Texture("uncovered_tile", "png", (512, 512), path)

        # states
        self.loaded = False

    def __load_texture(self, texture: Texture):
        """Internal method of class 'Textures' used to load one Texture"""
        try:
            texture.image = pygame.image.load(texture.path)

        except pygame.error as message:
            print("Cannot load texture:", texture.name_with_ext)
            raise SystemExit(message)

        except FileNotFoundError as message:
            print("Cannot find texture:", texture.name_with_ext)
            raise SystemExit(message, f"Path: {texture.path}")

        if texture.image.get_size() != texture.size:
            raise SystemExit(
                f"Texture {texture.name_with_ext} cannot be loaded, because it has unexpexted size!\nExpected: {texture.size}, actual: {texture.image.get_size()}\n"
            )

    def load_textures(self):
        """Method to load all Textures"""
        self.__load_texture(self.bomb_tile)
        self.__load_texture(self.bomb_tile_red)
        self.__load_texture(self.flag_tile)
        self.__load_texture(self.uncovered_tile)

        self.loaded = True


class Game:
    def __init__(self, sizeX: int, sizeY: int, bombsCount: int, textures: Textures):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeTile = None
        self.bombsCount = bombsCount
        self.textures = textures
        self.board = []

        self.__check()
        self.__create_board()

    def __check(self):
        """Internal method of class Game which checks internal values like sizeX, sizeY, bombCount"""
        if self.sizeX <= 0:
            raise SystemExit(f"Cannot have board with sizeX less or equal to 0! Inputed value: {self.sizeX}")
 
        if self.sizeY <= 0:
            raise SystemExit(f"Cannot have board with sizeY less or equal to 0! Inputed value: {self.sizeY}")

        if self.bombsCount >= self.sizeX * self.sizeY:
            raise SystemExit(f"Cannot have that much bombs! (Cant be equal to size of board or even bigger) Bombs count: {self.bombsCount}, size of borad: {self.sizeX * self.sizeY}")

    def __create_board(self):
        """Internal method of class Game which initialize board and all their Tiles"""
        self.board = [
            [self.Tile(x, y) for x in range(self.sizeX)] for y in range(self.sizeY)
        ]
        i = 0
        while i < self.bombsCount:
            x = random.randint(0, self.sizeX - 1)
            y = random.randint(0, self.sizeY - 1)
            tile = self.board[y][x]
            if not tile.hasBomb:
                tile.hasBomb = True
                i += 1

        for line in self.board:
            for tile in line:
                tile.find_neighbours(self)
                tile.count_bombs()

    class Tile:
        """Subclass of class 'Game', is used to represent one tile"""

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
            self.hasBomb = False
            self.bombNeighboursCount = None
            self.neighbours = []

        def find_neighbours(self, game):
            """Searches for 'neighbours' in Game.board and appends it to neighbours list"""
            dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            for dir in dirs:
                x = dir[0] + self.x
                y = dir[1] + self.y
                if x < game.sizeX and x >= 0 and y < game.sizeY and y >= 0:
                    self.neighbours.append(game.board[y][x])

        def count_bombs(self):
            """Counts how many 'neighbours' has a bomb"""
            self.bombNeighboursCount = 0
            for n in self.neighbours:
                if n.hasBomb:
                    self.bombNeighboursCount += 1

        def render(self, screen):
            pass


# TESTING

game = Game(5, 6, 7, Textures(os.path.join(os.path.dirname(__file__), "../textures")))
game.textures.load_textures()
# print(game.board)

for line in game.board:
    for item in line:
        print((item.x, item.y), end=" ")
    print()
for line in game.board:
    for item in line:
        print("X" if item.hasBomb else item.bombNeighboursCount, end=" ")
    print()
run = True
screen = pygame.display.set_mode((350, 250), pygame.RESIZABLE)
clock = pygame.time.Clock()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0, 255, 255))
    clock.tick(10)
    # print(screen.get_width(), screen.get_height())
    pygame.display.flip()
