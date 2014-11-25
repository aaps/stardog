#solarSystem.py

from utils import *
from floaters import *
from spaceship import *
from strafebat import *
from tinyFighter import *
from planet import *
from gui import *
import stardog

class SolarSystem:
	"""A SolarSystem holds ships and other floaters."""
	boundries = ((-30000, 30000), (-30000, 30000))
	drawEdgeWarning = False
	def __init__(self, game):
		self.game = game
		self.floaters = pygame.sprite.Group()
		self.ships = pygame.sprite.Group()
		self.specialOperations = []
		self.onScreen = []
		self.bg = BG(self.game) # the background layer
		pygame.mixer.music.load("res/sound/space music.ogg")
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(.15)
		
		
	def update(self):
		"""Runs the game."""
		self.floaters.update()
		
		#collision:
		# TODO: sort lists to minimize collision tests.
		floaters = self.floaters.sprites()
		for i in range(len(floaters)):
			for j in range(i + 1, len(floaters)):
				collide(floaters[i], floaters[j])
				#see collide() at bottom of this module.
				
		#keep ships in system for now:
		edge = self.boundries
		if self.drawEdgeWarning:
			self.drawEdgeWarning -= 1. / self.game.fps
			if self.drawEdgeWarning <=0:
				self.drawEdgeWarning = False
				
		for floater in self.floaters:
			if floater.x < edge[0][0] and floater.dx < 0 \
			or floater.x > edge[0][1] and floater.dx > 0:
				if isinstance(floater, Ship):
					floater.dx = 0
					if floater == self.game.player:
						self.drawEdgeWarning = 1
				else:
					floater.kill()
			if floater.y < edge[1][0] and floater.dy < 0 \
			or floater.y > edge[1][1] and floater.dy > 0:
				if isinstance(floater, Ship):
					floater.dy = 0
					if floater == self.game.player:
						self.drawEdgeWarning = self.game.fps
				else:
					floater.kill()
					
		#list floaters that are on screen now:
		self.onScreen = []
		offset = (self.game.player.x - self.game.width / 2, 
				self.game.player.y - self.game.height / 2)
		for floater in self.floaters:
			r = floater.radius
			if (r + floater.x > offset[0] \
				and floater.x - r < offset[0] + self.game.width)\
			and (r + floater.y > offset[1] \
				and floater.y - r < offset[1] + self.game.height):
					self.onScreen.append(floater)
					
		#do any special actions that don't fit elsewhere:
		#(currently just laser collisions)
		for function in self.specialOperations:
			function()
		self.specialOperations = []
		
	def draw(self, surface, offset):
		self.bg.draw(surface, self.game.player)
		for floater in self.onScreen:
				floater.draw(surface, offset)
		
	def add(self, floater):
		"""adds a floater to this game."""
		self.floaters.add(floater)
		if isinstance(floater, Ship):
			self.ships.add(floater)
		
	def empty(self):
		self.ships.empty()
		self.floaters.empty()

class SolarA1(SolarSystem):
	tinyFighters = []
	maxFighters = 15
	respawnTime = 30
	fightersPerMinute = 2
	def __init__(self, game, player, numPlanets = 10):
		SolarSystem.__init__(self, game)
		self.sun = (Sun( game, 0, 0, radius = 2000, mass = 180000, \
					color = (255, 255, 255), image = None)) # the star
		#place player:
		angle = randint(0,360)
		distanceFromSun = randint(8000, 18000)
		player.x = distanceFromSun * cos(angle)
		player.y = distanceFromSun * sin(angle)
		self.add(self.sun)
		self.planets = []
		#add planets:
		d = 5000
		for i in range(numPlanets):
			angle = randint(0,360)
			distanceFromSun = randint(d, d + 1200)
			color = randint(40,255),randint(40,255),randint(40,255)
			radius = randint(100,500)
			mass = randnorm(radius * 10, 800)
			self.planets.append(Planet(game, distanceFromSun * cos(angle), \
				distanceFromSun * sin(angle), radius = radius, mass = mass, \
				color = color))
			self.add(self.planets[i])
			d+= 1200
				
		for planet in self.planets:
			planet.numShips = 0
			planet.ships = pygame.sprite.Group()
			planet.respawn = 30
			self.add(planet)
		self.fighterTimer = 60
			
	def update(self):
		SolarSystem.update(self)
		#enemy respawning:
		for planet in self.planets:
			if not planet.ships.sprites():
				if planet.respawn > 0:#countdown the timer
					planet.respawn -= 1. / self.game.fps
					continue
				else:
					#respawn now!
					planet.respawn = self.respawnTime #reset respawn timer
					planet.numShips += 1
					for i in range(planet.numShips):
						angle = randint(0, 360)
						x = planet.x + cos(angle) * (planet.radius + 300)
						y = planet.y + sin(angle) * (planet.radius + 300)
						ship = Strafebat(self.game, x, y, color = planet.color)
						planet.ships.add(ship)
						self.add(ship)
						ship.planet = planet
		#tiny fighters
		if self.fighterTimer <= 0 and len(self.tinyFighters) < self.maxFighters:
			numSpawn = randint(1,3)
			for i in range(numSpawn):
				angle = randint(0,360)
				distance = randint(1000, 4000)
				x = distance * cos(angle) + self.game.player.x
				y = distance * sin(angle) + self.game.player.y
				fighter = TinyFighter(self.game, x, y, self.game.player.dx, 
									self.game.player.dy)
				self.add(fighter)
				self.tinyFighters.append(fighter)					
				self.fighterTimer = 60 / self.fightersPerMinute
		else:
			self.fighterTimer -= 1. / self.game.fps
		
	
