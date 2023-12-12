import pygame as pg
from models.constantes import DEBUG, DEBUG_BULLET,DEBUG_ENEMIES_GENERATOR
from models.auxiliar import SurfaceManager as sf

class Bala(pg.sprite.Sprite):
    def __init__(self, owner, x_init, y_init, x_end, y_end, speed: 100, frame_rate_ms, move_rate_ms, width=5, height=5):
        super().__init__()

        self.tiempo_transcurrido_move = 0
        self.original_image = pg.image.load("assets\img\player\spell\\bullet.png").convert()

        self.rect = pg.Rect(x_init, y_init, width + 20, height + 20)
        self.image = pg.transform.scale(self.original_image, (self.rect.width, self.rect.height))
        self.__actual_animation = self.image
        self.__initial_frame = 0
        self.x = x_init
        self.y = y_init
        self.owner = owner
        self.rect.x = x_init
        self.rect.y = y_init
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        self.__explosive_animation = pg.image.load('assets\img\player\explosion\explosive.png')
        self._is_active = True
        self.move_x = speed
        self.move_y = 0
        self.explosion_played = False
        
    def update(self, delta_ms, plataform_list, enemy_list, player, world):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0

            if self._is_active:
                self.rect.x += self.move_x
                self.rect.y += self.move_y
                self.check_impact(plataform_list, enemy_list, player, world)
            else:
                
                if not self.explosion_played:
                    if self.__initial_frame < len(self.__explosive_animation) - 1:
                        self.__initial_frame += 1
                        self.__actual_animation = self.image
                        self.rect.y = self.move_y
                        self.rect.x = self.move_x
                    else:
                        self.explosion_played = True
                        # No eliminar la instancia aquí
            if DEBUG_BULLET:
                print(f"is active?{self._is_active}")

    def check_impact(self, tile_list, enemy_list, player,world):
        if DEBUG_BULLET:
            print("CHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEKEOBULLLLLLLLLLLLLLLLLLLLLLLLLLLLLLET")
        for enemy in enemy_list:    
            if self.rect.colliderect(enemy.rect):
                if DEBUG_BULLET:
                    print("ENTROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                if DEBUG_ENEMIES_GENERATOR:
                    print("IMPACTO ENEMYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
                self.__image = self.__explosive_animation
                self._is_active = False
                enemy.kill()
                enemy.enemies_killed +=1
                print(f"Enemies killed (bullet) {enemy.enemies_killed}")
                player.score +=200
        for tile in world.tile_list:
            if self.rect.colliderect(tile[1]):
                self._is_active = False
                self.kill()
    # def check_impact(self, plataform_list, enemy_list, player):
    #     for enemy in enemy_list:
    #         if self._is_active and self.owner != enemy and self.rect.colliderect(enemy.rect):
    #             print("IMPACTO ENEMYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
    #             self._is_active = False
    #             self.kill()
                
                

    def draw(self, screen, bullet_list):
        if self._is_active:
            if DEBUG_BULLET:
                pg.draw.rect(screen, (255, 0, 0), self.rect, 2)
            screen.blit(self.__actual_animation, self.rect)
        else:
            self.kill()

        #     pg.draw.rect(screen, color=(255, 0, 0), rect=self.rect)
        #     screen.blit(self.__actual_animation, self.rect)#[self.__initial_frame], self.rect)
            
            for bullet in bullet_list:
                bullet_list.remove(bullet)