#spaceship.py

from utils import *
from parts import *
from partCatalog import *
from floaters import *
from pygame.locals import *
from adjectives import addAdjective
from skills import *

def makeFighter(game, x, y, dx = 0, dy = 0, dir = 270, script = None, \
				color = (255, 255, 255), player = False, system = None):
	"""starterShip(x,y) -> default starting ship at x,y."""
	if player:
		ship = Player(game, x, y, dx = dx, dy = dy, dir = dir, \
				script = script, color = color, system = system)
	else:
		ship = Ship(game, x, y, dx = dx, dy = dy, dir = dir, \
				script = script, color = color, system = system)
	cockpit = Fighter(game)
	gun = MachineGun(game)
	engine = Engine(game)
	shield = FighterShield(game)
	for part in [cockpit, gun, engine, shield]:
		part.color = color
	ship.addPart(cockpit)
	cockpit.addPart(engine, 3)
	cockpit.addPart(gun, 0)
	cockpit.addPart(shield, 2)
	ship.reset()
	ship.energy = ship.maxEnergy * .8
	ship.inventory.append(EmergencyEngine(game))
	return ship

def makeDestroyer(game, x, y, dx = 0, dy = 0, dir = 270, script = None, \
				color = (255, 255, 255), player = False, system = None):
	"""starterShip(x,y) -> default starting ship at x,y."""
	if player:
		ship = Player(game, x, y, dx = dx, dy = dy, dir = dir, \
				script = script, color = color, system = system)
	else:
		ship = Ship(game, x, y, dx = dx, dy = dy, dir = dir, \
				script = script, color = color, system = system)
	gyro = Gyro(game)
	generator = Generator(game)
	battery = Battery(game)
	cockpit = Destroyer(game)
	gun = RightLaser(game)
	engine = Engine(game)
	shield = Shield(game)
	for part in [gyro, generator, battery, cockpit, gun, engine, shield]:
		part.color = color
	ship.addPart(cockpit)
	cockpit.addPart(gun, 2)
	cockpit.addPart(battery, 3)
	cockpit.addPart(generator, 4)
	cockpit.addPart(gyro, 5)
	cockpit.addPart(shield, 6)
	gyro.addPart(engine, 1)
	ship.reset()
	ship.energy = ship.maxEnergy * .8
	ship.inventory.append(EmergencyEngine(game))
	return ship

def makeInterceptor(game, x, y, dx = 0, dy = 0, dir = 270, script = None, \
				color = (255, 255, 255), player = False, system = None):
	"""starterShip(x,y) -> default starting ship at x,y."""
	if player:
		ship = Player(game, x, y, dx = dx, dy = dy, dir = dir, \
				script = script, color = color, system = system)
	else:
		ship = Ship(game, x, y, dx = dx, dy = dy, dir = dir, \
				script = script, color = color, system = system)
	cockpit = Interceptor(game)
	gyro = Gyro(game)
	generator = Generator(game)
	battery = Battery(game)
	gun = LeftFlakCannon(game)
	gun2 = RightFlakCannon(game)
	missile = MissileLauncher(game)
	engine = Engine(game)
	engine2 = Engine(game)
	for part in [gyro, generator, battery, cockpit, gun, gun2, engine, engine2,
				missile]:
		part.color = color
	ship.addPart(cockpit)
	cockpit.addPart(missile, 0)
	cockpit.addPart(gun, 2)
	cockpit.addPart(gun2, 3)
	cockpit.addPart(generator, 4)
	cockpit.addPart(gyro, 5)
	generator.addPart(battery, 0)
	battery.addPart(engine, 0)
	gyro.addPart(engine2, 1)
	ship.reset()
	ship.energy = ship.maxEnergy * .8
	ship.inventory.append(EmergencyEngine(game))
	return ship

