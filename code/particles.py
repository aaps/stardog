#particles.py
from vec2d import Vec2d
import random

class Particle(object):
	
	def __init__(self, game, pos, dir, velocity, startcolor, stopcolor, life, startsize, stopsize):
		self.game = game
		self.relativepos = pos
		self.dir = pos
		self.relativevel = velocity
		self.startcolor = startcolor
		self.stopcolor = stopcolor
		self.life = self.beginlife = life
		self.startsize = startsize
		self.stopsize = stopsize
		

	def draw(self, surface):
			pygame.draw.circle(surface, self.color, self.pos, self.size)


	def update(self):
		self.pos += (self.relativepos + Vec2d(0,0).rotated(self.dir, velocity)) / self.game.fps
		self.life -= 1 / self.game.fps
		self.color = (self.startcolor / self.life + 0.01) + (self.stopcolor / (self.beginlife - self.life) + 0.01)
		self.size = round((self.startsize / self.life + 0.01) + (self.stopsize / (self.beginlife - self.life) + 0.01))
		

class Emitter(object):
	
	particles = []

	def __init__(self, game, pos, startdir, stopdir, startvelocity, stopvelocity, startcolor, stopcolor, starlife, stoplife, maximum, startsize, stopsize):
		self.image = pygame.Surface((game.width, game.height), flags = hardwareFlag).convert()
		self.game =  game
		self.pos = pos
		self.startdir = startdir
		self.stopdir = stopdir
		self.startsize = startsize
		self.stopsize = stopsize
		
		self.startvelocity = startvelocity
		self.stopvelocity = stopvelocity

		self.startcolor = startcolor
		self.stopcolor = stopcolor
		self.maximum = maximum
	
	def draw(self, surface, offset = (0,0)):
		for particle in self.particles:
			particle.draw(surface, offset)

	def update(self):
		if len(particles) < self.maximum:
			particles.add(Particle(game, self.pos, random.randint(self.startdir,self.stopdir), random.randint(self.startvelocity,self.stopvelocity), self.startcolor, self.stopcolor, random.randint(self.startlife,self.stoplife), self.startsize, self.stopsize))
		for particle in self.particles:
			particle.update()
