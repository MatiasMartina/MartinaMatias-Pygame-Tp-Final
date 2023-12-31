from models.constantes import  TILE_SIZES, DEBUG, DEBUG_TRAP, DEBUG_KEY, actual_level, DEBUG_COINS
import pygame as pg


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('assets\img\\title\\coin.png')
        self.image = pg.transform.scale(img, (TILE_SIZES, TILE_SIZES // 2))
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width
        self.rect_top = self.rect.top
        self.rect.x = x
        self.rect.y = y
        self.sound_coin = pg.mixer.Sound(r"sounds\\buble.wav")
		
        
    def detect_collisions(self, player):
        global actual_level
        if self.rect.colliderect(player.rect_collision):
            self.sound_coin.set_volume(0.2)
            self.sound_coin.play()
            player.capture_key = True
            self.kill()
            if DEBUG_COINS:
                    print("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111A")
            if player.current_lifes>0:
                if DEBUG_COINS:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            
                player.score +=50
                # actual_level +=1
                
                
                if DEBUG_KEY:
                    print(f"{actual_level}")
        
    def update(self, screen, player):
        self.draw(screen)
        self.detect_collisions(player)
        
        
    def draw(self,screen):
        if DEBUG:
            pg.draw.rect(screen, (0,0,0), self.rect, 2)
        screen.blit(self.image, self.rect)