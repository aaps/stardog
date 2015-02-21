#strafebat.py

from utils import *
from spaceship import *
from parts import *
from scripts import *
import stardog
from adjectives import *

class Strafebat(Ship):
	strafeRadius = 100
	planet = None
	level = 3
	
	def __init__(self, universe, pos, color, name):
		roll = rand()
		self.target = None
		self.universe = universe
		self.circling = False
		Ship.__init__(self, universe.game, pos, Vec2d(0,0), color = color, name=name)
		self.scripts.append(StrafebatScript(universe.game))
		self.baseBonuses['damageBonus'] = .5
		cockpit = StrafebatCockpit(universe)
		gyro = Gyro(universe)
		gun = StrafebatCannon(universe)
		quarters = Quarters(universe)
		engine = Engine(universe)
		generator = Generator(universe)
		battery = Battery(universe)
		shield = BigShield(universe)
		rCannon = RightCannon(universe)
		lCannon = LeftCannon(universe)
		interconnect = Interconnect(universe)
		missilelaunch = MissileLauncher(universe)
		for part in [cockpit, gyro, gun, engine, generator, battery, shield, 
						rCannon, lCannon, quarters, interconnect]:
			if rand() > .8:
				addAdjective(part)
				if rand() > .6:
					addAdjective(part)
			part.color = color
		self.addPart(cockpit)
		cockpit.addPart(gun, 0)
		cockpit.addPart(gyro, 2)
		gyro.addPart(engine, 1)
		gyro.addPart(generator, 0)
		if .9 < roll:
			generator.addPart(battery, 0)
			gyro.addPart(shield, 2)
		else: 
			gyro.addPart(battery, 2)
		if .8 < roll < .9:
			generator.addPart(rCannon, 0)
		if .7 < roll < .8:
			battery.addPart(lCannon, 0)
		if .6 < roll < .7:
			battery.addPart(quarters, 0)
		if .5 < roll < .6:
			battery.addPart(interconnect, 0)
			interconnect.addPart(missilelaunch, 2)
			self.energy = self.maxEnergy


class StrafebatScript(AIScript):
	"""A scripts with basic physics calculation functions."""
	interceptSpeed = 100.
	returnSpeed = 50.
	acceptableError = 2
	shootingRange = 400
	
	def update(self, ship):
		# if too close to planet
		if dist2(ship.planet, ship) < (300 + ship.planet.radius) ** 2:
			if self.turnTowards(ship, ship.planet, 180):
				ship.forward()# move away from planet.
				return
				
		# find closest ship:
		if not ship.radars[-1].enabled:
			ship.radars[-1].toggle()
		ships = ship.radars[-1].detected
		ship.curtarget = self.closestShip(ship, ships)
		
		if not ship.curtarget:# no target
			self.intercept(ship, ship.planet, self.returnSpeed)
			return
		
		if ship.curtarget.pos.get_distance(ship.pos) < self.shootingRange * 2 \
		and ship.guns: # within range.
			self.interceptShot(ship, ship.curtarget)
			return
			
		self.intercept(ship, ship.curtarget, self.interceptSpeed)
			
	def closestShip(self, ship, ships):
		"""finds the closest ship not-friendly to this one."""
		target = None

		for ship2 in ships:
			if isinstance( ship2, Ship):
				if not isinstance(ship2, Strafebat) or ship2.planet != ship.planet:
					target = ship2
		return target
		
