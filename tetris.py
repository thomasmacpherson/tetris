#tetris

from shapes import *
from math import log10
import socket

REMOTE_UDP_IP="10.0.0.203"
REMOTE_UDP_PORT = 4052

RECIEVING_UDP_IP ="10.0.0.209"
RECIEVING_UDP_PORT = 5005


scr_pos_x = -200
scr_pos_y = 0
in_play = True

import pygame, time, sys, threading, random
import piface.pfio as pfio
pfio.init()

from pygame.locals import *
pygame.init()
font = pygame.font.Font(None, 60)
big_font = pygame.font.Font(None, 400)
data = 4
addr = 0


sock2 = socket.socket(socket.AF_INET,
			socket.SOCK_DGRAM)
sock2.bind((RECIEVING_UDP_IP,RECIEVING_UDP_PORT))



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
	global shadow_block
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.absolutex = x
		self.absolutey = y
		rot = 0
		self.rot = rot
		self.shape = shape

		if shape == 7:
			self.blocks = [
				Block(x+shape_index[active_block.shape][rot][0][0],y+shape_index[active_block.shape][rot][1][0],shape),
				Block(x+shape_index[active_block.shape][rot][0][1],y+shape_index[active_block.shape][rot][1][1],shape),
				Block(x+shape_index[active_block.shape][rot][0][2],y+shape_index[active_block.shape][rot][1][2],shape),
				Block(x+shape_index[active_block.shape][rot][0][3],y+shape_index[active_block.shape][rot][1][3],shape)]
		else:
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


		if check_collision(self):
			for block in self.blocks:
				block.x -= x
				block.y -= y

			if y != 0:
				return True # new shape needed
			#	new_shape()
		else:
			return False
	
	def position(self):
		self.x = active_block.x
		self.y = active_block.y
		self.rot = active_block.rot
		for i, block in enumerate(self.blocks):
			block.x = active_block.blocks[i].x
			block.y = active_block.blocks[i].y

	def draw(self):
		for block in self.blocks:
			block.draw()	

	def delete(self):
		global y_count

		for block in self.blocks:
			line_number = (block.y-626)/32
			
			if line_number < -18:
				game_over()

			else:
				y_count[line_number] +=1
				dead_block_list.append(block)
		check_lines()
		del(self)
	
	def rotate(self):
		global active_block
		previous_rot = self.rot
		self.rot +=1
		if self.rot > 3:
			self.rot = 0

		for i, block in enumerate(self.blocks):
			temp_blocks = [ [self.blocks[0].x,self.blocks[0].y],
					[self.blocks[1].x,self.blocks[1].y],
					[self.blocks[2].x,self.blocks[2].y],
					[self.blocks[3].x,self.blocks[3].y] ]


		self.blocks[0].x = active_block.x + shape_index[active_block.shape][active_block.rot][0][0]
		self.blocks[0].y = active_block.y + shape_index[active_block.shape][active_block.rot][1][0]
		self.blocks[1].x = active_block.x + shape_index[active_block.shape][active_block.rot][0][1]
		self.blocks[1].y = active_block.y + shape_index[active_block.shape][active_block.rot][1][1]
		self.blocks[2].x = active_block.x + shape_index[active_block.shape][active_block.rot][0][2]
		self.blocks[2].y = active_block.y + shape_index[active_block.shape][active_block.rot][1][2]
		self.blocks[3].x = active_block.x + shape_index[active_block.shape][active_block.rot][0][3]
		self.blocks[3].y = active_block.y + shape_index[active_block.shape][active_block.rot][1][3]

		if check_collision(self):

			self.rot = previous_rot
			for i, block in enumerate(self.blocks):
				self.blocks[i].x = temp_blocks[i][0]
				self.blocks[i].y = temp_blocks[i][1]

def new_shape():
	global active_block
	global next_shape
	global shadow_block
	global next_shape_number
	for block in active_block.blocks:
		pass

	active_block.delete()
	active_block = Shape(scr_pos_x + 606,scr_pos_y + 18,next_shape_number)
	shadow_block = Shape(scr_pos_x + 606, scr_pos_y + 18, 7)
	next_shape_number = random.randint(0,6)
	
	while next_shape_number == active_block.shape:	# don't get the same block twice in a row
		next_shape_number = random.randint(0,6)

	if next_shape_number == 5:	# next shape box adjustment for line piece
		next_shape = Shape(scr_pos_x + 916, scr_pos_y + 232, next_shape_number)
	elif next_shape_number == 1:	# next shape box adjustment for square blocks
		next_shape = Shape(scr_pos_x + 950, scr_pos_y + 253, next_shape_number)
	else:
		next_shape = Shape(scr_pos_x + 933, scr_pos_y + 253, next_shape_number)

	for x in range(1,20):
		if shadow_block.y < (scr_pos_y + 594):
			if shadow_block.move(0,32):
				break