def playerShip(game, x, y, dx = 0, dy = 0, dir = 270, script = None, \
				color = (255, 255, 255), type = 'fighter', system = None):
	"""starterShip(x,y) -> default starting ship at x,y."""
	if type == 'destroyer':
		ship = makeDestroyer(game, x, y, dx, dy, dir,
				script, color, player=True, system = system)
	elif type == 'interceptor':
		ship = makeInterceptor(game, x, y, dx, dy, dir,
				script, color, player=True, system = system)
	else:
		ship = makeFighter(game, x, y, dx, dy, dir,
				script, color, player=True, system = system)
	#default controls:
	script.bind(K_DOWN, ship.reverse)
	script.bind(K_UP, ship.forward)
	script.bind(K_RIGHT, ship.turnRight)
	script.bind(K_LEFT, ship.turnLeft)
	script.bind(K_RCTRL, ship.shoot)
	script.bind(K_s, ship.reverse)
	script.bind(K_w, ship.forward)
	script.bind(K_e, ship.left)
	script.bind(K_q, ship.right)
	script.bind(K_d, ship.turnRight)
	script.bind(K_a, ship.turnLeft)
	script.bind(K_LCTRL, ship.shoot)
	script.bind(K_SPACE, ship.launchMissiles)

	return ship

class Ship(Floater):
	"""Ship(x, y, dx = 0, dy = 0, dir = 270,
	script = None, color = (255,255,255))
	script should have an update method that
	returns (moveDir, target, action)."""
	mass = 1
	moment = 0
	parts = []
	forwardEngines = []
	maxhp = 0
	hp = 0
	thrusting = False
	forwardThrust = 0
	reverseThrust = 0
	leftThrust = 0
	rightThrust = 0
	torque = 0
	reverseEngines = []
	leftEngines = []
	rightEngines = []
	guns = []
	missiles = []
	gyros = []
	tanks = []
	usingTank = None
	number = 0
	numParts = 0
	name = 'Ship'
	skills = []
	level = 1
	value = 0
	landed = False
	partEffects = []
	effects = []
	skillEffects = []
	partLimit = 8
	penalty = .1
	bonus = .05
	efficiency = 1.
	#bonuses:
	baseBonuses = {\
	'thrustBonus' : 1., 'torqueBonus' : 1.,\
	'shieldRegenBonus' : 1., 'shieldMaxBonus' : 1.,\
	'generatorBonus' : 1., 'batteryBonus' : 1., 'regeneration' : 0, 'energyUseBonus' : 1.,\
	'massBonus' : 1., 'sensorBonus' : 1., 'hiddenBonus' : 1., 'fireRateBonus' : 1.,\
	'damageBonus' : 1., 'cannonBonus' : 1., 'laserBonus' : 1., 'missileBonus' : 1.,\
	'cannonRateBonus' : 1., 'laserRateBonus' : 1., 'missileRateBonus' : 1.,\
	'cannonRangeBonus' : 1., 'laserRangeBonus' : 1., 'missileRangeBonus' : 1.,\
	'cannonDefenseBonus' : 1., 'laserDefenseBonus' : 1., 'missileDefenseBonus' : 1.,\
	'cannonSpeedBonus' : 1., 'missileSpeedBonus' : 1.\
	}
	#used by scripts:
	target = None
	destination = None

	def __init__(self, game, x, y, dx = 0, dy = 0, dir = 270, script = None, \
				color = (255, 255, 255), race = None, system = None):
		Floater.__init__(self, game, x, y, dx, dy, dir, 1)
		self.inventory = []
		self.ports = [Port((0,0), 0, self)]
		self.energy = 0
		self.maxEnergy = 0
		self.propellant = 0
		self.maxPropellant = 0
		self.color = color
		self.race = race
		if self.race: self.race.ships.append(self)
		self.part = None
		self.__dict__.update(self.baseBonuses)
		if script: self.script = script
		else: self.script = Script(game)
		if system: self.system = system
		else: self.system = game.curSystem
		self.baseImage = pygame.Surface((200, 200), hardwareFlag | SRCALPHA).convert_alpha()
		self.baseImage.set_colorkey((0,0,0))
		self.functions = [self.forward, self.reverse, self.left, self.right, \
				self.turnLeft, self.turnRight, self.shoot, self.launchMissiles]
		self.functionDescriptions = []
		for function in self.functions:
			self.functionDescriptions.append(function.__doc__)
		self.baseBonuses = self.baseBonuses.copy()

	def addPart(self, part, portIndex = 0):
		"""ship.addPart(part) -> Sets the main part for this ship.
		Only used for the base part (usually a cockpit), other parts are added to parts."""
		part.parent = self
		part.dir = 0
		part.offset = (0, 0)
		part.ship = self
		part.image = colorShift(part.baseImage, self.color).convert()
		part.image.set_colorkey((0,0,0))
		self.ports[0].part = part
		self.reset()

	def reset(self):
		self.parts = []
		self.forwardEngines = []
		self.forwardThrust = 0
		self.reverseThrust = 0
		self.leftThrust = 0
		self.rightThrust = 0
		self.torque = 0
		self.reverseEngines = []
		self.leftEngines = []
		self.rightEngines = []
		self.guns = []
		self.missiles = []
		self.gyros = []
		self.tanks = []
		self.partLimit = Ship.partLimit
		self.__dict__.update(Ship.baseBonuses)
		#recalculate stats:
		self.dps = 0
		self.partRollCall(self.ports[0].part)
		minX, minY, maxX, maxY = 0, 0, 0, 0
		#TODO: ? make the center of the ship the center of mass instead of the
		#center of the radii.
		for part in self.parts:
			minX = min(part.offset[0] - part.radius, minX)
			minY = min(part.offset[1] - part.radius, minY)
			maxX = max(part.offset[0] + part.radius, maxX)
			maxY = max(part.offset[1] + part.radius, maxY)
		self.radius = max(maxX - minX, maxY - minY) / 2
		#recenter:
		xCorrection = (maxX + minX) / 2
		yCorrection = (maxY + minY) / 2
		self.partEffects = []
		self.mass = 1
		self.moment = 1000
		self.maxEnergy = 0
		self.maxhp = 0
		self.propellant = 0
		self.maxPropellant = 0
		partNum = 1
		self.value = 0
		for part in self.parts:
			part.number = partNum
			self.value += part.value
			partNum += 1
			part.offset = 	part.offset[0] - xCorrection, \
							part.offset[1] - yCorrection
			part.attach()
		partNum -= 1
		self.mass -= 1
		self.numParts = partNum
		self.energy = min(self.energy, self.maxEnergy)
		self.hp = min(self.hp, self.maxhp)
		self.propellant = min(self.propellant, self.maxPropellant)
		maxDist = -1
		for tank in self.tanks:
			dist = tank.offset[0] ** 2 + tank.offset[1] ** 2
			if maxDist < dist:
				maxDist = dist
				self.usingTank = tank
		for skill in self.skills:
			skill.shipReset()

		if partNum > self.partLimit:
			self.efficiency = (1 - self.penalty) ** (partNum - self.partLimit)
		else:
			self.efficiency = 2 - (1 - self.bonus) ** (self.partLimit - partNum)
		#redraw base image:
		if self.game.pause:
			size = int(self.radius * 2 + 60)
		else:
			size = int(self.radius * 2)
		self.baseImage = pygame.Surface((size, size), \
					hardwareFlag | SRCALPHA).convert_alpha()
		self.baseImage.set_colorkey((0,0,0))
		if self.ports[0].part:
			self.ports[0].part.draw(self.baseImage)
		self.buffer = pygame.Surface((self.radius * 2, self.radius * 2),
					flags = hardwareFlag | SRCALPHA).convert_alpha()

	def partRollCall(self, part):
		"""adds parts to self.parts recursively."""
		if part:
			self.parts.append(part)
			if isinstance(part, Engine):
				if part.dir == 180:
					self.reverseEngines.append(part)
					self.reverseThrust += part.force
				if part.dir == 0:
					self.forwardEngines.append(part)
					self.forwardThrust += part.force
				if part.dir == 90:
					self.rightEngines.append(part)
					self.rightThrust += part.force
				if part.dir == 270:
					self.leftEngines.append(part)
					self.leftThrust += part.force
			if isinstance(part, Gyro):
				self.gyros.append(part)
				self.torque += part.torque
			if isinstance(part, Tank):
				self.tanks.append(part)
			if isinstance(part, Gun):
				if isinstance(part, MissileLauncher):
					self.missiles.append(part)
				else:
					self.guns.append(part)
				self.dps += part.getDPS()
			for port in part.ports:
				if port.part:
					self.partRollCall(port.part)

	def forward(self):
		"""thrust forward using all forward engines"""
		for engine in self.forwardEngines:
			engine.thrust()
	def reverse(self):
		"""thrust backward using all reverse engines"""
		for engine in self.reverseEngines:
			engine.thrust()
	def left(self):
		"""strafes left using all left engines"""
		for engine in self.leftEngines:
			engine.thrust()
	def right(self):
		"""strafes right using all right engines"""
		for engine in self.rightEngines:
			engine.thrust()
	def turnLeft(self, angle = None):
		"""Turns ccw using all gyros."""
		for gyro in self.gyros:
			gyro.turnLeft(angle)
	def turnRight(self, angle = None):
		"""Turns cw using all gyros."""
		for gyro in self.gyros:
			gyro.turnRight(angle)
	def shoot(self):
		"""fires all guns."""
		for gun in self.guns:
			gun.shoot()
	def launchMissiles(self):
		for missles in self.missiles:
			missles.shoot()


	def update(self, dt):
		self.dt = dt

		#check if dead:
		if not self.parts or self.parts[0].hp <= 0:
			self.kill()

		#allow race to update:
		if self.race:
			self.race.updateShip(self, dt)

		#check if landed:
		if self.landed:
			#orbital velocity is calculated with vis-viva equation, i don't know why,
			#but dividing by sqrt(2) fixes the problem with bullet speed discordance
			orbvel = sqrt(self.landed.g * self.game.curSystem.sun.mass * \
			(2/self.landed.distance - 1/self.landed.SMa)) / 1.4142135623730951
			smi = self.landed.SMa * sqrt(self.landed.p)
			#vx and vy are the components of the tangent vector to the elliptic trajectory
			vx = orbvel * -self.landed.SMa * math.sin(self.landed.EccAn) / sqrt((smi * \
			math.cos(self.landed.EccAn)) ** 2 + (self.landed.SMa * math.sin(self.landed.EccAn)) ** 2)
			vy = orbvel * smi * math.cos(self.landed.EccAn) / sqrt((smi * math.cos(self.landed.EccAn))
			** 2 + (self.landed.SMa * math.sin(self.landed.EccAn)) ** 2)
			planetvel = rotate(vx, vy, self.landed.LPe)
			self.dx, self.dy = planetvel[0], planetvel[1]
			if self.thrusting and abs(self.land - self.dir) < 90 and dist2(self,self.landed) > \
			self.landed.radius ** 2:
				self.landed = False
			else:
				self.x = self.landed.x + (self.landed.radius + self.radius) * cos(self.land)
				self.y = self.landed.y + (self.landed.radius + self.radius) * sin(self.land)

		self.thrusting = False
		#run script, get choices.
		self.script.update(self, dt)

		# actual updating:
		Floater.update(self, dt)
		#parts updating:
		if self.ports[0].part:
			self.ports[0].part.update(dt)


		#active effects:
		for effect in self.effects:
			effect(self)
			print effect,
		for effect in self.partEffects:
			effect(self)

	def draw(self, surface, offset = None, pos = (0, 0)):
		"""ship.draw(surface, offset) -> Blits this ship onto the surface.
		 offset is the (x,y) of the topleft of the surface, pos is the
		 position to draw the ship on the surface, where pos=(0,0) is the
		 center of the surface. If offset is none, the ship will be drawn down
		 and right from pos where pos(0,0) is the topleft of the surface."""
		#image update:
		#note: transform is counter-clockwise, opposite of everything else.
		buffer = self.buffer
		buffer.set_colorkey((0,0,0))
		self.image = pygame.transform.rotate(self.baseImage, \
									-self.dir).convert_alpha()
		self.image.set_colorkey((0,0,0))

		#imageOffset compensates for the extra padding from the rotation.
		imageOffset = [- self.image.get_width() / 2,\
					   - self.image.get_height() / 2]
		#offset is where on the input surface to blit the ship.
		if offset:
			pos =[self.x  - offset[0] + pos[0] + imageOffset[0], \
				  self.y  - offset[1] + pos[1] + imageOffset[1]]

		#draw to buffer:
		surface.blit(self.image, pos)
		for part in self.parts:
			part.redraw(surface, offset)

		#shield:
		if self.hp > .0002:
			r = int(self.radius)
			shieldColor = (50,100,200, int(255. / 3 * self.hp / self.maxhp) )
			pygame.draw.circle(buffer, shieldColor, \
						(r, r), r, 0)
			pygame.draw.circle(buffer, (50,50,0,50), \
						(r, r), r, 5)
			rect = (0,0, r * 2, r * 2)
			pygame.draw.arc(buffer, (50,50,200,100), rect, + math.pi/2,\
							math.pi * 2 * self.hp / self.maxhp + math.pi/2, 5)

		#draw to input surface:
		pos[0] += - imageOffset[0] - self.radius
		pos[1] += - imageOffset[1] - self.radius
		surface.blit(buffer, pos)

	def takeDamage(self, damage, other):
		self.hp = max(self.hp - damage, 0)
		if isinstance(other, Bullet) and other.ship == self.game.player:
			self.game.player.xpDamage(self, damage)

	def kill(self):
		"""play explosion effect than call Floater.kill(self)"""
		setVolume(explodeSound.play(), self, self.game.player)
		for part in self.inventory:
			part.scatter(self)
		if self.race:
			self.race.ships.remove(self)
		Floater.kill(self)

