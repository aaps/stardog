
"""
This is a simplified version of the game solely for testing ship AI
piloting algorithms.  Nothin in Stardog should import this.
The blue ship runs randomly and the red ship tries to catch it.
Controls: 
	space: restart.  
	Leftclick: set current runner heading (it will change)
	Rightclick: toggle human control of the runner.  
	Arrows: control the runner if enabled.
indicators:
	the blue ship moves towards the blue dot (if not human).
	the red ship moves tries to intercept by heading to the red dot.
	the red ship instead avoids the planet if the thick red line (its inertia)
		is between the pink lines and longer than half the thin red line.
SEE "TestAI figures.png"
"""

import pygame
from pygame.locals import *
from math import pi, sin, cos, atan2, sqrt, asin
from random import Random

redStart = 250, 300
blueStart = 600, 400
averageCourseChange = 3 #ai runner changes course this often seconds on avg.
safetyDistance = 20	#don't get this close to a planet
g = 1					#gravitational constant

player2Human = False
random = Random().random
resolution = 800, 600
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()


class Space:
	def __init__(self):
		self.clock = pygame.time.Clock()	#waits between frames.
		self.keys = []  #array of keyboard keys.  1 is pressed, 0 in up.
		for i in range(322):
			self.keys.append(0)
		self.mouse = [(0,0),0,0,0,0,0,0]
		self.ship1 = Ship(self, redStart[0], redStart[1])
		self.ship1.color = [255,0,0]
		self.ship2 = Ship(self, blueStart[0], blueStart[1])
		self.ship2.color = [0,0,255]
		self.ship2.heading =(int(random()*resolution[0]), 
						int(random()*resolution[1]))
		self.planets = []
		self.planets.append(Planet(self, 400, 300, 600, 80))
		self.running = True
		self.dt = .001
		
	def mainloop(self):
		while self.running:
		
			keypoll(self)
			
			handleInput(self)
			
			self.ship1.update()
			self.ship2.update()
			
			#update ship2 from keyboard input:
			if player2Human:
				if self.keys[K_UP % 322]:
					self.ship2.accel()
				if self.keys[K_LEFT % 322]:
					self.ship2.turnLeft()
				if self.keys[K_RIGHT % 322]:
					self.ship2.turnRight()
			else:
				if self.mouse[1]:
					#set heading to mouse click.
					self.ship2.heading = self.mouse[0]
				runnerAI(self.ship2)
			
			#update ship1 from script:
			ai(self.ship1, self.ship2, self.planets)
			
			#gravity:
			for planet in self.planets:
				planet.pull((self.ship1, self.ship2))
			
			#draw stuff:
			for planet in self.planets:
				planet.draw(screen)
			self.ship1.draw(screen)
			self.ship2.draw(screen)
			pygame.draw.circle(screen, self.ship1.color, self.ship1.heading, 1)
			pygame.draw.circle(screen, self.ship2.color, self.ship2.heading, 1)
			#frame maintanance:
			pygame.display.flip()
			screen.fill((0,0,0))
			self.dt = clock.tick(60) / 1000.
			
