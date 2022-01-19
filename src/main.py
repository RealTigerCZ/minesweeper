from game import *

# TESTING

Y_PADDING = 3
X_PADDING = 3

BOARD_SIZE = V2i(16, 8)

pygame.init()
DESKTOP_SCREEN = pygame.display.Info()

DESKTOP = Window(DESKTOP_SCREEN.current_w, DESKTOP_SCREEN.current_h)

SMILE_BUTTON_SIZE = 26

game = Game(BOARD_SIZE, 16, SmileButton(V2i(50, 3),
            V2i(SMILE_BUTTON_SIZE, SMILE_BUTTON_SIZE)))
# print(game.board)



MIN_TILE_SIZE = 18


game.board.sizeTile = 25
game.board.padding = V2i(X_PADDING, game.smileButton.size.y + Y_PADDING * 2)



MAX_SIZE = V2i()
MAX_SIZE.x = DESKTOP.w // MIN_TILE_SIZE - 1
MAX_SIZE.y = (DESKTOP.h - game.board.padding.y) // MIN_TILE_SIZE - 3

print((MAX_SIZE.x, MAX_SIZE.y))

DEFAULT_WIDTH  = game.board.size.x * 30 + 5
DEFAULT_HEIGHT = game.board.size.y * 30 + game.board.padding.y


sz = min(DEFAULT_WIDTH, DEFAULT_HEIGHT) // 8

game.smileButton.size = V2i(sz, sz)
game.smileButton.pos.x = DEFAULT_WIDTH // 2 - game.smileButton.size.x // 2
game.smileButton.pos.y = Y_PADDING

run = True
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
w, h = game.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
clock = pygame.time.Clock()

pygame.display.set_caption("Very bad minesweeper")


# TRACKING FPS
# fps_font = pygame.font.SysFont("Comic Sans MS", 50)
# import time
# start_time = time.time() - 1

segm = SevenSegmentDisplay(V2i(10, 10), 100, 200, 10, 3)

time_display = SevenSegmentTime(V2i(320, 10), 100, 200, 10)

while run:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.VIDEORESIZE:
            w, h = game.resize(event.w, event.h)
            screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONUP:
            game.handle_click(V2i(event.pos[0], event.pos[1]), event.button, False)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            segm.updateStateBy(1)
            game.handle_click(V2i(event.pos[0], event.pos[1]) , event.button, True)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                game.reset()
                frame = 0
    if game.won:
        screen.fill(colors.win_colors[game.frame//60 % 2])
    elif game.lost:
        screen.fill(colors.lose_colors[game.frame//60 % 2])
    else:
        screen.fill(colors.background)


    # TRACKING FPS
    # if frame % 30 == 0:
    #     fps = fps_font.render(str(round(30/(time.time() - start_time), 1)), True, (0,0,255))
    #     start_time = time.time()
    #     fpsRect = fps.get_rect()
    # screen.blit(fps, fpsRect)
 
    

    clock.tick(60)
    segm.render(screen)
    time_display.render(screen)
    #game.render(screen)
    game.frame += 1
    pygame.display.flip()
