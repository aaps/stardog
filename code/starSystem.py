#starSystem.py

from utils import *
from floaters import *
from spaceship import *
from strafebat import *
from planet import *
from gui import *
import stardog
from vec2d import Vec2d
from nameMaker import *
from Quadtree import *


class StarSystem(object):
    """A StarSystem holds ships and other floaters."""

    def __init__(self, universe, position=Vec2d(0, 0), boundrad=30000, edgerad=60000):
        self.boundrad = boundrad
        self.position = position
        self.edgerad = edgerad
        self.neighbors = []
        self.universe = universe
        self.floaters = []
        self.spawnScore = 0
        self.spawnMax = 50
        self.toSpawn = []
        self.player = None
        self.ships = []
        self.specialOperations = []
        self.bg = BGImage(self.universe) # the background layer
        self.soundsys = self.universe.game.soundSystem
        self.hitsound = 'se_sdest.wav'
        self.soundsys.register(self.hitsound)
        self.planets = []
        self.name = ""
        self.starpos=self.position-Vec2d(randint(-1100,1100),randint(-1100,1100))#star position

    def addNeighbor(self, starsystem):
        self.neighbors.append(starsystem)
        starsystem.neighbors.append(self)

    def getNeighbors(self):
        return self.neighbors

    def getNeighborposdiff(self):
        posdiffs = []
        for starsystem in self.neighbors:
            posdiff = -(starsystem.position - self.position)
            posdiffs.append((starsystem,posdiff))
        return posdiffs

    def update(self):
        """Runs the game."""

        if self.spawnScore > 0:
            self.spawnScore -= 1

        for floater in self.floaters:
            floater.setFPS(self.universe.game.fps)
            floater.update()

        quad = QuadTree(self.floaters, 3, Rect(-self.edgerad, -self.edgerad,self.edgerad,self.edgerad))

        for floater in self.floaters:
            for hitter in quad.hit(floater.rect):
                self.collide(hitter, floater)

        for floater in self.floaters:
            if floater.pos.get_distance(Vec2d(0,0)) > self.boundrad:
                if isinstance(floater, Ship):
                    floater.overedge = True
                elif floater.pos.get_distance(Vec2d(0,0)) > self.edgerad:   
                    try:
                        floater.kill()
                    except TypeError:
                        print(floater, "exception error")

        #do any special actions that don't fit elsewhere:
        #(currently just laser collisions)
        for function in self.specialOperations:
            function()
        self.specialOperations = []

        for planet in self.planets:

            if not planet.ships and not isinstance(planet, Star) and self.spawnScore < self.spawnMax:
                if planet.respawn > 0:
                    planet.respawn -= 1. / self.universe.game.fps
                    continue
                else:
                    #respawn now!
                    planet.respawn = self.respawnTime #reset respawn timer
                    planet.numShips += 1
                    for i in range(planet.numShips):
                        angle = randint(0, 360)
                        pos = planet.pos.rotatedd(angle, planet.radius + 300)
                        name = nameMaker().getUniqePilotName(self.ships)
                        ship = Strafebat(self.universe, pos,  planet.color, name)
                        
                        planet.ships.append(ship)
                        self.add(ship)
                        ship.planet = planet


    def add(self, floater):
        if (self.spawnScore + floater.spawncost) < self.spawnMax or floater.surespawn:
            if isinstance(floater, Player):
                angle = randint(0,360)
                distanceFromStar = randint(8000, 18000)
                floater.pos = self.starpos.rotatedd(angle, distanceFromStar)

                self.player = floater
            floater.pos=self.position+floater.pos #apsolute coordinates (coordinates system plus relative coordinates floater in system)
            self.spawnScore += floater.spawncost
            floater.starSystem = self
            self.floaters.append(floater)

    def empty(self):
        self.ships[:] = []
        self.floaters[:] = []

