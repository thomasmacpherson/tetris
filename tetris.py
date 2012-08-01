#tetris


bg_image = "background.png"




import pygame, time, sys, threading, random
import piface.pfio as pfio

from pygame.locals import *


class Block(object):
	global block_colours
	def __init__(self, x, y, colour):
		"""set up stuff"""
		self.x = x
		self.y = y
		self.colour = colour
	
	def draw(self):
		"""draws the block"""
		
		screen.blit(block_colours[self.colour],(self.x,self.y))





               
shape_index = [  
	       [       
	          [ [0,32,64,32],[-32,-32,-32,0] ],
	          [ [32,32,64,32],[-64,-32,-32,0] ],
	          [ [32,0,32,64],[-32,0,0,0] ],
	          [ [64,32,64,64],[-64,-32,-32,0] ]
	        ],
	        
	       [
	       	  [ [0,0,32,32],[0,-32,32,0] ],
	       	  [ [0,0,32,32],[0,-32,32,0] ],
	       	  [ [0,0,32,32],[0,-32,32,0] ],
	       	  [ [0,0,32,32],[0,-32,32,0] ],
	       ],
	        
	       [
	       	  [ [0,32,64,0],[-32,-32,-32,0] ],
	       	  [ [32,32,32,64],[-64,-32,0,0] ],
	       	  [ [64,0,32,64],[-32,0,0,0] ],
	       	  [ [0,32,32,32],[-64,-64,-32,0] ]
	       ],
	       
	       [
	       	  [ [0,32,64,64],[-32,-32,-32,0] ],
	       	  [ [32,64,32,32],[-64,-64,-32,0] ],
	       	  [ [0,0,32,64],[-32,0,0,0] ],
	       	  [ [32,32,0,32],[-64,-32,0,0] ]
	       ],
	       
	       [
	       	  [ [0,32,32,64],[-32,-32,0,0] ],
	       	  [ [32,0,32,0],[-64,-32,-32,0] ],
	       	  [ [0,32,32,64],[-32,-32,0,0] ],
	       	  [ [32,0,32,0],[-64,-32,-32,0] ] 
	       ],

	       [
	       	  [ [0,32,64,96],[0,0,0,0] ],
	       	  [ [32,32,32,32],[-96,-64,-32,0] ],
	       	  [ [0,32,64,96],[0,0,0,0] ],
	       	  [ [32,32,32,32],[-96,-64,-32,0] ] 
	       ],
	       
	       [
	       	  [ [32,64,0,32],[-32,-32,0,0] ],
	       	  [ [0,0,32,32],[-64,-32,-32,0] ],
	       	  [ [32,64,0,32],[-32,-32,0,0] ],
	       	  [ [0,0,32,32],[-64,-32,-32,0] ]
	       ]
	     ]


class Shape(object):
	global shape_index
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		rot = 0
		self.rot = rot
		self.shape = shape

		
		self.blocks = [
			Block(x+shape_index[shape][rot][0][0],y+shape_index[shape][rot][1][0],shape),
			Block(x+shape_index[shape][rot][0][1],y+shape_index[shape][rot][1][1],shape),
			Block(x+shape_index[shape][rot][0][2],y+shape_index[shape][rot][1][2],shape),
			Block(x+shape_index[shape][rot][0][3],y+shape_index[shape][rot][1][3],shape)]



	def move(self, x, y):
		self.x += x
		self.y += y
		for block in self.blocks:
			block.x += x
			block.y += y

		if check_collision():
			for block in self.blocks:
				block.x -= x
				block.y -= y
			if y != 0:
				new_shape()


	def draw(self):
		for block in self.blocks:
			block.draw()	

	def delete(self):
		global y_count
		for block in self.blocks:
			y_count[(block.y-626)/32] +=1
			print (block.y-626)/32
			print y_count
			dead_block_list.append(block)
		check_lines()
		del(self)
	
	def rotate(self):
		self.rot +=1
		if self.rot > 3:
			self.rot = 0

		self.blocks[0].x += shape_index[self.shape][self.rot][0][0]
		self.blocks[0].y += shape_index[self.shape][self.rot][1][0]
		self.blocks[0].x += shape_index[self.shape][self.rot][0][1]
		self.blocks[0].y += shape_index[self.shape][self.rot][1][1]
		self.blocks[0].x += shape_index[self.shape][self.rot][0][2]
		self.blocks[0].y += shape_index[self.shape][self.rot][1][2]
		self.blocks[0].x += shape_index[self.shape][self.rot][0][3]
		self.blocks[0].y += shape_index[self.shape][self.rot][1][3]



def new_shape():
	global active_block
	global next_shape
	global next_shape_number
	for block in active_block.blocks:
		pass

	active_block.delete()
	active_block = Shape(510,82,next_shape_number)
	next_shape_number = random.randint(0,6)
	next_shape = Shape(950, 215, next_shape_number)



def check_collision():
	for block in active_block.blocks:
		for dead_block in dead_block_list:
			if block.x == dead_block.x and block.y == dead_block.y:
				return True



def check_lines():
	global dead_block_list
	check_list = list()

	for block in dead_block_list[-4:]: # check last 4 blocks of list
		if block.y not in clear_list:
			clear_list.append(block.y)

	for y in clear_list:
		check_line((y - 594)/32)



def check_line(line_number):
	global dead_block_list
	if y_count[line_number] > 9:
		for block in dead_block_list:
			if block.y == (line_number * 32)+594:
				dead_block_list.remove(block)
				


dead_block_list = list() # list of deadblocks for displaying and detecting collisions

y_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # list of number of blocks in each y position for full line detection


pygame.init()

screen=pygame.display.set_mode((1000,800),FULLSCREEN)

background = pygame.image.load(bg_image).convert()
brown_block = pygame.image.load("pngs/tetblock1.png").convert()
beige_block = pygame.image.load("pngs/tetblock2.png").convert()
blue_block = pygame.image.load("pngs/tetblock3.png").convert()
red_block = pygame.image.load("pngs/tetblock4.png").convert()
green_block = pygame.image.load("pngs/tetblock5.png").convert()
purple_block = pygame.image.load("pngs/tetblock6.png").convert()
turq_block = pygame.image.load("pngs/tetblock7.png").convert()

block_colours = [brown_block,
				beige_block,
				blue_block,
				red_block,
				green_block,
				turq_block,
				purple_block ]


score = 0

clock = 0
speed = 150

active_block = Shape(510,82, random.randint(0,6))
next_shape_number = random.randint(0,6)
next_shape = Shape(950, 215, next_shape_number)

time.sleep(4)

running = True

while running == True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False

			elif event.key == K_RIGHT and active_block.x <766:
				active_block.move(32,0)

			elif event.key == K_LEFT and active_block.x >510:
				active_block.move(-32,0)

			elif event.key == K_UP:
				active_block.rotate()

			elif event.key == K_DOWN:
				if active_block.y < 594:
					active_block.move(0,32)
			
	screen.blit(background, (350,50))
	#screen.blit(g_block,(510,594))
	if clock % speed == 2:
		if active_block.y < 594:
			active_block.move(0,32)
		else:
			new_shape()

	active_block.draw()
	next_shape.draw()
	
	for block in dead_block_list:
		block.draw()
	

	pygame.display.update()
	clock +=1
	
	

exit()

