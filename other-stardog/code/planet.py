#planet.py


from utils import *
from floaters import Floater
from adjectives import randItem
import parts
import partCatalog


def planetGenerator(game, name, race, sun, distance, image=None):
	"""Generates a random planet from a few parameters.
	name:string, race:Race, sun:Sun, distance:float-min distance from the sun.
	Returns d,planet, where d is the minimum distance for the next planet."""
	ecc = rand() / 5
	rad = randint(200,1000)
	mass = abs(randnorm(rad ** 2.1 / 25, rad ** 1.3))
	grav = (1+ecc) * (sqrt(sun.mass*mass) - mass) / (sun.mass-mass)
	distanceFromSun = int(distance / (1 - ecc - grav) + randint(0,2000))
	color = randint(40,255),randint(40,255),randint(40,255)
	planet = Planet(game, sun, radius = rad, mass = mass, color = color,
		image = None, name = name, Anomaly = randint(1,360),
		SemiMajor = distanceFromSun, LongPeriapsis = randint(1,360),
		eccentricity = ecc, bounce = rand() / 2, race = race,
		population = randint(1000,20000), life = randint(1,5) / 100. / 3600.,
		resources = randint(5,20) / 10.)
	d = distanceFromSun * (1 + ecc + grav)
	return d, planet

def planetVel(planet):
	"""Gets the actual velocity of a planet"""
	orbvel = sqrt(planet.g * planet.parent.mass * (2/planet.distance-1/planet.SMa))
	smi = planet.SMa * sqrt(planet.p)
	vx = orbvel * -planet.SMa * math.sin(planet.EccAn) / sqrt((smi * math.cos(planet.EccAn)) ** 2 \
	+ (planet.SMa * math.sin(planet.EccAn)) ** 2)
	vy = orbvel * smi * math.cos(planet.EccAn) / sqrt((smi * math.cos(planet.EccAn)) ** 2 \
	+ (planet.SMa * math.sin(planet.EccAn)) ** 2)
	planetvel = rotate(vx, vy, planet.LPe)
	return planetvel

def hillRadius(primary,secondary,dis):
	"""Calculates the Hill radius of a secondary body orbiting the primary at a given distance.
	It assumes a circular orbit"""
	if isinstance(primary, Planet):
		M1 = primary.mass
	else:
		M1 = primary
	if isinstance(secondary, Planet):
		m2 = secondary.mass
	else:
		m2 = secondary
	h0 = 0
	h1 = dis * (m2/(3*M1)) ** 0.333
	while abs(h1-h0) > 1:
		h0 = h1 #Using Newton's method to solve the quintic equation. L1 distance calculated
		h1 -= (M1/dis**3*h0**5 - 3*M1/dis**2*h0**4 + 3*M1/dis*h0**3 - m2*h0**2 + 2*m2*dis*h0 - m2*dis**2)\
		/ (5*M1/dis**3*h0**4 - 12*M1/dis**2*h0**3 + 9*M1/dis*h0**2 - 2*m2*h0 + 2*m2*dis)
	return h1

def Eanomaly(M,e):
	"""Obtains eccentric anomaly for a given mean anomaly (M) and eccentricity (e). Use radians"""
	E0 = 0    #solve the Kepler equation (M=E-e*sin(E)) for E (eccentric anomaly)
	E1 = M    #the function works with radians to improve computing speed
	while abs(E1-E0) > 1e-6: #number of iterations depends strongly on e, and on M in less grade
		E0 = E1                 #with e<0.2 it varies between 1 and 10; typically there are 7 iterations
		E1 = M + e*math.sin(E0)
	return E1

