#floaters.py

from utils import *
from pygame.locals import *
import stardog
from vec2d import Vec2d
import math

FPS = 200
MISSILE_RADIUS = 50
SOUND_RADIUS = 3000

def setVolume(channel, floater1, floater2):
	from spaceship import Player
	"""sets volume for a channel based on the distance between
	 the player and floater."""
	distance = floater2.pos.get_distance(floater1.pos)
	if channel and floater1 and floater2:
		volume = 0.0
		if distance < SOUND_RADIUS and (isinstance(floater1, Player) or  isinstance(floater2, Player)):
			volume =  math.sqrt((SOUND_RADIUS - distance)**1.8 / (SOUND_RADIUS + 0.001)**1.8)
		channel.set_volume(volume)

BULLET_IMAGE = loadImage("res/shot.bmp")
MISSILE_IMAGE = loadImage("res/missile" + ext)
DEFAULT_IMAGE = loadImage("res/default" + ext)


		
class Ballistic:
	"""an abstraction of a Floater.  Just has a Vec2d,Vec2d."""
	def __init__(self, pos, delta):
		self.pos = pos
		self.delta = delta
			
class Floater(pygame.sprite.Sprite, Ballistic):
	"""creates a floater with position (x,y) in pixels, speed (dx,dy) 
	in pixels per second, direction dir 
	where 0 is pointing right and 270 is pointing up, radius radius 
	(for collision testing), and with the image image.  Image should be a 
	string of a file name without an axtension- there should be both a .gif 
	and	a .bmp, which is used depends on the pygame support on the run
	system."""
	hp = 1
	baseImage = None
	color = (200, 200, 0)
	mass = 1
	tangible = True

	def __init__(self, game, pos, delta, dir = 270, radius = 10, \
			image = None):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.dir = dir
		self.pos = pos
		self.delta = delta

		self.radius = radius
		if (not image):
			image = DEFAULT_IMAGE
		#rotate() takes a counter-clockwise angle. 
		self.image = pygame.transform.rotate(image, -self.dir).convert()
		#self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()

	def update(self):
		"""updates this floater based on its variables"""
		self.pos += self.delta / self.game.fps
		self.rect.center = self.pos

	def takeDamage(self, damage, other):
		self.hp -= damage
		if self.hp <= 0:
			self.kill(other)

	def draw(self, surface, offset = (0,0)):
		"""Blits this floater onto the surface. """
		poss = self.pos.x - self.image.get_width()  / 2 - offset[0], \
			  self.pos.y - self.image.get_height() / 2 - offset[1]
		surface.blit(self.image, poss)

class Bullet(Floater):
	def __init__(self, game, gun, damage, speed, range, image = None):
		dir = gun.dir + gun.ship.dir
		cost = cos(dir) #cost is short for cos(theta)
		sint = sin(dir)
		pos = gun.pos + Vec2d(gun.shootPoint).rotated(dir) + gun.ship.delta / game.fps

		dir += gun.shootDir # not needed for the offset, but needed for the dir.
		self.speed = speed
		delta = gun.ship.delta.rotatedd(dir, self.speed)		
		if image == None:
			image = BULLET_IMAGE
		Floater.__init__(self, game, pos, delta, \
							dir = dir, radius = gun.bulletRadius, \
							image = image)
		self.range = range
		self.hp = damage
		self.life = 0.
		self.ship = gun.ship
		if 'target' in gun.ship.__dict__:
			self.target = gun.ship.target

	def update(self):
		self.life += 1. / self.game.fps
		Floater.update(self)
		if self.life > self.range:
			self.softkill()

	def detonate(self,other):
		delta = other.delta / 10
		impact = Impact(self.game, self.pos, delta, 20, 14)
		self.game.curSystem.add(impact)

	def kill(self,other):
		self.detonate(other)
		if soundModule:
			setVolume(missileSound.play(), self, self.game.player)
		Floater.kill(self)

	def softkill(self):
		Floater.kill(self)



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
		
	def update(self):
		self.life += 1. / self.game.fps
		self.dir = (self.dir + 180) % 360 - 180
		Floater.update(self)
		self.delta.x += self.acceleration * cos(self.dir) / self.game.fps
		self.delta.y += self.acceleration * sin(self.dir) / self.game.fps
		if self.life > self.range:
			self.kill()

	def detonate(self):
		delta = self.delta.rotatedd(self.dir, -(self.acceleration * self.life))
		explosion = Explosion(self.game, self.pos, delta, self.explosionRadius, self.time, self.damage, self.force)
		self.game.curSystem.add(explosion)

	def kill(self,other):
		self.detonate()
		if soundModule:
			setVolume(missileSound.play(), self, self.game.player)
		Floater.kill(self)

	def takeDamage(self, damage, other):
		self.impacted = other
		Floater.takeDamage(self, damage, other)
		
