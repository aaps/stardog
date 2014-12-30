# nameMaker.py
import random
from spaceship import *
from planet import *

class nameMaker(object):

	firstnames = ["Donnie","Elena","Latoya","Franklin","Geraldine","Bob", "Perl", "Jacob"]
	secondnames = ["Bendson","Carr","Gutierrez","Bradley","Arnold","Knight","Hicks","Harrison"]
	starnames = ["Apus", "Andromida","Antila","Aquarius","Aquila","Ara","Aries","Auriga","Bootes","Caelum"]
	planetnames = ["Alpha","Beta","Gamma","Delta","Epsylon","Zeta","Eta","Theta","Iota"]


	def __init__(self):
		pass

	def getUniqePilotName(self, listoffloaters):
		while True:
			first = random.sample(self.firstnames,1)[0]
			second = random.sample(self.secondnames,1)[0]
			ships = False
			if len(listoffloaters) > 0:
				for floater in listoffloaters:
					if isinstance(floater, Ship):
						Ships = True
						if not floater.firstname == first and floater.secondname == second:
							return (first, second)
			if not ships:
				return (first, second)

	def getUniqueStarName(self, stars):
		while True:
			starname = random.sample(self.starnames,1)
			starsp = False
			if len(stars) > 0:
				for star in stars:
					if isinstance(sun, Star):
						starsp = True
						if not star.firstname == starname:
							return starname
			if not starsp:
				return starname

	def getUniquePlanetName(self, planets):
		while True:
			planetname = random.sample(self.planetnames,1)
			planetsp = False
			if len(planets) > 0:
				for planet in planets:
					if isinstance(planet, Planet):
						planetsp = True
						if not planet.firstname == planetname:
							return planetname
			if not planetsp:
				return planetname