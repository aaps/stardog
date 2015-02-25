#cargo.py

from floaters import *


class Cargo(Floater):
    
    def __init__(self, universe):
        
        Floater.__init__(self, universe, Vec2d(0,0), Vec2d(0,0), dir = 270, radius = 10)
        if not self.baseImage:
            self.baseImage = loadImage("res/part/default.png")
        # Part.__init__(self, universe)
        self.radius = max(self.baseImage.get_height() / 2, self.baseImage.get_width() / 2)
        self.resources = True
        # height, width = 9, 3
        self.pickuptimeout = 0
        self.width = self.image.get_width() - 4
        self.height = self.image.get_height() - 4
        self.parent = None
        self.color = PART1
        self.detach_space = 50
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.functions = []
        self.adjectives = []

    def update(self):
        if self.pickuptimeout > 0:
            self.pickuptimeout -= 1. / self.fps
        Floater.update(self)

    def shortStats(self):
        return self.name

    def shortStats(self):
        return  self.name

    def stats(self):
        return "It is " + self.name

    def scatter(self, ship):
        """Like detach, but for parts that are in an inventory when a 
        ship is destroyed."""
        self.pickuptimeout = 5
        angle = randint(0,360)
        offset = Vec2d(cos(angle) * self.detach_space, sin(angle) * self.detach_space)
        #set physics to drift away from ship (not collide):
        self.image = colorShift(pygame.transform.rotate(self.baseImage, angle), self.color).convert_alpha()
        # self.image.set_colorkey(BLACK)
        self.pos = ship.pos + offset
        self.delta.x = ship.delta.x + (rand()  * detach_speed)

        # self.ship = None
        self.universe.curSystem.add(self)

class Scrap(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/scrap.png")
        Cargo.__init__(self, universe)
        
        self.name = "Scrap"
        self.damage = 1


class Iron(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        Cargo.__init__(self, universe)
        
        self.name = "Iron"
        self.damage = 1


class IronOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "IronOre"
        self.damage = 1


class Chemicals(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Chemicals"
        self.damage = 1

class Food(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Food"
        self.damage = 1


class Gems(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Gems"
        self.damage = 1


class ExMetal(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Ex metal"
        self.damage = 1


class SheetMetal(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Sheet metal"
        self.damage = 1


class ConstMat(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "ConstMat"
        self.damage = 1


class CompComp(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "CompComp"
        self.damage = 1


class MachParts(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "MachParts"
        self.damage = 1

class Plastics(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Plastics"
        self.damage = 1


class Explosives(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Explosives"
        self.damage = 1

class Minerals(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Minerals"
        self.damage = 1


class AirFilters(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Air filters"
        self.damage = 1

class PleasureCubes(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Pleasure cubes"
        self.damage = 1


class Alcohol(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Alcohol"
        self.damage = 1


class Textiles(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Textiles"
        self.damage = 1

class Alcohol(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Alcohol"
        self.damage = 1

class HuskarCigars(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Huskar cigars"
        self.damage = 1

class Alcohol(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Alcohol"
        self.damage = 1

class ServantDroids(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Servant droids"
        self.damage = 1

class CloningDevice(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Cloning device"
        self.damage = 1

class PureWater(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "Pure water"
        self.damage = 1
