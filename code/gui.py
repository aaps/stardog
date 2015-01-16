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
from vec2d import *

numStars = 300
radarRadius = 100
radarScale = 200.0 # 1 radar pixel = radarScale space pixels

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
		
		
		self.keys = game.keys
		
		self.image = pygame.Surface((70, 220), flags = (SRCALPHA))
		
	def draw(self, surface):
		"""updates the HUD and draws it."""
		self.image.fill(SHIPDAMAGE)

		# energy:
		x = 25
		y = 20 
		h = 180
		pygame.draw.rect(self.image, HUD1, (x, y, \
			5, h), 1) # empty bar

		pygame.draw.rect(self.image, HUD2, (x, y \
			+ h - h * self.game.player.energy / self.game.player.maxEnergy, 5, h \
			* self.game.player.energy / self.game.player.maxEnergy)) # full bar
		#XP:
		x += 15
		pygame.draw.rect(self.image, HUD3, (x, y, \
			5, 180), 1) # empty bar
		pygame.draw.rect(self.image, HUD3, \
			(x, y + h - h * self.game.player.xp / self.game.player.next(), 5, \
			h * self.game.player.xp / self.game.player.next())) # full bar
		if(fontModule) and self.game.player.developmentPoints:
			self.image.blit(FONT.render(str(self.game.player.developmentPoints), False, HUD3), (x, y - 20))			

		#blit the HUD to the screen:
		surface.blit(self.image, (self.game.width-70, self.game.height-200))
	
class RadarField(Drawable):
	
	def __init__(self, game):
		Drawable.__init__(self, game)
		self.radarRadius = int(game.width / 10)
		self.center = (self.radarRadius, self.radarRadius)
		self.image = pygame.Surface((self.radarRadius*2, self.radarRadius*2))
		self.image.set_alpha(200)
		self.zoomModifier = 1
		self.maskimage = pygame.Surface((self.radarRadius*2, self.radarRadius*2))
		self.maskimage.fill((0, 0, 80))
		pygame.draw.circle(self.maskimage,BLACK, self.center, self.radarRadius )
		self.maskimage.set_colorkey(BLACK)
		self.targimage = pygame.Surface((8, 8))
		targetRect(self.targimage, RADAR4, BLACK , (4,4), 2, 2)
		self.targimage.set_colorkey(BLACK)

	def draw(self, surface):
		radius = self.radarRadius
		center = self.center
		self.image.fill((0, 0, 80))
		
		scale = self.radarRadius * self.zoomModifier

		pygame.draw.circle(self.image,(0, 0, 60), self.center, self.radarRadius )
		#draw floating part dots:
		if self.game.player.radars[-1].disk and self.game.player.radars[-1].enabled and int(self.game.player.radars[-1].disk.radius / scale + 2) < 100:
			pygame.draw.circle(self.image, RADAR3, center, int(self.game.player.radars[-1].disk.radius / scale + 2), 1)


		for planet in self.game.player.knownplanets:
			
				result = planet.pos - self.game.player.pos
				dotPos = int(center[0] + limit(-radius,	result.x / scale, self.radarRadius)), int(center[1] + limit(-self.radarRadius, result.y / scale, self.radarRadius))
				r = int(planet.radius / scale + 2)
				if collisionTest(Floater(self.game, Vec2d(dotPos), Vec2d(0,0), 0, 0), Floater(self.game, Vec2d(center), Vec2d(0,0), 0, 100)):
					color = planet.color
					if self.game.player.curtarget == planet:
						targetRect(self.image, RADAR4, RADAR2 , dotPos, r, 2)
					pygame.draw.circle(self.image, color, dotPos, r)
			
				else:
					color = (255, 250, 0)
					modi = 5
					if self.game.player.curtarget == planet:
						color = (0,255,250)
						modi = 10
					normalised = result.normalized()
					pos = []
					pos.append(normalised * (100 - modi) + center)
					pos.append((normalised * 100).rotated(2)  + center)
					pos.append((normalised * 100).rotated(-2) + center)
					pygame.draw.polygon(self.image, color, pos)


			
		for floater in self.game.player.radars[-1].detected:
			
			result = floater.pos - self.game.player.pos
			dotPos = int(center[0] + limit(-self.radarRadius,	result.x / scale, self.radarRadius)), \
					int(center[1] + limit(-self.radarRadius, result.y / scale, self.radarRadius))
			if collisionTest(Floater(self.game, Vec2d(dotPos), Vec2d(0,0), 0, 0), Floater(self.game, Vec2d(center), Vec2d(0,0), 0, 100)):
				if isinstance(floater, Ship):
					if self.game.player.curtarget == floater:
						self.image.blit(self.targimage,(dotPos[0]-4,dotPos[1]-4))

					pygame.draw.circle(self.image, (250, 250, 0), dotPos, 2)
					color = floater.color
					r = 1
					pygame.draw.rect(self.image, color, (dotPos[0]-1,dotPos[1]-1,2,2))
				elif not isinstance(floater, Planet):
					if self.game.player.curtarget == floater:
						self.image.blit(self.targimage,(dotPos[0]-4,dotPos[1]-4))
						
					if isinstance(floater, Bullet):
						pygame.draw.rect(self.image, (150,40,0), (dotPos[0]-1,dotPos[1]-1,2,2))
					elif isinstance(floater, Part):
						pygame.draw.rect(self.image, (200,200,0), (dotPos[0]-1,dotPos[1]-1,2,2))
			elif not isinstance(floater, Planet):
				color = (255, 0, 0)
				modi = 7
				if self.game.player.curtarget == floater:
					color = MINI2
					modi = 10
				normalised = result.normalized()
				pos = []
				pos.append(normalised * (100 - modi) + center)
				pos.append((normalised * 100).rotated(2)  + center)
				pos.append((normalised * 100).rotated(-2) + center)
				pygame.draw.polygon(self.image, color, pos)



		


		pygame.draw.line(self.image, SUPER_WHITE, (0,self.radarRadius), (self.radarRadius*2,self.radarRadius),1)
		pygame.draw.line(self.image, SUPER_WHITE, (self.radarRadius,0), (self.radarRadius,self.radarRadius*2),1)
		self.image.blit(self.maskimage,(0,0))
		pygame.draw.circle(self.image,SUPER_WHITE, self.center, self.radarRadius,1 )
		surface.blit(self.image, (self.game.width - self.image.get_width(), 0))

	def zoomInRadar(self):
		if self.zoomModifier <= 2.4:
			self.zoomModifier += 0.2

	def zoomOutRadar(self):
		if self.zoomModifier > 0.4:
			self.zoomModifier -= 0.2

