#tetris


bg_image = "background.png"
brown_block = "tetblock1.png"
beige_block = "tetblock2.png"
blue_block = "tetblock3.png"
red_block = "tetblock4.png"
green_block = "tetblock5.png"
turq_block = "tetblock7.png"

import pygame, time, sys, threading, random
import piface.pfio as pfio

from pygame import.locals import *

pygame.init()
screen=pygame.display.set_mode((),FULLSCREEN)

background = pygame.image.load(bg_image).convert()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
			
	screen.blit(background, (0,0))
	
	pygame.display.update()
	
	


