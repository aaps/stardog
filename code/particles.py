#particles.py

from vec2d import Vec2d
import random
import pygame
import copy

class Particle(object):
	
	def __init__(self, emitter, pos, delta, startcolor, stopcolor, life, startsize, stopsize, relative):
		
		self.image = pygame.Surface((max(startsize, stopsize)*2, max(startsize, stopsize)*2), pygame.HWSURFACE | pygame.SRCALPHA)
		
		self.relative = relative
		self.relpos = pos
		self.emitter = emitter 
		self.delta = delta
		self.startcolor = startcolor
		self.stopcolor = stopcolor
		self.transcolor = (255,255,255,255)
		self.life = self.beginlife = life
		self.startsize = self.size = startsize
		self.stopsize = stopsize
		self.size = 0
		self.fps = 10
		
	def draw(self, surface, offset=Vec2d(0,0)):
		self.image.fill((0,0,0,0))

		if self.relative:
			poss = self.emitter.floater.pos + self.relpos
		else:
			poss = self.emitter.floater.pos
			
		poss = int(poss[0] - offset.x - int(self.image.get_width()/2)), int(poss[1] - offset.y - int(self.image.get_height()/2))
		pygame.draw.circle(self.image, self.transcolor, (int(self.image.get_width()/2), int(self.image.get_height()/2)), self.size)
		
		surface.blit(self.image, poss)		


	def update(self):
		color = []
		self.relpos += self.delta / self.fps
		factor = self.life  / self.beginlife 
		color.append(tuple(int(x*factor) for x in self.startcolor))
		color.append(tuple(int(x*(1-factor)) for x in self.stopcolor))
		self.transcolor = tuple(map(lambda y: sum(y), zip(*color)))
		self.size = int((self.startsize *factor) + (self.stopsize * (1-factor)))
		self.life -= 1.0 / self.fps

class Emitter(object):
	
	def __init__(self, floater, condfunc ,anglewidth, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative, extraangle = False):

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
		self.extraangle = extraangle
		self.fps = 11
	
	def draw(self, surface, offset = Vec2d(0,0)):
		for particle in self.particles:
			particle.draw(surface, offset)

	def setFPS(self, fps):
		self.fps = fps


	def update(self):
		for particle in self.particles:
			particle.fps = self.fps
			particle.update()
			if particle.life <= 0:
				self.particles.remove(particle)

		if self.condfunc():
			if self.extraangle and self.floater.ship:
				startdir = self.floater.ship.direction + self.floater.direction + self.anglewidth
				stopdir = self.floater.ship.direction + self.floater.direction - self.anglewidth	
			else:
				startdir = self.floater.direction + self.anglewidth
				stopdir = self.floater.direction - self.anglewidth

			delta = -Vec2d(0,0).rotatedd(random.uniform(startdir,stopdir),random.uniform(self.startvelocity,self.stopvelocity))
			if len(self.particles) < self.maximum:
				self.particles.append(Particle(self, Vec2d(0,0), delta, self.startcolor, self.stopcolor, random.uniform(self.startlife,self.stoplife), self.startsize, self.stopsize, self.relative))
		
class CircleEmitter(Emitter):

	def __init__(self, floater, condfunc ,radius, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative):
		Emitter.__init__(self, floater, condfunc ,360, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative)
		self.radius = radius

	def update(self):
		for particle in self.particles:
			particle.fps = self.fps
			particle.update()
			if particle.life <= 0:
				self.particles.remove(particle)

		if self.condfunc():
			if self.floater.ship:
				startdir = self.floater.ship.direction + self.floater.direction + self.anglewidth
				stopdir = self.floater.ship.direction + self.floater.direction - self.anglewidth	
			else:
				startdir = self.floater.direction + self.anglewidth
				stopdir = self.floater.direction - self.anglewidth
			adir = random.uniform(startdir,stopdir)

			delta = Vec2d(0,0).rotatedd(adir,random.uniform(self.startvelocity,self.stopvelocity))
			pos = Vec2d(0,0).rotatedd(adir, self.radius)
			
			if len(self.particles) < self.maximum:
				self.particles.append(Particle(self, pos,delta, self.startcolor, self.stopcolor, random.uniform(self.startlife,self.stoplife), self.startsize, self.stopsize, self.relative))

class RingEmitter(Emitter):

	def __init__(self, floater, condfunc ,startradius, stopradius, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, totalmax, startsize, stopsize, relative):
		Emitter.__init__(self, floater, condfunc ,360, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative)
		self.startradius = startradius
		self.stopradius = stopradius
		self.totalmax =  totalmax
		self.countpart = 0

	def update(self):
		from spaceship import Ship
		for particle in self.particles:
			particle.fps = self.fps
			particle.update()
			if particle.life <= 0:
				self.particles.remove(particle)

		if self.condfunc():
			if isinstance(self.floater, Ship):
				startdir = self.floater.ship.direction + self.floater.direction + self.anglewidth
				stopdir = self.floater.ship.direction + self.floater.direction - self.anglewidth	
			else:
				startdir = self.floater.direction + self.anglewidth
				stopdir = self.floater.direction - self.anglewidth
			adir = random.uniform(startdir,stopdir)

			delta = Vec2d(0,0).rotatedd(adir,random.uniform(self.startvelocity,self.stopvelocity))
			pos = Vec2d(0,0).rotatedd(adir, random.uniform(self.startradius,self.stopradius))
			

			if len(self.particles) < self.maximum and (self.totalmax > self.countpart or self.totalmax == 0):
				self.countpart += 1
				self.particles.append(Particle(self, pos,delta, self.startcolor, self.stopcolor, random.uniform(self.startlife,self.stoplife), self.startsize, self.stopsize, self.relative))

class RingCollector(Emitter):

	def __init__(self, floater, condfunc ,startradius, stopradius, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative):
		Emitter.__init__(self, floater, condfunc ,360, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative)
		self.startradius = startradius
		self.stopradius = stopradius

	def update(self):
		from spaceship import Ship
		for particle in self.particles:
			particle.fps = self.fps
			particle.update()
			if particle.life <= 0:
				self.particles.remove(particle)

		if self.condfunc():
			if isinstance(self.floater, Ship):
				startdir = self.floater.ship.direction + self.floater.direction + self.anglewidth
				stopdir = self.floater.ship.direction + self.floater.direction - self.anglewidth	
			else:
				startdir = self.floater.direction + self.anglewidth
				stopdir = self.floater.direction - self.anglewidth
			adir = random.uniform(startdir,stopdir)

			delta = -Vec2d(0,0).rotatedd(adir,random.uniform(self.startvelocity,self.stopvelocity))
			pos = Vec2d(0,0).rotatedd(adir, random.uniform(self.startradius,self.stopradius))
			

			if len(self.particles) < self.maximum:
				self.particles.append(Particle(self, pos,delta, self.startcolor, self.stopcolor, random.uniform(self.startlife,self.stoplife), self.startsize, self.stopsize, self.relative))
