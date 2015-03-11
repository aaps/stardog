#cargo.py

from floaters import *


class Cargo(Floater):
    
    def __init__(self, universe):
        pygame.sprite.Sprite.__init__(self)
        # Floater.__init__(self, universe, Vec2d(0,0), Vec2d(0,0), dir = 270, radius = 10, image = self.baseImage)
        if not self.baseImage:
            self.baseImage = loadImage("res/part/default.png")
        
        if not self.color:
            self.color = PART1

        self.universe = universe
        self.detach_space = 50
        self.detach_speed = 100
        self.delta = Vec2d(0,0)
        self.spawncost = 2

        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        
        
        # Part.__init__(self, universe)
        self.radius = max(self.baseImage.get_height() / 2, self.baseImage.get_width() / 2)
        self.resources = True
        # height, width = 9, 3
        self.pickuptimeout = 0
        self.width = self.image.get_width() - 4
        self.height = self.image.get_height() - 4
        self.parent = None
        self.rect = self.image.get_rect()
        self.functions = []
        self.adjectives = []
        self.ports = []
        self.emitters = []
        self.tangible = True
        self.surespawn = False

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
        
        self.name = "Scrap"
        self.damage = 1


class Iron(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "Iron"
        self.damage = 1


class IronOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "IronOre"
        self.damage = 1

class TitaniumOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = (255,255,255)
        Cargo.__init__(self, universe)
        
        self.name = "titaniumOre"
        self.damage = 1

class Titanium(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        self.color = (255,255,255)
        Cargo.__init__(self, universe)
        
        self.name = "Titanium"
        self.damage = 1

class AluminiumOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = (255,100,100)
        Cargo.__init__(self, universe)
        
        self.name = "AluminiumOre"
        self.damage = 1

class Aluminium(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        self.color = (200,200,200)
        Cargo.__init__(self, universe)
        
        self.name = "Aluminium"
        self.damage = 1


class Chemicals(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/chemicals.png")
        self.color = (100,250,100)
        Cargo.__init__(self, universe)
        
        self.name = "Chemicals"
        self.damage = 1

class Food(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/food.png")
        self.color = (250,250,100)
        Cargo.__init__(self, universe)
        
        self.name = "Food"
        self.damage = 1


class Gems(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/gems.png")
        self.color = (250,50,50)
        Cargo.__init__(self, universe)
        
        self.name = "Gems"
        self.damage = 1


class ExMetal(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = (100,100,100)
        Cargo.__init__(self, universe)
        
        self.name = "Ex metal"
        self.damage = 1


class SheetMetal(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/sheetmetal.png")
        self.color = (100,100,100)
        Cargo.__init__(self, universe)
        
        self.name = "Sheet metal"
        self.damage = 1


class ConstMat(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "ConstMat"
        self.damage = 1


class CompComp(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/compcomp.png")
        self.color = (50,200,50)
        Cargo.__init__(self, universe)
        
        self.name = "CompComp"
        self.damage = 1


class MachParts(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/machparts.png")
        self.color = (100,150,100)
        Cargo.__init__(self, universe)
        
        self.name = "MachParts"
        self.damage = 1

class Plastics(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/plastics.png")
        self.color = (100,200,200)
        Cargo.__init__(self, universe)
        
        self.name = "Plastics"
        self.damage = 1


class Explosives(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/explosives.png")
        self.color = (100,150,150)
        Cargo.__init__(self, universe)
        
        self.name = "Explosives"
        self.damage = 1

class Minerals(Cargo):
    
    image = None
    def __init__(self, universe):
        self.color = (50,50,50)
        self.baseImage = loadImage("res/goods/minerals.png")
        Cargo.__init__(self, universe)
        
        self.name = "Minerals"
        self.damage = 1


class AirFilters(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "Air filters"
        self.damage = 1

class PleasureCubes(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/pleasurecubes.png")
        self.color = (200,200,100)
        Cargo.__init__(self, universe)
        
        self.name = "Pleasure cubes"
        self.damage = 1


class Alcohol(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = (150,150,100)
        Cargo.__init__(self, universe)
        
        self.name = "Alcohol"
        self.damage = 1


class Textiles(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/textiles.png")
        self.color = (200,200,200)
        Cargo.__init__(self, universe)
        
        self.name = "Textiles"
        self.damage = 1


class HuskarCigars(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "Huskar cigars"
        self.damage = 1


class ServantDroids(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "Servant droids"
        self.damage = 1

class CloningDevice(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        self.color = None
        Cargo.__init__(self, universe)
        
        self.name = "Cloning device"
        self.damage = 1

class PureWater(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/water.png")
        self.color = (0,100,200)
        Cargo.__init__(self, universe)
        
        self.name = "Pure water"
        self.damage = 1
