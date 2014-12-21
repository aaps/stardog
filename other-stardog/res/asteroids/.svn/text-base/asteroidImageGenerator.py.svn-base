#asteroidImageGenerator.py

import os
import pygame


files = os.listdir(".")
files = [file for file in files if file[-4:] == '.bmp' and file[-5].isdigit()]
files = 'asteroid1.bmp', 'asteroid2-8.bmp','asteroid3.bmp','asteroid5-4.bmp'
colors = [(120,110,100), (240,220,200), (160, 100, 60)]
#colors = [(170,160,150), (250,230,210), (210, 150, 110)] 
colorNames = ['lgry', 'dgry', 'brwn']

pygame.init()

def colorShift(surface, color, colorkey = (0,0,0)):
	"""Converts every pixel with equal red and blue values to a shade of 
	color.  Attempts to maintain value and saturation of surface. 
	Returns a new Surface."""
	s = pygame.Surface(surface.get_size())
	s.set_colorkey(colorkey)
	s.blit(surface, (0,0))
	pa = pygame.PixelArray(s)
	alpha = surface.get_alpha()
	for i in range(len(pa)):
		for j in range(len(pa[i])):
			oldColor = s.unmap_rgb(pa[i][j])
			if oldColor[0] == oldColor[2]: #a shade of magic pink
				newColor = [0, 0, 0, 0]
				for k in [0,1,2]:
					#oldColor[0] = oldColor[2] = main color
					#oldColor[1] = unsaturation
					newColor[k] = int(oldColor[0] * color[k] / 255 \
								+ oldColor[1] * (255 - color[k]) / 255)
				newColor[3] = oldColor[3]
				pa[i][j] = s.map_rgb(tuple(newColor))
	del pa
	return s


for file in files:
	image = pygame.image.load(file)
	for color, name in zip(colors,colorNames):
		pygame.image.save(colorShift(image, color), 'gen/' + file[:-4] + name + '.bmp')

print files
	