class Player(Ship):
	xp = 0
	developmentPoints = 2
	frameUpdating = True
	money = 0

	def __init__(self, game, x, y, dx = 0, dy = 0, dir = 270, script = None, \
				color = (255, 255, 255), system = None):
		Ship.__init__(self, game, x, y, dx, dy, dir, script, color,
						 system = system)
		self.skills = [Modularity(self), Agility(self), Composure(self)]

	def xpQuest(self, xp):
		self.xp += xp

	def xpKill(self, ship):
		self.xp +=  10. * ship.level / self.level

	def xpDamage(self, target, damage):
		if isinstance(target, Part) and target.parent:
			target = target.parent #count the ship, not the part.
		self.xp += 1. * target.level / self.level * damage

	def xpDestroy(self, target):
		self.xp += 2. * target.level / self.level

	def update(self, dt):
		if self.game.debug: print 'xp:',self.xp
		if self.xp >= self.next():
			self.level += 1
			self.developmentPoints += 1
			self.xp = 0

		Ship.update(self, dt)
		self.frameUpdating = 1
		self.thrustSoundFX()


	def thrustSoundFX(self):
		channel = pygame.mixer.Channel(0)
		if self.thrusting and not channel.get_busy():
				channel.play(thrustSound, -1)
		elif not self.thrusting and channel.get_busy():
			channel.stop()


	def next(self):
		return 1.1 ** self.level * 10