def check_collision(shape):
	for block in shape.blocks:
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
	removed_line_count = 0
	removed_list = list()
	for y in check_list:
		if check_line((y+(32*removed_line_count) - 18)/32):
			removed_list
			removed_line_count += 1
	if removed_line_count > 1:
		send_message(str(removed_line_count-1))

def check_line(line_number):

	global dead_block_list

	global score
	global level
	global lines
	global y_count


	if y_count[line_number] > 9:

		lines += 1
		score += level*10
		
		if lines %10 == 0:
			level += 1
		for block in dead_block_list:
			if block.y == (line_number*32)+18:
				block.colour +=8 
		draw_screen(False)
		time.sleep(0.1)

		dead_block_list = [block for block in dead_block_list if block.y != (line_number * 32)+18]

		for i in reversed(range(1,line_number+1)):
			y_count[i] = y_count[i-1]

			
		for block in dead_block_list:		
			if block.y < (line_number*32)+18:
				block.y += 32
		y_count[0] = 0
		
		return True
	else:
		return False



def add_lines(number_of_lines):
	global shadow
	for i in range(0,19-number_of_lines):
		print i
		y_count[i] = y_count[i+number_of_lines]

	for block in dead_block_list:
		block.y -= 32*number_of_lines

	for i in range(19-number_of_lines,19):
		y_count[i] = 0
		for j in range(1,11):
			dead_block_list.append(Block(j*32+278,i*32+18,15)) # draw in lines

	shadow_block.position()
	for x in range(1,20):
		if shadow_block.y < (scr_pos_y + 594):
			if shadow_block.move(0,32):
				break
	draw_screen(shadow)


	


def draw_screen(shadow):
	global in_play
	#global next_shape_help
	screen.blit(background, (scr_pos_x + 335,scr_pos_y + 49))

	screen.blit(background_images[level % len(background_images) ], (scr_pos_x + 510, scr_pos_y +49))

	if shadow:
		shadow_block.draw()
	active_block.draw()

	if next_shape_help:
		next_shape.draw()

	
	for block in dead_block_list:
		block.draw()
	
	display_score = font.render(str(score), 1, (0,0,0))
	display_lines = font.render(str(lines), 1, (0,0,0))
	display_level = font.render(str(level), 1, (0,0,0))
	#+(10*int(log10(score)))
	
	screen.blit(display_score, (880 + scr_pos_x, 358 + scr_pos_y))
	screen.blit(display_level, (880 + scr_pos_x, 454 + scr_pos_y))
	screen.blit(display_lines, (880 + scr_pos_x, 549 + scr_pos_y))

	if not in_play:
		display_game = big_font.render((" GAME"), 1, (150,0,0))
		display_over = big_font.render((" OVER!"), 1, (150,0,0))
		screen.blit(display_game, (200 + scr_pos_x, 60 + scr_pos_y))
		screen.blit(display_over, (200 + scr_pos_x, 360 + scr_pos_y))

	draw_black_box()

	pygame.display.update()

def draw_flashing_lines(line_list):
	pass


def draw_black_box():
	pygame.draw.rect(screen,(0,0,0), (scr_pos_x +450, scr_pos_y-50,1000,100),0)


def game_over():
	global score
	global in_play
	print "Your score was %d" %score
	#send_message("You win")
	in_play = False
	draw_screen(True)
	exit()

def move_right():
	active_block.move(32,0)
	shadow_block.position()
	for x in range(1,20):
		if shadow_block.y < (scr_pos_y + 594):
			if shadow_block.move(0,32):
				break

def move_left():	
	active_block.move(-32,0)
	shadow_block.position()
	for x in range(1,20):
		if shadow_block.y < (scr_pos_y + 594):
			if shadow_block.move(0,32):
				break

def rotate_piece():
	active_block.rotate()
	shadow_block.position()
	for x in range(1,20):
		if shadow_block.y < (scr_pos_y + 594):
			if shadow_block.move(0,32):
				break

def move_down():
	if active_block.y < 594:
		if active_block.move(0,32):
			new_shape()

def drop_down():
	for x in range(1,19):
		if active_block.y < (scr_pos_y + 594):
			if active_block.move(0,32):
				break

def send_message(message):
	global REMOTE_UDP_IP
	global REMOTE_UDP_PORT
	global sock
	MESSAGE= message

	#print "UDP target IP:", REMOTE_UDP_IP
	#print "UDP target port:", REMOTE_UDP_PORT
	print "message sent:", MESSAGE

	sock = socket.socket(socket.AF_INET,
			     socket.SOCK_DGRAM)
	sock.sendto(MESSAGE, (REMOTE_UDP_IP, REMOTE_UDP_PORT))


