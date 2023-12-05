import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, ALTO_VENTANA, GROUND_COLLIDE_H, GROUND_LEVEL
from bullet import *
from enemigo import Enemy
class Jugador:
    lista_balas = []
    def __init__(self, coordenada_x , coordenada_y, frame_rate = 1000, speed_walk = 6, speed_run = 12, gravity = 28, delta_ms = 300, jump = 150):

        

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
        
        self.__stay = False

        self.__reference_time = pg.time.get_ticks()
        self.__time_between_updates = 1500
        

        self.__initial_frame = 0 #Frame inicial que queremos tomar 
        self.__actual_animation = self.__iddle_r #Tomamos la lista entera de surfaces. Contiene cada frame de la animacion
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame] #Definimos cual va a ser el frame de toda la lista que comience la animacion
        self.__rect = self.__actual_image_animation.get_rect() #Utilizamos el metodo get_rect para definir el limite de nuestra img, para x ejemplo, después poder trabajar con las colisiones
        
        self.__ground_rect = pg.Rect(0, GROUND_LEVEL - GROUND_COLLIDE_H, ANCHO_VENTANA, GROUND_COLLIDE_H)

        self.__is_shooting = False
        self.__is_jumping = False
        self.__on_ground = False
        self.__on_platform = False
        self.__is_looking_right = True 
        self.__lifes = 3
        self.max_lifes = 3
        self.current_lifes = self.max_lifes
        self.score = 0
        self.__score = 0
        self.__stay = True
        self.__shot_cooldown = 1000  # Cooldown in milliseconds
        self.__last_shot_time = pg.time.get_ticks()



        

        self.collition_rect = pg.Rect(self.__move_x+self.__rect.width/12,self.__move_y,self.__rect.width/12,self.__rect.height/2)
        self.ground_collition_rect = pg.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = self.__move_y + self.__rect.height - GROUND_COLLIDE_H
        
    def actualizar_si_paso_segundo(self):
        actual_time = pg.time.get_ticks()

        if actual_time - self.__reference_time > self.__time_between_updates:
            self.__reference_time = actual_time
            
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
        if self.__actual_animation != animation_list:
            self.__actual_animation = animation_list
            self.__initial_frame = 0
        



        self.__is_looking_right = look_r

    
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
        

    def __set_and_animations_preset_y(self, move_y,animation_list: list[pg.surface.Surface], look_r : bool, delta_ms):
        '''
        ¿Qué hace?
        El método '__set_and_animations_preset' permite modificar la posicion horiontal en el eje y del 'main_player'

        ¿Qué recibe?
        N/A
        ¿Qué devuelve?
        N/A
        '''
        self.__move_y -= self.__jump *( delta_ms / self.__frame_rate)
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
        if self.__actual_animation != animation_list: #self.__jump_r if self.__is_looking_right else self.__jump_l
            self.__actual_animation = animation_list
            self.__initial_frame = 0
            
        '''
        establece que la animación actual ('__actual_animation') es igual a la lista que almacena las sprites recortadas del salto der
        ('__jump_r')  siempre y cuando '__is_looking_right' sea True. Caso contrario será ('__jump_l')
        '''

        #aaaa
        
        # if self.__initial_frame > len(self.__actual_animation) - 1:
        #     self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
        '''
        Seteamos con valor inicial de todos los sprites el indice 0. O sea el primero de la lista en '__actual_animation'
        '''
        self.__is_jumping = True
        '''
        Estado de salto en verdadero por que está saltando pero acá hay que cambiar algo, pues, salta y no puede quedar en verdadero, debe cambiar
        '''
        self.__on_platform = False
        self.__on_ground = False
  
    def walk(self, direction_walk: str = "Right"):
        print("caminando")
        match direction_walk:
            case 'Right':
                look_right = True
                if not self.__is_jumping:
                    self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    self.__rect.y += 0
                else:
                    self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    self.__rect.y += 0
            case 'Left':
                look_right = False
                if not self.__is_jumping:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r = look_right)
                    self.__rect.y += 0
                else:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r = look_right)
                    self.__rect.y += 0
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
    def jump(self, delta_ms):
        ("Saltando")
        # if not self.__is_jumping:
        #     print("NO ESTÁ SALTANDO")
        if self.__on_ground:
                self.__on_ground = True
                self.__on_platform = True
                if  self.__is_looking_right:
                    self.__set_and_animations_preset_y(-self.__jump, self.__jump_r, True, delta_ms)
                    print("EEEEEEEENTROOOOOOOOOOOO ACAAAAAAAAAAAAA")
                    
                else:
                    self.__set_and_animations_preset_y(-self.__jump, self.__jump_l, False, delta_ms)
                    "Entró acá Falseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

   
    # def handle_enemy_collision(self, enemy, enemies_list):
    #     if self.collition_rect.colliderect(enemy._collition_rect):
    #         print("888888888888888888888888888888888888888999999999999999999999999999999999999999999999988888888888888888888888888888888888888888")
    #         # El jugador ha tocado al enemigo
    #         self.current_lifes -= 1
    #         self.current_lifes = max(0, self.current_lifes)  # Limitar a 0 vidas como mínimo
    #         print(f'Vidas restantes: {self.current_lifes}')
    #         if enemy in enemies_list:
    #             enemies_list.remove(enemy)
    
    
    def __is_on_platform(self, plataforma):

        is_on_platform = False
        
         # Colisión detectada
        if self.__rect.y >= self.__ground_rect.y:
            # El piso del programa, acá hay que hacer el piso del programa
            is_on_platform = True
        else:
                for platform in plataforma:
                    if self.ground_collition_rect.colliderect(platform.rect):
                        print("COLISIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIONNN")
                        is_on_platform = True
                        self.__is_jumping = False
                        self.__on_ground = True
                        break
        return is_on_platform
        
    def shot(self):
        self.__is_shooting = True
        current_time = pg.time.get_ticks()

        if current_time - self.__last_shot_time > self.__shot_cooldown:
            self.__last_shot_time = current_time

            if self.__actual_animation not in (self.__shot_r, self.__shot_l): 
                self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
                self.__initial_frame = 0

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
            self.__is_shooting = False
    def stay(self):
        print("stay")
        ####RESVISAR EL STAY PORQUE NO HACE BIEN SU FUNCIÓN
        if self.__on_ground or self.__on_platform:
            if not (self.__is_jumping and self.__is_shooting):
                # if self.__actual_animation not in (self.__shot_r, self.__shot_l): 
                    
                    self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                    self.__initial_frame = 0 
                    print("Quieto iddle")
                    self.__move_x = 0
                    self.__move_y = 0
            
            elif self.__is_shooting:
                if self.__actual_animation != self.__shot_r if self.__is_looking_right else self.__shot_l:
                    self.__actual_animation  = self.__shot_r if self.__is_looking_right else self.__shot_l
        else:
            if not self.__on_ground and self.__is_shooting:
                print("acá no entra mucho tiempo me pareceeeeeeeeeeeeeeeeeeeeeeee")
                self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
                self.__initial_frame = 0 
                
            else:
                self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
                self.__initial_frame = 0 
            
        
                
        
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
        if self.__on_ground or self.__on_platform:
            self.__rect.y += self.__set_edges_limits_y()
            print(f"Posicion eje y: {self.__rect.y}")
            print(f"Posicion eje x: {self.__rect.x}")
        else: 
            self.__rect.y += 0
    
    def do_movement(self, delta_ms, plataforma):
        self.__player_move_time += delta_ms
        print(f"Tiempo movimiento: {self.__player_move_time} : - Tope 100 frame")
        if self.__player_move_time >= self.__frame_rate:
            print("REINICIO DE FRAME. SIGUIENTE MOVIMIENTO EN X E Y")
            self.__player_move_time = 0
        

        if self.__is_on_platform(plataforma) == False:
            self.__rect.y += self.__gravity_force(delta_ms)
        else: 
            self.__rect.y += 0
        self.update_x_y()
        if (self.__is_jumping): #Si está saltando, que deje de saltar y que su capacidad de movimiento sea 0 en eje y y eje x
                    self.__is_jumping = False
                    self.__move_y = 0
                    self.__move_x = 0
        
        
        
        self.actualizar_si_paso_segundo()
               
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        # print(f"Tiempo de animación{self.__frame_rate}")
        # print(f"fotograma numero {self.__initial_frame} de {len(self.__actual_animation)}")
        if self.__player_animation_time >= self.__frame_rate:
            # print(f"REINICIO DE FRAME. SIGUIENTE ANIMACIÓN ")
            self.__player_animation_time = 0
            self.__initial_frame = (self.__initial_frame + 1) % len(self.__actual_animation)
        #     if self.__initial_frame < len(self.__actual_animation) - 1:
        #         print(self.__initial_frame)
        #         print(len(self.__actual_animation))
        #         self.__initial_frame += 1
        #     else:
        #         self.__initial_frame = 0
        # print("actualizando animacion")
                
    

                    
    
    def update(self, delta_ms, platform, enemies_list, bullet_list,enemy):
        # print("Estados:")
        # print(f"En tierra: {self.__on_ground}")
        # print(f"Plataforma: {self.__on_platform}")
        # print(f"Saltando: {self.__is_jumping}")
        # print(f"Disparando: {self.__is_shooting}" )
        # print(f"Mirando derecha: {self.__is_looking_right}")
        # print("UPDATE - MOVIMIENTO EN X - Y - FOTOGRAMAS ANIMACIÓN")
        self.do_animation(delta_ms)
        self.do_movement(delta_ms, platform)
        self.actualizar_si_paso_segundo()
        # self.handle_enemy_collision(enemy, enemies_list)
        # self.handle_score(enemies_list, bullet_list)
        
    
    def draw(self, screen = pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,color=(255,0 ,0),rect = self.__rect)
            pg.draw.rect(screen,color=(255,255,0),rect= self.ground_collition_rect)
            pg.draw.rect(screen, color=(0, 0, 255), rect=self.__ground_rect)



        self.__actual_image_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_image_animation, self.__rect)

        self.collition_rect.x = self.__rect.x + self.__rect.width / 3
        self.collition_rect.y = self.__rect.y
        self.ground_collition_rect.x = self.collition_rect.x
        self.ground_collition_rect.y = self.__rect.y + self.__rect.height - GROUND_COLLIDE_H
    

    
    
    @property
    def get_score_value(self):
        return self.__score
    

        
    