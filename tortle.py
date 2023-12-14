from models.constantes import  DEBUG, DEBUG_ENEMY, FPS
import pygame as pg
from models.auxiliar import SurfaceManager as sf
class Turtle(pg.sprite.Sprite):
	def __init__(self, coordenada_x, coordenada_y, speed_walk, group):
		pg.sprite.Sprite.__init__(self)
		self.__walk_r = sf.get_surface_from_sprisheet("assets\img\enemies\Walk\Walk.png", 8, 1)
		self.__walk_l = sf.get_surface_from_sprisheet("assets\img\enemies\Walk\Walk.png", 8, 1, flip=True)
		self.__stay_r = sf.get_surface_from_sprisheet("assets\img\enemies\Stay\Idle.png", 6, 1)
		self.__stay_l = sf.get_surface_from_sprisheet("assets\img\enemies\Stay\Idle.png", 6, 1, flip=True)
		self.__atack_r = sf.get_surface_from_sprisheet("assets\img\enemies\Atack\Shot_1.png", 8, 1)
		self.__atack_l = sf.get_surface_from_sprisheet("assets\img\enemies\Atack\Shot_1.png", 14, 1, flip=True)
		self.__dead_r = sf.get_surface_from_sprisheet("assets\img\enemies\Dead\Dead.png", 3, 1)
		self.__dead_l = sf.get_surface_from_sprisheet("assets\img\enemies\Dead\Dead.png", 3, 1, flip=True)
		self.__is_looking_right = True
		self.__on_platform = False
		self.__is_jumping = True
		self.__is_fall = False
		self.stop = True
		self.__speed_walk = speed_walk
		self.__actual_animation = self.__stay_r

		######################
		## SPAWN
		######################
		self.enemy_spawn_timer = 0
		self.enemy_spawn_interval = 5
		self.enemies_killed = 0
		#######################
		##IMAGES
		########################
		self.image1 = pg.image.load('assets\img\\title\\tortle.png')
		self.__initial_frame = 0
		self.image = pg.image.load('assets\img\\title\\tortle.png')
		self.rect = self.image.get_rect()
		self.group = group
		#######################
        ##Positions
        ######################
		self.rect.x = coordenada_x
		self.rect.y = coordenada_y
		self.__vel_y = 0
		self.__move_x = 0
		self.__gravity = 1
		self.__count = 0
		self.__animation = self.__stay_r
		self.__widht = 10
		self.__height = 80
		self.rect_collision = pg.Rect(coordenada_x, coordenada_y, self.__widht,self.__height)

	def update(self, screen, world, player):
		self.control_movement_y(world)
		self.control_movement_x(world)
		self.detect_collisions(player)
		self.enemy_spawn()
		self.draw(screen)
		

	def enemy_spawn(self):
			self.enemy_spawn_timer += 1 / FPS
			if self.enemy_spawn_timer >= self.enemy_spawn_interval:
				self.enemies_generator()
				self.enemy_spawn_timer = 0 
			
		
		
		
	def enemies_generator(self, ):
		new_enemy = Turtle(300	,300,1, self.group)
		if DEBUG_ENEMY:
			print("ENEMIGO GENERADOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
		self.group.add(new_enemy)	

	def control_movement_y(self, world):
		movement_in_y = 0
		if self.detect_platform_falling(world):
			gravity = 0
		else:
			gravity = self.gravity_force()
		movement_in_y += gravity
		self.rect.y += movement_in_y
		self.rect.y += 0

	def detect_platform_falling(self, world):
		if DEBUG_ENEMY:
			print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
		for tiles in world.tile_list:
			if self.rect.colliderect(tiles[1]):
				if self.rect.bottom > tiles[1].top and self.rect.top < tiles[1].top:
                
                
					if DEBUG_ENEMY:
						print("8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888")
					return True
				 # Si colisiona por los costados, aplicar gravedad
		return False
	def detect_collision_walking(self, world):
		for tiles in world.tile_list:
			if self.rect.colliderect(tiles[1]):
				if self.rect.right > tiles[1].left and self.rect.left < tiles[1].right:
					# Cambiar la dirección del movimiento
					self.__speed_walk *= -1
					self.rect.x += 0
					
					return True
		return False
		
	def detect_collisions(self, player):
		if DEBUG_ENEMY:
			pass# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		if self.rect.colliderect(player.rect_collision):
			self.kill()
			if player.current_lifes > 0:
				player.current_lifes -= 1
				player.score +=100
				if player.current_lifes >1:
					player.restart_position()
			

	def gravity_force(self):
		gravity = 0
		self.__vel_y +=1
		if self.__vel_y > 10:
			self.__vel_y = 10
		gravity += self.__vel_y
		return gravity

	
	def control_movement_x(self, world):
		if self.stop:
		# Detectar colisiones antes de aplicar el movimiento
			if self.detect_collision_walking(world):
				self.__speed_walk *= -1
			# Resto del código para controlar el movimiento lateral
			if 0 <= self.__count <= 50:
				self.__move_x = -self.__speed_walk
				self.__animation = self.__walk_l
				self.__is_looking_right = False
				self.__count += 1
			elif 50 < self.__count <= 100:
				self.__move_x = self.__speed_walk
				self.__animation = self.__walk_r
				self.__is_looking_right = True
				self.__count += 1
			else:
				self.__count = 0
			self.rect.x += self.__move_x
			gravity = self.gravity_force()
		
	
	# 	movement_in_y = 0
		
	# 	self.__vel_y +=1
	# 	if self.__vel_y >10:
	# 		self.__vel_y = 10
	# 	movement_in_y += self.__vel_y
	# 	self.rect.y += self.__vel_y
	# 	return movement_in_y		
		
		
	def draw(self, screen):
		if DEBUG:
			print(f"Posicion de enemigo en x{self.rect_collision.x} Posicion de enemigo en y {self.rect_collision.y}")
			pg.draw.rect(screen, (0,0,0), self.rect, 2)
		screen.blit(self.image, self.rect)
	
	  
