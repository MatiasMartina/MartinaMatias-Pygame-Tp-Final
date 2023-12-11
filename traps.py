from models.constantes import  TILE_SIZES, DEBUG, DEBUG_TRAP
import pygame as pg


class Traps(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('assets\img\\title\\trap.png')
        self.image = pg.transform.scale(img, (TILE_SIZES, TILE_SIZES // 2))
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width
        self.rect_top = self.rect.top
        self.rect.x = x
        self.rect.y = y
    
    def detect_collisions(self, player):
        if DEBUG_TRAP:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        if self.rect.colliderect(player.rect_collision):
            if player.current_lifes>0:
                player.current_lifes -= 1
                if player.current_lifes >=1:
                    player.restart_position()
        pass

    def update(self, screen, player):
        self.draw(screen)
        self.detect_collisions(player)
        pass
    def draw(self,screen):
        if DEBUG:
            pg.draw.rect(screen, (0,0,0), self.rect, 2)
        screen.blit(self.image, self.rect)
        
