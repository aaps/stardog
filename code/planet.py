#planet.py

from utils import *
from floaters import Floater
from adjectives import randItem, randCargo
from parts import *
from Resources import *
from spaceship import *
import stardog
from vec2d import Vec2d
from facilitys import *


class Planet(Floater):
    
    
    def __init__(self, starsystem, pos, delta = Vec2d(0,0), grav=5000, radius = 100, mass = 10000, \
                    color = (100,200,50), image = None, race = None):
        Floater.__init__(self, starsystem.universe, pos, delta, radius = radius, image = image)
        self.maxRadius = 1000000 # no gravity felt past this (approximation).
        self.planet_damage = .0004
        self.landing_speed = 200 #pixels per second. Under this, no damage.
        self.spawncost = 5
        self.surespawn = True
        self.companys = []
        self.mass = mass #determines gravity.
        self.color = color
        self.starSystem = starsystem
        self.firstname = "Planet"
        self.secondname = "Unknown"
        self.g = grav
        self.damage = {}    
        #see solarSystem.planet_ship_collision
        self.race = None #race that owns this planet
        self.fps = 10
        self.image = None
        if image:
            self.image = pygame.Surface((radius*2, radius*2), flags = hardwareFlag)
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), int(self.radius))
            tempimg = pygame.transform.scale(image, (radius*2+10,radius*2+10))
            self.image.blit(tempimg, (-5,-5))
            self.image.set_colorkey((0,0,0))
        
        self.inventory = []
        for x in range(randint(1,8)):
            self.inventory.append(randItem(self.starSystem.universe, 1))

        self.inventory.append(randCargo(self.starSystem.universe))



    def setFPS(self, fps):
        self.fps = fps
    
    def update(self):
        for other in self.starSystem.floaters.sprites():
            if other != self \
            and not isinstance(other, Structure) \
            and not isinstance(other, Planet) \
            and not collisionTest(self, other) \
            and abs(self.pos.get_distance(other.pos)) < self.maxRadius \
            and abs(Vec2d(0,0).get_distance(other.pos)) < self.starSystem.boundrad:

                if isinstance(other, Ship) and other.landed:
                    return

                #accelerate that floater towards this planet:
                accel = self.g * (self.mass) / (dist2(self, other))
                angle = (self.pos - other.pos).get_angle()
                other.delta += Vec2d(0,0).rotatedd(angle,accel) / self.fps

        for emitter in self.emitters:
            emitter.update()

        for company in self.companys:
            company.update()

        # Floater.update(self) # for gravity sensitive planets update
    
    def draw(self, surface, offset = Vec2d(0,0)):
        
        pos = self.pos - offset
        
        if self.image:
            Floater.draw(self, surface, offset)
        else:
            pygame.draw.circle(surface, self.color, pos.inttup(), int(self.radius))
        for emitter in self.emitters:
            emitter.draw(surface, offset)


    def takeDamage(self, damage, other):
        pass

    def collision(self, other):
        if  sign(other.pos.x - self.pos.x) == sign(other.delta.x - self.delta.x) \
            and sign(other.pos.y - self.pos.y) == sign(other.delta.y - self.delta.y):# moving away from planet.
                return False
        # planet/ship
        #planet/part
        elif isinstance(other, Part) or isinstance(other, Cargo) and other.parent == None:
            self.freepartCollision(other)
            return True
        elif isinstance(other, Ship):
            if isinstance(self, Gateway):
                other.gatewayCollision(self)
            else:   
                other.planetCollision(self)
        #planet/planet
        elif isinstance(other, Planet):
            self.planetCollision(other)
            return True
        else:
            other.crash(self)

    def freepartCollision(self, part):
        part.kill()

        if rand() > .8 and not isinstance(part, Cargo):

            part.dir = 0
            part.image = colorShift(pygame.transform.rotate(part.baseImage, part.dir), part.color).convert_alpha()
        else:
            part = Scrap(self.starSystem.universe)
        self.inventory.append(part)

    def planetCollision(self, planet):
        if self.mass > planet.mass:
            planet.kill()
        else:
            self.kill()

    def addCompany(self, company):
        self.companys.append(company)



