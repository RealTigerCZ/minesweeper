from dataclasses import dataclass, field
from typing import Tuple
import pygame, sys, os, random


# not used: sys, field!

@dataclass
class Colors:
    """Global color settings (RGB)"""
    
    background      = (200, 200, 200)
    grid_line_color = (50, 50, 50)
    bombsCount = [(0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), (128, 0, 0), (0, 128, 128), (128, 128, 128), (0, 0, 0)]
    #TODO colors


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
    def __init__(self, sizeOfBoard: Tuple[int, int], bombsCount: int, textures: Textures):
        self.textures = textures
        self.board = self.Board(sizeOfBoard, bombsCount, self)
        self.colors = Colors()


        self.__check()
        self.board.create_board()



    def __check(self):
        """Internal method of class Game which checks internal values like sizeX, sizeY, bombCount"""
        if self.board.sizeX <= 0:
            raise SystemExit(f"Cannot have board with sizeX less or equal to 0! Inputed value: {self.sizeX}")
 
        if self.board.sizeY <= 0:
            raise SystemExit(f"Cannot have board with sizeY less or equal to 0! Inputed value: {self.sizeY}")

        if self.board.bombsCount >= self.board.sizeX * self.board.sizeY:
            raise SystemExit(f"Cannot have that much bombs! (Cant be equal to size of board or even bigger) Bombs count: {self.bombsCount}, size of borad: {self.sizeX * self.sizeY}")


    def __set_for_render(self, screen):
        self.w = screen.get_width()
        self.h = screen.get_height()
        #TODO render

    def render(self, screen):
        pass
        #TODO render

    class Board:
        """Subclass of class 'Game', is used to represent board"""

        def __init__(self,  size, bombsCount: int, game):
            self.sizeX = size[0]
            self.sizeY = size[1]
            self.bombsCount = bombsCount
            self.game = game #refernce to game
            self.sizeTile = None
            self.padding = None
            self.board = []

             
        def create_board(self):
            """Internal method of class Game which initialize board and all their Tiles"""
            self.board = [[self.Tile(x, y, self.game) for x in range(self.sizeX)] for y in range(self.sizeY)]

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
                    tile.find_neighbours()
                    tile.count_bombs()    

        def __render_grid(self, screen, colors: Colors):
            for i in range(self.sizeX + 1):
                start_pos = (self.padding[0] + i * self.sizeTile, self.padding[1])
                end_pos =   (self.padding[0] + i * self.sizeTile, self.padding[1] + self.sizeTile * (self.sizeY))
                pygame.draw.line(screen, colors.grid_line_color, start_pos, end_pos, width = self.padding[0])

            for i in range(self.sizeY + 1):
                start_pos = (self.padding[0] , self.padding[1] + i * self.sizeTile)
                end_pos = (self.padding[0] + self.sizeTile * self.sizeX + 1, self.padding[1] + i * self.sizeTile)
                pygame.draw.line(screen, colors.grid_line_color, start_pos, end_pos, width = self.padding[0])

        def __render_board(self, screen):
            for line in self.board:
                for tile in line:
                    tile.render(screen, self.padding, self.sizeTile)

        def render(self, screen, colors: Colors):
            self.font = pygame.font.SysFont("Comic Sans MS", round(self.sizeTile * 0.8))
            self.__render_grid(screen, colors)
            self.__render_board(screen)
        
        def calc_padding(self, w, h) -> Tuple[int, int]:
            x = (w - screen.get_width()//128) // (self.sizeX)
            y = (h - self.padding[1] - 1) // (self.sizeY)
            self.sizeTile = min(x, y)
            self.padding = (self.sizeTile // 12, self.padding[1])
            if self.sizeTile < MIN_TILE_SIZE:
                self.sizeTile = MIN_TILE_SIZE
                self.padding = (2, self.padding[1])

            
            return (self.sizeX * self.sizeTile + self.padding[0]*3//2 + 2, self.sizeY * self.sizeTile + self.padding[0]//2 + self.padding[1] + 2)

        def __pos_in_on_board(self, pos):
            if pos[0] >= self.padding[0] and pos[0] < self.padding[0] + self.sizeTile * self.sizeX:
                if pos[1] >= self.padding[1] and pos[1] < self.padding[1] + self.sizeTile * self.sizeY:
                    return True
            return False

        def handle_click(self, pos: Tuple[int, int], pressed: Tuple[int, int, int]):
            if pressed[0] or pressed[2]:
                if self.__pos_in_on_board(pos):
                    x = (pos[0] - self.padding[0]) // self.sizeTile
                    y = (pos[1] - self.padding[1]) // self.sizeTile
                    self.board[y][x].user_click(pressed)

        class Tile:
            """Subclass of class 'Board', is used to represent one tile"""

            def __init__(self, x: int, y: int, game):
                self.x = x
                self.y = y
                self.game = game
                self.hasBomb = False
                self.bombNeighboursCount = None
                self.neighbours = []

                self.clicked = False
                self.flag = False
                self.touching = False
                self.uncovered = False

            def find_neighbours(self):
                """Searches for 'neighbours' in Game.board and appends it to neighbours list"""
                dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                for dir in dirs:
                    x = dir[0] + self.x
                    y = dir[1] + self.y
                    if x < self.game.board.sizeX and x >= 0 and y < self.game.board.sizeY and y >= 0:
                        self.neighbours.append(self.game.board.board[y][x])

            def count_bombs(self):
                """Counts how many 'neighbours' has a bomb"""
                self.bombNeighboursCount = 0
                for n in self.neighbours:
                    if n.hasBomb:
                        self.bombNeighboursCount += 1

            def render(self, screen, padding: int, size: int):
                x = padding[0] + self.x * size
                y = padding[1] + self.y * size

                if self.uncovered:
                    self.__render_uncovered(screen, x, y, size)
                elif self.flag:
                    self.__render_texture(screen, self.game.textures.flag_tile, x, y, size)
                elif self.touching:
                    self.__render_texture(screen, self.game.textures.touching_tile, x, y, size)            
                else:
                    self.__render_texture(screen, self.game.textures.uncovered_tile, x, y, size)
                    
            def __render_uncovered(self, screen, x, y, size):
                if self.hasBomb:
                    if self.clicked:
                        self.__render_texture(screen, self.game.textures.bomb_tile_red, x, y, size)
                    else:
                        self.__render_texture(screen, self.game.textures.bomb_tile, x, y, size)
                
                elif self.bombNeighboursCount > 0:
                    surf = self.game.board.font.render(str(self.bombNeighboursCount), True ,self.game.colors.bombsCount[self.bombNeighboursCount - 1])
                    rect = surf.get_rect()
                    rect.center = (x + size //2, y + size//2)
                    screen.blit(surf, rect)


            def user_click(self, pressed):
                if pressed[0]:
                    self.clicked = True
                    if self.hasBomb:
                        for line in self.game.board.board:
                            for tile in line:
                                tile.uncovered = True
                    self.click()
                
                if pressed[2]:
                    self.flag = not self.flag
                    
                    
            def click(self):
                self.uncovered = True
                if self.bombNeighboursCount == 0:
                    for n in self.neighbours:
                        if not n.uncovered:
                            n.click()
                 
            def __render_texture(self, screen, texture: Texture, x: int, y: int, size: int):
                image = pygame.transform.scale(texture.image, (size, size))
                rect = image.get_rect()
                rect.x = x
                rect.y = y
                screen.blit(image, rect)



# TESTING

game = Game((16, 8), 16*4, Textures(os.path.join(os.path.dirname(__file__), "../textures")))
game.textures.load_textures()
# print(game.board)

pygame.init()
DESKTOP_SCREEN = pygame.display.Info()

DESKTOP_W = DESKTOP_SCREEN.current_w
DESKTOP_H = DESKTOP_SCREEN.current_h

MIN_TILE_SIZE = 18


game.board.sizeTile = 25
game.board.padding = (3, 25)

MAX_SIZEX = DESKTOP_W // MIN_TILE_SIZE - 1
MAX_SIZEY = (DESKTOP_H - game.board.padding[1]) // MIN_TILE_SIZE - 3

print((MAX_SIZEX, MAX_SIZEY))

run = True
screen = pygame.display.set_mode((350, 250), pygame.RESIZABLE)
clock = pygame.time.Clock()


colors = Colors()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.VIDEORESIZE:
            w, h = game.board.calc_padding(event.w, event.h)
            screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.board.handle_click(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    screen.fill(game.colors.background)
    clock.tick(10)
    game.board.render(screen, colors)
    #print(screen.get_width(), screen.get_height())
    pygame.display.flip()


#TODO FONT
#TODO Texture test