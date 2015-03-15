#cargo.py

from floaters import *


class Cargo(Floater):
    
    def __init__(self, universe):

        Floater.__init__(self, universe, Vec2d(0,0), Vec2d(0,0), direction = 270, radius = 10, spritename = None)

        self.detach_space = 50
        self.detach_speed = 100
        self.resources = True
        self.pickuptimeout = 0
        # self.width = self.image.get_width() - 4
        # self.height = self.image.get_height() - 4
        self.parent = None
        self.functions = []
        self.adjectives = []
        self.ports = []


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

        self.pos = ship.pos + offset
        self.delta.x = ship.delta.x + (rand()  * self.detach_speed)

        self.universe.curSystem.add(self)

    def setFPS(self, fps):
        for port in self.ports:
            if port.part:
                port.part.setFPS(fps)
        self.fps = fps

class Scrap(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/scrap.png")
        self.color = None
        Cargo.__init__(self, universe)
        self.color = PART1
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.name = "Scrap"
        self.damage = 1


class Iron(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        self.color = None
        Cargo.__init__(self, universe)
        self.color = PART1
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.name = "Iron"
        self.damage = 1


class IronOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        self.color = PART1
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.name = "IronOre"
        self.damage = 1

class TitaniumOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        
        Cargo.__init__(self, universe)
        self.color = (255,255,255)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.name = "titaniumOre"
        self.damage = 1

class Titanium(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        Cargo.__init__(self, universe)
        self.color = (255,255,255)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        
        self.name = "Titanium"
        self.damage = 1

class AluminiumOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        self.color = (255,100,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "AluminiumOre"
        self.damage = 1

class Aluminium(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        
        Cargo.__init__(self, universe)
        self.color = (200,200,200)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Aluminium"
        self.damage = 1


class Chemicals(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/chemicals.png")
        
        Cargo.__init__(self, universe)
        self.color = (100,250,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Chemicals"
        self.damage = 1

class Food(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/food.png")
        Cargo.__init__(self, universe)
        self.color = (250,250,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Food"
        self.damage = 1


class Gems(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/gems.png")
        
        Cargo.__init__(self, universe)
        self.color = (250,50,50)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Gems"
        self.damage = 1


class ExMetal(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        
        Cargo.__init__(self, universe)
        self.color = (100,100,100)

        
        self.name = "Ex metal"
        self.damage = 1


class SheetMetal(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/sheetmetal.png")
        
        Cargo.__init__(self, universe)
        self.color = (100,100,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Sheet metal"
        self.damage = 1


class ConstMat(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        
        Cargo.__init__(self, universe)
        self.color = (100,100,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "ConstMat"
        self.damage = 1


class CompComp(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/compcomp.png")
        Cargo.__init__(self, universe)
        
        self.color = (50,200,50)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.name = "CompComp"
        self.damage = 1


class MachParts(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/machparts.png")
        
        Cargo.__init__(self, universe)
        self.color = (100,150,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "MachParts"
        self.damage = 1

class Plastics(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/plastics.png")
        
        Cargo.__init__(self, universe)
        self.color = (100,200,200)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Plastics"
        self.damage = 1


class Explosives(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/explosives.png")
        Cargo.__init__(self, universe)
        self.color = (100,150,150)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Explosives"
        self.damage = 1

class Minerals(Cargo):
    
    image = None
    def __init__(self, universe):
        
        self.baseImage = loadImage("res/goods/minerals.png")
        Cargo.__init__(self, universe)
        self.color = (50,50,50)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Minerals"
        self.damage = 1


class AirFilters(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        
        Cargo.__init__(self, universe)
        self.color = (50,50,50)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Air filters"
        self.damage = 1

class PleasureCubes(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/pleasurecubes.png")
        
        Cargo.__init__(self, universe)
        self.color = (200,200,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Pleasure cubes"
        self.damage = 1


class Alcohol(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        
        Cargo.__init__(self, universe)
        self.color = (150,150,100)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Alcohol"
        self.damage = 1


class Textiles(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/textiles.png")
        
        Cargo.__init__(self, universe)
        self.color = (200,200,200)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Textiles"
        self.damage = 1


class HuskarCigars(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)

        
        self.name = "Huskar cigars"
        self.damage = 1


class ServantDroids(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")

        Cargo.__init__(self, universe)
        self.color = (200,200,200)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Servant droids"
        self.damage = 1

class CloningDevice(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        self.color = (200,200,200)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Cloning device"
        self.damage = 1

class PureWater(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/water.png")
        Cargo.__init__(self, universe)
        self.color = (0,100,200)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        self.name = "Pure water"
        self.damage = 1
