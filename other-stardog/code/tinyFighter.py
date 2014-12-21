#tinyFighter.py


from utils import *
from spaceship import *
from parts import *
from scripts import *
from adjectives import *

class TinyFighter(Ship):
	strafeRadius = 100
	planet = None
	stage = 0
	timeOut = 30
	level = .5
	def __init__(self, game, x, y, dx = 0, dy = 0, color = (120, 180, 120)):
		self.target = game.player
		self.circling = False
		Ship.__init__(self, game, x, y, dx, dy,
						script = TinyFighterScript(game), color = color)
		self.baseBonuses['damageBonus'] = .5
		self.addPart(Drone(game))
		self.energy = self.maxEnergy
		self.inventory.append(randItem(self.game, self.level))


class TinyFighterScript(AIScript):
	"""a script for tiny fighters."""
	shootingRange = 400
	retreatRadius = 300
	interceptSpeed = 300

	def update(self, ship, dt):
		"""tiny fighter retreats if it gets too close and
		has a max pursue speed."""
		# find closest ship:
		enemy = self.game.player
		planet = self.findClosestPlanet(ship, ship.system.planets)

		if planet and self.avoidPlanet(ship, planet):
			return
		elif enemy and self.retreat(ship, enemy):
			return
		elif enemy and self.attack(ship, enemy):
			return
		elif (enemy and self.pursue(ship, enemy)):
			return
		elif self.idle(ship):
			return

		assert("ship failed to idle?")

	def idle(self, ship):
		pass	#no home planet to return to.

	def retreat(self, ship, enemy):
		"""if within shooting range, turn at enemy and shoot it."""
		if (dist2(ship, enemy) < self.retreatRadius ** 2
			or self.speedTowards(ship, enemy) > self.interceptSpeed):
				self.flyAtDir(ship, relativeDir(ship, enemy) + 180)
				return True
		return False