class Planet(Floater):
	PLANET_DAMAGE = .001
	LANDING_SPEED = 200 #pixels per second. Under this, no damage.
	g = 3000 # the gravitational constant.
	shipInProgress = None
	shipValue = 0
	hp = 30000
	gravitates = False
	def __init__(self, game, parent, radius = 100, mass = 1000,
					color = (100,200,50), image = None, name = 'planet',
					Anomaly = 0, SemiMajor= 10000, LongPeriapsis = 0, eccentricity = 0,
                    period = 0, bounce = 0.5, race = None, population = 1, life = 1, resources = 1):
		#get initial position
		distance = SemiMajor * (1-eccentricity**2) / (1+eccentricity*cos(Anomaly))
		pos = rotate(distance * cos(Anomaly), distance * sin(Anomaly), LongPeriapsis)
		x, y = pos[0], pos[1]
		Floater.__init__(self, game, x, y, radius = radius)
		#orbital parameters
		self.SMa = SemiMajor #defines size of the orbit
		self.LPe = LongPeriapsis #the orientation of the ellipse
		self.e = eccentricity #defines the shape of the orbit, must be 0<e<1; it can be 0
		if period == 0: #by default, the period is the one of a classic keplerian orbit
			self.period = 2 * pi * sqrt(self.SMa ** 3 / (self.g * parent.mass))
		else:
			self.period = period
		self.ano = math.radians(Anomaly)
		self.n = 2*pi/self.period #mean motion
		self.tAn = sqrt((1+self.e)/(1-self.e)) #used to calculate true anomaly
		self.p = (1-self.e**2) #semi-latus rectum factor, SMa * p = Semi-latus rectum
		self.mass = mass #determines gravity.
		self.parent = parent #the parent body, a star for planets, a planet for moons
		self.color = color
		self.bounciness = bounce
		self.maxRadius2 = 200*self.g*self.mass # no gravity felt past the square root of this
		self.damage = {}
		# damage[ship] is the amount of damage a ship has yet to take,
		# see solarSystem.planet_ship_collision
		self.race = race #race that owns this planet
		self.population = population
		self.life = life #growth rate depends on value.
		self.resources = resources #build rate depends on resources and pop.
		self.buildProgress = 100
		self.name = name
		if image == None:
			self.image = None
		else:
			self.image = pygame.transform.rotate(pygame.transform.scale(
							image, (radius * 2, radius * 2)), -atan2(y,x))
		self.inventory = []
		self.inventory.append(partCatalog.TakeOffEngine(game))
		for x in range(randint(1,4)):
			self.inventory.append(randItem(game, 1))
		self.cities = self.population / 1000

	def update(self, dt):
		for other in self.game.curSystem.floaters:
			if  (other.gravitates
			and dist2(self, other) < self.maxRadius2
			and not collisionTest(self, other) ):
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / dist2(self, other)
				angle = atan2(self.y - other.y, self.x - other.x)
				other.dx += cos(angle) * accel * dt
				other.dy += sin(angle) * accel * dt
		#update orbital position
		self.M = self.n * self.game.playTime + self.ano
		self.EccAn = Eanomaly(self.M, self.e)
		self.tAnom = 2 * math.atan(self.tAn*math.tan(self.EccAn/2)) #get true anomaly
		self.distance = self.SMa * self.p / (1+self.e*math.cos(self.tAnom))
		pos = rotate(self.distance * math.cos(self.tAnom), self.distance * math.sin(self.tAnom), self.LPe)
		self.x, self.y = pos[0], pos[1]
		if self.race:
			self.race.updatePlanet(self)

	def draw(self, surface, offset = (0,0)):
		if self.image:
			pos = (int(self.x - self.image.get_width()  / 2 - offset[0]),
				  int(self.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos)

		else:
			pos = int(self.x - offset[0]), \
				  int(self.y - offset[1])
			pygame.draw.circle(surface, self.color, pos, int(self.radius))

	def takeDamage(self, damage, other):
		pass

class Sun(Planet):
	PLANET_DAMAGE = 300
	LANDING_SPEED = -999 #no landing on the sun.
	t = 0
	def __init__(self, game, radius = 1000, mass = 100000.,
					color = (255,128,0), image = None, name = 'star',
					Anomaly = 0, SemiMajor = 0, LongPeriapsis = 0, eccentricity = 0, period = 0):
		#get initial position
		distance = SemiMajor * (1-eccentricity**2) / (1+eccentricity*cos(Anomaly))
		pos = rotate(distance * cos(Anomaly), distance * sin(Anomaly), LongPeriapsis)
		x, y = pos[0], pos[1]
		Floater.__init__(self, game, x, y, radius = radius)
		#orbital parameters
		self.SMa = SemiMajor #defines size of the orbit
		self.LPe = LongPeriapsis #the orientation of the ellipse
		self.e = eccentricity #defines the shape of the orbit, must be 0<e<1; it can be 0
		if period == 0: #by default, the star doesn't orbit
			if self.SMa != 0:
				self.period = 2 * pi * sqrt(self.SMa ** 3 / (self.g * 1000000))
			else:
				self.period = 1
		else:
			self.period = period
		self.ano = math.radians(Anomaly)
		self.n = 2*pi/self.period #mean motion
		self.tAn = sqrt((1+self.e)/(1-self.e)) #used to calculate true anomaly
		self.p = (1-self.e**2) #semi-latus rectum factor, SMa * p = Semi-latus rectum
		self.mass = mass #determines gravity.
		self.maxRadius2 = 200*self.g*self.mass # no gravity felt past the square root of this
		self.color = color
		self.damage = {}
		# damage[ship] is the amount of damage a ship has yet to take,
		# see solarSystem.planet_ship_collision
		self.name = name
		if image == None:
			self.image = None
		else:
			self.image = pygame.transform.rotate(pygame.transform.scale(
							image, (radius * 2, radius * 2)), -atan2(y,x))
		self.inventory = []
	def update(self, dt):
			for other in self.game.curSystem.floaters:
				if  (other.gravitates
				and dist2(self, other) < self.maxRadius2
				and not collisionTest(self, other) ):
					#accelerate that floater towards this planet:
					accel = self.g * (self.mass) / dist2(self, other)
					angle = atan2(self.y - other.y, self.x - other.x)
					other.dx += cos(angle) * accel * dt
					other.dy += sin(angle) * accel * dt
			#update orbital position
			self.M = self.n * self.game.playTime + self.ano
			self.EccAn = Eanomaly(self.M, self.e)
			self.tAnom = 2 * math.atan(self.tAn*math.tan(self.EccAn/2)) #get true anomaly
			self.distance = self.SMa * self.p / (1+self.e*math.cos(self.tAnom))
			pos = rotate(self.distance * math.cos(self.tAnom), self.distance * math.sin(self.tAnom), self.LPe)
			self.x, self.y = pos[0], pos[1]

	def draw(self, surface, offset = (0,0)):
		if self.image:
			pos = (int(self.x - self.image.get_width()  / 2 - offset[0]),
				  int(self.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos)

		else:
			pos = int(self.x - offset[0]), \
				  int(self.y - offset[1])
			for x in range(21):
				color = (255 , 55 + (200 - (20 - x) * abs(10 - self.t % 20)), 100 / 20 * x)
				pygame.draw.circle(surface, color, pos, int(self.radius - 20 * x))
		self.t -= 5. * self.game.dt #speed of throbbing color.





