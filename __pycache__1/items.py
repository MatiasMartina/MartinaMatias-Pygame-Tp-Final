import sys
import pygame as pg
from models.constantes import *

class ItemBox(pg.sprite.Sprite):
    item_boxes_dict = {
        'Key': pg.image.load('assets\img\items\key_02b.png'),
        'Heart': pg.image.load('assets\img\items\health potion.png'),
        'Portal': pg.image.load('assets\img\items\hat_01c.png'),
        'Boot' : pg.image.load('assets\img\items\\boots_01e.png'),
        'Book'  : pg.image.load('assets\img\items\\book_03a.png'),
        'Time': pg.transform.scale(pg.image.load('assets\img\items\\time.png'), (50, 50)),
    }
    def __init__(self, item_type, x, y,level= False):
        pg.sprite.Sprite.__init__(self)
        self.level = level
        self.finish_level = False
        self.item_type = item_type
        self.image = ItemBox.item_boxes_dict[self.item_type]
        self.rect = self.image.get_rect()
        self._collition_rect = pg.Rect(x , y,
                                self.rect.width ,self.rect.height  )
        self.coor_x =x
        self.coor_y = y

    
    def detect_player_colision(self, player, items_list, chronometer, screen,x,y):
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            if self._collition_rect.colliderect(player.collition_rect):    
                print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                if self.item_type == 'Heart':
                    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
                    player.current_lifes += 1 
                if self.item_type == 'Portal':
                    sys.exit() #next level
                if self.item_type == 'Boot':
                    player.set_move_x(30)
                    pass
                if self.item_type == 'Book':
                    player.score +=50

                if self.item_type == 'Time':
                    chronometer.add_time(15)
                    
                if self.item_type == 'Key':
                    self.next_level()
                    pass  

                if self in items_list:
                    items_list.remove(self)  
                    self.kill() 
                return True    
            
    # def next_level(self):
    #     pass
    # def portal_apear(self, screen, x, y):
    #     # Cargar la imagen del portal
    #     print("PPPPPPPPPPPPPPPPPPPPPPPOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRTTTTTTTTTTTTTTTTTTAAAAAAAAAAAAAAAAAAAAA")
    #     portal_image = pg.image.load('assets\img\items\hat_01c.png')

    #     # Crear un rectángulo para el portal en las coordenadas dadas
    #     portal_rect = pg.Rect(x, y, portal_image.get_width(), portal_image.get_height())

    #     # Dibujar el rectángulo de colisión en modo DEBUG
    #     if DEBUG:
    #         pg.draw.rect(screen, (255, 0, 0), portal_rect, 2)

    #     # Dibujar el portal en la pantalla
    #     screen.blit(portal_image, (x, y))

        
    def update(self, player, items_list, chronometer,screen,x,y): #(main_player, lista_items, lista_balas, chronometer, 700,500)
        self.detect_player_colision(player, items_list, chronometer, screen,x,y) 
        
    def draw(self, screen):
        if DEBUG:
            pg.draw.rect(screen, (255, 0, 0), self._collition_rect, 2)
        
        print(self.finish_level)
        if self.finish_level:
            print(self.finish_level)
            imagen = pg.image.load(r'menu_1\win.jpg')
            screen.blit(imagen, (self.coor_x, self.coor_y ))
        else:
            screen.blit(self.image,(self.coor_x, self.coor_y))
          

    
