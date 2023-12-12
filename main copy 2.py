from models.player.main_player import Jugador
import pygame as pg
from pygame.locals import *
from models.constantes import *
from world import *
from chronometer import Chronometer
from level import Level
from GUI_form_main import FormPrueba
from game import Game
from level1 import Level1
pg.init()

screen_height = 800
screen_width = 800

world = None


screen = pg.display.set_mode((screen_height, screen_width))
pg.display.set_caption("BA-ME-APRO")
level_start = Level(actual_level)
nivel_actual = Level1(screen)
running = True
form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running)
# INSTANCIAMOS

while running:
    #load word()
    if not world:
        world = nivel_actual.load_map()

        # if DEBUG_LEVEL:
        #     print(f'{player.level}')

    pressed_key = pg.key.get_pressed()
    event_list = pg.event.get()
    form_main.update(event_list)

    for event in event_list:
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused

    # if not paused:
    #     screen.blit(scaled_background, scaled_background.get_rect())
    #     delta_ms = clock.tick(FPS)
    #     world.draw_grid(screen)
    if not paused:
        nivel_actual.run_game(event_list)
    pg.display.update()
    if paused:
        pg.time.delay(100)

pg.quit()