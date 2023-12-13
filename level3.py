import pygame as pg
from game import Game
from level import Level
from models.player.main_player import Jugador
from models.constantes import  actual_level, FPS
from chronometer import Chronometer
from GUI_form_main import FormPrueba
from world import World
class Level3(Game):
    def __init__(self, screen:pg.Surface) -> None:

        width = screen.get_width()
        height = screen.get_height()
        
        img_background = pg.image.load('assets\img\\background\\background1.png')
        scaled_background = pg.transform.scale(img_background, (1200, 800))



        initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)

        chronometer = Chronometer(initial_time)



        # INSTANCIAMOS
        player = Jugador(50, 650, frame_rate=1, speed_walk=5, speed_run=10, gravity=5, delta_ms=1, speed_jump=50)
        level_start = Level(1)
        enemies_list = pg.sprite.Group()
        coins_list = []
        trap_list = []
        bullet_list = []
        key_list = pg.sprite.Group()
        game_over = 0
        clock = pg.time.Clock()
        # world = None
        tile_list = pg.sprite.Group
        running = True
        paused = False
        form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running)
        world_data = level_start.load_level()
        world = World(world_data, enemies_list, coins_list, trap_list, key_list)
        delta_ms = clock.tick(FPS)
        game = Game(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background)
        
        # form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running) 
        # game = Game(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background, paused)    
        
        super().__init__(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player,delta_ms,bullet_list,tile_list, chronometer, form_main, scaled_background)