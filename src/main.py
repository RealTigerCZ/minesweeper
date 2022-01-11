from game import *


# TESTING
game = Game((16, 8), 16)
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

DEFAULT_WIDTH  = game.board.sizeX * 30 + 5
DEFAULT_HEIGHT = game.board.sizeY * 30 + game.board.padding[1]

run = True
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
w, h = game.board.calc_padding(DEFAULT_WIDTH, DEFAULT_HEIGHT)
screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
clock = pygame.time.Clock()

pygame.display.set_caption("Very bad minesweeper")

while run:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.VIDEORESIZE:
            w, h = game.board.calc_padding(event.w, event.h)
            screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONUP:
            game.board.handle_click(event.pos, event.button, False)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.board.handle_click(event.pos, event.button, True)

    screen.fill(colors.background)
    clock.tick(60)
    game.board.render(screen)
    #print(screen.get_width(), screen.get_height())
    pygame.display.flip()
