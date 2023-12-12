from models.constantes import DEBUG_FORM_EXIT, MAIN_MENU
import pygame
from pygame.locals import *
from GUI_button import *
from GUI_slider import *
from GUI_textbox import *
from GUI_label import *
from GUI_form import *
from GUI_button_image import *
from GUI_form_menu_score import *
from models.player.main_player import Jugador
from bee import Bee
from turtle import Turtle
import pygame as pg
from pygame.locals import * 
from models.constantes import * 
from world import *
from chronometer import Chronometer
from level import Level

    
class FormPrueba(Form):
    def __init__(self, screen: pygame.Surface, x: int, y: int, w:int, h: int, color_background, color_border = "Black", border_size: int = -1, active = True, main_running = None):
    
        super().__init__(screen, x,y,w,h,color_background, color_border, border_size, active)
        self.main_running = main_running
        self.flag_play = True
        
        
        
        self.btn_start =   Button(self._slave, 100, 100, 300, 100, 200, 50, "green", "blue", self.btn_start_click, "", "Play", "Verdana", 15, "white")
        self.btn_restart = Button(self._slave, 200, 300 , 300, 300, 200, 50, "green", "red", self.btn_start_click, "", "Restart", "Verdana", 15, "white")
        self.btn_exit =    Button(self._slave, 300, 500, 300, 500, 200, 50, "green", "green", self.btn_exit_click, "", "Exit", "Verdana", 15, "white")
        #AGREGO A LA LISTA WIDGET

        
        
       
        self.lista_widgets.append(self.btn_start)
        self.lista_widgets.append(self.btn_restart)
        self.lista_widgets.append(self.btn_exit)
                
        
    
    


    def render(self):
        self._slave.fill(self._color_background)

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)#POLIMORFISMO
                # self.update_volumen(lista_eventos)
                
        else:
            self.hijo.update(lista_eventos)

    
      
    def btn_start_click(self, param):
        if self.flag_play:
            enemies_list = pg.sprite.Group()
            level_start = Level(actual_level)  
            coins_list = []
            trap_list  = []
            bullet_list = []
            key_list = []
            game_over = 0
            world_data = level_start.load_level()
            world = World(world_data, enemies_list, coins_list, trap_list, key_list)
            

    def btn_exit_click(self, param):
        if DEBUG_FORM_EXIT:
            print("EXIT")
        if self.flag_play:
            print("EXIT")
            if self.main_running:
                self.main_running[0] = False

    def btn_start_click(self, param):
        if DEBUG_FORM_EXIT:
            print("START")
        if self.flag_play:
            MAIN_MENU = False


    def btn_play_click_music(self, param):
        if self.flag_play:
           pygame.mixer.music.pause()
           self.btn_play._color_background = "blue"
           
           self.btn_play.set_text("Play")
        else:
            
            pygame.mixer.music.unpause()
            self.btn_play._color_background = "red"
            self.btn_play.set_text("Pause")
            
        
        self.flag_play = not self.flag_play
        
    