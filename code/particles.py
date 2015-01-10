#particles.py
from vec2d import Vec2d

import random
import pygame
from utils import *


class Particle(object):
	
	def __init__(self, game, pos, delta, startcolor, stopcolor, life, startsize, stopsize):
		self.game = game
		self.relativepos = self.pos = pos
		self.delta = delta
		self.startcolor = startcolor
		self.stopcolor = stopcolor
		self.transcolor = (255,255,255,255)
		self.life = self.beginlife = life
		self.startsize = self.size = startsize
		self.stopsize = stopsize
		self.size = 0

		

	def draw(self, surface, offset=Vec2d(0,0)):
		
		poss = self.pos.inttup()
		poss = int(poss[0] - offset.x), \
			  int(poss[1] - offset.y)
		pygame.draw.circle(surface, self.transcolor, poss, self.size)		


	def update(self):
		color = []
		self.pos += self.delta / self.game.fps
		factor = self.life  / self.beginlife 
		color.append(tuple(int(x*factor) for x in self.startcolor))
		color.append(tuple(int(x*(1-factor)) for x in self.stopcolor))
		self.transcolor = tuple(map(lambda y: sum(y), zip(*color)))
		self.size = int((self.startsize / (self.life + 1)) - (self.stopsize / ((self.beginlife - self.life) + 1)))
		self.life -= 1.0 / self.game.fps
		

class Emitter(object):
	
	def __init__(self, game, floater,anglewidth, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize):
		
		self.image = pygame.Surface((game.width, game.height),
        hardwareFlag | SRCALPHA).convert_alpha()
		self.game =  game
		self.floater = floater
		self.startlife = startlife
		self.stoplife = stoplife
		self.anglewidth = anglewidth
		self.startsize = startsize
		self.stopsize = stopsize
		self.startvelocity = startvelocity
		self.stopvelocity = stopvelocity
		self.startcolor = startcolor
		self.stopcolor = stopcolor
		self.maximum = maximum
		self.particles = []
		self.enabled = True
	
	def draw(self, surface, offset = Vec2d(0,0)):
			self.image.fill((0, 0, 0,0))
			for particle in self.particles:
				particle.draw(self.image, offset)
			surface.blit(self.image, (0, 0))

	def update(self):
		
		for particle in self.particles:
			particle.update()
			if particle.life <= 0:
				# print particle.transcolor
				self.particles.remove(particle)

		if self.enabled:
			if self.floater.ship:
				startdir = self.floater.ship.dir + self.anglewidth
				stopdir = self.floater.ship.dir - self.anglewidth	
			else:
				startdir = self.floater.dir + self.anglewidth
				stopdir = self.floater.dir - self.anglewidth

			delta = -Vec2d(0,0).rotatedd(random.uniform(startdir,stopdir),random.uniform(self.startvelocity,self.stopvelocity))
			
				
			if len(self.particles) < self.maximum:
				self.particles.append(Particle(self.game, self.floater.pos, delta, self.startcolor, self.stopcolor, random.uniform(self.startlife,self.stoplife), self.startsize, self.stopsize))

	def enable(self):
		self.enabled = True

	def disable(self):
		self.enabled = False

		

			
