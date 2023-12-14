import sqlite3
import pygame
from pygame.locals import *
from options_menu import FormMenuOptions
from GUI.GUI_button import *
from GUI.GUI_slider import *
from GUI.GUI_textbox import *
from GUI.GUI_label import *
from GUI.GUI_form import *
from GUI.GUI_button_image import *
from GUI.GUI_form_menu_score import *
from play_menu import FormMenuPlay
from GUI.GUI_form_level_container import Level_container
from level_manager import Level_manager
from models.constantes import *
class FormPruebas(Form):
    
    
    def __init__(self, screen: pygame.Surface, x: int, y: int, w:int, h: int, color_background, color_border = "Black", border_size: int = -1, active = True):
    
        super().__init__(screen, x,y,w,h,color_background, color_border, border_size, active)

        self.level_manager = Level_manager(self._master)

        self.flag_play = True
        
        self.volumen = 0.2
                
        pygame.mixer.init()
        
        pygame.mixer.music.load(r"C:\Users\Mati\Desktop\BA-ME-APRO\sounds\menu.mp3")
        
        pygame.mixer.music.set_volume(self.volumen)
        
        pygame.mixer.music.play(-1)
        
        self.btn_tabla = Button_Image(self._slave, x, y, 225,100, 50, 50, "Recursos\Menu_BTN.png", 
                                      self.btn_tabla_click, "")
        
        self.btn_start = Button_Image(self._slave, x,y, 300, 300, 200,100, 'assets\img\lvl\start_btn.png', self.botn_start, "")

        self.btn_level = Button_Image(self._slave, x,y, 300, 450, 200,100, 'assets\img\lvl\lvls.png', self.btn_level_click, "")
        
        self.btm_exit = Button_Image(self._slave, x,y, 300, 600, 200, 100, 'assets\img\lvl\exit_btn.png', self.btn_exit, "")

        self.btn_option = Button_Image(self._slave,x,y, 100, 300, 50,50, 'assets\img\lvl\options.png', self.botn_option, "")

        self.txt_nombre = TextBox(self._slave, x, y, 
                                  300, 100, 200, 50, 
                                  "gray","white","red","blue",2,
                                  "Comic Sans MS", 15, "black")
        
        
        self.lista_widgets.append(self.btn_tabla)
        self.lista_widgets.append(self.btn_level)
        self.lista_widgets.append(self.btn_start)
        self.lista_widgets.append(self.btm_exit)
        self.lista_widgets.append(self.btn_option)
        self.lista_widgets.append(self.txt_nombre)


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
                # self.update_volumen(lista_eventos)
                
        else:
            self.hijo.update(lista_eventos)

    
    def btn_tabla_click(self, param):
        nombre = self.txt_nombre.get_text()  # insert nombre
        ultimo_score = list()

        # ACCEDO AL ULTIMO SCORE
        archivo = open("score.txt", "r")
        for linea in archivo:
            ultimo_score.append(linea)
        archivo.close()

        # INSERTO EN BD
        with sqlite3.connect("BAMEAPRO.db") as conexion:
            print("Conexión a la base de datos establecida")
            try:
                print("entre", nombre, ultimo_score[0])
                # Crear la tabla si no existe
                conexion.execute('''
                    CREATE TABLE IF NOT EXISTS score (
                        nombre TEXT,
                        score INTEGER
                    )
                ''')

                # Insertar datos
                sentencia = 'INSERT INTO score (nombre, score) VALUES (?, ?)'
                conexion.execute(sentencia, (nombre, ultimo_score[0]))
                conexion.commit()

                print("Sentencia ejecutada correctamente")

            except Exception as e:
                print(f"Error en Base de datos: {e}")

        dic_score = list()

        with sqlite3.connect("BAMEAPRO.db") as conexion:
            try:
                sentencia = '''
                    SELECT * FROM score ORDER BY score DESC LIMIT 3
                '''
                cursor = conexion.execute(sentencia)
                for fila in cursor:
                    print("select")
                    dic_score.append({"jugador": f"{fila[0]}", "Score": f"{fila[1]}"})
                print("Tabla creada")
            except Exception as e:
                print(f"Error en Base de datos: {type(e)}")

        form_puntaje = FormMenuScore(self._master, 300, 50, 500, 500, (220, 0, 220), "white", True,
                                     r'Recursos\\Window.png', dic_score, 100, 10, 10)
        self.show_dialog(form_puntaje)

    def btn_level_click(self, param):
        print("adentro")

        frm_levels = FormMenuPlay(screen=self._master,
                                  x=250,
                                  y=25,
                                  w=500,
                                  h=500,
                                  color_background=(220, 0, 220),
                                  color_border=(255, 255, 255),
                                  active=True,
                                  path_image='assets\img\lvl\Window.png')
        self.show_dialog(frm_levels)

        
    # def btn_level_click(self, param):
    #     print("adentro")
    
    #     frm_levels =  FormMenuPlay(screen=self._master,
    #                                x = 250,
    #                                y = 25,
    #                                w = 500,
    #                                h = 500,
    #                                color_background= (220,0,220),
    #                                color_border= (255,255,255),
    #                                active = True,
    #                                path_image= 'assets\img\lvl\Window.png')
    #     self.show_dialog(frm_levels)

    def botn_start(self, level_name):
        print("adentro")
    
        nivel = self.level_manager.get_level('level_one')
        print(f"nivel{nivel}")
        # Obtiene el nombre de usuario desde la caja de texto
        username = self.txt_nombre.get_text()
        # self.save_name(username)
        
        # # # Establece el nombre de usuario directamente en el jugador
        # self.player.username = username
        # print(f'{self.player.username}')
        frm_level_container = Level_container(self._slave, nivel)
        self.show_dialog(frm_level_container)
        self.btn_home = Button_Image(screen= self._slave,
                                     master_x= self._x,
                                     master_y= self._y,
                                     x = self._w,
                                     y = self._h,
                                     w = 600,
                                     h = 600,
                                     onclick=self.btn_home_click,
                                     onclick_param= "",
                                     path_image= 'assets\img\lvl\home.png')

        self.lista_widgets.append(self.btn_home)
        

    def botn_option(self, param):
        options = FormMenuOptions(screen=self._master,
                                  x = 0,
                                  y = 0,
                                  w= 500,
                                  h = 500,
                                  color_background= (0,0,0),
                                  color_border= (255,255,255),
                                  active = True,
                                  path_image = 'assets\img\lvl\Window.png')
        self.show_dialog(options)
        
    
    def btn_exit(self):
        self.end_dialog()

    def btn_home_click(self):
        self.end_dialog()

    