#floaters.py

from utils import *
from pygame.locals import *
import os

FPS = 200
MISSILE_RADIUS = 50

def setVolume(channel, floater1, floater2):
	"""sets volume for a channel based on the distance between
	 the player and floater."""
	if channel and floater1 and floater2:
		channel.set_volume(.25 / (min(1,
						(floater2.x - floater1.x) ** 2 +
						(floater2.y - floater1.y) ** 2 + .0001)))

BULLET_IMAGE = loadImage("res/shot.bmp")
MISSILE_IMAGE = loadImage("res/missile" + ext)
DEFAULT_IMAGE = loadImage("res/default.bmp")


class Ballistic:
	"""an abstraction of a Floater.  Just has a x,y,dx,dy."""
	def __init__(self, x, y, dx = 0, dy = 0):
		self.x, self.y = x, y
		self.dx, self.dy = dx, dy


class Floater(object):
	"""creates a floater with position (x,y) in pixels, speed (dx,dy)
	in pixels per second, direction dir
	where 0 is pointing right and 270 is pointing up, radius radius
	(for collision testing), and with the image image.  Image should be a
	string of a file name without an axtension- there should be both a .gif
	and	a .bmp, which is used depends on the pygame support on the run
	system."""
	system = None
	hp = 1
	baseImage = None
	color = (200, 200, 0)
	mass = 1
	tangible = True
	gravitates = True
	dead = False
	frameUpdating = False
	__slots__ = ['dx', 'dy', 'radius', 'dir', 'rect', 'image', 'dead',
				'frameUpdating', 'tangible', 'gravitates', 'game', 'system',
				 'mass', 'hp', 'color', 'baseImage', '__dict__']
	#"""
	def __init__(self, game, x, y, dx = 0., dy = 0., dir = 270, radius = 10,
			image = None):
		self.game = game
		self.dir = dir
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.radius = radius
		if (not image):
			if self.baseImage:
				image = self.baseImage
			else:
				image = DEFAULT_IMAGE
		#rotate() takes a counter-clockwise angle.
		self.image = pygame.transform.rotate(image, -self.dir).convert()
		#self.image.set_colorkey((0,0,0))

	def update(self, dt):
		"""updates this floater based on its variables"""
		self.x += self.dx * dt
		self.y += self.dy * dt

	def takeDamage(self, damage, other):
		self.hp -= damage
		if self.hp <= 0:
			self.kill()

	def draw(self, surface, offset = (0,0)):
		"""Blits this floater onto the surface. """
		pos = (self.x - self.image.get_width()  / 2 - offset[0],
			  self.y - self.image.get_height() / 2 - offset[1])
		surface.blit(self.image, pos)

	def kill(self):
		self.dead = True

	def left(self):
		return self.x - self.radius

	def top(self):
		return self.y - self.radius

class Bullet(Floater):
	frameUpdating = True
	tangibleDelay = 32 # pixels
	tangible = False
	def __init__(self, game, gun, damage, speed, range, image = None,
						color = (200,200,0)):
		self.color = color
		dir = gun.dir + gun.ship.dir
		cost = cos(dir) #cost is short for cos(theta)
		sint = sin(dir)
		x = gun.x + gun.shootPoint[0] * cost\
						- gun.shootPoint[1] * sint + gun.ship.dx * game.dt
		y = gun.y + gun.shootPoint[0] * sint\
						+ gun.shootPoint[1] * cost + gun.ship.dy * game.dt
		dir += gun.shootDir # not needed for the offset, but needed for the dir.
		self.speed = speed
		dx = self.speed * cos(dir) + gun.ship.dx
		dy = self.speed * sin(dir) + gun.ship.dy
		if image == None:
			image = BULLET_IMAGE
		Floater.__init__(self, game, x, y, dx = dx, dy = dy,
							dir = dir, radius = gun.bulletRadius,
							image = image)
		self.timer = self.tangibleDelay / self.speed
		self.range = range
		self.hp = damage
		self.life = 0.
		self.ship = gun.ship
		if 'target' in gun.ship.__dict__:
			self.target = gun.ship.target

	def update(self, dt):
		if not self.tangible:
			self.timer -= dt
			if self.timer <=0:
				self.tangible = 1
		self.life += 1. * dt
		Floater.update(self, dt)
		if self.life > self.range:
			self.kill()

