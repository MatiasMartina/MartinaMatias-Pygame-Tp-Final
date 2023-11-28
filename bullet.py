# bullet.py

import pygame as pg
from models.constantes import DEBUG
import math

class Bala(pg.sprite.Sprite):
    def __init__(self, owner, x_init, y_init, x_end, y_end, speed:100, frame_rate_ms, move_rate_ms, width=5, height=5):
        super().__init__()

        self.tiempo_transcurrido_move = 0
        self.original_image = pg.image.load("assets\img\player\spell\\bullet.png").convert()
        
        
        self.rect = pg.Rect(x_init, y_init, width + 40, height + 40)
        self.image = pg.transform.scale(self.original_image, (self.rect.width, self.rect.height))
        self.x = x_init
        self.y = y_init
        self.owner = owner
        self.rect.x = x_init
        self.rect.y = y_init
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        
        

        self.move_x = speed
        self.move_y = 0

        self.is_active = True

    def update(self, delta_ms, plataform_list, enemy_list, player):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0
            
            self.rect.x += self.move_x
            self.rect.y += self.move_y
            self.check_impact(plataform_list, enemy_list, player)

    def check_impact(self, plataform_list, enemy_list, player):
        if self.is_active and self.owner != player and self.rect.colliderect(player.rect):
            print("IMPACTO PLAYER")
            player.receive_shoot()
            self.is_active = False
        for aux_enemy in enemy_list:
            if self.is_active and self.owner != aux_enemy and self.rect.colliderect(aux_enemy.rect):
                print("IMPACTO ENEMY")
                self.is_active = False
    def draw(self, screen):
        if self.is_active:
            if DEBUG:
                pg.draw.rect(screen, color=(255, 0, 0), rect=self.rect)
            screen.blit(self.image, self.rect)