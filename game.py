from world import World
import pygame as pg
from models.constantes import MAIN_MENU, DEBUG_LEVEL

class Game():
    def __init__(self, level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background, paused) -> None:
        self.level_start = level_start  
        self.enemies_list = enemies_list
        self.coins_list = coins_list
        self.trap_list = trap_list
        self.key_list = key_list
        self.game_over = game_over
        self.slave = screen
        self.player = player
        self.world = self.load_map()
        self.delta_ms = delta_ms
        self.bullet_list = bullet_list
        self.tile_list = tile_list
        self.chronometer = chronometer
        self.form_main = form_main
        self.scaled_background = scaled_background
        self.paused = paused
    def load_map(self): #(se guarda mapa acá)
            world_data = self.level_start.load_level()
            world = World(world_data, self.enemies_list, self.coins_list, self.trap_list, self.key_list)
            if DEBUG_LEVEL:
                print(f'{self.player.level}')
            return world

    def update_enemies(self):
        
        for enemies in self.enemies_list:
                if self.game_over == 0:
                    enemies.update(self.slave, self.world, self.player)
                enemies.draw(self.slave)

    def update_traps(self):
        for trap in self.trap_list:
                trap.update(self.slave, self.player)

    def udpate_keys(self):
         for key in self.key_list:
                key.update(self.slave, self.player)
    def update_bullets(self):
        for bullet in self.bullet_list:
            if self.game_over == 0:
                bullet.update(self.delta_ms, self.tile_list, self.enemies_list, self.player, self.world)
            bullet.draw(self.slave, self.bullet_list)

    def world_draw_grid(self):
        self.world.draw_grid(self.slave) 
    
    def world_draw(self):
          self.world.draw(self.slave)
    def world_update(self):
        self.screen_blit()        
        self.world_draw_grid()
        self.world_draw()


    def chronometer_update(self):
        self.chronometer.update()
        self.chronometer.draw(self.slave)

    def player_update(self, event_list):
        pressed_key = pg.key.get_pressed()
        # event_list = pg.event.get()
        self.game_over = self.player.update(pressed_key, self.delta_ms, self.slave, self.world, self.trap_list, self.bullet_list, self.game_over)
        pass
    
    # def form_main_update(self):
    #     event_list = pg.event.get()
    #     self.form_main.update(event_list)
    def screen_blit(self):
        self.slave.blit(self.scaled_background, self.scaled_background.get_rect())

    def run_game(self,event_list):
        if not self.paused:
            self.world_update()
            if MAIN_MENU:
                event_list = pg.event.get()
                self.form_main.update(event_list)
            
            self.player_update(event_list)
            self.update_objects()
    
    def update_objects(self):
        self.update_enemies()
        self.update_traps()
        self.udpate_keys()
        self.update_bullets() 
        self.chronometer_update()

    def update_all_objetcs(self, event_list, paused):
        if not paused:
            self.run_game(event_list)
            pg.display.update()
        if paused:
            pg.time.delay(100)    