class Explosion(Floater):
	life = 0

	def __init__(self, game, pos, delta, radius = 10,\
				time = 1, damage = 0, force = 6000):
		image = pygame.Surface((radius * 2, radius * 2), flags = hardwareFlag).convert()
		image.set_colorkey((0,0,0))
		Floater.__init__(self, game, pos, delta, radius = 0,\
				image = image)
		self.maxRadius = int(radius)
		self.force = force
		self.radius = 0
		self.time = time
		self.damage = damage
		self.hp = damage / (self.time * self.game.fps)
		if damage == 0:
			self.tangible = False

	def update(self):
		Floater.update(self)
		self.life += 1. / self.game.fps
		if self.life > self.time:
			Floater.kill(self)
		self.hp = self.damage / (self.time * self.game.fps)
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
			poss = (int(cos(theta) * r + self.maxRadius), \
					  int(sin(theta) * r + self.maxRadius))
			pygame.draw.circle(self.image, color, poss, radius)
		Floater.draw(self, surface, offset)

	def kill(self,other):
		pass
		
	def takeDamage(self, damage, other):
		pass
	
class Impact(Floater):
	life = 10
	tangible = False
	mass = 0
	def __init__(self, game, pos, delta, radius = 5,\
				time = 1):
		image = pygame.Surface((radius * 2, radius * 2), flags = hardwareFlag).convert()
		image.set_colorkey((0,0,0))
		Floater.__init__(self, game, pos, delta, radius = 0,\
				image = image)
		self.maxRadius = int(radius)
		self.radius = 0
		self.time = time


	def update(self):
		Floater.update(self)
		self.life += 1. / self.game.fps
		if self.life > self.time:
			Floater.kill(self)
		#grow or shrink: size peaks at time / 2:
		if self.life < self.time / 4:
			self.radius = int(self.maxRadius * self.life * 4 / self.time)
		else:
			self.radius = int(self.maxRadius * (self.time * 4 / 3 \
						- self.life * 4 / 3) / self.time)
		
	def draw(self, surface, offset = (0,0)):
		self.image.fill((0, 0, 0, 0))
		for circle in range(min(self.radius / 4, 80)):
			color = (randint(100, 200), randint(100, 200), randint(100, 255), \
					randint(100, 255))
			radius = randint(self.radius / 4, self.radius / 2)
			r = randint(0, self.radius - radius)
			theta = randint(0, 360)
			poss = (int(cos(theta) * r + self.maxRadius), \
					  int(sin(theta) * r + self.maxRadius))
			pygame.draw.circle(self.image, color, poss, radius)
		Floater.draw(self, surface, offset)

	def kill(self,other):
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
		pos = laser.pos + Vec2d(laser.shootPoint).rotated(dir) + laser.ship.delta / game.fps

		start = pos
		dir = laser.dir + laser.ship.dir + laser.shootDir
		length = range

		stop = pos.rotatedd(dir, range)

		Floater.__init__(self, game, (start + stop) / 2, laser.ship.delta, dir,
						radius = 0)
		self.damage = damage
		self.start = start
		self.stop = stop
		left = min(start.x, stop.x)
		top = min(start.y, stop.y)
		width = abs(start.x - stop.x)
		height = abs(start.y - stop.y)
		self.rect = Rect(left, top, width, height)
		self.slope = (start.y-stop.y) / not0(start.x - stop.x)
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
		self.game.curSystem.specialOperations.append(self.collision)

		
	def intersect(self, floater, skipRect = False):
		#check rect collide:
		if floater != self and (skipRect or self.rect.colliderect(floater.rect)):
			#check line-circle collide:
			dist = linePointDist(self.start, self.stop, (floater.pos.x, floater.pos.y))
			if dist	< floater.radius:
				return dist
				
	def collision(self):
		from spaceship import Ship
		colliders = []
		for floater in self.game.curSystem.floaters:
			if floater.tangible and self.intersect(floater):
				colliders.append(floater)
		if colliders:
			#recurse for parts in a ship:
			for floater in colliders[:]:
				if isinstance(floater, Ship):
					for part in floater.parts:
						if self.intersect(part, True):
							colliders.append(part)
			#sort so that the nearest gets hit first:
			dir = sign(self.stop.y + self.stop.x * self.slope - 
					self.start.y + self.start.x * self.slope)
			colliders.sort(key = lambda f: 
					(f.pos.y + f.pos.x * self.slope) * dir - f.radius)
			#hit until damage is used up
			for floater in colliders:
				tmp = floater.hp
				floater.takeDamage(self.damage, self)
				self.damage -= tmp
				if self.damage < 1: #fudge it for effect: 1 not 0
					#adjust stop based on last hit target:
					self.stop = (floater.pos.x, (floater.pos.x - self.start.x) 
											* self.slope + self.start.y)
					
					self.length = self.start.get_distance(self.stop)
					break
				
					
	def update(self):
		self.life -= 1. / self.game.fps
		Floater.update(self)
		self.start = self.start + self.delta / self.game.fps
		self.stop = self.stop  + self.delta / self.game.fps
		if self.life < 0:
			self.kill()
	
		
	def takeDamage(self, damage, other):
		pass
	
		
		
		