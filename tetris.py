#tetris

from shapes import *
bg_image = "background.png"


scr_pos_x = -200
scr_pos_y = 0

import pygame, time, sys, threading, random
#import piface.pfio as pfio

from pygame.locals import *
pygame.init()
font = pygame.font.Font(None, 60)


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
class Shape(object):
	global shape_index
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.absolutex = x
		self.absolutey = y
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
		self.absolutex =self.x
		self.absolutey = self.y


		for block in self.blocks:
			block.x += x
			block.y += y

		if check_collision():
			for block in self.blocks:
				block.x -= x
				block.y -= y
			if y != 0:
				return True # new shape needed
			#	new_shape()


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
		previous_rot = self.rot
		self.rot +=1
		if self.rot > 3:
			self.rot = 0

		for i, block in enumerate(self.blocks):
			temp_blocks = [ [self.blocks[0].x,self.blocks[0].y],
					[self.blocks[1].x,self.blocks[1].y],
					[self.blocks[2].x,self.blocks[2].y],
					[self.blocks[3].x,self.blocks[3].y] ]


		self.blocks[0].x = self.x + shape_index[self.shape][self.rot][0][0]
		self.blocks[0].y = self.y + shape_index[self.shape][self.rot][1][0]
		self.blocks[1].x = self.x + shape_index[self.shape][self.rot][0][1]
		self.blocks[1].y = self.y + shape_index[self.shape][self.rot][1][1]
		self.blocks[2].x = self.x + shape_index[self.shape][self.rot][0][2]
		self.blocks[2].y = self.y + shape_index[self.shape][self.rot][1][2]
		self.blocks[3].x = self.x + shape_index[self.shape][self.rot][0][3]
		self.blocks[3].y = self.y + shape_index[self.shape][self.rot][1][3]

		if check_collision():
			print "Rotation collision"
			self.rot = previous_rot
			for i, block in enumerate(self.blocks):
				self.blocks[i].x = temp_blocks[i][0]
				self.blocks[i].y = temp_blocks[i][1]






def new_shape():
	global active_block
	global next_shape
	global next_shape_number
	for block in active_block.blocks:
		pass

	active_block.delete()
	active_block = Shape(scr_pos_x + 606,scr_pos_y + 18,next_shape_number)
	next_shape_number = random.randint(0,6)
	
	while next_shape_number == active_block.shape:	# don't get the same block twice in a row
		next_shape_number = random.randint(0,6)

	if next_shape_number == 5:	# next shape box adjustment for line piece
		next_shape = Shape(scr_pos_x + 926, scr_pos_y + 192, next_shape_number)
	else:
		next_shape = Shape(scr_pos_x + 950, scr_pos_y + 215, next_shape_number)


def check_collision():
	for block in active_block.blocks:
		if block.x > (scr_pos_x + 798) or block.x < (scr_pos_x + 510):
			return True
		for dead_block in dead_block_list:
			if block.x == dead_block.x and block.y == dead_block.y:
				return True



def check_lines():
	global dead_block_list
	global y_count
	check_list = list()

	for block in dead_block_list[-4:]: # check last 4 blocks of list
		if block.y not in check_list:
			check_list.append(block.y)
	check_list.sort()
	check_list.reverse()
	print check_list
	removed_line_count = 0

	for y in check_list:
		if check_line((y+(32*removed_line_count) - 82)/32):
			removed_line_count += 1

	print "Removed line count: %d" %removed_line_count


def check_line(line_number):
	print line_number
	global dead_block_list

	global score
	global level
	global lines
	global y_count

	print "Line number: %d" %line_number
	if y_count[line_number] > 9:
		#y_count[line_number] = 0
		lines += 1
		score += level*10
		
		if lines %10 == 0:
			level += 1

		dead_block_list = [block for block in dead_block_list if block.y != (line_number * 32)+82]

		for i in reversed(range(1,line_number+1)):
			y_count[i] = y_count[i-1]

			
		for block in dead_block_list:		
			if block.y < (line_number*32)+82:
				block.y += 32
		y_count[0] = 0
		
		return True

	else:
		return False






"""
		for block in dead_block_list:
			if block.y == (line_number * 32)+82:
				dead_block_list.remove(block)
"""				







def draw_black_box():
	pygame.draw.rect(screen,(0,0,0), (scr_pos_x +450, scr_pos_y-50,600,100),0)


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
lines = 0
level = 1

clock = 0
speed = 15

active_block = Shape(scr_pos_x + 606,scr_pos_y + 82, random.randint(0,6))
next_shape_number = random.randint(0,6)

while next_shape_number == active_block.shape:
	next_shape_number = random.randint(0,6)

if next_shape_number == 5:
	next_shape = Shape(scr_pos_x + 926, scr_pos_y + 192, next_shape_number)
else:
	next_shape = Shape(scr_pos_x + 950, scr_pos_y + 215, next_shape_number)
time.sleep(2)

running = True

while running == True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False

			elif event.key == K_RIGHT:# and active_block.x <766:
				active_block.move(32,0)

			elif event.key == K_LEFT:# and active_block.x >510:
				active_block.move(-32,0)

			elif event.key == K_UP:
				active_block.rotate()

			elif event.key == K_DOWN:
				if active_block.y < 594:
					if active_block.move(0,32):
						new_shape()

			elif event.key == K_SPACE:
				for x in range(1,17):
					if active_block.y < (scr_pos_y + 594):
						if active_block.move(0,32):
							break
				new_shape()


	screen.blit(background, (scr_pos_x + 350,scr_pos_y + 50))

	if clock % (speed/level) == 2:
		if active_block.y < 594:
			if active_block.move(0,32):
				new_shape()
		else:
			new_shape()

	active_block.draw()
	next_shape.draw()
	
	for block in dead_block_list:
		block.draw()
	
	display_score = font.render(str(score), 1, (0,0,0))
	display_lines = font.render(str(lines), 1, (0,0,0))
	display_level = font.render(str(level), 1, (0,0,0))

	screen.blit(display_score, (1030 + scr_pos_x, 358 + scr_pos_y))
	screen.blit(display_level, (1030 + scr_pos_x, 456 + scr_pos_y))
	screen.blit(display_lines, (1030 + scr_pos_x, 550 + scr_pos_y))

	draw_black_box()
	pygame.display.update()
	clock +=1


exit()