class Missile(Bullet):
	life = 0
	turning = 0
	percision = 0
	hp = 1
	impacted = None
	explode = False

	def __init__(self, game, launcher, damage, speed, acceleration, range,
				explosionRadius, image = None):
		Bullet.__init__(self, game, launcher, self.hp, speed, range, image)
		self.damage = damage
		self.turning = launcher.turning
		self.percision = launcher.percision
		self.acceleration = launcher.acceleration
		self.explosionRadius = explosionRadius
		self.time = launcher.explosionTime
		self.force = launcher.force

	def update(self, dt):
		self.life += 1. * dt
		self.dir = (self.dir + 180) % 360 - 180
		Floater.update(self, dt)
		self.dx += self.acceleration * cos(self.dir) * dt
		self.dy += self.acceleration * sin(self.dir) * dt
		if self.life > self.range:
			self.kill()

	def detonate(self):
		explosion = Explosion(self.game, self.x, self.y,
				self.dx - self.acceleration * self.life * cos(self.dir),
				self.dy - self.acceleration * self.life * sin(self.dir),
				self.explosionRadius, self.time, self.damage, self.force)
		self.system.add(explosion)

	def kill(self):
		self.detonate()
		if soundModule:
			setVolume(missileSound.play(), self, self.game.player)
		Floater.kill(self)

	def takeDamage(self, damage, other):
		self.impacted = other
		Floater.takeDamage(self, damage, other)

class Explosion(Floater):
	life = 0

	def __init__(self, game, x, y, dx = 0, dy = 0, radius = 10,\
				time = 1, damage = 0, force = 6000):
		image = pygame.Surface((radius * 2, radius * 2), flags = hardwareFlag).convert()
		image.set_colorkey((0,0,0))
		Floater.__init__(self, game, x, y, dx, dy, radius = 0,\
				image = image)
		self.maxRadius = int(radius)
		self.force = force
		self.radius = 0
		self.time = time
		self.damage = damage
		self.hp = damage * game.dt / not0(self.time)
		if damage == 0:
			self.tangible = False

	def update(self, dt):
		Floater.update(self, dt)
		self.life += 1. * dt
		if self.life > self.time:
			Floater.kill(self)
		self.hp = self.damage * dt / self.time
		#grow or shrink: size peaks at time / 2:
		if self.life < self.time / 4:
			self.radius = int(self.maxRadius * self.life * 4 / self.time)
		else:
			self.radius = int(self.maxRadius * (self.time * 4 / 3 \
						- self.life * 4 / 3) / self.time)

	def draw(self, surface, offset = (0,0)):
		self.image.fill((0, 0, 0, 0))
		for circle in range(min(self.radius / 4, 80)):
			color = (randint(100, 155), randint(000, 100), randint(0, 20), \
					randint(100, 255))
			radius = randint(self.radius / 4, self.radius / 2)
			r = randint(0, self.radius - radius)
			theta = randint(0, 360)
			pos = (int(cos(theta) * r + self.maxRadius),
					  int(sin(theta) * r + self.maxRadius))
			pygame.draw.circle(self.image, color, pos, radius)
		Floater.draw(self, surface, offset)

	def kill(self):
		pass

	def takeDamage(self, damage, other):
		pass



class LaserBeam(Floater):
	"""LaserBeam(game, laser, damage, range) -> new LaserBeam

	A LaserBeam is the projectile of a Laser.  They are line segments
	that reach their end point instantly.  A LaserBeam has a different
	collision mechanism: they use line/circle collision, and it is checked
	during initialization."""
	life = .5 #seconds
	hp = 0
	tangible = False
	baseImage = loadImage("res/laser.bmp").convert()
	baseImage.set_colorkey((0,0,0))

	def __init__(self, game, laser, damage, range):
		dir = laser.dir + laser.ship.dir
		cost = cos(dir) #cost is short for cos(theta)
		sint = sin(dir)
		self.system = laser.system
		self.firstFrame = True
		x = laser.x + laser.shootPoint[0] * cost\
					- laser.shootPoint[1] * sint + laser.ship.dx * game.dt
		y = laser.y + laser.shootPoint[0] * sint\
					+ laser.shootPoint[1] * cost + laser.ship.dy * game.dt
		start = x,y
		dir = laser.dir + laser.ship.dir + laser.shootDir
		length = range
		stop = x + range * cos(dir), y + range * sin(dir)
		x, y = (start[0] + stop[0]) / 2., (start[1] + stop[1]) / 2.
		Floater.__init__(self, game, x, y, laser.ship.dx, laser.ship.dy, dir,
						radius = 0)
		self.damage = damage
		self.start = start
		self.stop = stop
		left = min(start[0], stop[0])
		top = min(start[1], stop[1])
		width = abs(start[0] - stop[0])
		height = abs(start[1] - stop[1])
		self.rect = Rect(left, top, width, height)
		self.slope = (start[1]-stop[1]) / not0(start[0] - stop[0])
		self.laser = laser
		self.life = laser.imageDuration
		self.ship = laser.ship
		self.width = laser.beamWidth
		self.image = pygame.transform.rotate(
					pygame.transform.scale(
					colorShift(self.baseImage, self.ship.color),
					(int(length), 5)), -dir)
		if 'target' in laser.ship.__dict__:
			self.target = laser.ship.target


	def intersect(self, floater, skipRect = False):
		#check rect collide:
		if floater != self:
			#check line-circle collide:
			dist = linePointDist(self.start, self.stop, (floater.x, floater.y))
			if dist	< floater.radius:
				return dist

	def collision(self):
		from spaceship import Ship
		self.firstFrame = False
		colliders = []
		for floater in self.system.floaters:
			if (floater.tangible and self.intersect(floater)
			and floater != self.ship):
				colliders.append(floater)
		if colliders:
			#recurse for parts in a ship:
			for floater in colliders[:]:
				if isinstance(floater, Ship):
					for part in floater.parts:
						if self.intersect(part, True):
							colliders.append(part)
			#sort so that the nearest gets hit first:
			dir = sign(self.stop[1] + self.stop[0] * self.slope -
					self.start[1] + self.start[0] * self.slope)
			colliders.sort(key = lambda f:
					(f.y + f.x * self.slope) * dir - f.radius)
			#hit until damage is used up
			for floater in colliders:
				tmp = floater.hp
				floater.takeDamage(self.damage, self)
				self.damage -= tmp
				if self.damage < 1: #fudge it for effect: 1 not 0
					#adjust stop based on last hit target:
					self.stop = (floater.x, (floater.x - self.start[0])
											* self.slope + self.start[1])
					self.length = dist(self.start[0],self.start[1], self.stop[0], self.stop[1])
					break


	def update(self, dt):
		if self.firstFrame:
			self.collision()
		self.life -= 1. * dt
		Floater.update(self, dt)
		self.start = (self.start[0] + self.dx * dt,
						self.start[1] + self.dy * dt)
		self.stop = (self.stop[0] + self.dx * dt,
						self.stop[1] + self.dy * dt)
		if self.life < 0:
			self.kill()


