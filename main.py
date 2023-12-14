import os
from models.player.main_player import Jugador
import pygame as pg
from pygame.locals import *
from models.constantes import *
from world import *
from chronometer import Chronometer
from level import Level
from GUI.GUI_form_main import FormPrueba
from GUI.GUI_form_prueba import FormPruebas
from game import Game
from level1 import Level1
pg.init()

screen_height = 800
screen_width = 800
screen = pg.display.set_mode((screen_height, screen_width))
pg.display.set_caption("BA-ME-APRO")
clock = pg.time.Clock()
nivel_actual = Level1(screen)
paused = False
running = True
form_main = FormPruebas(screen, 0, 0, 900, 1200, "Black", "yellow", 5, True)


while running:

    clock.tick(FPS)
    event_list = pg.event.get()
    screen.fill("Black")
  
    for event in event_list:
        
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
    
    form_main.update(event_list)

    pg.display.update()
    pg.display.flip()
pg.quit()