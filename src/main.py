from dataclasses import dataclass, field
from typing import Tuple
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
class Texture:
    def __init__(self, name: str, ext: str, size: Tuple[int,int], path: os.path):
        self.name = name
        self.name_with_ext = name + "." + ext
        self.path = os.path.join(path, self.name_with_ext)
        self.size = size
        self.image = None


@dataclass
class Textures:
    def __init__(self, path: str):
        self.path = path

        #textures
        self.bomb_tile      = Texture("bomb_tile",      "png", (15, 15),    path) 
        self.bomb_tile_red  = Texture("bomb_tile_red",  "png", (15, 15),    path)
        self.flag_tile      = Texture("flag_tile",      "png", (512, 512),  path)
        self.uncovered_tile = Texture("uncovered_tile", "png", (512, 512),  path)

        #states
        self.loaded = False


    def __load_texture(self, texture: Texture):
        try:
            texture.image = pygame.image.load(texture.path)
        
        except pygame.error as message:
            print("Cannot load texture:", texture.name_with_ext)
            raise SystemExit(message)
        
        except FileNotFoundError as message:
            print("Cannot find texture:", texture.name_with_ext)
            raise SystemExit(message, f"Path: {texture.path}")
    
        if texture.image.get_size() != texture.size:
            raise SystemExit(f"Texture {texture.name_with_ext} cannot be loaded, because it has unexpexted size!\nExpected: {texture.size}, actual: {texture.image.get_size()}\n")


    def load_textures(self):
        self.__load_texture(self.bomb_tile)
        self.__load_texture(self.bomb_tile_red)
        self.__load_texture(self.flag_tile)
        self.__load_texture(self.uncovered_tile)

        self.loaded = True
    
        
        
     


@dataclass
class Glo:
    sizeX: int
    sizeY: int
    sizeTile: int
    bombsCount: int
    textures: Textures
    board: list[list[Tile]] = field(default_factory=list)


glo = Glo(1, 1, 1, 1, Textures(os.path.join(os.path.dirname(__file__), "../textures")))
glo.textures.load_textures()

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