asteroidImages = []
#(skip the .svn dir:)
files = [f for f in os.listdir('res/asteroids/gen')if f[-4:] == '.bmp']
for file in files:
	asteroidImages.append(loadImage('res/asteroids/gen/' + file))

class Asteroid(Floater):
	minRadius = 20		#do not split if less than this (just die).
	hpPerSplit = 1		#splits everytime it takes this much damage.
	splitSpeed = 20		#speed asteriods move away after splitting.
	gravitates = True
	images = asteroidImages
	def __init__(self, game, x, y, dx = 0, dy = 0, radius = 25., color = None,
				image = None):
		if color:
			self.color = color
		else:
			#asteroids are some mixture of brown and grey. Brown is dark orange.
			brownness = randint(0, 100)
			greyness = randint(70, 150)
			self.color = (brownness + greyness,
							brownness / 2 + greyness, greyness)
		#pick an asteroid image at random:
		image = image or self.images[randint(0, len(self.images) - 1)]
		#color it in:
		size = int(round(radius * 2 / 5) * 5)
		image = pygame.transform.scale(image, (int(size), int(size)))
		self.baseImage = image
		Floater.__init__(self, game, x, y, dx, dy, 0, radius, image)
		self.ddir = randint(-20, 20) * 1.0
		self.mass = self.radius ** 2 * pi
		self.hp = self.radius / 2

	# def update(self, dt):
		# self.dir += self.ddir * dt
		# Floater.update(self, dt)

	def draw(self, surface, offset = None, pos = (0, 0)):
		self.image = pygame.transform.rotate(self.baseImage, \
									-self.dir)
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

	def takeDamage(self, damage, other):
		self.hp -= damage
		if self.hp <= self.radius / 2 - self.hpPerSplit:
			self.radius = sqrt(max(self.radius ** 2 - damage ** 2, 0))
			if self.radius < self.minRadius:
				self.kill()
				return
			#make two new, smaller asteroids:
			dir1 = other.dir + 90
			dir2 = other.dir - 90
			ratio = randint(-1,1)
			if ratio == 0:
				size2 = size1 = self.radius / 1.414 - 1#1/2 area
			elif ratio == -1:
				size1 = self.radius / 2 - 1#1/4 area
				size2 = self.radius * 1.73 / 2 - 1#3/4 area
			elif ratio == 1:
				size1 = self.radius * 1.73 / 2 - 1#3/4 area
				size2 = self.radius / 2 - 1#1/4 area
			x1 = self.x + (size1 + 1) * cos(dir1)
			y1 = self.y + (size1 + 1) * sin(dir1)
			x2 = self.x + (size2 + 1) * cos(dir2)
			y2 = self.y + (size2 + 1) * sin(dir2)
			dx1 = self.dx + cos(dir1) * self.splitSpeed
			dy1 = self.dy + sin(dir1) * self.splitSpeed
			dx2 = self.dx + cos(dir2) * self.splitSpeed
			dy2 = self.dy + sin(dir2) * self.splitSpeed
			self.system.add(
					Asteroid(self.game, x1, y1, dx1, dy1, size1, self.color))
			self.system.add(
					Asteroid(self.game, x2, y2, dx2, dy2, size2, self.color))
			self.kill()

	def kill(self):
		self.radius = 0
		self.hp = 0
		Floater.kill(self)



