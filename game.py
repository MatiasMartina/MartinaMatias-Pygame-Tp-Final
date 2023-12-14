import sqlite3

from world import World
import pygame as pg
from models.constantes import MAIN_MENU, DEBUG_LEVEL, DEBUG_WORLD, ALTO_VENTANA, ANCHO_VENTANA
from GUI.GUI_form import Form
from GUI.GUI_button_image import Button_Image
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
    def update_coins(self):
        for coins in self.coins_list:
                coins.update(self.slave, self.player)
    
    
    def update_bullets(self):
        for bullet in self.bullet_list:
            if self.game_over == 0:
                bullet.update(self.delta_ms, self.tile_list, self.enemies_list, self.player, self.world)
            bullet.draw(self.slave, self.bullet_list)
    def update_chronometer(self):
        self.chronometer.update()
        self.chronometer.draw(self.slave)
    def update_all_objetcs(self):
        self.update_coins()
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
        for evento in event_list:       
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_p:
                    pg.time.delay(100)
        
        if self.player.current_lifes <= 0:
            self.dead_player()
            self.save_score()  # Guardar puntaje en caso de perder
        else:
            if self.player.game_finished:
                self.player_win()  # Guardar puntaje en caso de ganar

            else:   
                print(f'{self.player.username}')
                self.update_world()
                self.update_all_objetcs()
                self.update_player()
                
                # print(f"self total_pints: {self.total_points}")

    def player_win(self):
        if self.player.game_finished:
            image = pg.image.load('assets\img\lvl\win.png')
            image = pg.transform.scale(image,(ALTO_VENTANA, ANCHO_VENTANA))
            self.slave.blit(image, (0,0))
            self.player.sound_win.set_volume(0.2)
            self.player.sound_win.play()


    def dead_player(self):
        
        print("Perdiste")
        image = pg.image.load('assets\img\lvl\gameover.jpg')
        image = pg.transform.scale(image, (ALTO_VENTANA, ANCHO_VENTANA))
        self.slave.blit(image, (0, 0))
        self.player.sound_game_over.set_volume(0.2)
        self.player.sound_game_over.play()
    def save_game1(self):
        score = self.player.score

        with open("score1.txt", "a") as archivo:
            archivo.write(f"{score}\n")

    def save_game2(self):
        score = self.player.score

        with open("score2.txt", "a") as archivo:
            archivo.write(f"{score}\n")

    def save_game3(self):
        score = self.player.score

        with open("score3.txt", "a") as archivo:
            archivo.write(f"{score}\n")

    def save_name(self, name):
        self.player.username = name
    def save_score(self):
        print("Guardar puntaje en SQLite")
        
        PATH = 'C:\\Users\\Mati\\'
        nombre_del_archivo = 'BAMEAPRO.db'

        try:
            with sqlite3.connect(f"{PATH}{nombre_del_archivo}") as conexion:
                cursor = conexion.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS score (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        score REAL
                    )
                ''')
                print("Tabla creada o ya existente.")

                if not self.player.is_saved:
                    # Si el jugador no ha sido guardado aún, guardamos su puntaje
                    try:
                        with conexion:
                            sentencia = "INSERT INTO score (nombre, score) VALUES (?, ?)"
                            cursor.execute(sentencia, (self.player.username, self.player.score))
                            print("Registro insertado correctamente.")
                            self.player.is_saved = True  # Marcar al jugador como guardado

                    except sqlite3.Error as e:
                        print("Error al insertar en la tabla score:", e)

        except sqlite3.Error as e:
            print("Error al conectar con la base de datos:", e)
        #     self.player.is_saved = True
        # # try:
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
    
   