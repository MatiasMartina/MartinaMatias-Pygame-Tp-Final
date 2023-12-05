import pygame as pg
from models.constantes import *
from models.auxiliar import SurfaceManager as sf
from random import randint

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, speed_walk, gravity, jump_power, frame_rate_ms, move_rate_ms, jump_height, p_scale=1,
                 interval_time_jump=100) -> None:
        super().__init__()

        self.__walk_r = sf.get_surface_from_sprisheet("assets\img\enemies\Walk\Walk.png", 8, 1)
        self.__walk_l = sf.get_surface_from_sprisheet("assets\img\enemies\Walk\Walk.png", 8, 1, flip=True)
        self.__stay_r = sf.get_surface_from_sprisheet("assets\img\enemies\Stay\Idle.png", 6, 1)
        self.__stay_l = sf.get_surface_from_sprisheet("assets\img\enemies\Stay\Idle.png", 6, 1, flip=True)
        self.__atack_r = sf.get_surface_from_sprisheet("assets\img\enemies\Atack\Shot_1.png", 8, 1)
        self.__atack_l = sf.get_surface_from_sprisheet("assets\img\enemies\Atack\Shot_1.png", 14, 1, flip=True)
        self.__dead_r = sf.get_surface_from_sprisheet("assets\img\enemies\Dead\Dead.png", 3, 1)
        self.__dead_l = sf.get_surface_from_sprisheet("assets\img\enemies\Dead\Dead.png", 3, 1, flip=True)

        self.__count = 0
        self.__initial_frame = 0
        self.__lives = 5
        self.score_value = 200
        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = speed_walk

        self.__gravity = gravity
        self.__jump_power = jump_power
        self.__animation = self.__stay_r
        self.direction = 1
        self.__image = self.__animation[self.__initial_frame]
        self.rect = self.__image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._collition_rect = pg.Rect(x + self.rect.width / 4, y + self.rect.height / 4,
                                self.rect.width / 2, self.rect.height / 2)
        self.__ground_collition_rect = pg.Rect(self._collition_rect)
        self.__ground_collition_rect.height = GROUND_COLLIDE_H
        self.__ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.__dead_timer = 0
        self.__dead_duration = 1000

        self.__is_jump = False
        self.__is_fall = False
        self.__is_shoot = False
        self.__is_dead = False
        self.__is_active = True

        self.__is_looking_right = True
        self.__shoot_contact = False

        self.__tiempo_transcurrido_animation = 0
        self.__frame_rate_ms = frame_rate_ms
        self.__tiempo_transcurrido_move = 0
        self.__move_rate_ms = move_rate_ms
        self.__y_start_jump = 0
        self.__jump_height = jump_height

        self.__tiempo_transcurrido = 0
        self.__tiempo_last_jump = 0  # en base al tiempo transcurrido general
        self.__interval_time_jump = interval_time_jump

    def change_x(self, delta_x):
        self.rect.x += delta_x
        self._collition_rect.x += delta_x
        self.__ground_collition_rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self._collition_rect.y += delta_y
        self.__ground_collition_rect.y += delta_y

    def handle_enemy_hit(self):
        print("Enemy Hit!")
        self.__is_dead = True
        self.__animation = self.__dead_r if self.__is_looking_right else self.__dead_l
        self.__dead_timer = 0
        self.__initial_frame = 0
        self.__is_active = False
        self.kill()
        return self.score_value

    def handle_enemy_movement(self):
        self.__is_fall = False
        self.change_x(self.__move_x)

        if 0 <= self.__count <= 50:
            self.__move_x = -self.__speed_walk
            self.__animation = self.__walk_l
            self.__is_looking_right = False
            self.__count += 1
        elif 50 < self.__count <= 100:
            self.__move_x = self.__speed_walk
            self.__animation = self.__walk_r
            self.__is_looking_right = True
            self.__count += 1
        else:
            self.__count = 0

    def do_movement(self, delta_ms, plataform_list, bullet_list, enemies_list, player):
        self.__tiempo_transcurrido_move += delta_ms

        if self.__tiempo_transcurrido_move >= self.__move_rate_ms:
            self.__tiempo_transcurrido_move = 0

            if not self.is_on_plataform(plataform_list):
                if self.__move_y == 0:
                    self.__is_fall = True
                    self.change_y(self.__gravity)
            if self.detect_player_colision(player, enemies_list):
                self.kill()
                
            if self.detect_shoot_contact(bullet_list, enemies_list, player):
                print("Enemy hit by bullet!")
                self.handle_enemy_hit()
                
            else:
                self.handle_enemy_movement()

    # def handle_enemy_colision(self,bullet_list, enemies_list, player):
    #     if self.detect_shoot_contact(bullet_list, enemies_list, player):
    #             print("Enemy hit by bullet!")
    #             self.handle_enemy_hit()
    #     elif self._collition_rect.colliderect(player.collition_rect):
    #         self.detect_player_colision(player, enemies_list )
            

    #     else:
    #         self.handle_enemy_movement()
        
        



    def is_on_plataform(self, plataform_list):
        retorno = False

        if self.__ground_collition_rect.bottom >= GROUND_LEVEL:
            retorno = True
        else:
            for plataforma in plataform_list:
                if self.__ground_collition_rect.colliderect(plataforma.__ground_collition_rect):
                    retorno = True
                    break
        return retorno

    def detect_shoot_contact(self, bullet_list, enemies_list, player):
        
        for bullet in bullet_list:
            print(f"Enemy Rect: {self.rect}")
            print(f"Bullet Rect: {bullet.rect}")
            if self.rect.colliderect(bullet.rect):
                bullet.kill()
                bullet_list.remove(bullet)
                self.__shoot_contact = True
                player.score += self.score_value
                if self in enemies_list:
                    enemies_list.remove(self)
                print("Bullet hit the enemy!")
                break
            else:
                self.__shoot_contact = False
        # self.kill()
        return self.__shoot_contact

    def detect_player_colision(self, player, enemies_list):
        if self.rect.colliderect(player.collition_rect):    
            player.current_lifes -= 1
            self.kill()
            if self in enemies_list:
                enemies_list.remove(self)   
            return True                        
                    
                    
                

    def do_animation(self, delta_ms):
        self.__tiempo_transcurrido_animation += delta_ms
        if self.__tiempo_transcurrido_animation >= self.__frame_rate_ms:
            self.__tiempo_transcurrido_animation = 0

            if self.__initial_frame < len(self.__animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
        print(f"Animacion: {self.__initial_frame} de {len(self.__animation)} ")

    def enemies_generator(self, enemies_list, delta_ms):
        self.__tiempo_transcurrido += delta_ms
        print("Enemy Generator!")

        # Crear un nuevo enemigo en una posición aleatoria en el eje x
        new_enemy_x = randint(0 + self.__move_x, ANCHO_VENTANA - self.__move_x)
        new_enemy_y = 410
        new_enemy = Enemy(new_enemy_x, new_enemy_y, self.__speed_walk, self.__gravity, self.__jump_power,
                          self.__frame_rate_ms, self.__move_rate_ms, self.__jump_height)
        enemies_list.append(new_enemy)
        print("New enemy created!")

    def update(self, delta_ms, plataform_list, bullet_list, enemies_list, player):
        # self.handle_enemy_colision(bullet_list, enemies_list, player)
        if not self.__is_dead and self.__is_active:
            self.do_movement(delta_ms, plataform_list, bullet_list, enemies_list, player)
            self.do_animation(delta_ms)
            
            print(f"is dead? : {self.__is_dead}")
            print(f"is active? : {self.__is_active}")
        else:
            self.__dead_timer += delta_ms
            if self.__dead_timer >= self.__dead_duration:
                self.__is_active = False

    def draw(self, screen, enemies_list):
        if DEBUG and self.__is_active:
            pg.draw.rect(screen, color=(255, 0, 0), rect=self._collition_rect)

        if not self.__is_dead:
            self.__image = self.__animation[self.__initial_frame]
            screen.blit(self.__image, self.rect)
            print("")
        else:
            self.kill()
            

    def receive_shoot(self):
        self.__lives -= 1

    @property
    def get_score_value(self):
        return self.score_value
    
    @property
    def get_is_active(self):
        return self.__is_active
    
    @property
    def get_is_dead(self):
        return self.__is_dead
    
    @property
    def get_shoot_contact(self):
        return self.__shoot_contact