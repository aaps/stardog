#music.py

import pygame
from pygame.locals import *

pygame.mixer.pre_init(frequency = 44100, buffer = 1024 * 8)
pygame.init()
display =  pygame.display.set_mode((600,400))
running = True
alert = False
pygame.mixer.music.load('music simple.ogg')
pygame.mixer.music.play(-1, 30)
pos = 0
while(running):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.MOUSEBUTTONDOWN:
			alert = not alert
			if alert:
				pos = ((pos + pygame.mixer.music.get_pos()) % 98716)
				pygame.mixer.music.stop()
				pygame.mixer.music.load('music alert.ogg')
				pygame.mixer.music.play(-1, pos / 1000.)
			else: 
				pos = ((pos + pygame.mixer.music.get_pos()) % 98716)
				pygame.mixer.music.stop()
				pygame.mixer.music.load('music simple.ogg')
				pygame.mixer.music.play(-1, pos / 1000.)
			print pos
				