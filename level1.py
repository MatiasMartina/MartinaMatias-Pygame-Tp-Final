import pygame as pg
from game import Game
from level import Level
from models.player.main_player import Jugador
from models.constantes import  actual_level, FPS
from chronometer import Chronometer
from GUI_form_main import FormPrueba
class Level1(Game):
    def __init__(self, screen:pg.Surface) -> None:
        width = screen.get_width()
        height = screen.get_height()

        initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)

        # chronometer = Chronometer(initial_time) LO SACAMOS DE OTRO LADO

        # clock = pg.time.Clock() LO SACAMOS DE OTRO LADO
        # screen = pg.display.set_mode((screen_height, screen_width)) LO SACAMOS DE OTRO LADO
        #delta_ms = clock.tick(FPS) LO SACAMOS DE OTRO LADO
        pg.display.set_caption("BA-ME-APRO")
        #FONDO
        img_background = pg.image.load('assets\img\\background\\background1.png')
        scaled_background = pg.transform.scale(img_background, (width, height))

        # INSTANCIAMOS
        initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)
        chronometer = Chronometer(initial_time)
        clock = pg.time.Clock()
        player = Jugador(50, 650, frame_rate=1, speed_walk=5, speed_run=10, gravity=5, delta_ms=1, speed_jump=50)
        running = True
        form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running)
        level_start = Level(actual_level)
        enemies_list = pg.sprite.Group()
        coins_list = []
        trap_list = []
        bullet_list = []
        key_list = pg.sprite.Group()
        game_over = 0
        delta_ms = clock.tick(FPS)
        world = None
        tile_list = pg.sprite.Group
        running = True
        paused = False
        # form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running) 
        # game = Game(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background, paused)    
        
        super().__init__(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player,delta_ms,bullet_list,tile_list, chronometer, form_main, scaled_background, paused)