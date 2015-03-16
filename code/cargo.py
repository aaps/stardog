#cargo.py

from floaters import *


class Cargo(Floater):
    
    def __init__(self, universe):

        Floater.__init__(self, universe, Vec2d(0,0), Vec2d(0,0), direction = 270, radius = 10, spritename = None)

        self.detach_space = 50
        self.detach_speed = 100
        self.resources = True
        self.pickuptimeout = 0
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

    def __init__(self, universe):

        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/scrap.png", 'pos':(0,0), 'color':PART1, 'direction':None,'zoom':None}
        self.image=None

        self.name = "Scrap"
        self.damage = 1


class Iron(Cargo):
    
    def __init__(self, universe):

        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/iron.png", 'pos':(0,0), 'color':PART1, 'direction':None,'zoom':None}
        self.image=None

        self.name = "Iron"
        self.damage = 1


class IronOre(Cargo):
    
    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':PART1, 'direction':None,'zoom':None}
        self.image=None
        self.name = "IronOre"
        self.damage = 1

class TitaniumOre(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(255,255,255), 'direction':None,'zoom':None}
        self.image=None

        self.name = "titaniumOre"
        self.damage = 1

class Titanium(Cargo):
    
    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/iron.png", 'pos':(0,0), 'color':(255,255,255), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Titanium"
        self.damage = 1

class AluminiumOre(Cargo):
    
    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(255,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "AluminiumOre"
        self.damage = 1

class Aluminium(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/iron.png", 'pos':(0,0), 'color':(200,200,200), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Aluminium"
        self.damage = 1


class Chemicals(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/chemicals.png", 'pos':(0,0), 'color':(100,250,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Chemicals"
        self.damage = 1

class Food(Cargo):
    
    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/food.png", 'pos':(0,0), 'color':(250,250,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Food"
        self.damage = 1


class Gems(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/gems.png", 'pos':(0,0), 'color':(250,50,50), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Gems"
        self.damage = 1


class ExMetal(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None

        
        self.name = "Ex metal"
        self.damage = 1


class SheetMetal(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/sheetmetal.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Sheet metal"
        self.damage = 1


class ConstMat(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "ConstMat"
        self.damage = 1


class CompComp(Cargo):

    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/compcomp.png", 'pos':(0,0), 'color':(50,200,50), 'direction':None,'zoom':None}
        self.image=None        
        self.name = "CompComp"
        self.damage = 1


class MachParts(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/machparts.png", 'pos':(0,0), 'color':(100,150,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "MachParts"
        self.damage = 1

class Plastics(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/plastics.png", 'pos':(0,0), 'color':(100,200,200), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Plastics"
        self.damage = 1


class Explosives(Cargo):
    
    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/explosives.png", 'pos':(0,0), 'color':(100,150,150), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Explosives"
        self.damage = 1

class Minerals(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/minerals.png", 'pos':(0,0), 'color':(50,50,50), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Minerals"
        self.damage = 1


class AirFilters(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(50,50,50), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Air filters"
        self.damage = 1

class PleasureCubes(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/pleasurecubes.png", 'pos':(0,0), 'color':(200,200,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Pleasure cubes"
        self.damage = 1


class Alcohol(Cargo):
    
    def __init__(self, universe):
        
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(150,150,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Alcohol"
        self.damage = 1


class Textiles(Cargo):
    
    def __init__(self, universe):
       
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/textiles.png", 'pos':(0,0), 'color':(200,200,200), 'direction':None,'zoom':None}
        self.image=None
        
        self.name = "Textiles"
        self.damage = 1


class HuskarCigars(Cargo):
    
    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None

        
        self.name = "Huskar cigars"
        self.damage = 1


class ServantDroids(Cargo):
    
    def __init__(self, universe):


        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(250,200,200), 'direction':None,'zoom':None}
        self.image=None

        
        self.name = "Servant droids"
        self.damage = 1

class CloningDevice(Cargo):
    

    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/ironore.png", 'pos':(0,0), 'color':(200,200,250), 'direction':None,'zoom':None}
        self.image=None

        
        self.name = "Cloning device"
        self.damage = 1

class PureWater(Cargo):
    

    def __init__(self, universe):
        Cargo.__init__(self, universe)
        self.spritename = {'name':"res/goods/water.png", 'pos':(0,0), 'color':(0,100,200), 'direction':None,'zoom':None}
        self.image=None

        
        self.name = "Pure water"
        self.damage = 1
