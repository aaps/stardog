#races.py

from utils import *
from strafebat import *
from planet import Sun

class Race:
	planets = []
	parts = []
	adjectives = []
	playerRepute = 0
	playerCredits = 0
	enemies = []
	allies = []
	ships = []
	shipScripts = []
	script = None

	def __init__(self, game, name, color = (255,0,0)):
		self.game = game
		self.name = name
		self.color = color
		self.targetPlanet = None

	def update(self, dt):
		#find geographic mean of planets in system:
		x,y = 0,0
		count = 0
		enemies = []
		for planet in self.game.curSystem.planets:
			if isinstance(planet, Sun):
				continue
			if planet.race == self:
				x += planet.x
				y += planet.y
				count += 1
			else:
				enemies.append(planet)
		if not enemies:
			print "%s owns the entire system!"%(self,)
			return
		if count:
			x /= count
			y /= count
		# set target to enemy closest to mean.
		self.targetPlanet = min(enemies, key = lambda p: dist(p.x,p.y,x,y))


	def updateShip(self, ship, dt):
		if self.targetPlanet:
			ship.planet = self.targetPlanet

	def updatePlanet(self, planet):
		#people reproduce:
		planet.population += (1 * planet.life * self.game.dt)
		
		if not planet.shipInProgress and len(self.ships)<=30:
			#start new ship
			angle = randint(0, 360)
			x = planet.x + cos(angle) * (planet.radius + 300)
			y = planet.y + sin(angle) * (planet.radius + 300)
			planet.shipInProgress = Strafebat(self.game,
									x, y, color = self.color, race = self)
			planet.shipValue = planet.shipInProgress.value
			print ("planet %s (pop %i, res %.3f) building new ship." 
					% (planet.name, planet.population, planet.resources))
		
		if planet.shipInProgress:
			planet.buildProgress += (planet.population / 1000. * planet.resources
									* self.game.dt / 60)
		
			if planet.buildProgress >= planet.shipValue:
				#complete ship construction
				planet.buildProgress = 0
				self.game.curSystem.add(planet.shipInProgress)
				planet.shipInProgress.planet = planet
				orbvel = sqrt(planet.g * self.game.curSystem.sun.mass * \
				(2/planet.distance - 1/planet.SMa))
				smi = planet.SMa * planet.p
				vx = orbvel * -planet.SMa * math.sin(planet.EccAn) / sqrt((smi * \
				math.cos(planet.EccAn)) ** 2 + (planet.SMa * math.sin(planet.EccAn)) ** 2)
				vy = orbvel * smi * math.cos(planet.EccAn) / sqrt((smi * math.cos(planet.EccAn))
				** 2 + (planet.SMa * math.sin(planet.EccAn)) ** 2)
				planetvel = rotate(vx, vy, planet.LPe)
				planet.shipInProgress.dx = planetvel[0]
				planet.shipInProgress.dy = planetvel[1]
				planet.shipInProgress = None




