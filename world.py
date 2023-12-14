from traps import Traps
import pygame as pg
from models.constantes import TILE_SIZES, SCREEN_WIDTH,SCREEN_HEIGTH, DEBUG
from tortle import Turtle
from bee import Bee
from key import Key
class World():
	def __init__(self, data, enemies_list, coins_list, trap_list, key_list):
		self.tile_list = []

		#load images
		dirt_img = pg.image.load('assets\img\\title\\1.png')
		grass_img = pg.image.load('assets\img\\title\\2.png')
		platform_left= pg.image.load('assets\img\\title\\4.png')
		platgorm_right=pg.image.load('assets\img\\title\\5.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pg.transform.scale(dirt_img, (TILE_SIZES, TILE_SIZES))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZES
					img_rect.y = row_count * TILE_SIZES
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pg.transform.scale(grass_img, (TILE_SIZES, TILE_SIZES))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZES
					img_rect.y = row_count * TILE_SIZES
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 4:
					img = pg.transform.scale(platform_left, (TILE_SIZES, TILE_SIZES))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZES
					img_rect.y = row_count * TILE_SIZES
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 5:
					img = pg.transform.scale(platgorm_right, (TILE_SIZES, TILE_SIZES))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZES
					img_rect.y = row_count * TILE_SIZES
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					tortle = Turtle(col_count * TILE_SIZES, row_count * TILE_SIZES -15, 1, enemies_list)
					enemies_list.add(tortle)
				if tile == 7:
					bee = Bee(col_count * TILE_SIZES, row_count * TILE_SIZES -15, 1, enemies_list)
					enemies_list.add(bee)
				if tile == 6:
					trap = Traps(col_count * TILE_SIZES, row_count * TILE_SIZES+ (TILE_SIZES//3))
					trap_list.append(trap)
					# trap_list.append(trap)
				if tile == 8: #Nivel 1
					key = Key(col_count * TILE_SIZES, row_count * TILE_SIZES+ (TILE_SIZES//3))
					key_list.add(key)
				col_count += 1
			row_count += 1
	def draw(self,screen):
		for tile in self.tile_list:
				screen.blit(tile[0], tile[1])
				pg.draw.rect(screen, (0,255,0), tile[1],2)
			
	def draw_grid(self,screen):
		if DEBUG:
			for line in range(0, 20):
				pg.draw.line(screen, (255, 0, 0), (0, line * TILE_SIZES), (SCREEN_WIDTH, line * TILE_SIZES))
				pg.draw.line(screen, (255, 0, 0), (line * TILE_SIZES, 0), (line * TILE_SIZES, SCREEN_WIDTH))	
				
	