import pygame as pg
from pygame.locals import * 
from GUI_form import *
from GUI_button_image import *


class Level_container(Form):
    def __init__(self, screen: pygame.Surface, level):
        super().__init__(screen, 0,0, screen.get_width(), screen.get_height(), color_background= "Black")
        level._slave = self._slave
        self.level = level
        self._btn_home = Button_Image(screen = self._slave,
                                     x = -200,
                                     y = -200,
                                     master_x= self._w-50,
                                     master_y= self._h-50,
                                     w = 50,
                                     h= 50,
                                     onclick = self.btn_home_click,
                                     onclick_param= "",
                                     path_image= 'assets\img\lvl\home.png')
        # self._boton_home = Button_Image(screen = self._slave,
        #                                 master_x= self._w - 50,
        #                                 master_y = self._h - 50,
        #                                 x = 500,
        #                                 y= 500,
        #                                 w= 50,
        #                                 h= 50,
        #                                 path_image='assets\img\lvl\home.png',
        #                                 onclick= self.btn_home_click,
        #                                 onclick_param= "")

        self.lista_widgets.append(self._btn_home)
        # self.lista_widgets.append(self._boton_home)
    def update(self, event_list):
        for widget in self.lista_widgets:
            print(f"widget: {widget}")
            widget.update(event_list)
            widget.draw()
        self.draw()
        self.level.update(event_list)
    
    def btn_home_click(self, param):
        print("clickeaste")
        self.end_dialog()

