from GUI_form import *
from GUI_form_level_container import Level_container
from level_manager import Level_manager 
from GUI_button_image import Button_Image
from level import Level
from world import World
class FormMenuPlay(Form):
    def __init__(self, screen, x,y,w,h,color_background,color_border,active, path_image):
        super().__init__(screen,x,y,w,h,color_background, color_border,active)
        self.level_manager = Level_manager(self._master)
        image = pygame.image.load(path_image)
        image = pygame.transform.scale(image, (w,h))
        self._slave = image

        self._btn_level_1 = Button_Image(screen = self._slave,
                                           x = 100,
                                           y = 100,
                                           master_x = x,
                                           master_y = y,
                                           w = 100,
                                           h = 150,
                                           onclick = self.go_in_level,
                                           onclick_param = "level_one",
                                           path_image = 'assets\img\lvl\lvl1.png')
        
        self._btn_level_2 = Button_Image(screen = self._slave,
                                           x = 250,
                                           y = 100,
                                           master_x = x,
                                           master_y = y,
                                           w = 100,
                                           h = 150,
                                           onclick = self.go_in_level,
                                           onclick_param = "level_two",
                                           path_image = 'assets\img\lvl\lvl2.png') 
        
        self._btn_level_3 = Button_Image(screen = self._slave,
                                           x = 150,
                                           y = 300,
                                           master_x = x,
                                           master_y = y,
                                           w = 100,
                                           h = 150,
                                           onclick = self.go_in_level,
                                           onclick_param = "level_three",
                                           path_image = 'assets\img\lvl\lvl3.png')
        
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


        self.lista_widgets.append(self._btn_level_1)
        self.lista_widgets.append(self._btn_level_2)
        self.lista_widgets.append(self._btn_level_3)
        self.lista_widgets.append(self.btn_home)


    def on(self, paramether):
        print("hola", paramether)
                  
    def update(self, event_list):
        if self.verificar_dialog_result():
            
            for widget in self.lista_widgets:
                widget.update(event_list)
            self.draw()
        else:
            
            self.hijo.update(event_list)
        
    def go_in_level(self, level_name):
        
        nivel = self.level_manager.get_level(level_name)
        print(f"nivel{nivel}")
        frm_level_container = Level_container(self._slave, nivel)
        self.show_dialog(frm_level_container)
        

    def btn_home_click(self, param):
            self.end_dialog()

