#strafebat.py

from utils import *
from spaceship import *
from parts import *
from scripts import *
from adjectives import *

class Strafebat(Ship):
	strafeRadius = 250
	strafeDir = 1 #clockwise
	planet = None
	level = 3
	def __init__(self, game, x, y, color = (200,100,0), race = None):
		roll = rand()
		self.target = game.player
		self.circling = False
		Ship.__init__(self, game, x, y, script = StrafebatScript(game),
						color = color, race = race)
		self.baseBonuses['damageBonus'] = .5
		cockpit =StrafebatCockpit(game)
		gyro = Gyro(game)
		gun = StrafebatCannon(game)
		engine = Engine(game)
		generator = Generator(game)
		battery = Battery(game)
		shield = Shield(game)
		rCannon = RightCannon(game)
		lCannon = LeftCannon(game)
		for part in [cockpit, gyro, gun, engine, generator, battery, shield,
						rCannon, lCannon]:
			if rand() > .8:
				addAdjective(part)
				if rand() > .6:
					addAdjective(part)
			part.color = color
		self.addPart(cockpit)
		cockpit.addPart(gun, 0)
		cockpit.addPart(gyro, 2)
		gyro.addPart(engine, 1)
		gyro.addPart(generator, 0)
		if .9 < roll:
			generator.addPart(battery, 0)
			gyro.addPart(shield, 2)
		else:
			gyro.addPart(battery, 2)
		if .8 < roll < .9:
			generator.addPart(rCannon, 0)
		if .7 < roll < .8:
			battery.addPart(lCannon, 0)
		self.energy = self.maxEnergy

		self.strafeDir = choice((1,-1)) # whether self will strafe CW or CCW.


class StrafebatScript(AIScript):
	"""A scripts with basic physics calculation functions."""
	shootingRange = 600

	def pursue(self, ship, enemy):
		"""Makes a guess where self can intercept enemy, and flies there.
		Strafebats aim at a point near the enemy so that they strafe by."""
		enemyAcceleration = enemy.forwardThrust / enemy.mass
		if not enemy.thrusting:
			enemyAcceleration = 0
		relDir = relativeDir(ship, enemy)

		# predicted time in seconds before self can reach enemy is the time it
		# would take to accelerate to it:
		t = sqrt(sqrt(dist2(ship, enemy)) / not0(ship.forwardThrust / ship.mass))

		# target position is the position the enemy will be at at t if it keeps
		# doing what it's doing now:
		targetX = (enemy.x + t * (enemy.dx - ship.dx)
					+ t * t * enemyAcceleration * cos(enemy.dir)
					#strafebat special: don't run directly at them:
					+ cos(relDir + 90) * ship.strafeRadius * ship.strafeDir)
		targetY = (enemy.y + t * (enemy.dy - ship.dy)
					+ t * t * enemyAcceleration * sin(enemy.dir)
					#strafebat special: don't run directly at them:
					+ sin(relDir + 90) * ship.strafeRadius * ship.strafeDir)
		target = int(targetX), int(targetY)
		self.flyTowards(ship, (targetX, targetY))
		ship.goal = target
		return True

	def attack(self, ship, enemy):
		"""Predicts the enemies position and shoots at where it will be."""
		if ship.guns and dist2(ship, enemy) < self.shootingRange ** 2:
			speed = ship.guns[0].speed
			time = dist(ship.x, ship.y, enemy.x, enemy.y) / speed
			dummy = Ballistic(enemy.x - ship.x, enemy.y - ship.y,
							enemy.dx - ship.dx, enemy.dy - ship.dy)
			pos = self.predictBallistic(dummy, time)
			angle = atan2(pos[1], pos[0])
			if self.turnToDir(ship, angle):
					ship.shoot()
			return True
		return False

class StrafebatCockpit(Cockpit):
	pass