class TargetingRect(Drawable):

	def __init__(self, game):
		Drawable.__init__(self, game)
		self.image = pygame.Surface((50, 50))

	def draw(self, surface):
		
		if self.game.player.curtarget and not isinstance(self.game.player.curtarget, Planet) and self.game.player.curtarget in self.game.spaceview.onScreen:
			if self.image.get_width() != self.game.player.curtarget.radius:
				self.image = pygame.Surface((self.game.player.curtarget.radius*2+4, self.game.player.curtarget.radius*2+4))
				targetRect(self.image, RADAR12, BLACK , (self.image.get_width()/2, self.image.get_height()/2), self.game.player.curtarget.radius, 2)
				self.image.set_colorkey(BLACK)

			result = (self.game.player.curtarget.pos - self.game.player.pos).inttup()
			result = result[0] + self.game.width / 2 - self.image.get_width() / 2,  result[1] + self.game.height / 2 - self.image.get_height() / 2,
			surface.blit(self.image,result)


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
	font = SMALL_FONT
	maxChars = 50 #line width
	bottomleft = 0,0
	targimage = None
	mutatedimage = None
	texts = []

	def __init__(self, game,font = SMALL_FONT):
		Drawable.__init__(self, game)
		self.bottomleft = 2,  game.height - int(game.height/ 4 ) 
		self.game = game
		self.targ = None
		self.width = int(game.width / 8)
		self.height = int(game.height/ 4 )
		self.image = pygame.Surface((self.width,self.height))
		self.image.set_alpha(200)

	def update(self):

		self.targ = self.game.player.curtarget


	def draw(self, surface):
		self.image.fill((0, 0, 80))
		if self.targ:
			self.texts = []
			# speed = makeMs(self.targ)
			name = ""
			linedeltastart = Vec2d(10,180)
			linedirstart = Vec2d(40,180)
			pygame.draw.circle(self.image, MINI2, linedeltastart, 10, 1)
			pygame.draw.line(self.image, MINI2, linedeltastart, self.targ.delta.normalized()*10+linedeltastart)
			distance = "Distance Km:" + makeKMdistance(self.game.player,self.targ)
			pygame.draw.circle(self.image, MINI2, linedirstart, 10, 1)
			pygame.draw.line(self.image, MINI2, linedirstart, (self.targ.pos-self.game.player.pos).normalized()*10+linedirstart)

			if isinstance(self.targ, Ship):
				linedirstart = Vec2d(100,180)
				pygame.draw.circle(self.image, SUPER_WHITE, linedirstart, 10, 1)
				pygame.draw.line(self.image, SUPER_WHITE, linedirstart, linedirstart.normalized().rotated(self.targ.dir)*10+linedirstart)
				name = self.targ.firstname + " " + self.targ.secondname
				if not self.targimage == self.targ.baseImage:
					self.targimage = self.targ.baseImage
					self.mutatedimage = self.grayscale(self.targimage)
					self.mutatedimage = pygame.transform.rotozoom(self.mutatedimage, 90,2)
					self.mutatedimage.set_colorkey(BLACK)       
				offset = ((self.width/2) - (self.mutatedimage.get_width()/2), (self.height/2)-(self.mutatedimage.get_height()/2))
				self.image.blit(self.mutatedimage, offset)
				
			elif isinstance(self.targ, Planet):
				name = self.targ.firstname
				scale = self.game.radarfield.radarRadius * self.game.radarfield.zoomModifier
				if (self.targ.radius / scale) < self.width/2:
					r = int(self.targ.radius / scale)
				else:
					r = self.width / 2
				pygame.draw.circle(self.image, self.targ.color, ((self.width/2,self.height/2)), r)
			elif isinstance(self.targ, Part):
				name = self.targ.name
				if not self.targimage == self.targ.baseImage:
					self.targimage = self.targ.baseImage
					self.mutatedimage = self.grayscale(self.targimage)
					self.mutatedimage = pygame.transform.scale(self.mutatedimage, (self.targimage.get_width()*2,self.targimage.get_height()*2) )
					self.mutatedimage.set_colorkey(BLACK)     
				self.image.blit(self.mutatedimage,(self.width/2,self.height/2))
			
			
			self.texts.append(self.font.render(name , True, self.color))
			self.texts.append(self.font.render(distance , True, self.color))
			self.texts.append(self.font.render("speed: " + makeKMs(self.targ) + "Km/s" , True, self.color))
			for text in self.texts:
				self.image.blit(text, (0,self.texts.index(text)*15))
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
		self.totalhealth = 0
		self.font = font
		self.shownparts = []
		self.width = int(game.width / 5)
		self.height = int(game.height/ 4 )
		self.image = pygame.Surface((self.width,self.height))
		self.image.set_alpha(200)
	
	def update(self):
		totalhealth = sum(c.hp for c in self.player.parts)
		if totalhealth != self.totalhealth:
			totalhealth = self.totalhealth
			self.active = True
			self.shownparts = sorted(self.player.parts, key=lambda part: part.hp / part.maxhp)
			self.shownparts = self.shownparts[:6]
		else:
			self.active = False


	def draw(self,surface):
		
		if self.active:
			self.startrect = Rect(10, 0, 150, 5)
			self.image.fill(SHIPDAMAGE)
			for part in self.shownparts:
				partfactor = part.hp / part.maxhp 
				
				if partfactor >= 0 and partfactor <= 1:
					self.startrect[2] = partfactor * 150
					self.startrect[1] += 30
					color = (int((1-partfactor) * 255) , int(partfactor * 255), 50)
					
					pygame.draw.rect(self.image, color, self.startrect)
					text = self.font.render(part.name + " " + str(round(part.hp,1)) + "/" + str(part.maxhp), False, HUD3)
					self.image.blit(text, (10, self.startrect[1]-15))
			
			

		surface.blit(self.image, (self.game.width-self.width, 204))
				

