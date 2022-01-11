from textures import *
import random, colors

textures = Textures(os.path.join(os.path.dirname(__file__), "../textures"))
textures.load_textures()

MIN_TILE_SIZE = 18


class Game:
    def __init__(self, sizeOfBoard: Tuple[int, int], bombsCount: int):
        self.board = self.Board(sizeOfBoard, bombsCount, self)
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

            self.__lastHandledClicks = None

             
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

        def __render_grid(self, screen):
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

        def render(self, screen):
            self.font = pygame.font.SysFont("Comic Sans MS", round(self.sizeTile * 0.8))
            self.__render_grid(screen)
            self.__render_board(screen)
        
        def calc_padding(self, w, h) -> Tuple[int, int]:
            x = (w - w//128) // (self.sizeX)
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

        def handle_click(self, pos: Tuple[int, int], button: int, down: bool):
            if button in [1, 3]:
                if self.__pos_in_on_board(pos):
                    x = (pos[0] - self.padding[0]) // self.sizeTile
                    y = (pos[1] - self.padding[1]) // self.sizeTile
                    
                    if self.__allow_click(x, y, down):
                        self.board[y][x].user_click(button, down)


        def __allow_click(self, x, y, down):
            if down:
                self.__lastHandledClicks = (x, y)
                return True
            else:
                if self.__lastHandledClicks:
                    lx, ly = self.__lastHandledClicks
                    self.__lastHandledClicks = None
                    if x == lx and y == ly:
                        return True
                    else:
                        self.board[ly][lx].unpress()


            return False

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
                self.pressed = False
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
                    self.__render_texture(screen, textures.flag_tile, x, y, size)
                elif self.pressed:
                    self.__render_texture(screen, textures.pressed_tile, x, y, size)            
                else:
                    self.__render_texture(screen, textures.uncovered_tile, x, y, size)
                    
            def __render_uncovered(self, screen, x, y, size):
                if self.hasBomb:
                    if self.clicked:
                        self.__render_texture(screen, textures.bomb_tile_red, x, y, size)
                    else:
                        self.__render_texture(screen, textures.bomb_tile, x, y, size)
                
                elif self.bombNeighboursCount > 0:
                    surf = self.game.board.font.render(str(self.bombNeighboursCount), True, colors.bombsCount[self.bombNeighboursCount - 1])
                    rect = surf.get_rect()
                    rect.center = (x + size //2, y + size//2)
                    screen.blit(surf, rect)


            def user_click(self, button: int, down: bool):
                if button == 1:
                    if down:
                        self.pressed = True
                        self.press_num()
                    else:
                        self.unpress()
                        self.clicked = True
                        if self.hasBomb:
                            for line in self.game.board.board:
                                for tile in line:
                                    tile.uncovered = True
                        self.click()
                
                elif button == 3:
                    if not down:
                        if self.uncovered:
                            self.__flag_neighbours()
     
                        else:
                            self.flag = not self.flag
                    
                    
            def click(self):
                self.uncover_neighbours()
                with_flag = self.__countNeighboursWithFlag()
                if with_flag == self.bombNeighboursCount:
                    for n in self.neighbours:
                        if not n.flag:
                            n.uncover_neighbours()
    
            
            def uncover_neighbours(self):
                self.uncovered = True
                if self.bombNeighboursCount == 0:
                    for n in self.neighbours:
                        if not n.uncovered:
                            n.click()
                self.unpress()
            
            def press_num(self):
                if self.uncovered:
                    for n in self.neighbours:
                        if not n.uncovered:
                            n.pressed = True

            def unpress(self):
                self.pressed = False
                for n in self.neighbours:
                    n.pressed = False

            def __countNeighboursWithFlag(self):
                suma = 0
                for n in self.neighbours:
                    suma += n.flag
                return suma

            def __flag_neighbours(self):
                covered_without_flag = 0
                for n in self.neighbours:
                    covered_without_flag += not (n.uncovered or n.flag)

                if covered_without_flag > 0:
                    with_flag = self.__countNeighboursWithFlag()
                    if covered_without_flag + with_flag == self.bombNeighboursCount:
                        for n in self.neighbours:
                            if not n.uncovered:
                                n.flag = True   
                 
            def __render_texture(self, screen, texture: Texture, x: int, y: int, size: int):
                image = pygame.transform.scale(texture.image, (size, size))
                rect = image.get_rect()
                rect.x = x
                rect.y = y
                screen.blit(image, rect)