# refactor this and put all functionality in corresponding classes, be carefull can quickly spinn into mess.
# piecetime refactor
# perhaps this method can be brokenup in a collision method for planet, ship and part
    def collide(self, a, b):
        """test and act on spatial collision of Floaters a and b"""
        #Because this needs to consider the RTTI of two objects,
        #it is an external function.  This is messy and violates
        #good object-orientation, but when a new subclass is added
        #code only needs to be added here, instead of in every other
        #class.
        if a.tangible and b.tangible and collisionTest(a, b):
            #planet/?
            if isinstance(b, Planet): a,b = b,a
            if isinstance(a, Planet):
                return a.collision(b)

            if isinstance(b, Explosion): a,b = b,a
            if isinstance(a, Explosion):
                self.explosion_push(a,b)

            if isinstance(b, Ship) : a,b = b,a
            if isinstance(a, Ship):
                if isinstance(b, Part) and not b.parent:
                    a.freepartCollision(b)
                    return True

                if isinstance(b, Cargo):
                    a.freepartCollision(b)
                    return True

                hit = False
                if a.hp > 0:
                    if b.hp >= 0 and (sign(b.pos.x - a.pos.x) == - sign(b.delta.x - a.delta.x) \
                                    or sign(b.pos.y - a.pos.y) == - sign(b.delta.y - a.delta.y)):
                        # moving into ship, not out of it.
                        self.crash(a,b)
                        hit = True
                        #if this ship no longer has shields, start over:
                        if a.hp <= 0:
                            self.collide(a, b)
                            return True
                    #shield ship/no shield ship (or less shield than this one)
                    if isinstance(b, Ship) and b.hp <= 0:
                        for part in b.parts:
                            if self.collide(a, part):
                                #if that returned true, everything
                                #should be done already.
                                return True
                    return hit
                else:
                    #recurse to ship parts
                    for part in a.parts:
                        if self.collide(b, part):
                            #works for ship/ship, too.
                            #if that returned true, everything
                            #should be done already.
                            hit = True
                    return hit

            #free part/free part
            if (isinstance(b, Part) or isinstance(b, Cargo) )  and b.parent == None and (isinstance(a, Part) or isinstance(a, Cargo)) and a.parent == None:
                return False #pass through each other, no crash.

            #floater/floater (no ship, planet)
            else:
                self.crash(a, b)
                return True
        return False

    def explosion_push(self, explosion, floater):
        """The push of an explosion.  The rest of the effect is handled by the
        collision branching, which continues."""
        force = (explosion.force / not0(dist2(explosion, floater)) * explosion.radius ** 2)
        direction = floater.pos.get_angle_between(explosion.pos)
        accel = force / not0(floater.mass)
        floater.delta += Vec2d(0,0).rotatedd(direction, accel) / explosion.fps
        
    def crash(self, a, b):
        self.soundsys.play(self.hitsound)
        hpA = a.hp
        hpB = b.hp
        if hpB > 0: a.takeDamage(hpB, b)
        if hpA > 0: b.takeDamage(hpA, a)

    def minDistFromOthers(self, floater):
        mindist = 100000
        for otherfloater in self.planets:
            distance = floater.pos.get_distance(otherfloater.pos)
            if distance < mindist:
                mindist = distance
        return mindist

class SolarA1(StarSystem):
    tinyFighters = []
    maxFighters = 15
    respawnTime = 300
    fightersPerMinute = 2
    g=5000
    def __init__(self, universe, name, location ,numPlanets = 10, numStructures = 2, boundrad = 30000, edgerad= 60000):
        StarSystem.__init__(self, universe, location,boundrad, edgerad)
        self.star = (Star( self, Vec2d(0,0), radius = randint(2000,5000), image = None)) # the star
        #place player:
        angle = randint(0,360)
        self.location = location
        self.planets.append(self.star)
        self.star.numShips = 0
        self.add(self.star)
        self.name = name
        #add planets:

        for i in range(numPlanets):
            angle = randint(0,360)
            distanceFromStar = randint(self.star.radius + 5000, self.boundrad-5000)
            color = randint(40,200),randint(40,200),randint(40,200)
            radius = randint(500,900)
            mass = randnorm(radius * 10, 800)
            startpos = Vec2d(distanceFromStar * cos(angle), distanceFromStar * sin(angle))
            startdir = startpos.get_angle_between(self.star.pos) - 90
            accel = ((self.g * mass) / distanceFromStar) / 10
            # startdelta = Vec2d(0,0).rotatedd(startdir, accel) # preps for gravity sensitive planets
            startdelta = Vec2d(0,0)
            imagename = randImageInDir("res/planets")

            planetimage = loadImage(imagename)
            planet = Planet(self, startpos, startdelta ,self.g,radius = radius, mass = mass, color = color, image = planetimage)
            
            mindistance = self.minDistFromOthers(planet)
            if mindistance > (radius * 6):
                self.planets.append(planet)
            else:
                i-=1
            # d+= 1200

        for i in range(numStructures):
            angle = randint(0,360)
            distanceFromStar = randint(self.boundrad-5000, self.boundrad)
            color = randint(0,100),randint(0,100),randint(0,100)
            radius = randint(400,500)
            self.add(Structure( self, Vec2d(distanceFromStar * cos(angle), distanceFromStar * sin(angle)), color, radius))

        company = Company(self)
        company.addFacility(Fitter())
        self.planets[1].addCompany(Company(self))

        radius = randint(500,700)
        gateway1 = Gateway(self, Vec2d(10000,10000), radius)
        gateway2 = Gateway(self, Vec2d(-10000,-10000), radius)

        gateway1.setSister(gateway2)
        gateway2.setSister(gateway1)

        self.add(gateway1)
        self.add(gateway2)

        for planet in self.planets:
            planet.numShips = 0

            planet.respawn = 30
            self.add(planet)
