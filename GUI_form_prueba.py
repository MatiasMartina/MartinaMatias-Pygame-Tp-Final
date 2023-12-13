import pygame
from pygame.locals import *

from GUI_button import *
from GUI_slider import *
from GUI_textbox import *
from GUI_label import *
from GUI_form import *
from GUI_button_image import *
from GUI_form_menu_score import *
from play_menu import FormMenuPlay

    
class FormPruebas(Form):
    
    
    def __init__(self, screen: pygame.Surface, x: int, y: int, w:int, h: int, color_background, color_border = "Black", border_size: int = -1, active = True):
    
        super().__init__(screen, x,y,w,h,color_background, color_border, border_size, active)

        self.flag_play = True
        
        self.volumen = 0.2
                
        pygame.mixer.init()
        
        pygame.mixer.music.load(r"C:\Users\Mati\Desktop\BA-ME-APRO\sounds\menu.mp3")
        
        pygame.mixer.music.set_volume(self.volumen)
        
        pygame.mixer.music.play(-1)
        


        self.txt_nombre = TextBox(self._slave, x, y, 
                                  50, 50, 150, 30, 
                                  "gray","white","red","blue",2,
                                  "Comic Sans MS", 15, "black")
        
        self.btn_play = Button(self._slave, x, y, 100, 100,
                               100, 50,
                               "red", "blue", 
                               self. btn_play_click, "",
                               "Pause", "Verdana",15, "white"
                               )
        
        
        self.slider_volumen = Slider(self._slave, x, y, 100,200, 500, 15, self.volumen, 
                                     "blue", "white")
        
        
        
        porcentaje_volumen = f"{self.volumen * 100}%"
        self.label_volumen = Label(self._slave,650,190, 100, 50, porcentaje_volumen,
                                   "Comic Sans MS", 15,"white", "Recursos\Table.png")
        
        
        self.btn_tabla = Button_Image(self._slave, x, y, 225,100, 50, 50, "Recursos\Menu_BTN.png", 
                                      self.btn_tabla_click, "")
        
        self.btn_level = Button_Image(self._slave, x,y, 300, 100, 50,50, 'assets\img\lvl\lvls.png', self.btn_level_click, "")
        
        self.lista_widgets.append(self.txt_nombre)
        self.lista_widgets.append(self.btn_play)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.btn_tabla)
        self.lista_widgets.append(self.btn_level)
    
    def render(self):
        self._slave.fill(self._color_background)

    def update(self, lista_eventos):
        
        if self.verificar_dialog_result():
            if self.active:
                print(f"{self.active}")
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)#POLIMORFISMO
                self.update_volumen(lista_eventos)
                
        else:
            self.hijo.update(lista_eventos)

    def update_volumen(self, lista_eventos):
        self.volumen = self.slider_volumen.value
        self.label_volumen.update(lista_eventos)
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)
        
        
    
    def btn_play_click(self, param):
        if self.flag_play:
           pygame.mixer.music.pause()
           self.btn_play._color_background = "blue"
           
           self.btn_play.set_text("Play")
        else:
            
            pygame.mixer.music.unpause()
            self.btn_play._color_background = "red"
            self.btn_play.set_text("Pause")
            
        
        self.flag_play = not self.flag_play
        
    
    def btn_tabla_click(self, param):
        print("adentro")
        diccionario = [{"Jugador": "Mario", "Score": 100},
                       {"Jugador": "Gio", "Score": 150},
                       {"Jugador": "Uriel", "Score": 250}]
        
        nuevo_form = FormMenuScore(screen = self._master,
                                   x = 250,
                                   y = 25,
                                   w = 500,
                                   h = 550,
                                   color_background = "green",
                                   color_border = "gold",
                                   active = True,
                                   path_image = "Recursos\Window.png",
                                   scoreboard = diccionario,
                                   margen_x = 10,
                                   margen_y = 100,
                                   espacio = 10
                                   )
    

        self.show_dialog(nuevo_form)#Modal
    
    def btn_level_click(self, param):
        print("adentro")
    
        frm_levels =  FormMenuPlay(screen=self._master,
                                   x = 250,
                                   y = 25,
                                   w = 500,
                                   h = 500,
                                   color_background= (220,0,220),
                                   color_border= (255,255,255),
                                   active = True,
                                   path_image= 'assets\img\lvl\Window.png')
        self.show_dialog(frm_levels)

