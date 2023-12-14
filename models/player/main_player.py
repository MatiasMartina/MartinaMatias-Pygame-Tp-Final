import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *
from world import World
from bullet import Bala

class Jugador():
    def __init__(self, coordenada_x, coordenada_y, frame_rate = 500, speed_walk = 6, speed_run = 12,    gravity = 28, delta_ms = 100, speed_jump = 5)-> None:
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
        
        ########################
        """IMAGES AND ANIMATION"""############
        ########################
        self.__actual_animation = self.__iddle_r #Tomamos la lista entera de surfaces. Contiene cada frame de la animacion
        self.__initial_frame = 0
        self.__player_animation_time = 0
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame] #Definimos cual va a ser el frame de toda la lista que comience la animacion
        self.__frame_rate = frame_rate
        self.__image = pg.image.load('assets\img\player\player.png')
        self.__image_game_over = pg.image.load('assets\img\player\death\ghost.png')
        #########################
        """POSITION X AND Y"""############
        ########################
        self.__rect = self.__actual_image_animation.get_rect()
        self.__rect.x = coordenada_x
        self.__rect.y = coordenada_y
        #########################
        """COLISIONS"""############
        ########################
        self.__widht = 10
        self.__height = 80
        self.rect_collision = pg.Rect(coordenada_x, coordenada_y, self.__widht,self.__height)
        #########################
        """SHOT HANDLES"""############
        ########################
        self.__shot_cooldown = 1000
        self.__last_shot_time = pg.time.get_ticks()
        #########################
        """MOVEMENT IN X AND Y"""############
        ########################
        self.__speed_walk = speed_walk #Velocidad de caminata
        self.__speed_run = speed_run #Velocidad corriendo
        self.__speed_jump = speed_jump
        self.__gravity = gravity
        self.__vel_y = 0
        self.current_lifes = 1
        self.username = None
        ########################
        """FLAGS"""############
        ########################
        self.is_saved = False
        self.__on_ground = False
        self.__on_platform = False
        self.__is_looking_right = True
        self.__is_jumping = True        
        self.__is_shooting = False
        self.capture_key = False
        self.game_finished = False
        #######################
        ## SOUNDS AND FXS
        ######################  
        self.shoot_sound = pg.mixer.Sound(r"sounds\\disparo.wav")
        self.jump_sound = pg.mixer.Sound(r"sounds\jump.wav")
        self.sound_game_over = pg.mixer.Sound(r"sounds\gameover.wav")
        self.sound_win = pg.mixer.Sound(r'sounds\\win.mp3')
       
        #######################
        ## SCORE AND LIFES
        ######################
        self.score = 0
        self.life = 5
        self.current_lifes = self.life
        self.level = 1
        ########################
        self.delta_ms = delta_ms
        #######################
        ########################
        """MOVEMENTS"""############
        ########################
        self.__movement_in_x = 0
        """¡¡ATENCION!! NO CONFUNDIR MOVE_X CON COORDENADAS DE APARICION"""
        self.__movement_in_y = 0
        """¡¡ATENCION!! NO CONFUNDIR MOVE_Y CON COORDENADAS DE APARICION"""

    
    def walk(self, direction_walk:str = 'Right'):
        x= 0
        match direction_walk:
            case 'Right':
                look_right = True
                if not self.__is_jumping:
                    x =self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    
                else:
                    x = self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    
            case 'Left':
                look_right = False
                if not self.__is_jumping:
                    x = self.__set_x_animations_preset(self.__speed_walk, self.__walk_l, look_r = look_right)
                    
                else:
                    x = self.__set_x_animations_preset(self.__speed_walk, self.__walk_l, look_r = look_right)
                    
        return x  
    def run(self, direction_walk: str = "Right"):
        print("Corriendo")
        # if self.__is_jumping:
        #     x = self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = True)
        # else:

        match direction_walk:
                case 'Right':
                    look_right = True
                    x = self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = look_right)
                case 'Left':
                    look_right = False
                    x= self.__set_x_animations_preset(self.__speed_run, self.__run_l, look_r = look_right)
        return x
    def jump(self, delta_ms): 
        # print("ENTRO")
        y = 0
        x = 0
        if  not self.__is_jumping:
            if DEBUG_JUMP:
                print(f"__vel_y0: {self.__vel_y}")  
            if self.__is_looking_right:
                y,x = self.__set_and_animations_preset_y(-self.__speed_jump, self.__jump_r, True, delta_ms)
            else:
                y,x = self.__set_and_animations_preset_y(-self.__speed_jump, self.__jump_l, False, delta_ms)
            
        else:   
            y= 0
            x = 0
        self.jump_sound.set_volume(0.2)
        self.jump_sound.play()
        return y, x
    def stay(self):
        if DEBUG_PLAYER:

            print("stay")
        return 0
        # ####RESVISAR EL STAY PORQUE NO HACE BIEN SU FUNCIÓN
        # if self.__on_ground or self.__on_platform:
        #     if not (self.__is_jumping and self.__is_shooting):
        #         # if self.__actual_animation not in (self.__shot_r, self.__shot_l): 
                    
        #             if self.__actual_animation != self.__iddle_r or self.__actual_animation != self.__iddle_l:
        #                 self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
        #                 # self.__initial_frame = 0 
        #                 print("Quieto iddle")
        #                 self.__movement_in_x = 0
        #                 self.__movement_in_y = 0
            
        #     elif self.__is_shooting:
        #         if self.__actual_animation != self.__shot_r if self.__is_looking_right else self.__shot_l:
        #             self.__actual_animation  = self.__shot_r if self.__is_looking_right else self.__shot_l
        # else:
        #     if not self.__on_ground and self.__is_shooting:
        #         print("acá no entra mucho tiempo me pareceeeeeeeeeeeeeeeeeeeeeeee")
        #         self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
        #         self.__initial_frame = 0 
                
        #     else:
        #         self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        #         self.__initial_frame = 0 
        # return self.__movement_in_x
    def __set_x_animations_preset(self, speed_action_movement, animation_list: list, look_r:bool):
        """
        ¿Qué hace?
        El método 'set_x_animations_preset' permite modificar la posición horizontal en el eje x del main_player

        ¿Qué recibe?
        Recibe tres parámetros que son:
        'speed_action_movement'
        'animation_list': de tipo list. Que contiene cada frame de los spritesheet de los distintos movimientos 
        'look_r' : indica la direccion en donde está mirando el jugador
        ¿Qué devuelve?
        Retorna movement_in_x que es la cantidad de pixeles que se va a desplazar 'self.__rect.x' en el eje x
        """
        movement_in_x = 0
        
        self.__movement_in_x  = speed_action_movement
        if self.__actual_animation != animation_list:
            self.__actual_animation = animation_list
            self.__inital_frame = 0
        self.__is_looking_right = look_r
        if self.__is_looking_right:
            movement_in_x +=self.__movement_in_x
        else:
            movement_in_x -= self.__movement_in_x  

        return movement_in_x
    def __set_and_animations_preset_y(self, speed_action_movement,animation_list: list[pg.surface.Surface], look_r : bool, delta_ms):
        '''
        ¿Qué hace?
        El método '__set_and_animations_preset' permite modificar la posicion horiontal en el eje y del 'main_player'

        ¿Qué recibe?
        'speed_action_movement' la velocidad (cantidad de pixeles) en la que se va a desplazar 'self.__rect.x' en el eje x de la pantalla
        'animation_list': de tipo list. Que contiene cada frame de los spritesheet de los distintos movimientos 
        'look_r' : indica la direccion en donde está mirando el jugador
        ¿Qué devuelve?
        Retorna movement_in_y que es la cantidad de pixeles que se va a desplazar 'self.__rect.y' en el eje y de la pantalla
        '''
        self.__is_looking_right = look_r
        movement_in_y = 0
        movement_in_x = 0
        print(f"__vel_y1: {self.__vel_y}")  
       
        self.__vel_y = speed_action_movement
        if DEBUG_JUMP:
          print(f"__vel_y2: {self.__vel_y}")       
        self.__vel_y-=10
        if DEBUG_JUMP:
          print(f"__vel_y3: {self.__vel_y}")  
        if self.__vel_y < -105:
            if DEBUG_JUMP:
                print(f"__vel_y4: {self.__vel_y}")  
            self.__vel_y = -105
            if DEBUG_JUMP:
                print(f"__vel_y5: {self.__vel_y}")  
        # Límite superior para la velocidad en el eje Y durante el salto
        # if self.__vel_y < -50:
        #     self.__vel_y = -50

        if self.__actual_animation != animation_list:
            self.__actual_animation = animation_list
            self.__initial_frame = 0
        
        self.__is_jumping = True
        self.__on_platform =  False
        movement_in_y += self.__vel_y
        movement_in_x += self.__movement_in_x

        return movement_in_y, movement_in_x
        # self.__is_looking_right = look_r
        # movement_in_y = 0
        # movement_in_x = 0
        # # self.__vel_y = - speed_action_movement
        # self.__vel_y += speed_action_movement
        # if self.__vel_y<-50:
            
        #     self.__vel_y = -50
        # self.__movement_in_x = 0
        # # movement_in_y = -15
        # # *( delta_ms / self.__frame_rate)
        # '''
        # 'self.__movement_in_y' toma el valor del salto en negativo, puesto que controla el movimiento de la imagen de 'main_player'
        # sobre el 'eje_y'
        # '''
        # # self.__movement_in_x = 0
        # # self.__movement_in_x = self.__speed_walk if self.__is_looking_right else -self.__speed_walk
        # '''
        # Estamos diciendo que los pixeles de movimiento sobre el 'eje_x' es igual a la velocidad de caminata (__speed_walk en positivo) siempre 
        # y cuando el valor de '__is_looking_right' sea true. Ya que, eso garantiza que 'main_personaje' mira a la derecha. 
        # Caso contrario será negativo '-__speed_walk' ya que de esta forma se desplazará hacia la izquieda en el eje x

        # '''
        # if self.__actual_animation != animation_list: #self.__jump_r if self.__is_looking_right else self.__jump_l
        #     self.__actual_animation = animation_list
        #     self.__initial_frame = 0
            
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
        # self.__on_platform = False
        # self.__on_ground = False
        movement_in_y += self.__vel_y
        movement_in_x += self.__movement_in_x
        return movement_in_y, movement_in_x
    def do_animation(self, delta_ms):
        if DEBUG:
            print("DO ANIMATION DEBUG")
            
        self.__player_animation_time += delta_ms
        if DEBUG:
            print(f"Tiempo de animación{self.__frame_rate}")
            print(f"fotograma numero {self.__initial_frame} de {len(self.__actual_animation)}")
        if self.__player_animation_time >= self.__frame_rate:
            if DEBUG:
                print(f"REINICIO DE FRAME. SIGUIENTE ANIMACIÓN ")
            self.__player_animation_time = 0
            self.__initial_frame = (self.__initial_frame + 1) % len(self.__actual_animation)
    
    
    def gravity_force(self, movement_in_y):
        if DEBUG_JUMP:
            print(f"__vel_y_jump_before_gravity_force: {self.__vel_y}")
        self.__vel_y += self.__gravity
        if self.__vel_y >10:
            self.__vel_y = 10
            movement_in_y += self.__vel_y
            self.__is_jumping = True
        return movement_in_y
    
    def shot(self, bullet_list):
        self.__is_shooting = True
        current_time = pg.time.get_ticks()

        if current_time - self.__last_shot_time > self.__shot_cooldown:
            self.__last_shot_time = current_time

            if self.__actual_animation not in (self.__shot_r, self.__shot_l): 
                self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                self.__initial_frame = 0

            if self.__is_looking_right:
                bullet = Bala(
                    owner=self,
                    x_init=self.rect_collision.x,
                    y_init=self.rect_collision.y+30,
                    x_end=600,
                    y_end=0,
                    speed=20,
                    frame_rate_ms=100,
                    move_rate_ms=50)
                bullet_list.append(bullet)
            else:
                bullet = Bala(
                    owner=self,
                    x_init=self.rect_collision.x-20 ,
                    y_init=self.rect_collision.y+30 ,
                    x_end=0,
                    y_end=0,
                    speed=-20,
                    frame_rate_ms=100,
                    move_rate_ms=50)
                bullet_list.append(bullet)        
            self.__is_shooting = False
        self.shoot_sound.set_volume(0.2)
        self.shoot_sound.play()
        pass
    def check_player_alive(self):
        if self.current_lifes <= 0:
            return -1
        else:
            return 0

    def movement_control(self, key_get_pressed, delta_ms, world, trap_list,bullet_list, game_over):
        #GET PRESSED KEY
        movement_in_x = 0
        movement_in_y = 0
        if game_over == 0:
        #     if isinstance(key_get_pressed, dict):
        # # Verificar la existencia de las teclas antes de acceder a ellas
        #         left_key_pressed = key_get_pressed.get(pg.K_LEFT, False)
        #         right_key_pressed = key_get_pressed.get(pg.K_RIGHT, False)

        #         if not left_key_pressed and not right_key_pressed and not self.__is_jumping:
        #             # Resto del código
        #             pass
        #     else:
                
        #         print("key_get_pressed no es un diccionario:", key_get_pressed)
            if not key_get_pressed[pg.K_LEFT] and not key_get_pressed[pg.K_RIGHT] and not self.__is_jumping:
                movement_in_x = self.stay()
            if key_get_pressed[pg.K_LEFT]:
                movement_in_x = self.walk("Left")
            if key_get_pressed[pg.K_RIGHT]:
                movement_in_x = self.walk("Right")
            if key_get_pressed[pg.K_LEFT] and key_get_pressed[pg.K_LSHIFT]:
                movement_in_x = self.run("Left")
            if key_get_pressed[pg.K_RIGHT] and key_get_pressed[pg.K_LSHIFT]:
                movement_in_x = self.run("Right")          
            if key_get_pressed[pg.K_UP] and not self.__is_jumping:
                if DEBUG_JUMP:
                    print("salto")
                if DEBUG_JUMP:
                    print(f"{movement_in_y}")
                    print(f"__vel_y_jump{self.__vel_y}")
                movement_in_y, movement_in_x= self.jump(delta_ms)
                if DEBUG_JUMP:
                    print(f"{movement_in_y}")
            # if key_get_pressed[pg.K_UP] == False:
            #     self.__is_jumping = False
            if key_get_pressed[pg.K_SPACE]:
                self.shot(bullet_list)
                

            #GRAVITY CONTROL
            gravedad = self.gravity_force(movement_in_y)
            if DEBUG_JUMP:
                print(f"Gravity {gravedad}")
                print(f"Desplazamiento en x {movement_in_y}")
                print(f"__vel_y_jump_before_gravity_force: {self.__vel_y}")
            
            movement_in_y += gravedad
            if DEBUG_JUMP:
                print(f"__vel_y_jump_after_gravity_force: {self.__vel_y}")
            if DEBUG:
                print(f"{movement_in_y} and {gravedad}")
            movement_in_y, movement_in_x = self.control_platform_collisions(world, movement_in_y, movement_in_x)
            #ACTUALIZACIÓN DE COORDENADAS 
            self.__rect.x += movement_in_x
            self.__rect.y += movement_in_y
            self.rect_collision.x = self.__rect.x+57
            self.rect_collision.y = self.__rect.y+50
        elif game_over == -1:
            self.__actual_animation = [self.__image_game_over]
            gravedad = self.gravity_force(movement_in_y)
            self.__rect.y -= gravedad
            self.rect_collision.y -= self.__rect.y+ 50 
            
        return game_over

    def draw(self, screen):
        #animacion actual
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame]
        #posicion actual de la imagen
        #Limite de la pantalla
        # self.__rect.y = min(self.__rect.y, ALTO_VENTANA - self.__actual_image_animation.get_height()) 
        #dibujamos el cuadrado rectangulo de colisón de la animación del personaje.
        # pg.draw.rect(screen, (255, 0, 0), self.__rect, 2)

        #Dibujamos el rectangulo de colisón
        pg.draw.rect(screen, (255, 255, 255), self.rect_collision) 
        #bliteamos imagen actual
        screen.blit(self.__actual_image_animation, self.__rect) 
       
    def control_platform_collisions(self,world, movement_in_y, movement_in_x):
       
        for tile in world.tile_list:
                if  tile[1].colliderect(self.rect_collision.x + movement_in_x, self.rect_collision.y , self.__widht, self.__height):
                    movement_in_x = 0
                    movement_in_y = movement_in_y
                if  tile[1].colliderect(self.rect_collision.x, self.rect_collision.y + movement_in_y, self.__widht, self.__height):
                    if DEBUG_COLLISION:
                        print("Colisiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiooooooooooooooooooooooooonnnnnnnnnnnnnnnnnn")
                        print(f"MOVEMENT IN Y: {movement_in_y}")
                    if movement_in_y <= 0: #subiendoaaa
                        if DEBUG_COLLISION:
                            print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                        movement_in_y = tile[1].bottom - self.rect_collision.top
                        # movement_in_x = 0
                        # self.__vel_y = 0
                        self.__on_platform = False
                        self.__is_jumping = True
                    if movement_in_y > 0: #bajando
                        if DEBUG_COLLISION:
                            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    #     print(f"{movement_in_y}")
                        movement_in_y = tile[1].top - self.rect_collision.bottom
                    #     print(f"{movement_in_y}")
                        # movement_in_x = 0
                        # self.__vel_y = 0
                        self.__on_platform = True
                        self.__is_jumping = False
                        
        return movement_in_y, movement_in_x
    
    def restart_position(self):
        self.__rect.x = 50
        self.__rect.y = 630
        self.rect_collision.x = self.__rect.x
        self.rect_collision.y = self.__rect.y
  
                   
            

            
    def update(self,key_get_pressed, delta_ms,screen, world, trap_list, bullet_list, game_over):
        #DRAW PLAYER
        self.draw(screen)
        self.draw_player_lives(screen)
        self.draw_score(screen)
        go = self.check_player_alive()
        self.movement_control(key_get_pressed, delta_ms, world, trap_list, bullet_list, go)
        #UPDATE PLAYER COORDINATES
        #ANIMATION
        self.do_animation(delta_ms)
        if DEBUG:
            print(f"X = {self.__rect.x}, Y = {self.__rect.y}")
            print(f"is jumping?: {self.__is_jumping}")
            print(f"on ground?: {self.__on_ground}")
            print(f"is on platform?: {self.__on_platform}")
            print(f"is looking right?: {self.__is_looking_right}")
        return go

    def draw_player_lives(self, screen):
        font = pg.font.Font(None, 36)
        lives_text = font.render(f"Lives: {self.current_lifes}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))
    
    def draw_score(self, screen):
        font = pg.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 50))

    def restart(self):
        self.__rect.x =50
        self.__rect.y = 630   
        self.rect_collision.x = self.__rect.x
        self.rect_collision.y = self.__rect.y