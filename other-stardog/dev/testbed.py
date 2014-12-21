#testbed.py
import math
	
def dist2(floater1, floater2):
	"""returns the squared distance between two floaters (center to center)."""
	return (floater1.x - floater2.x) ** 2 + (floater1.y - floater2.y) ** 2
	
def atan2(rise, run):
	return math.degrees(math.atan2(rise, run))
	
def avoidPlanet( ship):
	for planet in ship.system.planets:
		if (abs(planet.x - ship.x) < planet.radius * 2 
		and abs(planet.y - ship.y) < planet.radius * 2 
		and dist2(planet, ship) < (planet.radius* 2) ** 2 ):
			planetDir = atan2(planet.y - ship.y, planet.x - ship.x)
			motionDir = atan2(ship.dy, ship.dx)
			print planet
			# if traveling towards the planet, move away!
			if (not 90 <= (planetDir - motionDir) % 360 <= 270 
			or if ship.dx == 0 and ship.dy == 0):
				# if self.turn(ship, planetDir + 180):
					# ship.forward()
					# print 'thrusting away from planet'
				print 'avoid!', planetDir + 180
				return True
	return False



class Holder:
	x = 0
	y = 0
	radius = 10

p = Holder()
p.x, p.y = 0,0
p.radius = 50

s = Holder()
s.x, s.y = 0,-80
s.radius = 10
s.dx, s.dy = -10, -10

system = Holder()
system.planets = [p]
s.system = system

print avoidPlanet(s)