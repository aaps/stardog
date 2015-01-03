#gui.py

import pygame
from pygame.locals import *
from utils import *
import stardog
from spaceship import Ship
from planet import Planet
from parts import *
import time
import numpy

numStars = 300
radarRadius = 100
radarScale = 200.0 # 1 radar pixel = radarScale space pixels
radarRadiusBig = 400
radarScaleBig = 200.0 # 1 radar pixel = radarScale space pixels
edgeWarning = loadImage('res/edgeofsystem.bmp')

class Drawable(object):
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
		
		self.zoomModifier = 1
		self.keys = game.keys
		self.center = (game.width - radarRadius, radarRadius)
		self.radarImage = pygame.image.load("res/radar small.png").convert_alpha()
		self.radarImage.set_colorkey((0,0,0))
		self.radarImageBig = pygame.image.load("res/radar large.png").convert_alpha()
		self.radarImageBig.set_colorkey((0,0,0))
		self.image = pygame.Surface((self.game.width, self.game.height), flags = (SRCALPHA)).convert_alpha()
		
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
			self.image.blit(FONT.render(str(self.game.player.developmentPoints), False, (0, 180, 80)), (x, y - 20))			
		#FPS
		if(fontModule):
			self.image.blit(FONT.render(str(self.game.fps), False, (200, 20, 255)), (100, 100))
		if self.game.player.game.universe.curSystem.drawEdgeWarning:
			self.image.blit(edgeWarning, (20, self.game.height - 100))
		#blit the HUD to the screen:
		surface.blit(self.image, (0, 0))
		
	def drawRadar(self, surface, thisShip, big = False):
		if big:
			#these temp locals replace the globals:
			radius = radarRadiusBig
			center = (self.game.width / 2, self.game.height / 2)
			scale = radarScaleBig * self.zoomModifier
			self.image.blit(self.radarImageBig, \
				(center[0] - radius, center[1] - radius))
		else:
			radius = radarRadius
			center = self.center
			scale = radarScale * self.zoomModifier
			self.image.blit(self.radarImage, \
				(center[0] - radius, center[1] - radius))


		#draw floating part dots:
		if thisShip.radars[0].disk and thisShip.radars[0].enabled:
			pygame.draw.circle(self.image, (255,255,255, 50), center, int(thisShip.radars[0].disk.radius / radarScale + 2), 1)

		for radar in thisShip.radars:
			for floater in radar.detected:
				
				result = floater.pos - thisShip.pos
				dotPos = int(center[0] + limit(-radius,	result.x / scale, radius)), \
						int(center[1] + limit(-radius, result.y / scale, radius))
				if isinstance(floater, Ship):
					if thisShip.curtarget == floater:
						pygame.draw.circle(self.image, (0, 250, 250), dotPos, 4, 1)
					pygame.draw.circle(self.image, (250, 250, 0), dotPos, 2)
					color = floater.color
					r = 1
					pygame.draw.rect(self.image, color, (dotPos[0]-1,dotPos[1]-1,2,2))
				elif not isinstance(floater, Planet):
					# color = (150,40,0)
					if thisShip.curtarget == floater:
						pygame.draw.circle(self.image, (0, 250, 250), dotPos, 3, 1)
					if isinstance(floater, Bullet):
						pygame.draw.rect(self.image, (150,40,0), (dotPos[0]-1,dotPos[1]-1,2,2))
					elif isinstance(floater, Part):
						pygame.draw.rect(self.image, (200,200,0), (dotPos[0]-1,dotPos[1]-1,2,2))

		for planet in thisShip.knownplanets:
			
			result = planet.pos - thisShip.pos
			dotPos = int(center[0] + limit(-radius,	result.x / scale, radius)), int(center[1] + limit(-radius, result.y / scale, radius))
			r = int(planet.radius / scale + 2)
			if collisionTest(Floater(self.game, Vec2d(dotPos), Vec2d(0,0), 0, 1), Floater(self.game, Vec2d(center), Vec2d(0,0), 0, 100)):
				color = planet.color
				if thisShip.curtarget == planet:
					pygame.draw.circle(self.image, (0, 250, 250), dotPos, r+3, 1)
				pygame.draw.circle(self.image, color, dotPos, r)

	def zoomInRadar(self):
		if self.zoomModifier <= 2.4:
			self.zoomModifier += 0.2

	def zoomOutRadar(self):
		if self.zoomModifier > 0.4:
			self.zoomModifier -= 0.2


class StarField(Drawable):
	
	def __init__(self, game):
		Drawable.__init__(self, game)
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
		
	def draw(self, surface):
		# surface.blit(self.pic, (0,0))
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