def listener():
	global data
	global addr
	global sock2
	while True:
		data, addr = sock2.recvfrom(1024)
		print "Lines received %s", data




dead_block_list = list() # list of deadblocks for displaying and detecting collisions

y_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # list of number of blocks in each y position for full line detection

pygame.init()

screen=pygame.display.set_mode((1000,800))

background = pygame.image.load("pngs/tetbackground.png").convert()

brown_block = pygame.image.load("pngs/tetblock1.png").convert()
beige_block = pygame.image.load("pngs/tetblock2.png").convert()
blue_block = pygame.image.load("pngs/tetblock3.png").convert()
red_block = pygame.image.load("pngs/tetblock4.png").convert()
green_block = pygame.image.load("pngs/tetblock5.png").convert()
purple_block = pygame.image.load("pngs/tetblock6.png").convert()
turq_block = pygame.image.load("pngs/tetblock7.png").convert()
clear_block = pygame.image.load("pngs/tetblockclear.png")	# not converted to keep png transparency
dead_brown_block = pygame.image.load("pngs/tetblock1dead.png").convert()
dead_beige_block = pygame.image.load("pngs/tetblock2dead.png").convert()
dead_blue_block = pygame.image.load("pngs/tetblock3dead.png").convert()
dead_red_block = pygame.image.load("pngs/tetblock4dead.png").convert()
dead_green_block = pygame.image.load("pngs/tetblock5dead.png").convert()
dead_purple_block = pygame.image.load("pngs/tetblock6dead.png").convert()
dead_turq_block = pygame.image.load("pngs/tetblock7dead.png").convert()
net_block = pygame.image.load("pngs/tetnetblock.png").convert() # 15

image1 = pygame.image.load("pngs/sacktetris.png").convert()
image2 = pygame.image.load("pngs/placetetris.png").convert()
image3 = pygame.image.load("pngs/oaktetris.png").convert()

block_colours = [brown_block,
		beige_block,
		blue_block,
		red_block,
		green_block,
		turq_block,
		purple_block,
		clear_block,
		dead_brown_block,
		dead_beige_block,
		dead_blue_block,
		dead_red_block,
		dead_green_block,
		dead_turq_block,
		dead_purple_block
		net_block]

background_images = [ 	image1,
			image2,
			image3 ]
score = 0
lines = 0
level = 1

clock = 0
speed = 15.0

shadow = True
next_shape_help = True

active_block = Shape(scr_pos_x + 606,scr_pos_y + 82, random.randint(0,6))

shadow_block = Shape(scr_pos_x + 606,scr_pos_y + 82, 7)


for x in range(1,20):
	if shadow_block.y < (scr_pos_y + 594):
		if shadow_block.move(0,32):
			break

next_shape_number = random.randint(0,6)

while next_shape_number == active_block.shape:
	next_shape_number = random.randint(0,6)

if next_shape_number == 5:	# next shape box adjustment for line piece
	next_shape = Shape(scr_pos_x + 916, scr_pos_y + 232, next_shape_number)
elif next_shape_number == 1:	# next shape box adjustment for square blocks
	next_shape = Shape(scr_pos_x + 950, scr_pos_y + 253, next_shape_number)
else:
	next_shape = Shape(scr_pos_x + 933, scr_pos_y + 253, next_shape_number)


time.sleep(2)

running = True

keyboard = True

t = threading.Thread(target=listener)
t.start()


while running == True:
	if data != 4:
		add_lines(int(data))
		data = 4
		
	if keyboard == True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False

				elif event.key == K_p:
					keyboard = False

				elif event.key == K_RIGHT:# and active_block.x <766:
					move_right()

				elif event.key == K_LEFT:# and active_block.x >510:
					move_left()

				elif event.key == K_UP:
					rotate_piece()
				elif event.key == K_DOWN:
					move_down()
				elif event.key == K_SPACE:
					drop_down()
					new_shape()
				elif event.key == K_s:
					shadow = not shadow

				elif event.key == K_h:
					next_shape_help = not next_shape_help
	else:
		if clock % 5 == 1:
			if pfio.digital_read(7):
				shadow = not shadow
		if clock % 3 == 1:

			if pfio.digital_read(5):
				drop_down()
			elif pfio.digital_read(3):
				rotate_piece()
		else:
			if pfio.digital_read(1):
				move_left()
			elif pfio.digital_read(2):
				move_right()


			if pfio.digital_read(4):
				move_down()

		if pfio.digital_read(6):
			keyboard = True

	current_speed = speed/level
	if current_speed < 3:
		current_speed = 3
	if clock % (current_speed) == 1:
		if active_block.y < 594:
			if active_block.move(0,32):
				new_shape()
		else:
			new_shape()
	draw_screen(shadow)
	clock +=1
exit()

