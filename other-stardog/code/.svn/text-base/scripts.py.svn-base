#scripts.py

from utils import *
from pygame.locals import *
from floaters import *

class Script:
	def __init__(self, game):
		self.game = game

	def update(self, ship, dt):
		pass

	def agent(self, state):
		return None

#InputScript is controlled by the keyboard:
class InputScript(Script):
	"""A script controlled by the keyboard."""
	mouseControl = True
	def __init__(self, game):
		Script.__init__(self, game)
		self.keys = game.keys
		self.mouse = game.mouse
		self.bindings = []
		self.center =self.game.width / 2, self.game.height / 2

	def update(self, ship, dt):
		"""decides what to do each frame."""
		for binding in self.bindings:
			if self.keys[binding[0]]:
				binding[1]()
		if self.game.mouseControl:
			dir = angleNorm(atan2(self.game.mouse[0][1] - self.center[1], \
								  self.game.mouse[0][0] - self.center[0])\
								  -ship.dir)

			if dir < 0:
				ship.turnLeft(dir)
			elif dir > 0:
				ship.turnRight(dir)
			if self.game.mouse[3]:
				ship.forward()
			if self.game.mouse[1]:
				ship.shoot()

	def bind(self, key, function):
		"""binds function to key so function will be called if key is pressed.
		Can bind more than one function to a key, and more than one key to
		a function."""
		key = key % 322
		if not self.bindings.count((key, function)):
			self.bindings.append((key, function))

	def unbind(self, key, function):
		"""removes the exact binding key > function"""
		if self.bindings.count((key, function)):
			self.bindings.remove((key, function))

	def freeKey(self, key):
		"""removes all bindings with the given key."""
		self.bindings = [x for x in self.bindings if x[0] != key]

class AIScript(Script):
	"""This is the base script for AI ships.  A subclass of this script can
	override any subset of its methods to change behavior.

	The default update() calls,
	in order, avoidPlanet(), attack(), pursue(), and idle(), calling the each
	option only if the previous returned false.  This way a subclass can
	override"""
	shootingRange = 400 ** 2
	safetyDistance = 20
	def update(self, ship, dt):
		# find closest ship:
		enemy = self.findClosestEnemy(ship, ship.system.ships)
		planet = self.findClosestPlanet(ship, ship.system.planets)

		if planet and self.avoidPlanet(ship, planet):
			return
		elif enemy and self.attack(ship, enemy):
			return
		elif enemy and self.pursue(ship, enemy):
			return
		elif self.idle(ship):
			return

		assert("ship failed to idle?")

	def attack(self, ship, enemy):
		"""if within shooting range, turn at enemy and shoot it."""
		if ship.guns and dist2(ship, enemy) < self.shootingRange ** 2:
				if self.turnToTarget(ship, enemy):
					ship.shoot()
				return True
		return False

	def pursue(self, ship, enemy):
		"""Makes a guess where self can intercept enemy, and flies there"""
		enemyAcceleration = enemy.forwardThrust / enemy.mass
		if not enemy.thrusting:
			enemyAcceleration = 0

		# predicted time in seconds before self can reach enemy is the time it
		# would take to accelerate to it:
		t = sqrt(sqrt(dist2(ship, enemy)) / not0(ship.forwardThrust / ship.mass))

		# target position is the position the enemy will be at at t if it keeps
		# doing what it's doing now:
		targetX = (enemy.x + t * (enemy.dx - ship.dx)
					+ t * t * enemyAcceleration * cos(enemy.dir))
		targetY = (enemy.y + t * (enemy.dy - ship.dy)
					+ t * t * enemyAcceleration * sin(enemy.dir))
		target = int(targetX), int(targetY)
		self.flyTowards(ship, (targetX, targetY))
		ship.goal = target
		return True

	def avoidPlanet(self, ship, planet):#find nearest planet:
		"""if close to a planet and headed closer, thrust perpendicular to it."""
		distance = sqrt(dist2(ship,planet))
		#see if our current trajectory will hit the planet:
		missDist = planet.radius + ship.radius + self.safetyDistance #min safe distance.
		dangerAngle = asin((missDist) / max(distance, missDist))	#min angle to miss planet by.
		planetDir = relativeDir(ship, planet) 		#direction of the planet.
		currentHeadingAngle = atan2(ship.dy, ship.dx) 	#our inertia vector.
		speed2 = ship.dx**2 + ship.dy**2 			# our inertia speed squared.

		if dangerAngle < 0 or dangerAngle > 90:
			dangerAngle = 90

		#if too close already
		#or (heading towards planet
		#	 and safe distance < 2 x distance it should take to stop)
		if (distance < missDist
		or planetDir - dangerAngle < currentHeadingAngle < planetDir + dangerAngle
			and (distance - missDist) / 2
				< speed2 / ((ship.forwardThrust / ship.mass)
							 - planet.mass * planet.g / (distance / 2)**2)):
			#we're headed towards the planet!  Thrust perpendicular to it!
			if angleNorm(currentHeadingAngle - planetDir) < 0:
				self.flyAtDir(ship, planetDir - 90)
			else:
				self.flyAtDir(ship, planetDir + 90)
			return True
		return False

	def idle(self, ship):
		self.flyTowards(ship, getPos(ship.planet))

	def flyTowards(self, ship, point):
		"""make the ship fly towards an absolute point."""
		return self.flyAtDir(ship, atan2(point[1] - ship.y, point[0] - ship.x))

	def flyAtDir(self, ship, dir):
		"""make the ship fly towards an absolute angle."""
		if self.turnToDir(ship, dir):
			ship.forward()
			return True
		return False

	def turnToDir(self, ship, dir, threshold = 30):
		"""turn self towards the absolute direction.  Returns true if the
		result is within threshold of the goal direction."""
		dirDif = angleNorm(dir - ship.dir)
		if dirDif < 0:
			ship.turnLeft(dirDif)
		elif dirDif > 0:
			ship.turnRight(dirDif)
		if -threshold < dirDif < threshold:
			return True
		return False


	def turnToTarget(self, ship, target, offset = 0):
		"""turn the ship to face a target.  If an offset is given then turn
		that many degrees past the target.  Returns true if result is within
		30 degrees of the goal."""
		return self.turnToDir(ship,
						atan2(target.y - ship.y, target.x - ship.x) + offset)

	def predictBallistic(self, floater, time):
		"""predictBallistic(floater, time) ->
		the point (x,y) the floater will be in after time seconds if there is
		no acceleration."""
		return (floater.x + time * floater.dx, \
				floater.y + time * floater.dy)

	def speedTowards(self, ship, target):
		"""projects your relative speed onto the vector to the target,
		e.g. how fast you are approaching a thing.  Does not care if you will
		hit it."""
		#theta is the angle between relative angle and current velocity vector.
		theta = (atan2(ship.dy - target.dy, ship.dx - target.dx)
				- relativeDir(ship,target))
		return (  sqrt((ship.dx - target.dx) ** 2 + (ship.dy - target.dy) ** 2)
			    * cos(theta))

	def findClosestPlanet(self, ship, planets):
		closest = None
		distance2 = float("inf")
		for planet in planets:
			if dist2(ship,planet) < distance2:
				distance2 = dist2(ship,planet)
				closest = planet
		return closest

	def findClosestEnemy(self, ship, ships):
		"""finds closest ship that is a different race."""
		closest = None
		distance2 = float("inf")
		for enemy in ships:
			if enemy.race != ship.race and dist2(ship,enemy) < distance2:
				distance2 = dist2(ship,enemy)
				closest = enemy
		return closest