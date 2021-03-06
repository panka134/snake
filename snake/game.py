import pygame as pg
from .classes import *
from .language import *

def display(board, snake, food):
    board.display()
    snake.display(board)
    for f in food:
        f.display(board)

    pg.display.update()

def game(personalize):
    lang = languages[personalize['lang']]

    screen_size = int(personalize['board_size'])
    food_quantity = int(personalize['food'])
    speed_increase = personalize['speed_increase']
    show_score = personalize['show_score']

    # INITIALIZE PYGAME AND CREATE THE WINDOW
    pg.init()
    screen = pg.display.set_mode((screen_size, screen_size))
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,1000' # sets window position – DOESN'T WORK

    # Title and icon
    pg.display.set_caption("Snake")
    icon = pg.image.load("snake/snake.png")
    pg.display.set_icon(icon)

    clock = pg.time.Clock()

    board = Board(surface = screen)
    center = board.sizeInFields/2
    snake = Snake(start_position = center, wall_die = personalize['wall_die'], speed = personalize['speed']*5)

    food = [Food(board_size = board.sizeInFields) for _ in range(food_quantity)]

    # display 3...2...1...
    font_big = pg.font.SysFont(None, 300)

    for i in range(3,0,-1):
        text = font_big.render(f"{i}", True, (0,0,0))
        display(board, snake, food)
        screen.blit(text, ((center*board.field_size)-50, (center*board.field_size)-80))
        pg.display.update()
        clock.tick(1)

    font = pg.font.SysFont(None, 30)

    # GAME LOOP
    running = True
    paused = False
    while running:
        clock.tick(snake.speed)
        # EVENTS HANDLING
        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    snake.changeDirection(event)

            if not(paused):
                snake.move(event, board.sizeInFields, food, speed_increase)

        except GameOver:
            print(lang['your_score'].format(snake.length))
            running = False
        except GamePause:
            paused = not(paused)

        display(board, snake, food)
        if show_score:
            text = font.render(lang['score'].format(snake.length), True, (0,0,0))
            screen.blit(text, (10, 20))
            pg.display.update()

        if paused:
            text = font.render(lang['pause'], True, (0,0,0))
            screen.blit(text, (screen_size-100, 20))
            pg.display.update()

    clock.tick(1)
    pg.quit()

    return snake.length

if __name__ == '__main__':
    main()
