import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, ALTO_VENTANA


class Jugador:
    def __init__(self, coordenada_x , coordenada_y, frame_rate = 100, speed_walk = 6, speed_run = 12, gravity = 16, jump = 50):

        self.__iddle_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\idle\\idle.png",6,1,) 
        self.__iddle_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\idle\\idle.png",6,1, flip = True)
        self.__walk_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\walk\\Walk.png",7,1,)
        self.__walk_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\walk\\Walk.png",7,1, flip = True)
        self.__jump_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\jump\\Jump.png",11,1,)
        self.__jump_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\jump\\Jump.png",11,1, flip = True)
        self.__run_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\run\\Run.png",8,1,)
        self.__run_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\run\\Run.png",8,1, flip = True)
        self.__move_x = coordenada_x  
        """¡¡ATENCION!! NO CONFUNDIR MOVE_X CON COORDENADAS DE APARICION"""
        self.__move_y = coordenada_y
        """¡¡ATENCION!! NO CONFUNDIR MOVE_Y CON COORDENADAS DE APARICION"""
        self.__speed_walk = speed_walk #Velocidad de caminata
        self.__speed_run = speed_run #Velocidad corriendo
        self.__frame_rate = frame_rate #velocidad de frames
        self.__player_move_time = 0 
        self.__player_animation_time = 0
        self.__gravity = gravity #Cuantos pixeles de GRAVEDAD
        self.__jump = jump   #cuantos pixeles de salto
        self.__is_jumping = False
        self.__on_ground = False
        self.__initial_frame = 0 #Frame inicial que queremos tomar 
        self.__actual_animation = self.__iddle_r #Tomamos la lista entera de surfaces. Contiene cada frame de la animacion
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame] #Definimos cual va a ser el frame de toda la lista que comience la animacion
        self.__rect = self.__actual_image_animation.get_rect() #Utilizamos el metodo get_rect para definir el limite de nuestra img, para x ejemplo, después poder trabajar con las colisiones
        self.__is_looking_right = True 
        self.lifes = 5
        self.score = 0


    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r:bool):
        """
        ¿Qué hace?
        El método 'set_x_animations_preset' permite modificar la posición horizontal en el eje x del main_player

        ¿Qué recibe?
        Recibe tres parámetros que son:
        'move_x'
        'animation_list': de tipo list. Que contiene cada frame de los spritesheet de los distintos movimientos 
        'look_r' : indica la direccion en donde está mirando el jugador
        ¿Qué devuelve?
        No retorna nada
        """

        self.__move_x = move_x
        '''
        '__move_x' es igual al valor 
        
        '''
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    def __gravity_force(self):
        if self.__rect.y < (ALTO_VENTANA - self.__actual_image_animation.get_height())-100:  #Control de gravedad
                self.__rect.y += self.__gravity
                return self.__rect.y


    def __set_and_animations_preset_y(self):
        '''
        ¿Qué hace?
        El método '__set_and_animations_preset' permite modificar la posicion horiontal en el eje y del 'main_player'

        ¿Qué recibe?
        N/A
        ¿Qué devuelve?
        N/A
        '''
        self.__move_y = -self.__jump
        '''
        '__move_y' toma el valor del salto en negativo, puesto que controla el movimiento de la imagen de 'main_player'
        sobre el 'eje_y'
        '''
        self.__move_x = self.__speed_walk if self.__is_looking_right else -self.__speed_walk
        '''
        Estamos diciendo que los pixeles de movimiento sobre el 'eje_x' es igual a la velocidad de caminata (__speed_walk en positivo) siempre 
        y cuando el valor de '__is_looking_right' sea true. Ya que, eso garantiza que 'main_personaje' mira a la derecha. 
        Caso contrario será negativo '-__speed_walk' ya que de esta forma se desplazará hacia la izquieda en el eje x

        '''
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        '''
        establece que la animación actual ('__actual_animation') es igual a la lista que almacena las sprites recortadas del salto der
        ('__jump_r')  siempre y cuando '__is_looking_right' sea True. Caso contrario será ('__jump_l')
        '''
        self.__initial_frame = 0
        '''
        Seteamos con valor inicial de todos los sprites el indice 0. O sea el primero de la lista en '__actual_animation'
        '''
        self.__is_jumping = True
        '''
        Estado de salto en verdadero por que está saltando pero acá hay que cambiar algo, pues, salta y no puede quedar en verdadero, debe cambiar
        '''
        


        

    def walk(self, direction_walk: str = "Right"):
        match direction_walk:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r = look_right)

    def run(self, direction_walk: str = "Right"):
        match direction_walk:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r = look_right)

    def jump(self):
        if not self.__is_jumping:
            self.__set_and_animations_preset_y()
            
        

    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0

    def __set_edges_limits_x(self):
        '''
        ¿Qué hace?
        El método '__set_edges_limits' establece los pixeles ('pixels_move') que podrá moverse 'main_player' siempre y cuando esté dentro de los límites
        establecidos. En este caso, los límites se establecen con una cuenta que es (ANCHO_VENTANA - ANCHO_IMAGEN_ANIMACION_ACTUAL)
        Siempre y cuando el valor (ubicación) de 'main_player 'en el 'eje_x' sea menor a tal resta el movimiento que tendrá 'main_player'
        será igual a 'self.__move_x' que equivale al valor instanciado de la clase. De lo contrario su valor de movimiento será 0.
        Esto se traduce de la siguiente forma. Siempre y cuando estés dentro de los límites establecidos vas a poder moverte, caso contrario no.

        ¿Que recibe?
        No recibe parámetros
        ¿Qué devuelve?
        No devuelve parámetros
        '''
        
        pixels_move_x = 0
        if self.__move_x > 0:
            pixels_move_x = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_image_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move_x = self.__move_x if self.__rect.x > 0 else 0

        return pixels_move_x
    
    def set_edges_limits_y(self):
        pixels_move_y = 0
        if self.__move_y > 0:
            pixels_move_y = self.__move_y if self.__rect.y < ALTO_VENTANA - (self.__actual_image_animation.get_height() - 100) else 0
        elif self.__move_y < 0:
            pixels_move_y = self.__move_y if self.rect.y > 0 else 0
        
        return pixels_move_y
    

        
        
        pass
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_edges_limits_x()
            self.__rect.y += self.__gravity_force()
            self.__rect.y += self.__move_y
            # if self.__rect.y < (ALTO_VENTANA - self.__actual_image_animation.get_height())-100:  #Control de gravedad
            #     self.__rect.y += self.__gravity 
            #     self.__on_ground = False
        
            # if self.__rect.y == (ALTO_VENTANA - self.__actual_image_animation.get_height()) - 100:
            #     self.__on_ground = True
                            
            #     self.__rect.y += self.__gravity
            # if self.__is_jumping and self.__on_ground:
            #     if self.__is_looking_right:
            #         self.__rect.y -= self.__jump
            #         self.__rect.x += self.__jump/2
            #         self.__is_jumping = False
            #         self.__on_ground = False
            #     else:
            #         self.__rect.y -= self.__jump
            #         self.__rect.x -= self.__jump/4
            #         self.__is_jumping = False
            #         self.__on_ground = False
            

        else:
                self.__rect.y += self.__move_y
               

    

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                if self.__is_jumping:
                    self.__is_jumping = False
                    self.__move_y = 0
                    
    
    def update(self, delta_ms):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
    
    def draw(self, screen = pg.surface.Surface):
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_image_animation, self.__rect)
    



        pass    