def keypoll(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.running = 0
		elif event.type == pygame.MOUSEBUTTONDOWN:
			game.mouse[event.button] = 1
			game.mouse[0] = event.pos
		elif event.type == pygame.MOUSEBUTTONUP:
			game.mouse[event.button] = 0
			game.mouse[0] = event.pos
		elif event.type == pygame.MOUSEMOTION:
			game.mouse[0] = event.pos
		elif event.type == pygame.KEYDOWN:
			game.keys[event.key % 322] = 1
		elif event.type == pygame.KEYUP:
			game.keys[event.key % 322] = 0
			
def handleInput(game):
	game.debug = False
	if game.keys[K_BACKSPACE % 322]:
		#you can print your debug info at any point by 
		#using "if game.debug: print(...)"
		game.debug = True #print debug information
		game.keys[K_BACKSPACE % 322] = False
		print "Debug:"
	# quit on esc:
	if game.keys[K_ESCAPE % 322]:
		game.running = False
	
	#toggle human control on right click:
	if game.mouse[3]:
		global player2Human
		player2Human = not player2Human
		game.mouse[3] = 0
		
	#reset ships when space is pressed:
	if game.keys[K_SPACE % 322]:
		game.ship1.x, game.ship1.y = redStart
		game.ship2.x, game.ship2.y = blueStart
		game.ship1.dx, game.ship1.dy = 0,0
		game.ship2.dx, game.ship2.dy = 0,0
			
class Planet:
	def __init__(self, game, x, y, mass, radius):
		self.x, self.y = x,y
		self.game = game		
		self.mass = mass
		self.radius = radius
		
	def pull(self, things):
		for thing in things:
			sqdistance = distance2(self, thing)
			dir = relativeDir(thing, self)
			if sqdistance > self.radius * self.radius:
				thing.dx += cos(dir) * g * self.mass / sqdistance
				thing.dy += sin(dir) * g * self.mass / sqdistance
			else:
				#dir is direction of planet wrt ship, so negative.
				thing.x = self.x - cos(dir) * self.radius
				thing.y = self.y - sin(dir) * self.radius
				thing.color[1] = 255
			
	def draw(self, screen):
		pygame.draw.circle(screen, (50,90,200), (self.x,self.y), self. radius)
			
class Ship:
	dx,dy = 0,0
	dir = 0
	tri = (5,0), (-3, -3), (-3, 3)
	acceleration = 8
	torque = 2 * pi
	turned = False
	acceled = False
	radius = 5
	def __init__(self, game, x, y):
		self.x, self.y = x,y
		self.game = game
	
	def draw(self, surface):
		newTri = []
		sint = sin(self.dir)
		cost = cos(self.dir)
		for point in self.tri:
			newTri.append([point[0] * cost - point[1] * sint + self.x,
						 point[0] * sint + point[1] * cost + self.y])
		pygame.draw.polygon(surface, self.color, newTri)
		
	def update(self):
		self.x += self.dx * self.game.dt
		self.y += self.dy * self.game.dt
		self.color[1] = 0
		self.acceled = False
		self.turned = False
		#keep them on the screen.
		if self.x < 0: 
			self.x = 0 
			self.dx = max(0, self.dx)
		elif self.x > resolution[0]: 
			self.x = resolution[0]
			self.dx = min(0, self.dx)
		if self.y < 0: 
			self.y = 0
			self.dy = max(0, self.dy)
		elif self.y > resolution[1]:
			self.y = resolution[1]
			self.dy = min(0, self.dy)
		
	def accel(self):
		if self.acceled: return
		self.acceled = True
		self.color[1] = 50
		self.dx += self.acceleration * cos(self.dir) * self.game.dt
		self.dy += self.acceleration * sin(self.dir) * self.game.dt
		
	def turnRight(self):
		if self.turned: return
		self.turned = True
		self.dir += self.torque * self.game.dt
		self.dir = angleNorm(self.dir)
		
	def turnLeft(self):
		if self.turned: return
		self.turned = True
		self.dir -= self.torque * self.game.dt
		self.dir = angleNorm(self.dir)
			
def runnerAI(ship):
	"""An AI that commands a ship to fly towards a point that is randomly
	picked at random intervals."""
	if random() * averageCourseChange < ship.game.dt:
		ship.heading =(int(random()*resolution[0]), 
						int(random()*resolution[1]))
	flyTowards(ship, ship.heading)
	
def ai(ship, enemy, planets):
	"""there are three important cases here:
	1. the enemy is not accelerating.
		-should intercept quickly with 0 relative velocity.
	2. the enemy is constantly accelerating.
		-should exceed acceleration and 
	3. the enemy is attempting to avoid us, accelerating in different ways.
	"""
	#get heading to intercept enemy:
	if enemy.acceled:
		accel = enemy.acceleration
	else:
		accel = 0
		
	t = sqrt(distance(ship, enemy) / ship.acceleration) #seconds
	
	targetX = enemy.x + (t * (enemy.dx - ship.dx) + t * t * accel * cos(enemy.dir))
	targetY = enemy.y + (t * (enemy.dy - ship.dy) + t * t * accel * sin(enemy.dir))
	ship.heading = int(targetX), int(targetY)
	
	##check if in danger of crashing into a planet:
	#find nearest planet:
	closest = planets[0]
	dist2 = distance2(ship, closest)
	for planet in planets:
		if distance2(ship,planet) < dist2:
			dist2 = distance(ship,planet)
			closest = planet
	dist = sqrt(dist2)
	#see if our current trajectory will hit the planet:	
	missDist = closest.radius + ship.radius + safetyDistance #min safe dist.
	dangerAngle = asin((missDist) / max(dist, missDist))	#min angle to miss planet by.
	planetDir = relativeDir(ship, closest) 		#direction of the planet.
	currentHeadingAngle = atan2(ship.dy, ship.dx) 	#our inertia vector.
	speed2 = ship.dx**2 + ship.dy**2 			# our inertia speed squared.
	
	if dangerAngle < 0 or dangerAngle > pi / 2:
		dangerAngle = pi / 2
	
	#draw some lines for debugging:
	drawLineFromShip(ship, currentHeadingAngle, speed2 / ship.acceleration, 
						(200,0,0), width=2)
	pygame.draw.line(screen, ship.color, (ship.x,ship.y), (closest.x, closest.y))
	drawLineFromShip(ship, planetDir - dangerAngle, dist, (200,50,100))
	drawLineFromShip(ship, planetDir + dangerAngle, dist, (200,50,100))
	
	if (dist < missDist
	or planetDir - dangerAngle < currentHeadingAngle < planetDir + dangerAngle
		and (dist - missDist) 
			< speed2 / (ship.acceleration - closest.mass * g / (dist2/4)) * 2):
		#we're headed towards the planet!  Thrust perpidicular to it!
		ship.color[2] = 200
		if angleNorm(currentHeadingAngle - planetDir) < 0:
			flyAtDir(ship, planetDir - pi / 2)
		else:
			flyAtDir(ship, planetDir + pi / 2)
	else:
		ship.color[2] = 0
		#we're safe, pursue the target!
		flyTowards(ship, (targetX, targetY))
	
def flyTowards(ship, point):
	"""make the ship fly towards an absolute point."""
	flyAtDir(ship, atan2(point[1] - ship.y, point[0] - ship.x))
	
def flyAtDir(ship, dir):
	"""make the ship fly towards an absolute angle."""
	dirDif=angleNorm(dir - ship.dir)
	if dirDif < 0:
		ship.turnLeft()
	elif dirDif > 0:
		ship.turnRight()
	if -pi/6 < dirDif < pi/6:
		ship.accel()
	if ship.game.debug:
		print("ship heading towards %s, pointed at %s, turning to %s"
					%(ship.heading, ship.dir, goalDir))
					
def distance2(ship1, ship2):
	"""skipping the sqrt makes it faster."""
	return ((ship1.x - ship2.x) * (ship1.x - ship2.x) 
		  + (ship1.y - ship2.y) * (ship1.y - ship2.y))
	
def distance(ship1, ship2):
	return sqrt((ship1.x - ship2.x) ** 2 + (ship1.y - ship2.y) ** 2)
	
def relativeDir(ship1, ship2):
	"""compare this to ship1.dir to see if you're pointed at him."""
	return atan2(ship2.y - ship1.y, ship2.x - ship1.x)
	
def angleNorm(angle):
	"""mods an angle to between -pi and pi."""
	return (angle + pi) % (2 * pi) - pi
	
def drawLineFromShip(ship, angle, dist, color, width=1):
	pygame.draw.line(screen, color, (ship.x,ship.y), 
						(ship.x + dist * cos(angle),
						 ship.y + dist * sin(angle)), width)

if __name__ == "__main__":
	space = Space()
	space.mainloop()			
else:
	print "The AI test is being imported by something. This is probably an error!"
			