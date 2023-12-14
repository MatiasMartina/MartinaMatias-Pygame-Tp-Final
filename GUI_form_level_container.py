
import pygame as pg
from pygame.locals import * 
from GUI.GUI_form import *
from GUI.GUI_button_image import *


class Level_container(Form):
    def __init__(self, screen: pygame.Surface, levelac):
        super().__init__(screen, 0,0, screen.get_width(), screen.get_height(), color_background= "Black")
        levelac._slave = self._slave
        self.level = levelac
        self._btn_home = Button_Image(screen = self._master,
                                    master_x= self._x,
                                    master_y= self._y,
                                     x = self._w - 100,
                                     y = self._h - 100,
                                     w = 600,
                                     h= 600,
                                     onclick = self.btn_home_click,
                                     onclick_param= "",
                                     path_image= 'assets\img\lvl\home.png')
        
        # self.game_over_form = GameOverForm(screen, 0, 0, 900, 1200, "Black", "yellow", 5, True)  # Instancia del formulario de Game Over
        # self.show_game_over = False
        self.lista_widgets.append(self._btn_home)
        
        # self.lista_widgets.append(self._boton_home)
    def update(self, event_list):
        self.level.update(event_list)
        self.draw()
        for widget in self.lista_widgets:
            # print(f"widget: {widget}")
            widget.update(event_list)
            # widget.draw()
    
    def btn_home_click(self, param):
        print("clickeaste")
        self.end_dialog()

