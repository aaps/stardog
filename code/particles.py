#particles.py
from vec2d import Vec2d

import random
import pygame
from utils import *
import copy


class Particle(object):
	
	def __init__(self, emitter, delta, startcolor, stopcolor, life, startsize, stopsize, relative):
		
		self.image = pygame.Surface((max(startsize, stopsize)*2, max(startsize, stopsize)*2), hardwareFlag | SRCALPHA).convert_alpha()
		self.game = emitter.game
		self.relative = relative
		self.relpos = Vec2d(0,0)
		self.pos = emitter.floater.pos
		self.emitter = emitter 

		self.delta = delta

		self.startcolor = startcolor
		self.stopcolor = stopcolor
		self.transcolor = (255,255,255,255)
		self.life = self.beginlife = life
		self.startsize = self.size = startsize
		self.stopsize = stopsize
		self.size = 0

		

	def draw(self, surface, offset=Vec2d(0,0)):
		if self.relative:
			poss = self.emitter.floater.pos + self.relpos
		else:
			poss = self.pos
		poss = int(poss[0] - offset.x), \
			  int(poss[1] - offset.y)
		pygame.draw.circle(self.image, self.transcolor, (int(self.image.get_width()/2), int(self.image.get_height()/2)), self.size)
		surface.blit(self.image, poss)		


	def update(self):
		color = []
		self.pos += self.delta / self.game.fps
		self.relpos += self.delta / self.game.fps
		factor = self.life  / self.beginlife 
		color.append(tuple(int(x*factor) for x in self.startcolor))
		color.append(tuple(int(x*(1-factor)) for x in self.stopcolor))
		self.transcolor = tuple(map(lambda y: sum(y), zip(*color)))
		self.size = int((self.startsize *factor) + (self.stopsize * (1-factor)))
		self.life -= 1.0 / self.game.fps
		

class Emitter(object):
	
	def __init__(self, game, floater, condfunc ,anglewidth, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative):
		# pass
		# self.image = pygame.Surface((game.width, game.height),
  #       hardwareFlag | SRCALPHA).convert_alpha()
		self.game =  game
		self.relative = relative
		self.condfunc = condfunc
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
		# self.image.fill((0, 0, 0,0))
		for particle in self.particles:
			particle.draw(surface, offset)
		# surface.blit(self.image, (0, 0))

	def update(self):
		for particle in self.particles:
			particle.update()
			if particle.life <= 0:
				self.particles.remove(particle)

		if self.condfunc():
			if self.floater.ship:
				startdir = self.floater.ship.dir + self.anglewidth
				stopdir = self.floater.ship.dir - self.anglewidth	
			else:
				startdir = self.floater.dir + self.anglewidth
				stopdir = self.floater.dir - self.anglewidth

			delta = -Vec2d(0,0).rotatedd(random.uniform(startdir,stopdir),random.uniform(self.startvelocity,self.stopvelocity))
			if len(self.particles) < self.maximum:
				self.particles.append(Particle(self, delta, self.startcolor, self.stopcolor, random.uniform(self.startlife,self.stoplife), self.startsize, self.stopsize, self.relative))


		

			
