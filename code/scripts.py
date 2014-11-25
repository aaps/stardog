#scripts.py

from utils import *
from pygame.locals import *
from floaters import *
import stardog

class Script:
	def __init__(self, game):
		self.game = game
	
	def update(self, ship):
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

	def update(self, ship):
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
	interceptSpeed = 200. / 3
	acceptableError = 5
	"""A scripts with basic physics calculation functions.  Virtual."""
	def update(self, ship):
		# find closest ship:
		ships = ship.game.curSystem.ships.sprites()
		target, distance = self.closestShip(ship, ships)
				
		if ship.guns:
			shootingRange = 400 ** 2
				#(ship.guns[0].bulletRange * ship.guns[0].speed) ** 2 / 2
		else: #without guns kamikaze. 
			if self.turnTowards(ship, target):
				ship.forward()
			return
		if distance < shootingRange:
			if self.turnTowards(ship, target):
				ship.shoot()
			return

		if dist(ship.dx, ship.dy, target.dx, target.dy) < self.interceptSpeed\
			or sign(ship.dx - target.dx) == sign(ship.x - target.x) \
			or sign(ship.dy - target.dy) == sign(ship.y - target.y):
			#speed up:
			if self.turnTowards(ship, target):
				ship.forward()
		else:
			#slow down:
			if self.turnTowards(ship, target, 180):
				ship.forward()
				
	def closestShip(self, ship, ships):
		"""finds the closest ship to this one."""
		target = ships[0]
		distance = dist2(ship, target)
		for s in ships:
			if dist2(s, ship) < distance and s != ship:
				distance = dist2(s,ship)
				target = s
		return target, distance
	
	def turn(self, ship, angle):
		angle = angleNorm(angle - ship.dir)
		if angle < 0:
			ship.turnLeft()
		elif angle > 0:
			ship.turnRight()
		return -self.acceptableError < angle < self.acceptableError
		
	
	def turnTowards(self, ship, target, angleOffset = 0):
		"""tells ship to turn toward the target.  Target can be a Floater or
		point. 
		returns True if the ship is pointed within self.acceptableError degrees 
		of the target."""
		if isinstance(target, Floater):
			angleToTarget = atan2(target.y - ship.y, target.x - ship.x) - ship.dir
		else:#target is a point
			angleToTarget = atan2(target[1] - ship.y, target[0] - ship.x) - ship.dir
			
		angleToTarget = (angleToTarget - angleOffset + 180) % 360 - 180
		if angleToTarget < 0:
			ship.turnLeft()
		elif angleToTarget > 0:
			ship.turnRight()
		return -self.acceptableError < angleToTarget < self.acceptableError
	
	def relativeSpeed(self, ship, target):
		"""relativeSpeed2(ship, target) -> the relative speed between two 
		floaters. Note that this is negative if they are getting closer."""
		#distance next second - distance this second (preserves sign):
		return sqrt((ship.x + ship.dx - target.x - target.dx)**2 \
					+ (ship.y + ship.dy - target.y - target.dy)**2) \
				- sqrt((ship.x - target.x)**2 + (ship.y - target.y)**2)
	
	def intercept(self, ship, target, relativeSpeedLimit = 0):
		"""intercept(ship, target) -> ship moves to intercept target. 
		Call this every frame to intercept.
		To almost intercept, monitor distance and 
		do something else when close."""
		if relativeSpeedLimit:
			speed = relativeSpeedLimit
		else: 
			#roughly guess speed:
			accel = ship.forwardThrust / ship.mass
			speed = sqrt( dist(ship.x, ship.y, target.x, target.y) / not0(accel))
		time = dist(ship.x, ship.y, target.x, target.y) / not0(speed)
		if self.game.debug: print time, ship
		dummy = Ballistic(target.x, target.y, \
						target.dx - ship.dx, target.dy - ship.dy)
		pos = self.predictBallistic(dummy, time)
		angle = atan2(pos[1] - ship.y, pos[0] - ship.x)
		if self.turn(ship, angle):
			if not relativeSpeedLimit\
			or self.relativeSpeed(ship, target) > - relativeSpeedLimit:
				ship.forward()
			
		
			
	def straightShot(self, ship, target):
		if self.turnTowards(ship, target):
			ship.shoot() #shoot.
		
	def interceptShot(self, ship, target):
		if not ship.guns:
			return
		speed = ship.guns[0].speed
		time = dist(ship.x, ship.y, target.x, target.y) / speed
		dummy = Ballistic(target.x, target.y, \
						target.dx - ship.dx, target.dy - ship.dy)
		pos = self.predictBallistic(dummy, time)
		angle = atan2(pos[1] - ship.y, pos[0] - ship.x)
		if self.turn(ship, angle):
			ship.shoot()
	
	def predictBallistic(self, floater, time):
		"""predictBallistic(floater, time) ->
		the point (x,y) the floater will be in after time seconds if there is 
		no acceleration."""
		return (floater.x + time * floater.dx, \
				floater.y + time * floater.dy)
		
	def predictTimeMin(self, ship, distance):
		"""predictTimeMin(ship, distance) ->
		the time it would take this ship to travel distance
		accelerating the whole way. Assumes there is no starting velocity.
		Note: this method ends with very high velocity.  
		See also predictTimeStop()."""
		if isinstance(point, Floater):
			point = point.x, point.y
		accel = ship.forwardThrust / ship.mass
		return sqrt(distance / accel)
		
	def predictTimeStop(self, ship, distance, speed = 0):
		"""predictTimeStop(ship, distance) ->
		the time it would take this ship to travel distance
		accelerating the first half and deccelerating the second half. 
		Assumes there is no starting velocity."""
		accel = ship.forwardThrust / ship.mass
		if accel == 0:
			return 0
		if speed == 0:
			return sqrt(distance / 2 / accel) * 2
		
	def goto(self, ship, pos, target = None):
		"""directs the ship to fly to the position. 
		If target, pos is a position relative to the target."""
		accel = ship.forwardThrust / ship.mass
		time = sqrt(dist(ship.x, ship.y, pos[0], pos[1]) / accel)
		if not target:
			dummy = Ballistic(pos[0], pos[1], 0, 0)
		else:
			dummy = Ballistic(pos[0] + target.x, pos[1] + target.y,\
								target.dx, target.dy)
		
		turnTime = ship.moment / ship.torque * 180
		angle = atan2(dummy.y - ship.y, dummy.x - ship.x)
		distance = dist(dummy.x, dummy.y, ship.x, ship.y)
		relativeSpeed = self.relativeSpeed(ship, dummy)
		if - relativeSpeed / not0(accel) + turnTime > distance / abs(not0(relativeSpeed)):
			#slow down
			if self.turn(ship, angle + 180):
				ship.forward()
		else:
			self.intercept(ship, dummy, 500)
		

	
	
	
	
	
	
	
	
	
	
	
	
	