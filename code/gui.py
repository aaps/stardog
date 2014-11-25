#gui.py

import pygame
from pygame.locals import *
from utils import *
import stardog
from spaceship import Ship
from planet import Planet

radarRadius = 100
radarScale = 200.0 # 1 radar pixel = radarScale space pixels
radarRadiusBig = 400
radarScaleBig = 200.0 # 1 radar pixel = radarScale space pixels
edgeWarning = loadImage('res/edgeofsystem.bmp')
class HUD:

	def __init__(self, game):
		self.game = game
		self.image = pygame.Surface((self.game.width, self.game.height), \
							flags = (SRCALPHA)).convert_alpha()
		self.keys = game.keys
		self.center = (game.width - radarRadius, radarRadius)
		self.radarImage = pygame.image.load(
					"res/radar small.png").convert_alpha()
		self.radarImage.set_colorkey((0,0,0))
		self.radarImageBig = pygame.image.load(
					"res/radar large.png").convert_alpha()
		self.radarImageBig.set_colorkey((0,0,0))

	def draw(self, surface, thisShip):
		"""updates the HUD and draws it."""
		self.image.fill((0, 0, 0, 0))
		#TODO: don't hard-code this key:
		self.drawRadar(surface, thisShip, self.game.keys[K_TAB])

		# energy:
		x = self.game.width - 25
		y = self.game.height - 20 - self.game.height / 6
		h = self.game.height / 6
		pygame.draw.rect(self.image, (20, 25, 130), (x, y, \
			5, h), 1) # empty bar

		pygame.draw.rect(self.image, (0, 50, 230), (x, y \
			+ h - h * thisShip.energy / thisShip.maxEnergy, 5, h \
			* thisShip.energy / thisShip.maxEnergy)) # full bar
			
		#XP:
		x += 15
		pygame.draw.rect(self.image, (0, 180, 80), (x, y, \
			5, self.game.height / 6), 1) # empty bar

		pygame.draw.rect(self.image, (0, 180, 80), \
			(x, y + h - h * thisShip.xp / thisShip.next(), 5, \
			h * thisShip.xp / thisShip.next())) # full bar
		if(fontModule) and thisShip.developmentPoints:
			self.image.blit(FONT.render(str(thisShip.developmentPoints), \
						False, (0, 180, 80)), (x, y - 20))
						
		#FPS
		if(fontModule):
			self.image.blit(FONT.render(str(self.game.fps), \
						False, (200, 20, 255)), (100, 100))
		if thisShip.game.curSystem.drawEdgeWarning:
			self.image.blit(edgeWarning, (20, self.game.height - 100))
		#blit the HUD to the screen:
		surface.blit(self.image, (0, 0))
		
	def drawRadar(self, surface, thisShip, big = False):
		if big:
			#these temp locals replace the globals:
			radius = radarRadiusBig
			center = (self.game.width / 2, self.game.height / 2)
			scale = radarScaleBig
			self.image.blit(self.radarImageBig, \
				(center[0] - radius, center[1] - radius))
		else:
			radius = radarRadius
			center = self.center
			scale = radarScale
			self.image.blit(self.radarImage, \
				(center[0] - radius, center[1] - radius))
		#draw floating part dots:
		for floater in self.game.curSystem.floaters:
			dotPos = int(center[0] + limit(-radius, \
					(floater.x - thisShip.x) / scale, radius)), \
					int(center[1] + limit(-radius, \
					(floater.y - thisShip.y) / scale, radius))
			if isinstance(floater, Ship):
				pygame.draw.circle(self.image, (250, 250, 0), dotPos, 2)
				color = floater.color
				r = 1
				pygame.draw.rect(self.image, color, (dotPos[0]-1,dotPos[1]-1,2,2))
			elif isinstance(floater, Planet):
				r = int(floater.radius / radarScale + 2)
				color = floater.color
				pygame.draw.circle(self.image, color, dotPos, r)
			else:
				color = (150,40,0)
				pygame.draw.rect(self.image, color, (dotPos[0],dotPos[1],2,2))


numStars = 300
class BG:
	def __init__(self, game):
		self.game = game
		self.stars = []
		dimmer = 1
		for star in range(numStars):
			brightness = int(randint(100, 255))
			# a position, a color, and a depth.
			self.stars.append((
				randint(0, self.game.width), 
				randint(0, self.game.height),
				randint(1,20), 
				(randint(brightness * 3 / 4, brightness), 
				 randint(brightness * 3 / 4, brightness), 
				 randint(brightness * 3 / 4, brightness))))
		self.pic = pygame.transform.scale(loadImage('res/Tarantula Nebula.jpg', None), 
					(game.width,game.height))

	def draw(self, surface, thisShip):
		surface.blit(self.pic, (0,0))
		pa = pygame.PixelArray(surface)
		"""updates the HUD and draws it."""
		depth = 1.
		for star in self.stars:
			x = int(star[0] - thisShip.x / star[2]) % (self.game.width-1)
			y =	int(star[1] - thisShip.y / star[2]) % (self.game.height-1)
			pa[x][y] = star[3]
			pa[x+1][y] = star[3]
			pa[x][y+1] = star[3]
			pa[x+1][y+1] = star[3]
			
class BGNova:
	def __init__(self, game):
		self.game = game
		nova1 = pygame.image.load("res/bgnova1.jpg").convert(32, HWSURFACE)
		nova2 = pygame.image.load("res/bgnova2.jpg").convert(32, HWSURFACE)
		nova3 = pygame.image.load("res/bgnova3.jpg").convert(32, HWSURFACE)
		nova4 = pygame.image.load("res/bgnova4.jpg").convert(32, HWSURFACE)
		self.bg = [nova1, nova2, nova3, nova4]
		nova4.set_alpha(30)
		nova3.set_alpha(40)
		nova2.set_alpha(50)
		nova1.set_alpha(60)
		self.width = nova1.get_width()
		self.height = nova1.get_height()

	def draw(self, surface, thisShip):
		depth = 10
		for layer in self.bg:
			offset = thisShip.x / depth % 800, thisShip.y / depth % 800
			rects = (((0, 0, offset[0], offset[1]), \
						(self.width - offset[0], self.height - offset[1])), \
					((offset[0], 0, self.width - offset[0], offset[1]), \
						(0, self.height - offset[1])), \
					((0, offset[1], offset[0], self.height - offset[1]), \
						(self.width - offset[0], 0)), \
					((offset[0], offset[1], 	self.width - offset[0], \
											self.width - offset[1]), \
						(0, 0)))
			for rect in rects:
				surface.blit(layer, rect[1], area = rect[0])
			depth = depth * 2