def collide(a, b):
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
			if  sign(b.x - a.x) == sign(b.dx - a.dx) \
			and sign(b.y - a.y) == sign(b.dy - a.dy):# moving away from planet.
				return False
			# planet/ship
			if isinstance(b, Ship):
				planet_ship_collision(a, b)
				return True
			#planet/part
			if isinstance(b, Part) and b.parent == None:
				planet_freePart_collision(a, b)
				return True
			#planet/planet
			if isinstance(b, Planet):
				planet_planet_collision(a,b)
				return True
				
		if isinstance(b, Explosion): a,b = b,a
		if isinstance(a, Explosion):
			explosion_push(a,b)
			#but don't return!
		#shield ship/?
		if isinstance(b, Ship) and b.hp > 0: a,b = b,a
		if isinstance(a, Ship) and a.hp > 0:
			#shield ship/free part
			if isinstance(b, Part) and b.parent == None:
				ship_freePart_collision(a, b)
				return True
			#crash against ship's shields, if any:
			hit = False
			if b.hp >= 0 and (sign(b.x - a.x) == - sign(b.dx - a.dx) \
							or sign(b.y - a.y) == - sign(b.dy - a.dy)):
				# moving into ship, not out of it.
				crash(a,b)
				hit = True
				#if this ship no longer has shields, start over:
				if a.hp <= 0:
					collide(a, b)
					return True
			#shield ship/no shield ship (or less shield than this one)
			if isinstance(b, Ship) and b.hp <= 0:
				for part in b.parts:
					if collide(a, part):
						#if that returned true, everything
						#should be done already.
						return True
			return hit

		#ship / ?
		if isinstance(b, Ship): a,b = b,a
		if isinstance(a, Ship):
			#ship/free part
			if isinstance(b, Part) and b.parent == None:
				ship_freePart_collision(a, b)
				return True
							
			#recurse to ship parts
			hit = False
			for part in a.parts:
				if collide(b, part):#works for ship/ship, too.
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
			crash(a, b)
			return True
	return False

def planet_ship_collision(planet, ship):
	angle = atan2(planet.y - ship.y, planet.x - ship.x)
	dx, dy = rotate(ship.dx, ship.dy, angle)
	speed = sqrt(dy ** 2 + dx ** 2)
	if speed > planet.LANDING_SPEED:
		if planet.damage.has_key(ship):
			damage = planet.damage[ship]
		else:
			if soundModule:
				setVolume(hitSound.play(), planet, planet.game.player)
			#set damage based on incoming speed and mass.
			damage = speed * ship.mass * planet.PLANET_DAMAGE
		for part in ship.parts:
			if collisionTest(planet, part):
				temp = part.hp
				part.takeDamage(damage, planet)
				damage -= temp
				if damage <= 0:
					r = ship.radius + planet.radius
					temp = ship.dx * -(ship.x - planet.x) / r \
							+ ship.dy * -(ship.y - planet.y) / r
					ship.dy = ship.dx * (ship.y - planet.y) / r \
							+ ship.dy * -(ship.x - planet.x) / r
					ship.dx = temp
					if planet.damage.has_key(ship):
						del planet.damage[ship]
					return
		if damage > 0:
			planet.damage[ship] = damage
	else:
		#landing:
		if ship == planet.game.player and not ship.landed:
			planet.game.pause = True
			ship.landed = planet
			ship.game.menu.parts.reset()
		ship.dx, ship.dy = planet.dx, planet.dy

def planet_freePart_collision(planet, part):
	part.kill()
	planet.inventory.append(part)
	
def planet_planet_collision(a, b):
	if a.mass > b.mass:
		b.kill()
	else:
		a.kill()
		
def ship_freePart_collision(ship, part):
	part.kill()
	ship.inventory.append(part)
	if ship.game.player == ship:
		ship.game.menu.parts.inventoryPanel.reset() #TODO: make not suck
	
def explosion_push(explosion, floater):
	"""The push of an explosion.  The rest of the effect is handled by the
	collision branching, which continues."""
	force = (explosion.force / 
			not0(dist2(explosion, floater)) * explosion.radius ** 2)
	dir = atan2(floater.y - explosion.y, floater.x - explosion.x)
	accel = force / not0(floater.mass)
	floater.dx += accel * cos(dir) / explosion.game.fps
	floater.dy += accel * sin(dir) / explosion.game.fps
	
def crash(a, b):
	if soundModule:
		setVolume(hitSound.play(), a, b)
	hpA = a.hp
	hpB = b.hp
	if hpB > 0: a.takeDamage(hpB, b)
	if hpA > 0: b.takeDamage(hpA, a)
	
