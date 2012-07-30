#space invaders using pygame
#because everyone loves a classic
#also its not going to take a week and a half
#
#

import pygame , time, threading , sys, random
import piface.pfio as pfio

from pygame.locals import * 

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (250,250,0)
black = 0, 0, 0
white = (255,255,255)


class user_input(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#set class variables here		
	def run(self):
		global player
		global running
		global laser_list
		global green
		pfio.init()
		tick = 0
		while running:
			try:
				x = pfio.read_input()
				if x >= 8 :
					x=0
				if tick + 0.8 < time.time():
					#FIRE!!!!!!
					if x - 4 >= 0:
						x = x-4
						newlaser = laser_sprite(4,10,1, green)
						newlaser.rect.x = 28 + player.rect.x # laser is 4 wide player is 60; 60 /2 + 4 /2 = 28
						newlaser.rect.y =  player.rect.y
						laser_list.add(newlaser)		
					tick = time.time()
				# go right
				if x - 2 >= 0:
					x = x-2
					player.rect.x += 2
				#go left
				if x - 1 >= 0:
					player.rect.x -= 2
			except:
				pass
		pfio.deinit()
#to do seperate player movment from alien movment cause currently its lazy


class update_lasers(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#set class variables here		
	def run(self):
		global alien_list
		global running
		global fleet_number
		global laser_list
		global fleet_speed
		global fleet_collums 
		global fleet_rowsg
		global player_list
		global number_of_alien_lasers
		global score
		global fleet_speed_init	
		tock = 0
		while running:
			if  tock + 0.05 < time.time():
				laser_list.update()
				alien_laser_list.update()
				for laser in alien_laser_list:
					for players in player_list:
						if laser.rect.x+4 >= players.rect.x and laser.rect.x <= players.rect.x+60 :
							if laser.rect.y <= players.rect.y + 60  and laser.rect.y +10 >= players.rect.y :
								try:
									alien_laser_list.remove(laser)
									players.image = players.boom
									time.sleep(2)
									running = False
								except:
									print "Exception thrown during sprite removal for player"
					if laser.rect.y > 800:
						try:
							alien_laser_list.remove(laser)
							number_of_alien_lasers -=1
						except:
							pass


				for laser in laser_list:
					for alien in alien_list:
						if laser.rect.x+4 >= alien.rect.x and laser.rect.x <= alien.rect.x+40 and alien.expload == False:
							if laser.rect.y <= alien.rect.y +40 and laser.rect.y+10  >= alien.rect.y:

								alien.expload = True
								score += 10
								fleet_number -=1

								#speed up alien invasion!!!!
								try:
									laser_list.remove(laser)
								except:
									print "Exception thrown during sprite removal for green laser"
									try:
										laser_list.remove(laser)
									except:
										pass



								if fleet_number <= 1:
									fleet_speed = 2.5 * fleet_speed_init
								elif fleet_number < fleet_rows * fleet_collums / 4 :
									fleet_speed = fleet_speed_init * 2
								elif fleet_number < fleet_rows * fleet_collums / 2 :
									fleet_speed = fleet_speed_init * 1.5


					if laser.rect.y < -1:
						try:
							laser_list.remove(laser)
						except:
							pass
						
				tock = time.time()



class update_aliens(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		#set class variables here		
	def run(self):
		global alien_list
		global running
		global fleet_number
		global laser_list
		global fleet_speed
		global red
		global number_of_alien_lasers
		tick = 0


		while running:
			if  tick + 0.1 < time.time():
				#print time.time()
				alien_list.update()

				tick = time.time()
				for bob in alien_list:
					global fleet_direction
					global player

					if bob.rect.y + 40 >= 740:
						player.image = player.boom
						running = False

					far_left = 10
					far_right = 950
	
					if(bob.rect.x >= far_right):
						fleet_direction = -1
					elif(bob.rect.x <= far_left):
						fleet_direction = 1

					if random.random() > 0.3 and number_of_alien_lasers < 15:
						newlaser = laser_sprite(4,10,-1, red)
						newlaser.rect.x = 20 + bob.rect.x
						newlaser.rect.y = 40 + bob.rect.y
						number_of_alien_lasers +=1
						alien_laser_list.add(newlaser)
					
					


class alien(pygame.sprite.Sprite):
	def __init__(self, invader_type, width, height):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		# Create an image of the block, and fill it with a color.
                # This could also be an image loaded from the disk.

		if invader_type == 2:
			self.image = pygame.image.load("spaceinvader.png")
		elif invader_type ==1:
			self.image = pygame.image.load("secondinvader.png")
		elif invader_type ==0:
			self.image = pygame.image.load("thirdinvader.png")

		self.rect = self.image.get_rect()
		self.height = height
		self.last_dir = 1
		self.expload = False
		self.boomtime =0
		self.boom = pygame.image.load("explosion.png")
	def update(self):
		global fleet_direction
		global fleet_descent
		global fleet_speed
		global fleet_number
		global fleet_collums 
		global fleet_rows
		global alien_list
		global score
		accelerated = False

		if self.expload == False  :
			self.rect.x = self.rect.x + fleet_speed * fleet_direction
			if fleet_direction != self.last_dir:
				self.last_dir = fleet_direction
				self.rect.y += fleet_descent
		else:
			if self.boomtime == 0:
				self.boomtime = time.time()
				self.image = self.boom

			if self.boomtime +0.5 < time.time():
				try:
					alien_list.remove(self)

				except:
					pass


class player_sprite(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		# Create an image of the block, and fill it with a color.
                # This could also be an image loaded from the disk.
		self.image = pygame.image.load("rasplayer.png")
		self.boom = pygame.image.load("explosionbig.png")
		self.rect = self.image.get_rect()

	def update(self):
		pass



class laser_sprite(pygame.sprite.Sprite):
	def __init__(self, width, height , up , color ):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		global green
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.up = up
	def update(self):
		self.rect.y -= (10* self.up)









#pygame init
pygame.init()
#define a display area and size
screen = pygame.display.set_mode((1000,800),FULLSCREEN)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

score = 0

if pygame.font:
	font = pygame.font.Font(None, 36)
	string = "Score: ", str(score)

	text = font.render(("Score " + str(score)), 1,(white) )
	textpos = text.get_rect()
	textpos.x = 0 
	textpos.y = 0


#list of sprites to be aliens
alien_list = pygame.sprite.RenderPlain()
player_list = pygame.sprite.RenderPlain()
laser_list = pygame.sprite.RenderPlain()
alien_laser_list = pygame.sprite.RenderPlain()
 


clock = pygame.time.Clock()


#game logic variables
fleet_direction = 1
fleet_speed_init = 15
fleet_speed = fleet_speed_init
fleet_descent = 21
fleet_collums = 9
fleet_rows = 6
fleet_number = fleet_collums * fleet_rows #python can math for me

player_x = 470
player_y = 740

number_of_alien_lasers = 0


#sapwn aliens
y = 20 
color = 0 #
invader_type = 0

for a in range(fleet_rows):
	x = 100
	for b in range(fleet_collums):
		newalien = alien(invader_type, 40, 40)
		newalien.rect.x = x
		newalien.rect.y = y
		alien_list.add(newalien)
		x += 70
		print "spawning alien"
	if a >= 1 :
		invader_type = 1
	if a >= 3 :
		invader_type = 2
	y += 70
	color += 1
	
#spawn the player
player = player_sprite(60,60)
player.rect.x = player_x
player.rect.y = player_y
player_list.add(player)



score = 0
running = True
#render loop


tick = 0

alien_updater = update_aliens()
alien_updater.start()

ui = user_input()
ui.start()

laser_updater = update_lasers()
laser_updater.start()


while running == True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if (event.type == KEYDOWN):
			if (event.key == K_ESCAPE):
				running = False


	text = font.render(("Score " + str(score)), 1,(white) )
	textpos = text.get_rect()
	textpos.x = 0 
	textpos.y = 0
																																																							
	screen.blit(text, textpos)

	screen.fill(black)
	screen.blit(text, textpos)
	alien_list.draw(screen)
	player_list.draw(screen)
	laser_list.draw(screen)
	alien_laser_list.draw(screen)
	pygame.display.update()

	clock.tick(35)




print "Your score was: ", score
exit()
