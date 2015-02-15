#starSystem.py

from utils import *
from floaters import *
from spaceship import *
from strafebat import *
from planet import *
from gui import *
import stardog
from vec2d import Vec2d
from nameMaker import *

class StarSystem(object):
	"""A StarSystem holds ships and other floaters."""
	
	def __init__(self, universe, position=Vec2d(0,0), boundrad = 30000, edgerad = 60000):
		self.boundrad = boundrad
		self.position = position
		self.edgerad = edgerad
		self.neighbors = []		
		self.universe = universe
		self.floaters = pygame.sprite.Group()
		self.player = None
		# self.ships = pygame.sprite.Group()
		self.specialOperations = []
		self.bg = BGImage(self.universe) # the background layer
		pygame.mixer.music.load("res/sound/space music.ogg")
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(.15)
		self.planets = []
		self.name = ""
	
	def addNeighbor(self, starsystem):
		self.neighbors.append(starsystem)
		starsystem.neighbors.append(self)

	def getNeighbors(self):
		return self.neighbors

	def getNeighborposdiff(self):
		posdiffs = []
		for starsystem in self.neighbors:
			posdiff = -(starsystem.position - self.position)
			posdiffs.append((starsystem,posdiff))
		return posdiffs
		
	def update(self):
		"""Runs the game."""
		# self.floaters.update()
		for floater in self.floaters:

			floater.setFPS(self.universe.game.fps)
			floater.update()

		
		#collision:
		floaters = self.floaters.sprites()
		for i in range(len(floaters)):
			for j in range(i + 1, len(floaters)):
				self.collide(floaters[i], floaters[j])
			

				
		for floater in self.floaters:
			if floater.pos.get_distance(Vec2d(0,0)) > self.boundrad:
				if isinstance(floater, Ship):
					floater.overedge = True
				else:
					try:
						floater.kill()
					except TypeError:
						print floater, "exception error"

		
					
		#do any special actions that don't fit elsewhere:
		#(currently just laser collisions)
		for function in self.specialOperations:
			function()
		self.specialOperations = []

		for planet in self.planets:
			
			if not isinstance(planet, Star) :
				if planet.respawn > 0:#countdown the timer
					planet.respawn -= 1. / self.universe.game.fps
					continue
				else:
					#respawn now!
					planet.respawn = self.respawnTime #reset respawn timer
					planet.numShips += 1
					for i in range(planet.numShips):
					
						angle = randint(0, 360)
						pos = planet.pos.rotatedd(angle, planet.radius + 300)
						name = nameMaker().getUniqePilotName(self.floaters)
						
						ship = Strafebat(self.universe, pos,  planet.color, name)
						
						# planet.ships.add(ship)
						self.add(ship)
						ship.planet = planet
		
		
	def add(self, floater):
		"""adds a floater to this game."""
		self.floaters.add(floater)
		# if isinstance(floater, Ship):
		# 	self.ships.add(floater)
		if isinstance(floater, Player):
			
			
			if self.universe.curSystem == self:
				init = False
				while self.minDistFromOthers(floater) < 3000 or init == False:
					init = True
					angle = randint(0,360)
					distanceFromStar = randint(8000, 18000)
					self.universe.player.pos = self.star.pos.rotatedd(angle, distanceFromStar)
			self.player = floater
		
	def empty(self):
		# self.ships.empty()
		self.floaters.empty()


