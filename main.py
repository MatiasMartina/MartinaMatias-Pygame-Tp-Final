from models.player.main_player import Jugador
from bee import Bee
from turtle import Turtle
import pygame as pg
from pygame.locals import * 
from models.constantes import * 
from world import *
from chronometer import Chronometer
from level import Level
from GUI_form_main import FormPrueba
pg.init()


screen_height = 800
screen_width = 800
initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)


chronometer = Chronometer(initial_time)




clock = pg.time.Clock()
screen = pg.display.set_mode((screen_height,screen_width))
pg.display.set_caption("BA-ME-APRO")

# CARGAMOS BACKGROUNG

img_background = pg.image.load('assets\img\\background\\background1.png')
scaled_background = pg.transform.scale(img_background, (1200, 800))

#INSTANCIAMOS 
player = Jugador(50 , 650, frame_rate = 1, speed_walk = 5, speed_run = 10, gravity = 5, delta_ms = 1, speed_jump= 50 )
level_start = Level(ACTUAL_LEVEL)
enemies_list = pg.sprite.Group()
coins_list = []
trap_list  = []
bullet_list = []
key_list = []
game_over = 0
form_prueba = FormPrueba(screen, 50, 50, 300, 300, "gray")  # Crea una instancia de tu formulario


world = None
tile_list = pg.sprite.Group
running = True
paused = False
while running:

    # if not world:
    #     world_data = level_start.load_level()
    #     world = World(world_data, enemies_list, coins_list, trap_list, key_list)
    #     if DEBUG_LEVEL:
    #         print(f"Nivel 1 {ACTUAL_LEVEL}")
    #     pass
    # if ACTUAL_LEVEL == 2:
    #     if DEBUG_LEVEL:
    #         print(f"Nivel 2 {ACTUAL_LEVEL}")
    #     world_data=[]
    #     world_data = level_start.load_level()
    #     if DEBUG_LEVEL:
    #         print(f"{world_data}")
    #     world = World(world_data, enemies_list, coins_list, trap_list, key_list)   
    #     player.restart()  # Restablecemos el jugador al cambiar de nivel
    #     enemies_list.empty()  # Limpiamos la lista de enemigos
    #     coins_list.clear()  # Limpiamos la lista de monedas
    #     trap_list.clear()  # Limpiamos la lista de trampas
    #     bullet_list.clear()  # Limpiamos la lista de balas
    #     key_list.clear()  # Limpiamos la lista de llaves

    #     if DEBUG_LEVEL:    
    #         print(f'{player.level}')
    # pressed_key = pg.key.get_pressed()
    # event_list = pg.event.get()
    # for event in event_list:
    #     if event.type == QUIT:
    #         running = False
    #     elif event.type == KEYDOWN:
    #         if event.key == K_p:  # Presiona la tecla "P" para pausar o reanudar el juego
    #             paused = not paused

    # BLITEAMOS
    # UPDATEAMOS
    form_prueba.update(pg.event.get())
    form_prueba.draw()
    if not paused:
         # SCREEN
        # screen.blit(scaled_background, scaled_background.get_rect())
    
        # delta_ms = clock.tick(FPS)
        # #WORLD
        # world.draw_grid(screen)
        # world.draw(screen)
        # #ENEMIES
        # for enemies in enemies_list:
        #     if game_over == 0:
        #         enemies.update(screen, world, player)
        #     enemies.draw(screen)
        # #TRAPS
        # for trap in trap_list:
        #     trap.update(screen, player)
        # #KEYS
        # for key in key_list:
        #     key.update(screen,player)
        # #BULLETS
        # for bullet in bullet_list:
        #     if game_over == 0:
        #         bullet.update(delta_ms, tile_list, enemies_list, player, world)
        #     bullet.draw(screen, bullet_list)
        # #     enemies.draw(screen, enemies_list)
        # # #PLAYER
        # chronometer.update()
        # chronometer.draw(screen)
        # game_over = player.update(pressed_key,delta_ms,screen, world, trap_list, bullet_list, game_over)
        # if DEBUG_GAME_OVER:
        #     print(f"game over: {game_over}")
    # if chronometer.get_time() <= 0 or player.current_lifes <= 0:
    #     print("game over")
    #     running = False
        pg.display.update() 
    if paused: 
        pg.time.delay(100)
pg.quit()
