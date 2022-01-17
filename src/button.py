from textures import *

textures = Textures(os.path.join(os.path.dirname(__file__), "../textures"))
textures.load_textures()

class Button:
    """Template button class"""
    def __init__(self, pos: V2i, size: V2i):
        self.pos = pos
        self.pos2 = pos + size
        self.size = size

    def posOnButton(self, pos: V2i):
        return pos.x >= self.pos.x and pos.x <= self.pos2.x and pos.y >= self.pos.y and pos.y <= self.pos2.y

    def userClick(self, pressed: int):
        if pressed == 1:
            self.__action()

    def __action(self):
        print("clicked on: ",self)



class SmileButton(Button):
    """Class that implements the 'Smile button'"""
    def __init__(self, pos: V2i, size: V2i):
        self.__state = 0
        super().__init__(pos, size)

        self.initialized = False

    def gameInit(self, game):
        """Initialize with game object reference"""
        self.__game = game
        self.initialized = True

    def __action(self):
        """Executes action when is cliked on button"""
        assert self.initialized, "Button not initialized with game"
        self.__game.reset()

    def updateState(self, state: int):
        """Updates internal state -> 4 states: 4 for faces"""
        self.__state = state
    
    def render(self, screen):
        """Renders button with correct texture"""
        image = pygame.transform.scale(textures.smiles[self.__state].image, (self.size.x, self.size.y))
        rect = image.get_rect()
        rect.x = self.pos.x
        rect.y = self.pos.y
        screen.blit(image, rect)

    def resize(self, w, h):
        """Resizes button"""
        size = min(w, h) // 5
        self.size = V2i(size, size)
        self.pos.x = w//2 - self.size.x // 2
        self.pos2 = self.pos + self.size

    def handle_click(self, pos: V2i, pressed: int, down: bool):
        """Handles the click -> calls action"""
        if pressed == 1:
            if down:
                if self.posOnButton(pos):
                    self.__action()