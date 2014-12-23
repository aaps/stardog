#gui.py

import pygame
from pygame.locals import *
from utils import *
from spaceship import Ship
from strafebat import Strafebat
from floaters import Asteroid
from planet import Planet, Sun

radarRadius = 100
radarScale = 20000.0 # 1 radar pixel = radarScale space pixels
radarRadiusBig = 400
radarScaleBig = 10000.0 # 1 radar pixel = radarScale space pixels
edgeWarning = loadImage('res/edgeofsystem.bmp')

class HUD:
	debugging = False

	def __init__(self, game):
		self.game = game
		self.image = pygame.Surface((self.game.width, self.game.height), \
							flags = hardwareFlag)
		self.image.set_alpha(150)
		self.image.set_colorkey((0,0,0))
		self.keys = game.keys
		self.center = (game.width - radarRadius, radarRadius)
		self.radarImage = pygame.image.load(
					"res/radar small.png").convert()
		self.radarImage.set_colorkey((0,0,0))
		self.radarImageBig = pygame.image.load(
					"res/radar large.png").convert()
		self.radarImageBig.set_colorkey((0,0,0))

	def scanSystem(self):
		self.orbitImage = pygame.Surface((0,0))
		self.orbitOffset = 0, 0
		scale = radarScaleBig
		for planet in self.game.curSystem.planets:
			#new width = h*sin(angle) + w*cos(angle) <=> w1 + w2
			#new height = h*cos(angle) + w*sin(angle) <=> h1 + h2
			#w1, w2, h1, h2 may or not be considered for correction
			#of the "orbit" surface position depending on the angle
			if isinstance(planet, Sun):
				continue
			orbPos = rotate(-planet.SMa * (1 + planet.e), \
			-planet.SMa * sqrt(planet.p), planet.LPe)
			if planet.LPe < 90:
				w1, w2 = 2*planet.SMa*sqrt(planet.p)*sin(planet.LPe), 0
				h1, h2 = 0, 0
			elif planet.LPe < 180:
				w1 = 2*planet.SMa*sqrt(planet.p)*sin(planet.LPe)
				w2 = -2*planet.SMa*cos(planet.LPe)
				h1, h2 = -2*planet.SMa*sqrt(planet.p)*cos(planet.LPe), 0
			elif planet.LPe < 270:
				w1, w2 = 0, -2*planet.SMa*cos(planet.LPe)
				h1 = -2*planet.SMa*sqrt(planet.p)*cos(planet.LPe)
				h2 = -2*planet.SMa*sin(planet.LPe)
			else:
				w1, w2 = 0, 0
				h1, h2 = 0, -2*planet.SMa*sin(planet.LPe)
			correction = w1 + w2, h1 + h2
			orbPos = int((orbPos[0] - correction[0]) / scale), \
			int((orbPos[1] - correction[1]) / scale)
			while(True):
				try:
					orbit = pygame.Surface((int(2 * planet.SMa / scale),
					int(2 * planet.SMa * sqrt(planet.p) / scale)))
					break
				except:
					scale += radarScaleBig
			orbit.set_colorkey((0,0,0))
			pygame.draw.ellipse(orbit, (150,150,150), (0, 0, int(2*\
			planet.SMa/scale), int(2*planet.SMa*sqrt(planet.p)/scale)), 1)
			orbit = pygame.transform.rotate(orbit, -planet.LPe)
			orbit.blit(self.orbitImage, (self.orbitOffset[0] - orbPos[0],
			self.orbitOffset[1] - orbPos[1]))
			self.orbitImage = orbit
			self.orbitOffset = orbPos

	def draw(self, surface, thisShip):
		"""updates the HUD and draws it."""
		if self.game.debug:
			self.debugging = not self.debugging
			print "gui debugging %s"%(self.debugging,)
			if hasattr(thisShip, 'oldx'):
				dx = (thisShip.x - thisShip.oldx) / self.game.dt
				dy = (thisShip.y - thisShip.oldy) / self.game.dt
				print 'dx: %.1f dy: %.1f' % (dx, dy)
			thisShip.oldx, thisShip.oldy = thisShip.x, thisShip.y
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

		#edge warning:
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
			sunPos = (int(center[0] + (self.game.curSystem.sun.x - thisShip.x) / scale),
			int(center[1] + (self.game.curSystem.sun.y - thisShip.y) / scale))
			offset = (sunPos[0] + self.orbitOffset[0], sunPos[1] + self.orbitOffset[1])
			self.image.blit(self.orbitImage, offset)
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
			if isinstance(floater, Ship):	#ship
				color = floater.color
				pygame.draw.rect(self.image, (0,0,0),
						(dotPos[0] - 1, dotPos[1] - 1, 3,3))
				pygame.draw.line(self.image, color,
						(dotPos[0] - 1, dotPos[1]), (dotPos[0] + 1, dotPos[1]))
				pygame.draw.line(self.image, color,
						(dotPos[0], dotPos[1] - 1), (dotPos[0], dotPos[1] + 1))
				if self.debugging:
					if isinstance(floater, Ship):#direction arrow
						p2 = (dotPos[0] + 3 * cos(floater.dir),
								dotPos[1] + 3 * sin(floater.dir))
						pygame.draw.line(self.image, (200,200,0), dotPos, p2)
						if hasattr(floater, 'goal'):
							p2 = (int(center[0] + limit(-radius,
								(floater.goal[0] - thisShip.x) / scale, radius)),
								int(center[1] + limit(-radius,
								(floater.goal[1] - thisShip.y) / scale, radius)))
							pygame.draw.line(self.image, color, dotPos, p2)
			elif isinstance(floater, Sun):		#sun
				r = int(floater.radius / scale)
				pygame.draw.circle(self.image, (255,100,0), dotPos, r)
				pygame.draw.circle(self.image, (255,150,0), dotPos, 9 * r / 10)
				pygame.draw.circle(self.image, (255,200,50), dotPos, 4 * r / 5)
				pygame.draw.circle(self.image, (255,255,50), dotPos, 7 * r / 10)
			elif isinstance(floater, Planet):	#planet
				if floater.race:
					color = floater.race.color
				else:
					color = (100,100,100)
				r = int(floater.radius / radarScale + 2)
				pygame.draw.circle(self.image, color, dotPos, r)
			elif isinstance(floater, Asteroid):	#Asteroid
				pass #don't draw asteroids.
			else:								#Other floater
				color = floater.color
				pygame.draw.circle(self.image, color, (dotPos[0],dotPos[1]), 0)


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
				randint(0, self.game.width), 	#x
				randint(0, self.game.height),	#y
				randint(1,20), 					#depth
				(randint(brightness * 3 / 4, brightness),
				randint(brightness * 3 / 4, brightness),
				randint(brightness * 3 / 4, brightness))))		#color
		self.pic = pygame.transform.scale(loadImage('res/Tarantula Nebula.jpg', None),
					(game.width,game.height)).convert()

	def draw(self, surface, thisShip):
		surface.blit(self.pic, (0,0))
		pa = pygame.PixelArray(surface)
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
