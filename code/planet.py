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
	g = 5000 # the gravitational constant.
	
	def __init__(self, game, pos, radius = 100, mass = 10000, \
					color = (100,200,50), image = None, race = None):
		Floater.__init__(self, game, pos, Vec2d(0,0), radius = radius, image = image)
		self.mass = mass #determines gravity.
		self.color = color
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
			if  not isinstance(other, Planet) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.maxRadius:
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / dist2(self, other)
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
			pygame.draw.circle(surface, self.color, pos.inttup(), int(self.radius))
	
	def takeDamage(self, damage, other):
		pass

	def collide(self):
		pass

	def collidePart(self):
		pass

	def collidePlanet(self):
		pass


	# ship - ship
	# ship - freepart
	# ship - planet
	# planet - freepart
	# bullet - freepart
	# bullet - planet
	# ship - bullet
	# explotion - floater
	# planet - planet
	# floater - floater
	
class Sun(Planet):
	PLANET_DAMAGE = 300
	LANDING_SPEED = -999 #no landing on the sun.
	# def __init__(self, game, pos, radius = 100, mass = 10000, \
	# 				color = (100,200,50), image = None, race = None):
	# 	Floater.__init__(self, game, pos, radius = radius, image = image)


class Structure(Floater):
	LANDING_SPEED = 200 #pixels per second. Under this, no damage.
	
	def __init__(self, game, pos, color = (100,200,50), radius = 100, image = None):
		Floater.__init__(self, game, pos, Vec2d(0,0), 0, image=image)
		self.color = (0,0,255)
		self.damage = {}	
		self.radius = radius
		#damage[ships] = amount of damage ship will take. 
		#see solarSystem.planet_ship_collision
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []

	def update(self):
		pass

	def draw(self, surface, offset = Vec2d(0,0)):
		if self.image:
			pos = (int(self.pos.x - self.image.get_width()  / 2 - offset[0]), 
				  int(self.pos.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos())
		else:
			pos = self.pos - offset
			pygame.draw.circle(surface, self.color, pos.inttup(), int(self.radius))
			# pygame.draw.rect(surface, self.color, Rect(self.pos.x,self.pos.y,self.radius,self.radius), 0)