from game import *


# TESTING

game = Game((16, 8), 1)
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


# TRACKING FPS
# fps_font = pygame.font.SysFont("Comic Sans MS", 50)
# import time
# start_time = time.time() - 1

frame = 0
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

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                game.reset()
                frame = 0
    if game.win:
        screen.fill(colors.win_colors[frame//60 % 2])
    elif game.lose:
        screen.fill(colors.lose_colors[frame//60 % 2])
    else:
        screen.fill(colors.background)


    # TRACKING FPS
    # if frame % 30 == 0:
    #     fps = fps_font.render(str(round(30/(time.time() - start_time), 1)), True, (0,0,255))
    #     start_time = time.time()
    #     fpsRect = fps.get_rect()
    # screen.blit(fps, fpsRect)
 
    clock.tick(60)
    game.board.render(screen)
    frame += 1
    pygame.display.flip()
