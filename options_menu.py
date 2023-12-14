from GUI.GUI_form import *
from GUI.GUI_form_level_container import Level_container
from level_manager import Level_manager 
from GUI.GUI_button_image import Button_Image
from level import Level
from world import World
from GUI.GUI_slider import Slider
from GUI.GUI_label import Label
class FormMenuOptions(Form):
    def __init__(self, screen, x,y,w,h,color_background,color_border,active, path_image):
        super().__init__(screen,x,y,w,h,color_background, color_border,active)
        self.level_manager = Level_manager(self._master)
        image = pygame.image.load(path_image)
        image = pygame.transform.scale(image, (w,h))
        self._slave = image
        self.volumen = 0.2
        self.flag_play = True
    


        self.slider_volumen = Slider(self._slave, x, y,100,300, 300,15, self.volumen, 
                                     "blue", "white")
        


        self.btn_play = Button(self._slave, x, y, 100, 400,
                               50, 50,
                               "red", "blue", 
                               self. btn_play_click, "",
                               "Pause", "Verdana",15, "white"
                               )
        
        porcentaje_volumen = f"{self.volumen * 100}%"
        self.label_volumen = Label(self._slave,200,400, 100, 50, porcentaje_volumen,
                                   "Comic Sans MS", 15,"white", "Recursos\Table.png")

        self.btn_home = Button_Image(screen= self._slave,
                                     x = 400,
                                     y = 400,
                                     master_x= x,
                                     master_y= y,
                                     w = 50,
                                     h = 50,
                                     onclick=self.btn_home_click,
                                     onclick_param= "",
                                     path_image= 'assets\img\lvl\home.png' )
        
        self.lista_widgets.append(self.btn_home)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_play)

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
            self.lista_widgets.append(self.btn_home)


    
        

    def btn_home_click(self, param):
            self.end_dialog()

