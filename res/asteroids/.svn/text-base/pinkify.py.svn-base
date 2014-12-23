import pygame
pygame.init()

def pinkify(filename, threshold = 10):
	"""Converts every pixel with equal red and blue values to a shade of 
	color.  Attempts to maintain value and saturation of surface. 
	Returns a new Surface."""
	s = pygame.image.load(filename)
	pa = pygame.PixelArray(s)
	for i in range(len(pa)):
		for j in range(len(pa[i])):
			oldColor = s.unmap_rgb(pa[i][j])
			if abs(oldColor[0] - oldColor[2]) < threshold: #a shade of magic pink
				newColor = [0, 0, 0, 0]
				for k in [0,1,2]:
					newColor = oldColor[0], oldColor[1], oldColor[0]
				pa[i][j] = s.map_rgb(newColor)
	del pa
	pygame.image.save(s, filename)
	
if __name__ == '__main__':
	import sys
	if len(sys.argv) !=2:
		print 'use: pythone pinkify filename threshold'
		return
	pinkify(sys.argv[0], sys.argv[1])