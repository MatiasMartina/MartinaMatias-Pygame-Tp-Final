from level3 import Level3
import pygame as pg
from game import Game
from level import Level
from models.player.main_player import Jugador
from models.constantes import  actual_level, FPS
from chronometer import Chronometer
from GUI_form_main import FormPrueba
from world import World
class Level2(Game):
    def __init__(self, screen:pg.Surface) -> None:

        width = screen.get_width()
        height = screen.get_height()
        
        img_background = pg.image.load('assets\img\\background\\background1.png')
        scaled_background = pg.transform.scale(img_background, (1200, 800))

        self.screen = screen
        self.level_3 = None
        self.nivel_actual = 2
        self.is_active = True
        initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)

        chronometer = Chronometer(initial_time)



        # INSTANCIAMOS
        player = Jugador(50, 650, frame_rate=1, speed_walk=5, speed_run=10, gravity=5, delta_ms=1, speed_jump=50)
        level_start = Level(2)
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
        # paused = False
        form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running)
        # world_data = level_start.load_level()
        # world = World(world_data, enemies_list, coins_list, trap_list, key_list)
        delta_ms = clock.tick(FPS)
        # game = Game(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background)
        
        # form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running) 
        # game = Game(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background, paused)    
        
        super().__init__(level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player,delta_ms,bullet_list,tile_list, chronometer, form_main, scaled_background)

    def cargar_nivel_tres(self, event_list):
            print(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasdadasdasdasdasdadasd {self.player.score}")
            
            print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasfasdfsdfsfasf {self.player.score}')
            # self.total_points +=self.player.score
            self.level_3 = Level3(self.screen)
            self.nivel_actual = 3
            self.level_3.update(event_list)
           
            
    def update(self,event_list):
        if self.is_active:
            super().update(event_list)
            if self.player.capture_key:
                self.cargar_nivel_tres(event_list)
                self.total_points += self.player.score
                print(f"cargar nivel tres {self.player.score}")
                self.is_active = False
        else:
            self.level_3.update(event_list)  
 