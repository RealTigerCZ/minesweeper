from button import *
import random, colors




MIN_TILE_SIZE = 18


class Game:
    """The main Game class"""

    def __init__(self, sizeOfBoard: V2i, bombsCount: int, smileButton: SmileButton):
        self.board = self.Board(sizeOfBoard, bombsCount, self)
        self.__check()
        self.board.create_board()
        self.smileButton = smileButton

        self.smileButton.gameInit(self)

        self.won = False
        self.lost = False

        self.frame = 0        

    def __check(self):
        """Internal method of class Game which checks internal values like size.x, size.y, bombCount"""
        if self.board.size.x <= 0:
            raise SystemExit(f"Cannot have board with size.x less or equal to 0! Inputed value: {self.size.x}")
 
        if self.board.size.y <= 0:
            raise SystemExit(f"Cannot have board with size.y less or equal to 0! Inputed value: {self.size.y}")

        if self.board.bombsCount >= self.board.size.x * self.board.size.y:
            raise SystemExit(f"Cannot have that much bombs! (Cant be equal to size of board or even bigger) Bombs count: {self.bombsCount}, size of borad: {self.size.x * self.size.y}")

    def lose(self):
        self.smileButton.updateState(3)
        self.lost = True
        self.frame = 0

    def win(self):
        self.smileButton.updateState(2)
        self.won = True
        self.frame = 0

    def __set_for_render(self, screen):
        self.w = screen.get_width()
        self.h = screen.get_height()
        #TODO render

    def reset(self):
        size = V2i(self.board.size.x, self.board.size.y)
        bombs = self.board.bombsCount
        padding = self.board.padding
        size_tile = self.board.sizeTile

        self.board = self.Board(size, bombs, self)
        self.board.create_board()
        self.board.padding = padding
        self.board.sizeTile = size_tile

        self.smileButton.updateState(0)
        self.won = False
        self.lost = False
        self.frame = 0

    def render(self, screen):
        self.smileButton.render(screen)
        self.board.render(screen)
        #TODO render

    def resize(self, w, h) -> Tuple[int, int]:
        """Handles window resizing"""
        w, h = self.board.calc_padding(w, h)
        self.smileButton.resize(w, h)
        return w, h

    def handle_click(self, pos: V2i, button: int, down: bool):
        """Handles click from user -> redirect it to smile button or game.board"""
        self.smileButton.handle_click(pos, button, down)
        if self.won + self.lost == 0:
            if button in [1, 3]:
                self.smileButton.updateState(0 + down)
                self.board.handle_click(pos, button, down)


    class Board:
        """Subclass of class 'Game', is used to represent board. It can:
        - renders itself, calculates its position
        - handles click from user
        - stores internal states of board
        """

        def __init__(self,  size: V2i, bombsCount: int, game):
            self.size = size
            self.bombsCount = bombsCount
            self.game = game #refernce to game class
            self.sizeTile = None
            self.padding = None
            self.board = []

            self.__lastHandledClicks = None

             
        def create_board(self):
            """Internal method of class Game which initialize board and all their Tiles"""
            self.board = [[self.Tile(x, y, self.game) for x in range(self.size.x)] for y in range(self.size.y)]

            i = 0
            while i < self.bombsCount:
                x = random.randint(0, self.size.x - 1)
                y = random.randint(0, self.size.y - 1)
                tile = self.board[y][x]          
                if not tile.hasBomb:
                    tile.hasBomb = True
                    i += 1

            for line in self.board:
                for tile in line:
                    tile.find_neighbours()
                    tile.count_bombs()    

        def __render_grid(self, screen):
            """Renders the background grid"""
            for i in range(self.size.x + 1):
                start_pos = (self.padding.x + i * self.sizeTile, self.padding.y)
                end_pos =   (self.padding.x + i * self.sizeTile, self.padding.y + self.sizeTile * (self.size.y))
                pygame.draw.line(screen, colors.grid_line_color, start_pos, end_pos, width = self.padding.x)

            for i in range(self.size.y + 1):
                start_pos = (self.padding.x , self.padding.y + i * self.sizeTile)
                end_pos = (self.padding.x + self.sizeTile * self.size.x + 1, self.padding.y + i * self.sizeTile)
                pygame.draw.line(screen, colors.grid_line_color, start_pos, end_pos, width = self.padding.x)

        def __render_board(self, screen):
            """Render the tiles of the board"""
            for line in self.board:
                for tile in line:
                    tile.render(screen, self.padding, self.sizeTile)

        def render(self, screen):
            """Creates font for game with correct size and calls render functions"""
            self.font = pygame.font.SysFont("Comic Sans MS", round(self.sizeTile * 0.8))
            self.__render_grid(screen)
            self.__render_board(screen)
        
        def calc_padding(self, w, h) -> Tuple[int, int]:
            """Calculates padding and returnes is to correct the window size"""
            x = (w - w//128) // (self.size.x)
            y = (h - self.padding.y - 1) // (self.size.y)
            self.sizeTile = min(x, y)
            self.padding.y = 6 + min(w, h) // 5
            self.padding.x = self.sizeTile // 12
            if self.sizeTile < MIN_TILE_SIZE:
                self.sizeTile = MIN_TILE_SIZE
                self.padding.x = 2

            
            return (self.size.x * self.sizeTile + self.padding.x*3//2 + 2, self.size.y * self.sizeTile + self.padding.x//2 + self.padding.y + 2)

        def __pos_in_on_board(self, pos: V2i):
            """Returns true if position is on some tile of the board"""
            if pos.x >= self.padding.x and pos.x < self.padding.x + self.sizeTile * self.size.x:
                if pos.y >= self.padding.y and pos.y < self.padding.y + self.sizeTile * self.size.y:
                    return True
            return False

        def handle_click(self, pos: V2i, button: int, down: bool):
            """Haddles the click from user and passes it ot correct tile"""
            if button in [1, 3]: #ignores button 2 -> midlle click
                if self.__pos_in_on_board(pos):
                    x = (pos.x - self.padding.x) // self.sizeTile
                    y = (pos.y - self.padding.y) // self.sizeTile
                    
                    if self.__allow_click(x, y, down):
                        self.board[y][x].user_click(button, down)
            self.check_win()

        def __allow_click(self, x, y, down):
            """Hadles the click: cancels it if it is not on the same tile"""
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

        def check_win(self):
            if self.game.lost:
                return False
            for line in self.board:
                for tile in line:
                    if not tile.uncovered:
                        if not tile.hasBomb:
                            return 
            for line in self.board:
                for tile in line:
                    if tile.hasBomb:
                        tile.flag = True
            self.game.win()



        class Tile:
            """Subclass of class 'Board', is used to represent one tile. It can:
            - render itself with correct texture
            - handle the click from board
            - find and work with its neighbours
            - store internal states
            """

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
                    if x < self.game.board.size.x and x >= 0 and y < self.game.board.size.y and y >= 0:
                        self.neighbours.append(self.game.board.board[y][x])

            def count_bombs(self):
                """Counts how many 'neighbours' has a bomb"""
                self.bombNeighboursCount = 0
                for n in self.neighbours:
                    if n.hasBomb:
                        self.bombNeighboursCount += 1

            def render(self, screen, padding: int, size: int):
                """Renders itself to correct position with correct texture"""
                x = padding.x + self.x * size
                y = padding.y + self.y * size

                if self.uncovered:
                    self.__render_uncovered(screen, x, y, size)
                elif self.flag:
                    self.__render_texture(screen, textures.flag_tile, x, y, size)
                elif self.pressed:
                    self.__render_texture(screen, textures.pressed_tile, x, y, size)            
                else:
                    self.__render_texture(screen, textures.covered_tile, x, y, size)
                    
            def __render_uncovered(self, screen, x, y, size):
                """Renders number of neighbours with bomb or the bomb itself"""
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
                """Handles user click send by board"""
                if button == 1:
                    if self.flag:
                        return
                    if down:
                        self.pressed = True
                        self.press_num()
                    else:
                        self.unpress()
                        self.clicked = True
                        if self.hasBomb:
                            self.game.lose()
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
                """Handles click from other Tile or itself"""
                self.uncover_neighbours()
                with_flag = self.__countNeighboursWithFlag()
                if with_flag == self.bombNeighboursCount:
                    for n in self.neighbours:
                        if not n.flag:
                            if n.hasBomb:
                                n.user_click(1, False)
                                break
                            n.uncover_neighbours()



            def uncover_neighbours(self):
                """Uncoveres its neighbours if there are none with a bomb"""
                self.uncovered = True
                if self.bombNeighboursCount == 0:
                    for n in self.neighbours:
                        if not n.uncovered:
                            n.click()
                self.unpress()
            
            def press_num(self):
                """Presses neighbours -> highlighting"""
                if self.uncovered:
                    for n in self.neighbours:
                        if not n.uncovered:
                            n.pressed = True

            def unpress(self):
                """Unpresses the neighbours when mouse is not press anymore"""
                self.pressed = False
                for n in self.neighbours:
                    n.pressed = False

            def __countNeighboursWithFlag(self):
                """Counts neighours with flag"""
                suma = 0
                for n in self.neighbours:
                    suma += n.flag
                return suma

            def __flag_neighbours(self):
                """Flags neighbours if there are exacly same uncovered or flag tiles as there are neighbours with a bomb"""
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
                """Transforms and renders given texture to given position"""
                image = pygame.transform.scale(texture.image, (size, size))
                rect = image.get_rect()
                rect.x = x
                rect.y = y
                screen.blit(image, rect)
