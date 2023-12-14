import sqlite3

from world import World
import pygame as pg
from models.constantes import MAIN_MENU, DEBUG_LEVEL, DEBUG_WORLD, ALTO_VENTANA, ANCHO_VENTANA
from GUI_form import Form
from GUI_button_image import Button_Image
class Game():
    def __init__(self, level_start, enemies_list, coins_list, trap_list, key_list, game_over, screen, player, delta_ms, bullet_list, tile_list, chronometer, form_main, scaled_background) -> None:
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
        self.total_points = 0
    def read_user_imput(self, pressed_key):
        self.game_over = self.player.update(pressed_key, self.delta_ms, self.slave, self.world, self.trap_list, self.bullet_list,self.game_over)
    def load_map(self):
        world_data = self.level_start.load_level()
        world = World(world_data, self.enemies_list, self.coins_list, self.trap_list, self.key_list)
        return world
    def update_enemies(self):
        for enemies in self.enemies_list:
                if self.game_over == 0:
                    enemies.update(self.slave, self.world, self.player)
                enemies.draw(self.slave)
    def update_traps(self):
        for trap in self.trap_list:
            trap.update(self.slave, self.player)
    def update_keys(self):
         for key in self.key_list:
                key.update(self.slave, self.player)
    def update_bullets(self):
        for bullet in self.bullet_list:
            if self.game_over == 0:
                bullet.update(self.delta_ms, self.tile_list, self.enemies_list, self.player, self.world)
            bullet.draw(self.slave, self.bullet_list)
    def update_chronometer(self):
        self.chronometer.update()
        self.chronometer.draw(self.slave)
    def update_all_objetcs(self):
        self.update_enemies()
        self.update_traps()
        self.update_keys()
        self.update_bullets()
        self.update_chronometer()

    def update_player(self):
        key_get_pressed = pg.key.get_pressed()
        self.game_over = self.player.update(key_get_pressed, self.delta_ms, self.slave, self.world, self.trap_list, self.bullet_list, self.game_over)

    def update_world(self):
        self.slave.blit(self.scaled_background, self.scaled_background.get_rect())
        if DEBUG_WORLD:
            self.world.draw_grid(self.slave)

        
        self.world.draw(self.slave)
    
    # def win_check(self):
    #     if self.player.capture_key:
    #         self.total_points += self.player.score  # Acumular puntos del jugador
    #         return True
    #     return False
    def update(self,event_list):#, paused):
        # if not paused:
        


        for evento in event_list:       
            if evento == pg.KEYDOWN:
                if evento.key == pg.K_P:
                    pg.time.delay(100)
        
        if self.player.current_lifes <= 0:
           self.dead_player()
           self.save_score()
        else:
            if self.player.game_finished:
 
                self.save_score()

            else:   
                print(f'{self.player.username}')
                self.update_world()
                self.update_all_objetcs()
                self.update_player()
                
                # print(f"self total_pints: {self.total_points}")
    def dead_player(self):
        print("perdiste")
        image = pg.image.load('assets\img\lvl\gameover.jpg')
        image = pg.transform.scale(image,(ALTO_VENTANA,ANCHO_VENTANA))  # Ajusta las dimensiones según sea necesario
        self.slave.blit(image, (0, 0))
    
    def save_score(self):
        print("Guardar listado de promedio de rebotes por partido en SQLite ")
        
        PATH = 'C:\\Users\\Mati\\'
        # PATH = 'C:\\Users\\Mati\\Desktop\\PrimerParcial'
        nombre_del_archivo = 'BAMEAPRO.db'


        with sqlite3.connect(f"{PATH}{nombre_del_archivo}") as conexion:
            try:
                sentencia = """
                    create table score
                    (
                            id integer primary key autoincrement,
                            nombre text,
                            score real
                    )
                    """
                conexion.execute(sentencia)
                print("Se creo la tabla.")


            except sqlite3.OperationalError:
                 print("La tabla score ya existe.")
            except sqlite3.Error as e:
                 print("error al crear la tabla score", e)
        nombre =""
        
        try:
            with conexion:
                sentencia = "INSERT INTO score (nombre, score) VALUES (?, ?)"
                conexion.execute(sentencia, (self.player.username, self.player.score))
                print("Registro insertado correctamente.")
        except sqlite3.Error as e:
            print("Error al insertar en la tabla score:", e)
        
        # try:
        #     with sqlite3.connect("BAMEAPRO.db") as connection:
        #         cursor = connection.cursor()
        #         cursor.execute('''
        #             INSERT INTO Ranking (username, score)
        #             VALUES (?, ?)
        #         ''', (self.player.username, self.total_points))
        #         connection.commit()
        #         print("Puntuación guardada en la base de datos")
        # except Exception as e:
        #     print(f"Error al guardar la puntuación en la base de datos: {e}")
    
   