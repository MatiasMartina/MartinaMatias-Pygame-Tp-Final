import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, ALTO_VENTANA
from bullet import *

class Jugador:
    lista_balas = []
    def __init__(self, coordenada_x , coordenada_y, frame_rate = 1000, speed_walk = 6, speed_run = 12, gravity = 8, delta_ms = 300, jump = 250):

        '''
        self.__iddle_r = sf.get_surface_from_sprisheet("./assets/img/player/idle/idle.png",6,1,) 
        self.__iddle_l = sf.get_surface_from_sprisheet("./assets/img/player/idle/idle.png",6,1, flip = True)
        self.__walk_r = sf.get_surface_from_sprisheet("./assets/img/player/walk/Walk.png",7,1,)
        self.__walk_l = sf.get_surface_from_sprisheet("./assets/img/player/walk/Walk.png",7,1, flip = True)
        self.__jump_r = sf.get_surface_from_sprisheet("./assets/img/player/jump/Jump.png",11,1,)
        self.__jump_l = sf.get_surface_from_sprisheet("./assets/img/player/jump/Jump.png",11,1, flip = True)
        self.__run_r = sf.get_surface_from_sprisheet("./assets/img/player/run/Run.png",8,1,)
        self.__run_l = sf.get_surface_from_sprisheet("./assets/img/player/run/Run.png",8,1, flip = True)
        self.__shot_r = sf.get_surface_from_sprisheet("./assets/img/player/shot/shot.png", 7, 1)
        self.__shot_l = sf.get_surface_from_sprisheet("./assets/img/player/shot/shot.png" ,7, 1, flip=True)
        '''

        self.__iddle_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\idle\\idle.png",6,1,) 
        self.__iddle_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\idle\\idle.png",6,1, flip = True)
        self.__walk_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\walk\\Walk.png",7,1,)
        self.__walk_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\walk\\Walk.png",7,1, flip = True)
        self.__jump_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\jump\\Jump.png",11,1,)
        self.__jump_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\jump\\Jump.png",11,1, flip = True)
        self.__run_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\run\\Run.png",8,1,)
        self.__run_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\run\\Run.png",8,1, flip = True)
        self.__shot_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\shot\\shot.png", 7, 1)
        self.__shot_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\shot\\shot.png" ,7, 1, flip=True)

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
        self.delta_ms = delta_ms
        self.__jump = jump   #cuantos pixeles de salto
        
        self.__state = "Stay"

        self.__reference_time = pg.time.get_ticks()
        self.__time_between_updates = 1500
        

        self.__initial_frame = 0 #Frame inicial que queremos tomar 
        self.__actual_animation = self.__iddle_r #Tomamos la lista entera de surfaces. Contiene cada frame de la animacion
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame] #Definimos cual va a ser el frame de toda la lista que comience la animacion
        self.__rect = self.__actual_image_animation.get_rect() #Utilizamos el metodo get_rect para definir el limite de nuestra img, para x ejemplo, después poder trabajar con las colisiones
        
        self.__is_shoting = False
        self.__is_jumping = False
        self.__on_ground = False
        self.__is_looking_right = True 
        self.lifes = 5
        self.score = 0
        self.__stay = True
        self.__shot_cooldown = 1000  # Cooldown in milliseconds
        self.__last_shot_time = pg.time.get_ticks()

    def actualizar_si_paso_segundo(self):
        actual_time = pg.time.get_ticks()

        if actual_time - self.__reference_time > self.__time_between_updates:
            self.__reference_time = actual_time
            # Tu código para ejecutar después de que haya pasado un segundo
            return False
        else:
            
            return True
            print("Ha pasado un segundo.")

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

    '''
    def __gravity_force(self.delta_msself):
        if self.__rect.y < (ALTO_VENTANA - self.__actual_image_animation.get_height()) - 100:
            self.__is_jumping = True
            self.__on_ground = False
            return self.__gravity
        elif self.__rect.y >= (ALTO_VENTANA - self.__actual_image_animation.get_height()) - 100:
            self.__is_jumping = False
            self.__on_ground = True
            return 0
    '''

    def __gravity_force(self, delta_ms):
        gravity_speed = self.__gravity * (delta_ms / self.__frame_rate)
    
        if self.__rect.y < (ALTO_VENTANA - self.__actual_image_animation.get_height()) - 100:
            self.__is_jumping = True
            self.__on_ground = False
            return gravity_speed
        
        elif self.__rect.y >= (ALTO_VENTANA - self.__actual_image_animation.get_height()) - 100:
            self.__is_jumping = False
            self.__on_ground = True
            return 0
    

    def __set_and_animations_preset_y(self, move_y,animation_list: list[pg.surface.Surface], look_r : bool):
        '''
        ¿Qué hace?
        El método '__set_and_animations_preset' permite modificar la posicion horiontal en el eje y del 'main_player'

        ¿Qué recibe?
        N/A
        ¿Qué devuelve?
        N/A
        '''
        self.__move_y = move_y
        '''
        '__move_y' toma el valor del salto en negativo, puesto que controla el movimiento de la imagen de 'main_player'
        sobre el 'eje_y'
        '''
        # self.__move_x = 0
        self.__move_x = self.__speed_walk/2 if self.__is_looking_right else -self.__speed_walk/2
        '''
        Estamos diciendo que los pixeles de movimiento sobre el 'eje_x' es igual a la velocidad de caminata (__speed_walk en positivo) siempre 
        y cuando el valor de '__is_looking_right' sea true. Ya que, eso garantiza que 'main_personaje' mira a la derecha. 
        Caso contrario será negativo '-__speed_walk' ya que de esta forma se desplazará hacia la izquieda en el eje x

        '''
        self.__actual_animation = animation_list#self.__jump_r if self.__is_looking_right else self.__jump_l
        '''
        establece que la animación actual ('__actual_animation') es igual a la lista que almacena las sprites recortadas del salto der
        ('__jump_r')  siempre y cuando '__is_looking_right' sea True. Caso contrario será ('__jump_l')
        '''
        self.__initial_frame = 0
        # if self.__initial_frame > len(self.__actual_animation) - 1:
        #     self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
        '''
        Seteamos con valor inicial de todos los sprites el indice 0. O sea el primero de la lista en '__actual_animation'
        '''
        self.__is_jumping = True
        '''
        Estado de salto en verdadero por que está saltando pero acá hay que cambiar algo, pues, salta y no puede quedar en verdadero, debe cambiar
        '''
        self.__on_ground = False
  
    def walk(self, direction_walk: str = "Right"):
        print("caminando")
        match direction_walk:
            case 'Right':
                look_right = True
                if not self.__is_jumping:
                    self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    self.__rect.y += self.__gravity_force(self.delta_ms)

                else:
                    self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    self.__rect.y += self.__gravity_force(self.delta_ms)
            case 'Left':
                look_right = False
                if not self.__is_jumping:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r = look_right)
                    self.__rect.y += self.__gravity_force(self.delta_ms)
                else:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r = look_right)
                    self.__rect.y += self.__gravity_force(self.delta_ms)
    def run(self, direction_walk: str = "Right"):
        print("Corriendo")
        if self.__is_jumping:
            self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = True)
        else:

            match direction_walk:
                case 'Right':
                    look_right = True
                    self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = look_right)
                case 'Left':
                    look_right = False
                    self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r = look_right)
    def jump(self):
        ("Saltando")
        if not self.__is_jumping and self.__on_ground:
            if  self.__is_looking_right:
                self.__set_and_animations_preset_y(-self.__jump, self.__jump_r, True)
                print("EEEEEEEENTROOOOOOOOOOOO ACAAAAAAAAAAAAA")
                
            else:
                self.__set_and_animations_preset_y(-self.__jump, self.__jump_l, False)
                "Entró acá False"
               
       
                  
    # def stop_jump(self):
    #     self.__is_jumping = False
    #     self.__on_ground = True
    #     self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
    # def handle_collision(self, plataforma):
    #     if self.__rect.colliderect(plataforma.rect):
    #         # Colisión detectada
    #         if self.__rect.y -200 < plataforma.rect.y:
    #             # El jugador está por encima de la plataforma
    #             self.__on_ground = True
    #             self.__is_jumping = False
    #             self.__rect.y = plataforma.rect.y - self.__rect.height
    #             print("aca wachongui")
    #         else:
    #             # El jugador está por debajo de la plataforma
    #             self.__rect.y = plataforma.rect.y + plataforma.rect.height
    #             self.__move_y = 0
    #             print("cuack aca")

    #     # Verificar colisión en el eje x solo si el jugador no está saltando
    #     if not self.__is_jumping and self.__rect.colliderect(plataforma.rect):
    #         if self.__rect.x < plataforma.rect.x:
    #             # El jugador está a la izquierda de la plataforma
    #             self.__rect.x = plataforma.rect.x - self.__rect.width
    #         else:
    #             # El jugador está a la derecha de la plataforma
    #             self.__rect.x = plataforma.rect.x + plataforma.rect.width
    def handle_collision(self, plataforma):
        if self.__is_jumping:
            if self.__rect.colliderect(plataforma.rect):
                # Colisión detectada
                if self.__rect.y + self.__rect.height - 200 < plataforma.rect.y:
                    # El jugador está por encima de la plataforma
                    self.__on_ground = True
                    self.__is_jumping = False
                    self.__rect.y = plataforma.rect.y - self.__rect.height
                    print("Está arriba de la plataforma")
                elif self.__rect.y >= plataforma.rect.y + plataforma.rect.height:
                    # El jugador está por debajo de la plataforma
                    self.__rect.y = plataforma.rect.y + plataforma.rect.height
                    self.__move_y = self.__jump
                    self.__on_ground = True
                    print("Está abajo de la plataforma")

            # Verificar colisión en el eje x solo si el jugador no está saltando
            if not self.__is_jumping and self.__rect.colliderect(plataforma.rect):
                if self.__rect.x < plataforma.rect.x:
                    # El jugador está a la izquierda de la plataforma
                    self.__rect.x = plataforma.rect.x - self.__rect.width
                else:
                    # El jugador está a la derecha de la plataforma
                    self.__rect.x = plataforma.rect.x + plataforma.rect.width
        
    '''
    def shot(self):
            
            self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
            if self.__is_looking_right:
                bullet = Bala(
                owner = self,
                x_init = self.__rect.x-50,
                y_init = self.__rect.y+80,
                x_end = 600,
                y_end = 0,
                speed = 100,
                frame_rate_ms = 100,
                move_rate_ms = 50)
                self.lista_balas.append(bullet)
            else:
                bullet = Bala(
                owner = self,
                x_init = self.__rect.x+120,
                y_init = self.__rect.y+80,
                x_end = 0,
                y_end = 0,
                speed = -100,
                frame_rate_ms = 100,
                move_rate_ms = 50)
                self.lista_balas.append(bullet)
            # print("Disparando")
            # if self.__is_jumping:
            #     print("si salta")
            #     self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
            #     self.__initial_frame = 0
            #     self.__is_shoting = False
            # elif self.__on_ground:
            #     print("si tierra")
            #     self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
            # else:
                
            #     self.__actual_animation =  self.__shot_r if self.__is_looking_right else self.__shot_l
    '''

    def shot(self):
        current_time = pg.time.get_ticks()

        if current_time - self.__last_shot_time > self.__shot_cooldown:
            self.__last_shot_time = current_time

            self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l

            if self.__is_looking_right:
                bullet = Bala(
                    owner=self,
                    x_init=self.__rect.x - 50,
                    y_init=self.__rect.y + 80,
                    x_end=600,
                    y_end=0,
                    speed=100,
                    frame_rate_ms=100,
                    move_rate_ms=50)
                self.lista_balas.append(bullet)
            else:
                bullet = Bala(
                    owner=self,
                    x_init=self.__rect.x + 120,
                    y_init=self.__rect.y + 80,
                    x_end=0,
                    y_end=0,
                    speed=-100,
                    frame_rate_ms=100,
                    move_rate_ms=50)
                self.lista_balas.append(bullet)        
            
    def stay(self):
        print("stay")
        
        if self.__on_ground:
            if not (self.__is_jumping or self.__is_shoting):
                self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                print("Quieto iddle")
                self.__move_x = 0
                self.__move_y = 0
            
            elif self.__is_shoting:
                self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
        else:
            if not self.__on_ground and self.__is_shoting:
                print("acá no entra mucho tiempo me pareceeeeeeeeeeeeeeeeeeeeeeee")
                self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
            else:
                self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
            
        # if self.__on_ground:
            
        #     if self.__actual_animation not in [self.__iddle_l, self.__iddle_r, self.__shot_l, self.__shot_r, self.__jump_l, self.__jump_r]:
        #         print("Pasó el primer if")
        #         self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                
        #         print("Quieto iddle")
        #         self.__move_x = 0
        #         self.__move_y = 0
        #     elif self.__is_jumping:
        #         print("acá siiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii else if jumping if sino está en el piso entonces está volando")
        #         self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        #     elif self.__is_shoting:
        #         self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
                
        # else:
        #     if not self.__on_ground and self.__is_shoting:
        #         print("acá no entra mucho tiempo me pareceeeeeeeeeeeeeeeeeeeeeeee")
        #         self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
                
        #     else:
        #         self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
                
        
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
    
    def __set_edges_limits_y(self):
        
        pixels_move_y = 0
        if self.__move_y > 0:
            pixels_move_y = self.__move_y if self.__rect.y < ALTO_VENTANA - (self.__actual_image_animation.get_height() - 100) else 0
        elif self.__move_y < 0:
            pixels_move_y = self.__move_y if self.__rect.y > 0 else 0
        
        return pixels_move_y
    





        
    def update_x_y(self):
        self.__rect.x += self.__set_edges_limits_x()
        if self.__rect.y >= (ALTO_VENTANA - self.__actual_image_animation.get_height())-100:
            self.__rect.y += self.__set_edges_limits_y()
            print(f"Posicion eje y: {self.__rect.y}")
            print(f"Posicion eje x: {self.__rect.x}")
        else: 
            self.__rect.y += 0;
    
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        print(f"Tiempo movimiento: {self.__player_move_time} : - Tope 100 frame")
        if self.__player_move_time >= self.__frame_rate:
            print("REINICIO DE FRAME. SIGUIENTE MOVIMIENTO EN X E Y")
            self.__player_move_time = 0
        self.__rect.y += self.__gravity_force(self.delta_ms)
        self.update_x_y()
        if (self.__is_jumping): #Si está saltando, que deje de saltar y que su capacidad de movimiento sea 0 en eje y y eje x
                    # self.__is_jumping = False
                    self.__move_y = 0
                    self.__move_x = 0
        
        
        
        self.actualizar_si_paso_segundo()
               
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        print(f"Tiempo de animación{self.__frame_rate}")
        print(f"fotograma numero {self.__initial_frame} de {len(self.__actual_animation)}")
        if self.__player_animation_time >= self.__frame_rate:
            print(f"REINICIO DE FRAME. SIGUIENTE ANIMACIÓN ")
            self.__player_animation_time = 0
            self.__initial_frame = (self.__initial_frame + 1) % len(self.__actual_animation)
        #     if self.__initial_frame < len(self.__actual_animation) - 1:
        #         print(self.__initial_frame)
        #         print(len(self.__actual_animation))
        #         self.__initial_frame += 1
        #     else:
        #         self.__initial_frame = 0
        # print("actualizando animacion")
                
    

                    
    
    def update(self, delta_ms):
        print("Estados:")
        print(f"En tierra: {self.__on_ground}")
        print(f"Saltando: {self.__is_jumping}")
        print(f"Disparando: {self.__is_shoting}" )
        print(f"Mirando derecha: {self.__is_looking_right}")
        print("UPDATE - MOVIMIENTO EN X - Y - FOTOGRAMAS ANIMACIÓN")
        self.do_animation(delta_ms)
        self.do_movement(delta_ms)
        self.actualizar_si_paso_segundo()
    
    def draw(self, screen = pg.surface.Surface):
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_image_animation, self.__rect)
    

    
    


        
    