class BGImage(Drawable):
	pic = None
	
	def __init__(self, game):
		Drawable.__init__(self, game)
		self.pic = pygame.transform.scale(loadImage('res/Tarantula Nebula.jpg', None), 
					(game.width,game.height))

	def draw(self, surface):
		surface.blit(self.pic, (0,0))
			
class MiniInfo(Drawable):
	color = (100, 100, 255)
	font = FONT
	maxChars = 50 #line width
	bottomleft = 0,0
	targimage = None
	mutatedimage = None
	texts = []

	def __init__(self, game,font = FONT):
		Drawable.__init__(self, game)
		self.bottomleft = 2,  game.height - int(game.height/ 4 ) 
		self.targ = None
		self.width = int(game.width / 8)
		self.height = int(game.height/ 4 )
		self.image = pygame.Surface((int(game.width / 8),int(game.height/ 4 )))
		self.image.set_alpha(200)

	def update(self):
		self.targ = self.game.player.curtarget

	def draw(self, surface):
		self.image.fill((0, 0, 80))
		if self.targ:
			self.texts = []
			speed = round(self.targ.delta.get_length(), 2)
			name = ""
			linedeltastart = Vec2d(10,40)
			linedirstart = Vec2d(10,60)
			pygame.draw.circle(self.image, (0,255,255), linedeltastart, 10, 1)
			pygame.draw.line(self.image, (0,255,255), linedeltastart, self.targ.delta.normalized()*10+linedeltastart)
			distance = "Distance:" + str(round(self.game.player.pos.get_distance(self.targ.pos),1))
			pygame.draw.circle(self.image, (0,255,255), linedirstart, 10, 1)
			pygame.draw.line(self.image, (0,255,255), linedirstart, (self.targ.pos-self.game.player.pos).normalized()*10+linedirstart)

			if isinstance(self.targ, Ship):
				linedirstart = Vec2d(40,40)
				pygame.draw.circle(self.image, (255,255,255), linedirstart, 10, 1)
				pygame.draw.line(self.image, (255,255,255), linedirstart, linedirstart.normalized().rotated(self.targ.dir)*10+linedirstart)
				name = self.targ.firstname + " " + self.targ.secondname
				if not self.targimage == self.targ.baseImage:
					self.targimage = self.targ.baseImage
					self.mutatedimage = self.grayscale(self.targimage)
					self.mutatedimage = pygame.transform.rotozoom(self.mutatedimage, 90,2)
					self.mutatedimage.set_colorkey((0,0,0))       
				offset = ((self.width/2) - (self.mutatedimage.get_width()/2), (self.height/2)-(self.mutatedimage.get_height()/2))
				self.image.blit(self.mutatedimage, offset)
				
			elif isinstance(self.targ, Planet):
				name = self.targ.firstname
				r = int(self.targ.radius / radarScale + 2)
				
				pygame.draw.circle(self.image, self.targ.color, ((self.width/2,self.height/2)), r)
			elif isinstance(self.targ, Part):
				name = self.targ.name
				if not self.targimage == self.targ.baseImage:
					self.targimage = self.targ.baseImage
					self.mutatedimage = self.grayscale(self.targimage)
					self.mutatedimage = pygame.transform.scale(self.mutatedimage, (self.targimage.get_width()*2,self.targimage.get_height()*2) )
					self.mutatedimage.set_colorkey((0,0,0))     
				self.image.blit(self.mutatedimage,(self.width/2,self.height/2))
			
			
			self.texts.append(self.font.render(name , True, self.color))
			self.texts.append(self.font.render(distance , True, self.color))
			self.texts.append(self.font.render("speed: " + str(speed) , True, self.color))
			for text in self.texts:
				self.image.blit(text, (0,self.texts.index(text)*10))
		surface.blit(self.image, self.bottomleft)

	def grayscale(self, img):
		arr = pygame.surfarray.array3d(img)
		#luminosity filter
		avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
		arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
		return pygame.surfarray.make_surface(arr)

class shipDamage(Drawable):

	def __init__(self, game, font=SMALL_FONT):
		self.game = game
		self.player = self.game.player
		self.font = font
		
	

	def draw(self,surface):
		self.startrect = Rect(self.game.width-120, 220, 100, 5)
		for part in self.player.parts:
			

			#color fades green to red as hp decreases.
			color = limit(0, int((1 - part.hp * 1. / part.maxhp ) * 255),255), \
					limit(0, int(1. * part.hp / part.maxhp * 255), 255), 0, 100 
			rect = (0,0, part.radius * 2, part.radius * 2)
			text = self.font.render(part.name, False, (0, 180, 80))
			surface.blit(text, (self.game.width-120, self.startrect[1]+10))
			pygame.draw.rect(surface, color, self.startrect)
			self.startrect[1] += 30
			self.startrect[2] = limit(0, int(1. * part.hp / part.maxhp * 100), 100)

				