class Star(Planet):
   
    
    def __init__(self, starsystem, pos, delta = Vec2d(0,0), grav=5000, radius = 3000, image = None):

        mass = radius * 100
        color = bulletColor((mass+.1)/250000)
        Planet.__init__(self, starsystem, pos, delta, grav, radius, mass, color, image)
        self.planet_damage = 300
        self.landing_speed = -999
        self.firstname = "Star Unknown"
        self.emitters.append(RingEmitter( self, self.condAlways , radius, radius+50, 200, 220,  (255,255,255,250), (251,0,0,1), 2, 3, 800, 0, 10, 1, True))


class Structure(Planet):

    def __init__(self, starsystem, pos, delta, grav=5000, color = (100,200,50), radius = 100, image = None):
        Floater.__init__(self, starsystem.universe, pos, Vec2d(0,0), 0, image=image)
        self.firstname = "Structure Unknown"
        self.landing_speed = 200 #pixels per second. Under this, no damage.
        self.planet_damage = .0004
        self.color = BLUE
        self.g = grav
        self.starSystem = starsystem
        self.damage = {}    
        self.radius = radius
        #see solarSystem.planet_ship_collision
        self.race = None #race that owns this planet
        if image == None:
            self.image = None
        self.inventory = []

    def update(self):
        pass

    def draw(self, surface, offset = Vec2d(0,0)):
        if self.image:
            pos = (int(self.pos.x - self.image.get_width()  / 2 - offset[0]), 
                  int(self.pos.y - self.image.get_height() / 2 - offset[1]))
            surface.blit(self.image, pos())
        else:
            pos = self.pos - offset
            rect = Rect(pos.x-self.radius*0.875,pos.y-self.radius*0.875,self.radius*1.75,self.radius*1.75)
            pygame.draw.rect(surface, self.color, rect)

    def takeDamage(self, damage, other):
        pass

class Gateway(Planet):
	
	
	def __init__(self, starsystem, pos, radius, mass = 10000, color = (100,200,50), image = None, race = None):
		Floater.__init__(self, starsystem.universe, pos, Vec2d(0,0), radius = radius, image = image)
		
		self.image = pygame.Surface((radius*2, radius*2), flags = hardwareFlag).convert()
		self.image.set_colorkey(BLACK)
		self.starSystem = starsystem
		maxRadius = 50000 # no gravity felt past this (approximation).
		self.tangible = True
		self.g = 5000 # the gravitational constant.
		self.firstname = "Gateway Unknown"
		# self.rect = None

		self.sister = None
		self.mass = mass #determines gravity.
		self.starsystem = starsystem
		self.color = color
		self.race = None 
		self.inventory = []
	
	def setSister(self, gateway):
		if isinstance(gateway, Gateway):
			self.sister = gateway

	def update(self):
		
		for other in self.starsystem.floaters.sprites():
			if  not isinstance(other, Planet) \
			and not isinstance(other, Structure) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.radius * 1.2:
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / dist2(self, other)
				angle = (self.pos - other.pos).get_angle()
				other.delta += Vec2d(0,0).rotatedd(angle, accel) / self.fps
				

	def getSister(self):
		return self.sister
	
	def draw(self, surface, offset = Vec2d(0,0)):
			self.image.fill((0, 0, 0))

			poss = Vec2d(self.image.get_width()/2, self.image.get_height()/2)
			pos = self.pos - offset - poss

			pygame.draw.circle(self.image, self.color, poss.inttup(), int(self.radius))
			pygame.draw.circle(self.image, (0,0,0,0), poss.inttup(), int(self.radius)-50)
			surface.blit(self.image, pos)
			

	def takeDamage(self, damage, other):
		pass
