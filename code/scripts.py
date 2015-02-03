#scripts.py

from utils import *
from pygame.locals import *
from floaters import *
import stardog

class Controllable(object):
	# this will take the place of ship script update
	

	def __init__(self, active=True):
		self.active = active
		self.scripts = []


	def addScript(self, script):
		self.scripts.append(script)

	def setActive(self):
		self.active = True

	def setInactive(self):
		self.active = False

	def toggleActive(self):
		self.active = not self.active

	def update(self):
		print self
		if len(self.scripts) > 0 and self.active:
			for script in self.scripts:
				script.update(self)

class Script(object):
	def __init__(self, game):
		self.game = game
		self.bindings = []
		self.keys = game.keys
	
	def update(self, ship):

		for binding in self.bindings:
			if self.keys[binding[0]] == 1:

				if binding[2]:
					if binding[3]:
						self.bindings[self.bindings.index(binding)] = (binding[0], binding[1],binding[2], False)
						binding[1]()
				else:
					binding[1]()
			elif self.keys[binding[0]] == 0:
				if binding[2]:
					self.bindings[self.bindings.index(binding)] = (binding[0], binding[1],binding[2], True)

	def agent(self, state):
		return None

	def initbind(self, key, function, toggle):
		"""binds function to key so function will be called if key is pressed.
		Can bind more than one function to a key, and more than one key to
		a function."""
		key = key % 322
		if not self.bindings.count((key, function,toggle, True)):
			self.bindings.append((key, function, toggle, True))	
	
	def bind(self, key, function):
		"""binds function to key so function will be called if key is pressed.
		Can bind more than one function to a key, and more than one key to
		a function."""
		key = key % 322
		if not self.bindings.count((key, function,False, True)):
			self.bindings.append((key, function,False, True))
			
	def unbind(self, key, function):
		"""removes the exact binding key > function"""
		if self.bindings.count((key, function)):
			self.bindings.remove((key, function))
			
	def freeKey(self, key):
		"""removes all bindings with the given key."""
		self.bindings = [x for x in self.bindings if x[0] != key]

	def setAllUnpressed(self):

		for key in self.keys:
			self.keys[key] = False

		for bind in self.bindings:
			bind = (bind[0], bind[1], False, bind[3])

#InputScript is controlled by the keyboard:
class InputScript(Script):
	"""A script controlled by the keyboard."""
	mouseControl = True
	def __init__(self, game):
		Script.__init__(self, game)
		# self.active = True
		
		self.mouse = game.mouse
		
		self.center =self.game.width / 2, self.game.height / 2

	def update(self, ship):
		"""decides what to do each frame."""
		# if self.active:
		for binding in self.bindings:
			if self.keys[binding[0]] == 1:

				if binding[2]:
					if binding[3]:
						self.bindings[self.bindings.index(binding)] = (binding[0], binding[1],binding[2], False)
						binding[1]()
				else:
					binding[1]()
			elif self.keys[binding[0]] == 0:
				if binding[2]:
					self.bindings[self.bindings.index(binding)] = (binding[0], binding[1],binding[2], True)
						

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



	# def toggleActive(self):
	# 	if self.active:
	# 		self.active = False
	# 	else:
	# 		self.active = True


		