# refactor this and put all functionality in corresponding classes, be carefull can quickly spinn into mess.
# piecetime refactor 
# perhaps this method can be brokenup in a collision method for planet, ship and part
	def collide(self, a, b):
		"""test and act on spatial collision of Floaters a and b"""
		#Because this needs to consider the RTTI of two objects,
		#it is an external function.  This is messy and violates
		#good object-orientation, but when a new subclass is added
		#code only needs to be added here, instead of in every other
		#class.
		if a.tangible and b.tangible and collisionTest(a, b):
			#planet/?
			if isinstance(b, Planet): a,b = b,a
			if isinstance(a, Planet):
				return a.collision(b)

					
			if isinstance(b, Explosion): a,b = b,a
			if isinstance(a, Explosion):
				self.explosion_push(a,b)
				#but don't return!
			#shield ship/?

			if isinstance(b, Ship) : a,b = b,a
			if isinstance(a, Ship):
				
				if isinstance(b, Part) and b.parent == None:
					a.freepartCollision(b)
					return True

				hit = False
				if a.hp > 0:
					
					if b.hp >= 0 and (sign(b.pos.x - a.pos.x) == - sign(b.delta.x - a.delta.x) \
									or sign(b.pos.y - a.pos.y) == - sign(b.delta.y - a.delta.y)):
						# moving into ship, not out of it.
						self.crash(a,b)
						hit = True
						#if this ship no longer has shields, start over:
						if a.hp <= 0:
							self.collide(a, b)
							return True
					#shield ship/no shield ship (or less shield than this one)
					if isinstance(b, Ship) and b.hp <= 0:
						for part in b.parts:
							if self.collide(a, part):
								#if that returned true, everything
								#should be done already.
								return True
					return hit
				else:

					#recurse to ship parts
					for part in a.parts:
						if self.collide(b, part):#works for ship/ship, too.
							#if that returned true, everything
							#should be done already.
							hit = True
					return hit
				
			#free part/free part
			if isinstance(b, Part) and b.parent == None \
			and isinstance(a, Part) and a.parent == None:
				return False #pass through each other, no crash.

			#floater/floater (no ship, planet)
			else:
				self.crash(a, b)
				return True
		return False


		
	def explosion_push(self, explosion, floater):
		"""The push of an explosion.  The rest of the effect is handled by the
		collision branching, which continues."""
		force = (explosion.force / 
				not0(dist2(explosion, floater)) * explosion.radius ** 2)
		dir = floater.pos.get_angle_between(explosion.pos)
		accel = force / not0(floater.mass)
		floater.delta += Vec2d(0,0).rotatedd(dir, accel) / explosion.fps
		
	def crash(self, a, b):
		if soundModule:
			setVolume(hitSound.play(), a, b)
		hpA = a.hp
		hpB = b.hp
		if hpB > 0: a.takeDamage(hpB, b)
		if hpA > 0: b.takeDamage(hpA, a)

	def minDistFromOthers(self, floater):
		mindist = 100000
		for otherfloater in self.planets:
			distance = floater.pos.get_distance(otherfloater.pos)
			if distance < mindist:
				mindist = distance
		return mindist

class SolarA1(StarSystem):
	tinyFighters = []
	maxFighters = 15
	respawnTime = 30
	fightersPerMinute = 2
	g=5000
	def __init__(self, universe, name, location ,numPlanets = 10, numStructures = 2, boundrad = 30000, edgerad= 60000):
		StarSystem.__init__(self, universe, location,boundrad, edgerad)
		self.star = (Star( self, Vec2d(0,0), radius = randint(2000,5000), image = None)) # the star
		#place player:
		angle = randint(0,360)
		self.location = location
		self.planets.append(self.star)
		self.star.numShips = 0
		self.add(self.star)
		self.name = name
		
		#add planets:

		for i in range(numPlanets):
			angle = randint(0,360)
			distanceFromStar = randint(self.star.radius + 5000, self.boundrad-5000)
			color = randint(40,200),randint(40,200),randint(40,200)
			radius = randint(500,900)
			mass = randnorm(radius * 10, 800)
			startpos = Vec2d(distanceFromStar * cos(angle), distanceFromStar * sin(angle))
			startdir = startpos.get_angle_between(self.star.pos) - 90
			accel = ((self.g * mass) / distanceFromStar) / 10
			# startdelta = Vec2d(0,0).rotatedd(startdir, accel) # preps for gravity sensitive planets
			startdelta = Vec2d(0,0)
			planet = Planet(self, startpos, startdelta ,self.g,radius = radius, mass = mass, color = color)
			
			mindistance = self.minDistFromOthers(planet)
			if mindistance > (radius * 6):
				self.planets.append(planet)
			else:
				i-=1
			# d+= 1200

		for i in range(numStructures):
			angle = randint(0,360)
			distanceFromStar = randint(self.boundrad-5000, self.boundrad)
			color = randint(0,100),randint(0,100),randint(0,100)
			radius = randint(400,500)
			self.add(Structure( self, Vec2d(distanceFromStar * cos(angle), distanceFromStar * sin(angle)), color, radius))

		radius = randint(500,700)
		gateway1 = Gateway(self, Vec2d(10000,10000), radius)
		gateway2 = Gateway(self, Vec2d(-10000,-10000), radius)

		gateway1.setSister(gateway2)
		gateway2.setSister(gateway1)

		self.add(gateway1)
		self.add(gateway2)

				
		for planet in self.planets:
			planet.numShips = 0
			# planet.ships = pygame.sprite.Group()
			planet.respawn = 30
			self.add(planet)


		


		
	

	
