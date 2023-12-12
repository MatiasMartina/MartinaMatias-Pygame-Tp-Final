from models.player.main_player import Jugador
import pygame as pg
from pygame.locals import *
from models.constantes import *
from world import *
from chronometer import Chronometer
from level import Level
from GUI_form_main import FormPrueba
from game import Game
pg.init()

screen_height = 800
screen_width = 800
initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)

chronometer = Chronometer(initial_time)

clock = pg.time.Clock()
delta_ms = clock.tick(FPS)
screen = pg.display.set_mode((screen_height, screen_width))
pg.display.set_caption("BA-ME-APRO")

img_background = pg.image.load('assets\img\\background\\background1.png')
scaled_background = pg.transform.scale(img_background, (1200, 800))

# INSTANCIAMOS
player = Jugador(50, 650, frame_rate=1, speed_walk=5, speed_run=10, gravity=5, delta_ms=1, speed_jump=50)
level_start = Level(actual_level)
enemies_list = pg.sprite.Group()
coins_list = []
trap_list = []
bullet_list = []
key_list = pg.sprite.Group()
game_over = 0

world = None
tile_list = pg.sprite.Group
running = True
paused = False
form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running)
game = Game(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background, paused)
while running:
    #load word()
    if not world:
        world = game.load_map()

        if DEBUG_LEVEL:
            print(f'{player.level}')

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
        game.run_game(event_list)
    pg.display.update()
    if paused:
        pg.time.delay(100)

pg.quit()