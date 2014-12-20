#planet.py

from utils import *
from floaters import Floater
from adjectives import randItem
import parts
import stardog
from vec2d import Vec2d


class Planet(Floater):
	maxRadius = 1000000 # no gravity felt past this (approximation).
	PLANET_DAMAGE = .0004
	LANDING_SPEED = 200 #pixels per second. Under this, no damage.
	name = "Planet Unknown"
	
	def __init__(self, game, pos, delta = Vec2d(0,0), grav=5000, radius = 100, mass = 10000, \
					color = (100,200,50), image = None, race = None):
		Floater.__init__(self, game, pos, delta, radius = radius, image = image)
		self.mass = mass #determines gravity.
		self.color = color
		self.g = grav
		self.damage = {}	
		#damage[ships] = amount of damage ship will take. 
		#see solarSystem.planet_ship_collision
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []
		for x in range(randint(1,8)):
			self.inventory.append(randItem(game, 1))
	
	def update(self):
		for other in self.game.curSystem.floaters.sprites():
			if other != self \
			and not isinstance(other, Structure) \
			and not isinstance(other, Planet) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.maxRadius: # remove planets test for gravity sensitive planets
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / (dist2(self, other))
				angle = (self.pos - other.pos).get_angle()
				other.delta.x += cos(angle) * accel / self.game.fps
				other.delta.y += sin(angle) * accel / self.game.fps
		# Floater.update(self) # for gravity sensitive planets update
	
	def draw(self, surface, offset = Vec2d(0,0)):
		if self.image:
			pos = (int(self.pos.x - self.image.get_width()  / 2 - offset[0]), 
				  int(self.pos.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos())
		else:
			pos = self.pos - offset
			pygame.draw.circle(surface, self.color, pos.inttup(), int(self.radius))

	def takeDamage(self, damage, other):
		pass

	def freepartCollision(self, part):
		part.kill()
		self.inventory.append(part)

	def planetCollision(self, planet):
		if self.mass > planet.mass:
			planet.kill()
		else:
			self.kill()


	
class Sun(Planet):
	PLANET_DAMAGE = 300
	LANDING_SPEED = -999 #no landing on the sun.
	# def __init__(self, game, pos, radius = 100, mass = 10000, \
	# 				color = (100,200,50), image = None, race = None):
	# 	Floater.__init__(self, game, pos, radius = radius, image = image)


class Structure(Planet):
	LANDING_SPEED = 200 #pixels per second. Under this, no damage.
	PLANET_DAMAGE = .0004
	name = "Structure Unknown"
	def __init__(self, game, pos, delta, grav=5000, color = (100,200,50), radius = 100, image = None):
		Floater.__init__(self, game, pos, Vec2d(0,0), 0, image=image)
		self.color = (0,0,255)
		self.g = grav
		self.damage = {}	
		self.radius = radius
		#damage[ships] = amount of damage ship will take. 
		#see solarSystem.planet_ship_collision
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []

	def update(self):
		for other in self.game.curSystem.floaters.sprites():
			if  not isinstance(other, Planet) \
			and not isinstance(other, Structure) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.maxRadius:
				#accelerate that floater towards this planet:
				accel = self.g * 100 / dist2(self, other)
				angle = (self.pos - other.pos).get_angle()
				other.delta.x += cos(angle) * accel / self.game.fps
				other.delta.y += sin(angle) * accel / self.game.fps

	def draw(self, surface, offset = Vec2d(0,0)):
		if self.image:
			pos = (int(self.pos.x - self.image.get_width()  / 2 - offset[0]), 
				  int(self.pos.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos())
		else:
			pos = self.pos - offset
			rect = Rect(pos.x-self.radius*0.875,pos.y-self.radius*0.875,self.radius*1.75,self.radius*1.75)
			pygame.draw.rect(surface, self.color, rect)

	def takeDamage(self, damage, other):
		pass

class Gateway(Planet):
	maxRadius = 50000 # no gravity felt past this (approximation).
	tangible = True
	g = 5000 # the gravitational constant.
	name = "Gateway Unknown"
	rect = None
	image = None
	sister = None
	
	def __init__(self, game, pos, radius = 100, mass = 10000, \
					color = (100,200,50), image = None, race = None):
		image = pygame.Surface((radius * 4, radius * 4), flags = hardwareFlag).convert()
		image.set_colorkey((0,0,0))
		Floater.__init__(self, game, pos, Vec2d(0,0), radius = radius, image = image)
		self.mass = mass #determines gravity.
		self.color = color
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []
	
	def setSister(self, gateway):
		if instance(gateway, Gateway):
			self.sister = gateway

	
	def update(self):
		for other in self.game.curSystem.floaters.sprites():
			if  not isinstance(other, Planet) \
			and not isinstance(other, Structure) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.radius * 1.2:
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / dist2(self, other)
				angle = (self.pos - other.pos).get_angle()
				other.delta.x += cos(angle) * accel / self.game.fps
				other.delta.y += sin(angle) * accel / self.game.fps
	
	def draw(self, surface, offset = Vec2d(0,0)):
			self.image.fill((0, 0, 0, 0))

			pos = self.pos - offset
			pygame.draw.circle(self.image, self.color, pos.inttup(), int(self.radius))
			pygame.draw.circle(self.image, (0,0,0,0), pos.inttup(), int(self.radius)-30)
			Floater.draw(self, surface, offset)

	def takeDamage(self, damage, other):
		pass
