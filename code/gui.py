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

class Drawable:
	game = None
	drawBorder = True
	rect = None

	def __init__(self, game):
		self.game = game

		self.rect = Rect(0 ,0 ,game.width, game.height)

	def setRect(self, rect):
		self.rect = rect

	def update(self):
		pass

	def draw(self):
		pass



class HUD(Drawable):

	def __init__(self, game):
		Drawable.__init__(self, game)
		# self.game = game
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


	def draw(self, surface):
		"""updates the HUD and draws it."""
		self.image.fill((0, 0, 0, 0))
		#TODO: don't hard-code this key:
		self.drawRadar(surface, self.game.player, self.game.keys[K_TAB])

		# energy:
		x = self.game.width - 25
		y = self.game.height - 20 - self.game.height / 6
		h = self.game.height / 6
		pygame.draw.rect(self.image, (20, 25, 130), (x, y, \
			5, h), 1) # empty bar

		pygame.draw.rect(self.image, (0, 50, 230), (x, y \
			+ h - h * self.game.player.energy / self.game.player.maxEnergy, 5, h \
			* self.game.player.energy / self.game.player.maxEnergy)) # full bar
			
		#XP:
		x += 15
		pygame.draw.rect(self.image, (0, 180, 80), (x, y, \
			5, self.game.height / 6), 1) # empty bar

		pygame.draw.rect(self.image, (0, 180, 80), \
			(x, y + h - h * self.game.player.xp / self.game.player.next(), 5, \
			h * self.game.player.xp / self.game.player.next())) # full bar
		if(fontModule) and self.game.player.developmentPoints:
			self.image.blit(FONT.render(str(self.game.player.developmentPoints), \
						False, (0, 180, 80)), (x, y - 20))
						
		#FPS
		if(fontModule):
			self.image.blit(FONT.render(str(self.game.fps), \
						False, (200, 20, 255)), (100, 100))
		if self.game.player.game.curSystem.drawEdgeWarning:
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
		
		for radar in thisShip.radars:
			for floater in radar.detected:
				result = floater.pos - thisShip.pos
				dotPos = int(center[0] + limit(-radius,	result.x / scale, radius)), \
						int(center[1] + limit(-radius, result.y / scale, radius))
				if isinstance(floater, Ship):
					pygame.draw.circle(self.image, (250, 250, 0), dotPos, 2)
					color = floater.color
					r = 1
					pygame.draw.rect(self.image, color, (dotPos[0]-1,dotPos[1]-1,2,2))
				elif not isinstance(floater, Planet):
					color = (150,40,0)
					pygame.draw.rect(self.image, color, (dotPos[0],dotPos[1],2,2))

		for planet in thisShip.knownplanets:
			if isinstance(planet, Planet):
				result = planet.pos - thisShip.pos
				dotPos = int(center[0] + limit(-radius,	result.x / scale, radius)), int(center[1] + limit(-radius, result.y / scale, radius))
				r = int(planet.radius / radarScale + 2)
				color = planet.color
				pygame.draw.circle(self.image, color, dotPos, r)
			else:
				thisShip.knownplanets.remove(planet)


numStars = 300
class BG(Drawable):
	def __init__(self, game):
		Drawable.__init__(self, game)
		# self.game = game
		self.stars = []
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

	def draw(self, surface):
		surface.blit(self.pic, (0,0))
		pa = pygame.PixelArray(surface)
		"""updates the HUD and draws it."""
		depth = 1.
		for star in self.stars:
			x = int(star[0] - self.game.player.pos.x / star[2]) % (self.game.width-1)
			y =	int(star[1] - self.game.player.pos.y / star[2]) % (self.game.height-1)
			pa[x,y] = star[3]
			pa[x+1,y] = star[3]
			pa[x,y+1] = star[3]
			pa[x+1,y+1] = star[3]
			
class MiniInfo(Drawable):
	color = (100, 100, 255, 250)
	font = FONT
	maxChars = 50 #line width
	bottomleft = 0,0

	def __init__(self, game,font = FONT):
		Drawable.__init__(self, game)
		# self.game = game
		self.bottomleft = 2,  game.height - int(game.height/ 4 ) 
		self.targ = None
		self.image = pygame.Surface((int(game.width / 8),int(game.height/ 4 )))
		self.image.set_alpha(200)

	def update(self):
		self.targ = self.game.player.curtarget

		
	def draw(self, surface):
		self.image.fill((0, 0, 80))
		if self.targ:
			# self.image.blit(userplaatje, (0,0))
			text = self.font.render(self.targ.name, True, color)
			self.image.blit(text, (0,0))
		surface.blit(self.image, self.bottomleft)