class AIScript(Script):
	interceptSpeed = 200. / 3
	acceptableError = 10
	"""A scripts with basic physics calculation functions.  Virtual."""
	def update(self, ship):
		# find closest ship:
		if not ship.radars[-1].enabled:
			ship.radars[-1].toggle()
		ships = ship.radars[-1].detected
		curtarget, distance = self.closestShip(ship, ships)
				
		if ship.guns:
			shootingRange = 400 ** 2
			(ship.guns[0].bulletRange * ship.guns[0].speed) ** 2 / 2
		else: #without guns kamikaze. 
			if self.turnTowards(ship, curtarget):
				ship.forward()
			return
		if distance < shootingRange:
			if self.turnTowards(ship, curtarget):
				ship.shoot()
			return

		if dist(ship.dx, ship.dy, curtarget.dx, curtarget.dy) < self.interceptSpeed\
			or sign(ship.dx - curtarget.dx) == sign(ship.x - curtarget.x) \
			or sign(ship.dy - curtarget.dy) == sign(ship.y - curtarget.y):
			#speed up:
			if self.turnTowards(ship, curtarget):
				ship.forward()
		else:
			#slow down:
			if self.turnTowards(ship, curtarget, 180):
				ship.forward()
				
	def closestShip(self, ship, ships):
		"""finds the closest ship to this one."""
		curtarget = ships[0]
		distance = dist2(ship, curtarget)
		for s in ships:
			if dist2(s, ship) < distance and s != ship:
				distance = dist2(s,ship)
				curtarget = s
		return curtarget, distance
	
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
			angleToTarget = atan2(target.pos.y - ship.pos.y, target.pos.x - ship.pos.x) - ship.dir
		else:#target is a point
			angleToTarget = atan2(target[1] - ship.pos.y, target[0] - ship.pos.x) - ship.dir
			
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
		return sqrt((ship.pos.x + ship.delta.x - target.pos.x - target.delta.x)**2 \
					+ (ship.pos.y + ship.delta.y - target.pos.y - target.delta.y)**2) \
				- sqrt((ship.pos.x - target.pos.x)**2 + (ship.pos.y - target.pos.y)**2)
	
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
			speed = sqrt( dist(ship.pos.x, ship.pos.y, target.pos.x, target.pos.y) / not0(accel))
		time = dist(ship.pos.x, ship.pos.y, target.pos.x, target.pos.y) / not0(speed)
		dummy = Ballistic(target.pos, \
						target.delta - ship.delta)
		pos = self.predictBallistic(dummy, time)
		angle = atan2(pos[1] - ship.pos.y, pos[0] - ship.pos.x)
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
		time = dist(ship.pos.x, ship.pos.y, target.pos.x, target.pos.y) / speed
		dummy = Ballistic(target.pos, \
						target.delta - ship.delta)
		pos = self.predictBallistic(dummy, time)
		angle = atan2(pos[1] - ship.pos.y, pos[0] - ship.pos.x)
		if self.turn(ship, angle):
			ship.shoot()
	
	def predictBallistic(self, floater, time):
		"""predictBallistic(floater, time) ->
		the point (x,y) the floater will be in after time seconds if there is 
		no acceleration."""
		return (floater.pos.x + time * floater.delta.x, \
				floater.pos.y + time * floater.delta.y)
		
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
		time = sqrt(dist(ship.pos.x, ship.pos.y, pos[0], pos[1]) / accel)
		if not curtarget:
			dummy = Ballistic(pos[0], pos[1], 0, 0)
		else:
			dummy = Ballistic(pos[0] + target.pos.x, pos[1] + target.pos.y,\
								target.delta.x, target.delta.y)
		
		turnTime = ship.moment / ship.torque * 180
		angle = atan2(dummy.pos.y - ship.pos.y, dummy.pos.x - ship.pos.x)
		distance = dist(dummy.pos.x, dummy.pos.y, ship.pos.x, ship.pos.y)
		relativeSpeed = self.relativeSpeed(ship, dummy)
		if - relativeSpeed / not0(accel) + turnTime > distance / abs(not0(relativeSpeed)):
			#slow down
			if self.turn(ship, angle + 180):
				ship.forward()
		else:
			self.intercept(ship, dummy, 500)

def makeConsoleBindings(script, game):
	script.initbind(K_6, game.player.toggleActive, True)
	script.initbind(K_6, game.chatconsole.toggleActive, True)

def makeMenuBindings(script, game):
	script.initbind(K_RETURN, game.player.toggleActive, True)
	script.initbind(K_RETURN, game.menu.toggleActive, True)

		
def makeGameBindings(script, game):
	script.initbind(K_6, game.chatconsole.toggleActive, True)
	script.initbind(K_6, game.player.toggleActive, True)
	script.initbind(K_RETURN, game.menu.toggleActive, True)
	script.initbind(K_RETURN, game.player.toggleActive, True)

	script.initbind(K_MINUS, game.radarfield.zoomInRadar,False)
	script.initbind(K_EQUALS, game.radarfield.zoomOutRadar,False)
	
def makePlayerBindings(script, ship):
	
	script.initbind(K_DOWN, ship.reverse,False)
	script.initbind(K_UP, ship.forward,False)
	script.initbind(K_RIGHT, ship.turnRight,False)
	script.initbind(K_LEFT, ship.turnLeft,False)
	script.initbind(K_RCTRL, ship.shoot,False)
	


	script.initbind(K_s, ship.reverse,False)
	script.initbind(K_r, ship.toggleRadar,True)
	script.initbind(K_t, ship.targetNextShip,True)
	script.initbind(K_y, ship.targetPrefShip,True)
	script.initbind(K_g, ship.targetNextPlanet,True)
	script.initbind(K_h, ship.targetPrefPlanet,True)
	script.initbind(K_b, ship.targetNextPart,True)
	script.initbind(K_n, ship.targetPrefPart,True)
	script.initbind(K_j, ship.toggleGatewayFocus,True)
	script.initbind(K_w, ship.forward,False)

	script.initbind(K_e, ship.left,False)
	script.initbind(K_q, ship.right,False)
	script.initbind(K_d, ship.turnRight,False)
	script.initbind(K_a, ship.turnLeft,False)
	script.initbind(K_SPACE, ship.shoot,False)
	script.initbind(K_m, ship.launchMines,False)
	
	
	
	
	
	
	
	
	
	
	
