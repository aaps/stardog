# parts.py

from utils import *
from pygame.locals import *
from floaters import *
from vec2d import Vec2d
import copy
from particles import *
import sys


class Port(object):
    def __init__(self, offset, dir, parent):
        self.offset = offset
        self.dir = dir
        self.part = None

        self.parent = parent
        
    def addPart(self, part):
        self.parent.addPart(part, self.parent.ports.index(self))

class Part(Floater):
    """A part of a ship."""
   
    # height, width = 9, 3
    
    acted = False


    def __init__(self, universe):
        self.buffer = pygame.Surface((30,30), flags = hardwareFlag | SRCALPHA).convert_alpha()
        if not self.baseImage:
            self.baseImage = loadImage("res/part/default.png")
        radius = max(self.baseImage.get_height() / 2, self.baseImage.get_width() / 2)
        Floater.__init__(self, universe, Vec2d(0,0), Vec2d(0,0), dir = 270, radius = radius)
        self.enabled = False
        self.functions = []
        self.functionDescriptions = []
        self.adjectives = []
        self.parent = None
        self.offset = Vec2d(0, 0)
        self.shipoffset = Vec2d(0, 0)
        self.animatedBaseImage = None
        self.animatedImage = None
        self.pickuptimeout = 0
        self.number = -1
        self.name = 'part'
        self.part_overlap = 0
        self.detach_space = 50
        self.detach_speed = 100
        self.level = 1
        self.dir = 270
        self.color = PART1
        self.animated = False
        self.ship = None
        self.volume = 1
        self.resources = False
        self.mass = 10
        self.maxhp = 10
        self.hp = 10
        self.fps = 10
        self.universe = universe
        # every part needs to know where to register sounds.
        self.soundsys = self.universe.game.soundSystem
        # a list of functions that are called on the ship during ship.update:
        self.shipEffects = []
        # a list of functions that are called on this part at attach time:
        self.attachEffects = []
        
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.width = self.image.get_width() - 4
        self.height = self.image.get_height() - 4
        # the length of this list is the number of connections.
        # each element is the part there, (x,y,dir) position of the connection.
        # the example is at the bottom of the part, pointed down.
        self.ports = [Port(Vec2d(-self.width / 2, 0), 0, self)]
        self.emitters.append(Emitter( self, self.condHalfDamage , 180, 10, 20, BLACK, PARTICLE1, 4, 5, 5, 3, 5, True))
        self.emitters.append(Emitter( self, self.condThQuarterDamage , 180, 40, 50, PARTICLE3, RED, 0, 1, 1, 1, 2.5, True))
        
    def setFPS(self, fps):
        for port in self.ports:
            if port.part:
                port.part.setFPS(fps)
        self.fps = fps

    # def setUniverse(self, universe):
    #     self.universe = universe
    
    def stats(self):
        stats = (self.hp, self.maxhp, self.mass, len(self.ports))
        statString = """HP: %i/%i \nMass: %i KG\nPorts: %i"""
        return statString % stats
    
    def shortStats(self):
        stats = (self.hp, self.maxhp)
        statString = """%i/%i"""
        return statString % stats
        
    def addPart(self, part, port):
        """addPart(part, port) -> connects part to port of this part.
        port can be a port number or a reference to the port."""
        from spaceship import Player
        from strafebat import Strafebat
        if port in self.ports:
            pass
        else:
            if len(self.ports) > port:
                port = self.ports[port]
                
        #detach old part, if any:
        if port.part:
            port.part.unequip()
        
        part.ship = self.ship
        part.dir = port.dir + self.dir
        part.offset = self.offset + port.offset.rotated(self.dir) - Vec2d(0,0).rotatedd(part.dir,(part.width - part.part_overlap) / 2)

        part.parent = self


        if isinstance(self.parent, Player) or isinstance(self.parent, Strafebat):
            part.shipoffset = part.offset
        else:
            part.shipoffset = part.offset + self.parent.shipoffset

        for other in self.ship.parts:
            if other is not self and other is not part:                
                if part.shipoffset.get_distance(other.shipoffset) < round((part.radius + other.radius)/2):                   
                    if part in self.ship.inventory:
                        self.ship.inventory.remove(part)
                        part = copy.copy(part)
                        

                    self.ship.inventory.append(part)
                    return

        port.part = part
        
        #calculate offsets:

        #rotate takes a ccw angle and color.
        part.image = colorShift(pygame.transform.rotate(part.baseImage, \
                    -part.dir), part.color)
        part.greyimage = colorShift(pygame.transform.rotate(part.baseImage, \
                    -part.dir), (100,100,100))
        # part.image.set_colorkey(BLACK)
        # part.greyimage.set_colorkey(BLACK)
        if part.animatedBaseImage:
            part.animatedImage = colorShift(part.animatedBaseImage, part.color)
            # part.animatedImage.set_colorkey(BLACK)
        #unequip the part if it collides with others, except parent(self).
        


        #allow the ship to re-adjust:
        self.ship.reset()

            
    def attach(self):
        """attaches this part to a ship. This includes increases ship mass
        and moment and possibly other stats."""
        #NOTE: this is done recursively to all parts every time a part
        #is added or removed, so it is not neccesary to undo it in detach.
        #It must be recalculated because moment is calculated from the center
        #of the ship.  
        self.ship.mass += self.mass
        self.ship.moment += self.mass * self.offset.get_length()
        #These two can be modified by adjectives:
        self.ship.partEffects.extend(self.shipEffects)
        for effect in self.attachEffects:
            effect(self)

    def detach(self):
        """removes this part from its parent and ship,
        and recursively detaches its children."""
        #recurse to children:
        for port in self.ports:
            if port.part:
                port.part.detach()
        #set physics to drift away from ship (not collide):
      
        if self.parent:
            cost = cos(self.ship.dir) #cost is short for cos(theta)
            sint = sin(self.ship.dir)
            self.pos = self.ship.pos +  self.offset * self.detach_space

            self.delta = self.ship.delta + Vec2d(0,0).rotatedd(random.randrange(0,360), self.detach_speed)
            #if this is the root of the ship, kill the ship:
            root = False
            if self.parent and self.parent == self.ship:
                self.ship.kill()
                root = True
            #cleanup relations:
            if self.parent and self.parent != self.ship:
                for port in self.parent.ports:
                    if port.part == self:
                        port.part = None

                self.ship.parts.remove(self)
            self.ship.reset()
            self.ship = None
            self.parent = None

            #otherwise add this to the game as an independent Floater:
            if not root:
                self.universe.curSystem.add(self)
        
    def scatter(self, ship):
        """Like detach, but for parts that are in an inventory when a 
        ship is destroyed."""
        self.pickuptimeout = 5
        angle = randint(0,360)
        offset = Vec2d(cos(angle) * self.detach_space, sin(angle) * self.detach_space)
        #set physics to drift away from ship (not collide):
        self.image = colorShift(pygame.transform.rotate(self.baseImage, angle), self.color).convert_alpha()
        # self.image.set_colorkey(BLACK)
        self.pos = ship.pos + self.offset
        self.delta.x = ship.delta.x + (rand()  * self.detach_speed)

        self.ship = None
        self.universe.curSystem.add(self)
        
    def unequip(self, toInventory = True):
        """move a part from on a ship to a ship's inventory"""
        #recurse to children first:
        if not self.ship:
            return
        for port in self.ports:
            if port.part:
                port.part.unequip()
        if self.parent: 
            for port in self.parent.ports:
                if port.part == self:
                    port.part = None
        if self in self.ship.parts:
            self.ship.parts.remove(self)
        self.ship.reset()
        self.parent = None
        if toInventory == True and not self in self.ship.inventory:
            self.ship.inventory.append(self)
        self.ship.reset()
        
    def update(self):
        """updates this part."""

        #reset so this part can act again this frame:
        self.acted = False
        #if it's attached to a ship, just rotate with the ship:
        if self.ship:
            cost = cos(self.ship.dir) #cost is short for cos(theta)
            sint = sin(self.ship.dir)
            self.pos = self.ship.pos + self.offset.rotated(self.ship.dir)
        #if it's floating in space, act like a floater:
        else:
            Floater.update(self)
        #update children:
        #
        for port in self.ports:
            if port.part:
                port.part.update()

        if self.pickuptimeout > 0:
            self.pickuptimeout -= 1. / self.fps

        for emitter in self.emitters:
            emitter.setFPS(self.fps)
            emitter.update()


    def draw(self, surface, offset = None, redraw = True, grey = False):
        """draws this part onto the surface."""
        if not offset:
            offset = Vec2d((surface.get_width() \
                    - self.image.get_width()) / 2 + self.offset[0], \
                    (surface.get_height() \
                    - self.image.get_height()) / 2 + self.offset[1])
        
        if self.ship == None:
            Floater.draw(self, surface, offset)
        elif not grey:
            surface.blit(self.image, offset)
        else:
        	surface.blit(self.greyimage, offset)

        #draw children:
        for port in self.ports:
            if port.part:
                port.part.draw(surface, grey = grey)
                
        if not self.parent and redraw:
            self.redraw(surface, offset)
        

    def exdraw(self, surface, offset = None, redraw = True):
        """draws this part onto the surface."""
        if not offset:
            offset = Vec2d((surface.get_width() \
                    - self.image.get_width()) / 2 + self.offset[0], \
                    (surface.get_height() \
                    - self.image.get_height()) / 2 + self.offset[1])
        
        if self.ship == None:
            Floater.draw(self, surface, offset)
        else:
            surface.blit(self.image, offset)

    def redraw(self, surface, offset):
        """redraw(surface, offset) -> draws 
        animated elements of this part to surface. 
        This should circumvent the ship surface and draw directly onto space."""

        if self.animated and self.animatedImage and self.ship:
            image = pygame.transform.rotate(self.animatedImage,- self.dir - self.ship.dir).convert_alpha()
            # image.set_colorkey(BLACK)
            pos = self.pos.x - image.get_width() / 2 - offset[0], \
                  self.pos.y - image.get_height() / 2 - offset[1]
            surface.blit(image, pos)
        
        for emitter in self.emitters:
            emitter.draw(surface, offset)


    def takeDamage(self, damage, other):
        from spaceship import Player
        
        hitByPlayer = False
        if isinstance(self, Part) and self.parent:
            self.ship.attention += 5
        if isinstance(other, Bullet) and other.ship == self.universe.player:
            hitByPlayer = True
            self.universe.player.xpDamage(self, damage)
        if self.parent and self.parent != self.ship \
        and not isinstance(self.ship, Player)  \
        and rand() <  1. * damage / (self.hp + 1):
            self.detach()
        self.hp -= damage
        if self.hp <= 0:
            if hitByPlayer:
                self.universe.player.xpDestroy(self)
                if self.ship:
                    self.universe.player.xpKill(self.ship)
            if self.parent:
                self.detach()
            if rand() < 0.3 and not isinstance(self, Scrap):
                scrap = Scrap(self.universe)
                scrap.pos = self.pos
                scrap.delta = self.delta

                self.universe.curSystem.add(scrap)
            self.kill()

            
            #if dead, make an explosion here.
            self.universe.curSystem.add(Explosion(self.universe, self.pos, \
                        self.delta, radius = self.radius * 4,\
                        time = self.maxhp / 5))

class Dummy(Part):
    """A dummy part used by the parts menu."""
    # mass = 0
    def __init__(self, universe):
        Part.__init__(self, universe)
        self.ports = []
        self.mass = 0
        self.part_overlap = 0
        
    def update(self):
        if self.parent: 
            #a Dummy should never be a base part, so ignore that case.
            for port in self.parent.ports:
                if port.part == self:
                    port.part = None
                    self.kill()
                    self.ship.reset()


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
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.greyimage = colorShift(self.baseImage.copy(), (100,100,100))
        self.functions = [] # thisshould go eventualy
        self.adjectives = [] #this should go eventualy

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
        offset = Vec2d(cos(angle) * detach_space, sin(angle) * detach_space)
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

    def shortStats(self):
        return self.name

    def stats(self):
        return self.name

class Iron(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/iron.png")
        Cargo.__init__(self, universe)
        
        self.name = "Iron"
        self.damage = 1

    def shortStats(self):
        return self.name

    def stats(self):
        return self.name

class IronOre(Cargo):
    
    image = None
    def __init__(self, universe):
        self.baseImage = loadImage("res/goods/ironore.png")
        Cargo.__init__(self, universe)
        
        self.name = "IronOre"
        self.damage = 1

    def shortStats(self):
        return self.name

    def stats(self):
        return self.name

class FlippablePart(Part):
    def flip(self):
        try:
            self.shootPoint = self.shootPoint[0], -self.shootPoint[1]
            self.shootDir = -self.shootDir
        except AttributeError:
            pass
        if self.baseImage:
            self.baseImage = pygame.transform.flip(self.baseImage, False, True)
        if self.name and self.name.find('Right') != -1:
            i = self.name.find('Right')
            self.name = self.name[:i] + 'Left' + self.name[i+5:]
        elif self.name and self.name.find('Left') != -1:
            i = self.name.find('Left')
            self.name = self.name[:i] + 'Right' + self.name[i+4:]
                    
class Gun(Part):
    

    shootDir = 180
    shootPoint = -30, 0 
    
    def __init__(self, universe):
        # self.baseImage = loadImage("res/default" + ext)
        Part.__init__(self, universe)
        
        self.functions.append(self.shoot)
        self.functionDescriptions.append("shoot")
        self.ports = []
        self.damage = 2
        self.range = 4
        self.name = "Gun"
        
        
        self.reloadTime = .5 #in seconds
        self.reload = 0
        self.energyCost = 3
        self.bulletRadius = 2

        # register our self with the sound system.
        self.gunShotSound = 'gunShot-Duality-edit.ogg'
        self.soundsys.register(self.gunShotSound)
    
    def stats(self):
        stats = (self.damage, 60. / self.reloadTime, self.energyCost, \
                self.range, self.shootDir)
        statString = ("\nDamage: %s \nRate: %s/minute \nCost: %s "
        "energy/shot \nRange: %s \nFiring angle:"
        "%s CW from attach")
        return Part.stats(self) + statString % stats
    
    def shortStats(self):
        stats = (self.damage, 60. / self.reloadTime)
        statString = """\n%s damage\n%s/minute"""
        return Part.shortStats(self) + statString % stats
    
    def update(self):
        #reload cooldown:
        if self.reload > 0:
            self.reload -= 1. / self.fps
        Part.update(self)
    
    def getDPS(self):
        return 1.0 * self.damage / self.reloadTime
        
class Cannon(Gun):
    bulletImage = None

    
    def __init__(self, universe):
        Gun.__init__(self, universe)
        if self.bulletImage == None:
            self.bulletImage = loadImage("res/ammo/shot.png").copy()
        self.speed = 300
        self.name = "Cannon"
        
    def stats(self):
        stats = (self.speed,)
        statString = ("\nBullet Speed: %s m/s")
        return Gun.stats(self) + statString % stats
                
    def attach(self):
        self.bulletImage = colorShift(loadImage("res/ammo/shot.png"), bulletColor(self.damage))
        Part.attach(self)
            
    def shoot(self):
        """fires a bullet."""
        if self.acted: return
        self.acted = True
        s = self.ship
        if self.reload <= 0 and s.energy > self.energyCost:
            self.reload = self.reloadTime / s.efficiency * s.cannonRateBonus
            s.energy -= self.energyCost
            self.soundsys.play(self.gunShotSound)
            self.universe.curSystem.add( 
                    Bullet(self.universe, self, 
                    self.damage * s.efficiency * s.damageBonus * s.cannonBonus, 
                    self.speed * s.cannonSpeedBonus,
                    self.range * s.cannonRangeBonus, image = self.bulletImage))

class MineDropper(Gun):
    
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/minelayer.png")
        Gun.__init__(self, universe)
        
        self.mineImage = loadImage("res/ammo/mine.png")
        self.damage = 30
        self.speed = 0
        self.reloadTime = 2
        self.acceleration = 0
        self.range = 1
        self.turning = 0
        self.percision = 0
        self.explosionRadius = 120
        self.explosionTime = .6
        self.force = 6000
        self.name = "Mine-Layer"
        self.mineImage = colorShift(self.mineImage , (100,100,100)) 

    def stats(self):
        stats = (self.speed, self.acceleration)
        statString = ("\n Mine Speed: %s m/s\nMine Accel: %s m/s/s")
        return Gun.stats(self)+statString%stats

    def shoot(self):
        if self.acted: return
        self.acted = True
        s = self.ship
        if self.reload <= 0 and s.energy > self.energyCost:
            self.reload = self.reloadTime
            s.energy -= self.energyCost
            self.soundsys.play(self.gunShotSound)
            self.universe.curSystem.add(Mine(self.universe, self,
                    self.damage*s.efficiency*s.damageBonus,
                    self.speed,
                    self.acceleration,
                    self.range, self.explosionRadius,
                    image = self.mineImage))

class MissileLauncher(Gun):
    
    missileImage = None
    
    
    def __init__(self, universe):
        if self.missileImage == None:
            self.missileImage = loadImage("res/ammo/missile.png").copy()
        self.baseImage = loadImage("res/parts/misilelauncher.png")
        Gun.__init__(self, universe)
        
        self.damage = 20
        self.speed = 40
        self.reloadTime = 5
        self.acceleration = 600
        self.range = 1
        self.turning = 0
        self.percision = 0
        self.explosionRadius = 120
        self.explosionTime = 3
        self.force = 6000
        self.name = 'Missile Launcher'
        self.missileLaunchSound = 'lazer.ogg'
        self.soundsys.register(self.missileLaunchSound)

    def stats(self):
        stats = (self.speed, self.acceleration)
        statString = ("\nMissile Speed: %s m/s\nMissile Acceleration: %s m/s/s")
        return Gun.stats(self) + statString % stats
        
    def shoot(self):
        if self.acted: return 
        self.acted = True
        s = self.ship
        if self.reload <= 0 and s.energy > self.energyCost:
            self.reload = self.reloadTime
            s.energy -= self.energyCost
            self.soundsys.play(self.missileLaunchSound)
            self.universe.curSystem.add( Missile(self.universe, self, 
                    self.damage * s.efficiency * s.damageBonus * s.missileBonus,
                    self.speed * s.missileSpeedBonus,
                    self.acceleration * s.missileSpeedBonus,
                    self.range * s.missileRangeBonus, self.explosionRadius,
                    image = loadImage("res/ammo/missile.png")))

class Laser(Gun):
    
    def __init__(self, universe):
        # self.baseImage = loadImage("res/parts/leftlaser.png")
        Gun.__init__(self, universe)
        
        self.damage = 10
        self.range = 300
        self.name = "Laser"
        self.reloadTime = 2. #in seconds
        self.energyCost = 35
        self.beamWidth = 1
        self.imageDuration = .08
        # register the lasersound with the game soundsystem
        self.laserSound = 'lazer-duality-edit.ogg'
        self.soundsys.register(self.laserSound)
                
    def shoot(self):
        """fires a laser"""
        if self.acted: return
        self.acted = True
        s = self.ship
        if self.reload <= 0 and self.ship.energy > self.energyCost:
            self.reload = self.reloadTime / s.efficiency * s.cannonRateBonus
            self.ship.energy -= self.energyCost
            # play the laser sound
            self.soundsys.play(self.laserSound)
            self.universe.curSystem.add( \
                    LaserBeam(self.universe, self, \
                    self.damage * s.efficiency * s.damageBonus * s.laserBonus, \
                    self.range * s.laserRangeBonus))

class FlakCannon(Cannon):
    burstSize = 8
    reloadBurstTime = 4
    def __init__(self, universe):
        self.burst = self.burstSize
        self.reloadBurst = self.reloadBurstTime
        Cannon.__init__(self, universe)
        self.range = 6
        self.speed = 200
        self.spread = 18.75
        self.damage = 0.5
        self.reloadTime = 0.2
        self.energyCost = 1
        
    def stats(self):
        stats = (self.speed, self.burstSize, self.reloadBurstTime, self.spread)
        statString = ("\nBullet Speed: %i m/s\nBurst Size: %i"
                    "\nBurst reload: %i seconds\nBullet Spread: %i degrees")
        return Gun.stats(self) + statString % stats

    def update(self):
        Gun.update(self)
        self.reloadBurst -= 1. / self.fps
        if self.reloadBurst <= 0 :
            self.burst = self.burstSize
            self.reloadBurst = self.reloadBurstTime
        
    def shoot(self):
        """fires a bullet."""
        if self.acted: return
        self.acted = True
        s = self.ship
        if self.reload <= 0 and s.energy > self.energyCost\
        and self.burst > 0:
            self.reload = self.reloadTime / s.efficiency * s.cannonRateBonus
            s.energy -= self.energyCost
            self.burst -= 1
            self.soundsys.play(self.gunShotSound)
            #shoot several bullets, changing shootDir for each:
            baseDir = self.shootDir
            self.shootDir = baseDir + rand() * self.spread - self.spread / 2
            self.universe.curSystem.add( 
                Bullet(self.universe, self, 
                self.damage * s.efficiency * s.damageBonus * s.cannonBonus, 
                self.speed * s.cannonSpeedBonus,
                self.range * s.cannonRangeBonus, image = self.bulletImage))
            self.shootDir = baseDir # restore shootDir.
            if self.burst <= 0:
                self.reloadBurst = self.reloadBurstTime

class Radar(Part):

    image = None

    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/radar.png")
        Part.__init__(self, universe)
        self.energyCost = 0.5
        self.radarrange = 18000
        self.name = "Radar"
        self.init_extra()


    def init_extra(self):
        self.radartime = 0
        self.disk = None
        self.detected = []
        self.radarspeed = 1

    
    def toggle(self):
        
        if self.ship.radars[-1] == self:
            self.enabled = not self.enabled



    def shortStats(self):
        return "nothing yet"

    def stats(self):
        return "nothing yet"
     
    def update(self):
        from planet import Planet
        if self.ship and self == self.ship.radars[-1]:
            if self.enabled and self.ship and self.ship.energy > self.energyCost:
                self.radartime -= 1.0 / self.fps
                if self.radartime <= 0:
                    self.ship.radars = sorted(self.ship.radars, key=lambda radar: radar.radarrange)
                    if self == self.ship.radars[-1]:
                        self.detected = []
                        self.disk = RadarDisk(self.universe, self.ship.pos, self.ship.delta, self.dir, self.radarrange)
                        self.radartime = self.radarspeed
                        for floater in self.universe.curSystem.floaters:
                            if collisionTest(self.disk, floater) and floater != self.ship:
                                self.detected.append(floater)

                                if self.universe.curSystem in self.ship.knownsystems:
                                    if floater not in self.ship.knownsystems[self.universe.curSystem] and isinstance (floater, Planet):
                                        self.ship.knownsystems[self.universe.curSystem].append(floater)
                                else:
                                    self.ship.knownsystems.update({self.universe.curSystem:[]})
                        if not self.ship.curtarget in self.detected and not isinstance (self.ship.curtarget,Planet):
                            self.ship.curtarget = None
                self.ship.energy -= self.energyCost / self.fps

            else:
                self.detected = []
        Part.update(self)

    def targetNextShip(self):
        from spaceship import Ship
        if self == self.ship.radars[-1]:
            resultList = []
            for radar in self.ship.radars:
                resultList= list(set(radar.detected)|set(resultList))
            resultList =  filter(lambda f: isinstance(f, Ship), resultList)
            resultList = sorted(resultList, key = self.radarDistance)
            length = len(resultList)
            if self.ship.curtarget and self.ship.curtarget in resultList  and length-1 > resultList.index(self.ship.curtarget):
                self.ship.curtarget = resultList[resultList.index(self.ship.curtarget)+1]
            elif length > 0:
                self.ship.curtarget = resultList[0]
            else:
                self.ship.curtarget = None

    def targetPrefShip(self):
        from spaceship import Ship
        if self == self.ship.radars[-1]:
            resultList = []
            for radar in self.ship.radars:
                resultList= list(set(radar.detected)|set(resultList))
            resultList = filter(lambda f: isinstance(f, Ship), resultList)
            resultList = sorted(resultList, key = self.radarDistance)
            length = len(resultList)
            if self.ship.curtarget and self.ship.curtarget in resultList  and  resultList.index(self.ship.curtarget) > 0:
                self.ship.curtarget = resultList[resultList.index(self.ship.curtarget)-1]
            elif length > 0:
                self.ship.curtarget = resultList[length-1]
            else:
                self.ship.curtarget = None

    def targetNextPlanet(self):
        from planet import Planet
        if self == self.ship.radars[-1] and len(self.ship.knownsystems) > 0:
            planets = self.ship.knownsystems[self.universe.curSystem]
            planets = sorted(planets, key = self.radarDistance)
            if self.ship.curtarget in planets:
                index = planets.index(self.ship.curtarget)
                if index+1 < len(planets):
                    self.ship.curtarget = planets[index+1]
                else:
                    self.ship.curtarget = planets[0]
            elif len(planets) > 0:
                self.ship.curtarget = planets[0]
            else:
                self.ship.curtarget = None



    def targetPrefPlanet(self):
        from planet import Planet
        if self == self.ship.radars[-1] and len(self.ship.knownsystems) > 0:
            planets = self.ship.knownsystems[self.universe.curSystem]
            planets = sorted(planets, key = self.radarDistance)
            if self.ship.curtarget in planets:
                index = planets.index(self.ship.curtarget)
                if index > 0:
                    self.ship.curtarget = planets[index-1]
                else:
                    self.ship.curtarget = planets[len(planets)-1]
            elif len(planets) > 0:
                self.ship.curtarget = planets[len(planets)-1]
            else:
                self.ship.curtarget = None

    def targetNextPart(self):
        if self == self.ship.radars[-1]:
            resultList = []
            for radar in self.ship.radars:
                resultList= list(set(radar.detected)|set(resultList))
            resultList =  filter(lambda f: isinstance(f, Part) or isinstance(f, Cargo), resultList)
            resultList = sorted(resultList, key = self.radarDistance)
            length = len(resultList)
            if self.ship.curtarget and self.ship.curtarget in resultList  and length-1 > resultList.index(self.ship.curtarget):
                self.ship.curtarget = resultList[resultList.index(self.ship.curtarget)+1]
            elif length > 0:
                self.ship.curtarget = resultList[0]
            else:
                self.ship.curtarget = None

    def targetPrefPart(self):
        if self == self.ship.radars[-1]:
            resultList = []
            for radar in self.ship.radars: 
                resultList= list(set(radar.detected)|set(resultList))
            resultList =  filter(lambda f: isinstance(f, Part) or isinstance(f, Cargo), resultList)
            resultList = sorted(resultList, key = self.radarDistance)
            length = len(resultList)
            if self.ship.curtarget and self.ship.curtarget in resultList  and resultList.index(self.ship.curtarget) > 0:
                self.ship.curtarget = resultList[resultList.index(self.ship.curtarget)-1]
            elif length > 0:
                self.ship.curtarget = resultList[length-1]
            else:
                self.ship.curtarget = None

    def radarDistance(self, floater):
        return floater.pos.get_distance(self.ship.pos)

class Engine(Part):
    
    image = None

    
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/engine.png")
        Part.__init__(self, universe)
        
        self.width -= 6	#move the engines in 6 pixels.
        self.name = "Engine"
        self.ports = []
        self.functions.append(self.thrust)
        self.functionDescriptions.append('thrust')
        self.emitters.append(Emitter( self, self.condActive , 5, 50, 100, PARTICLE5, PARTICLE6, 2, 4, 100, 2, 5, True, True))
        self.animatedtime = 0
        self.animatedspeed = 0.5
        self.exspeed = 5000
        self.exmass = 10
        self.thrusting = False
        self.energyCost = 1.

    
    def condActive(self):
        return self.animated

    def stats(self):
        stats = (self.exspeed,self.exmass, self.energyCost)
        statString = """\nexhoustspeed: %s m/s\nexhoustmass: %s k/g\nCost: %s /second thrusting"""
        return Part.stats(self) + statString % stats
        
    def shortStats(self):
        stats = (self.exspeed)
        statString = """\n%s N"""
        return Part.shortStats(self) + statString % stats

    def update(self):
        if self.animatedtime > 0:
            self.animatedtime -= 1. / self.fps
            self.animated = True
        else:
            self.animated = False

        Part.update(self)
    
    def thrust(self):
        """thrust: pushes the ship from the direction this engine points."""
        if self.acted: return
        self.acted = True
        if self.ship and self.ship.energy >= self.energyCost:
            dir = self.dir + self.ship.dir
            
            effectiveexspeed = Vec2d(0,0)
            maxi = Vec2d(0,0).rotatedd(dir, self.exspeed).get_length()
            if maxi > self.ship.delta.get_length():
                effectiveexspeed =  (Vec2d(0,0).rotatedd(dir, self.exspeed) - self.ship.delta)
                accel = self.ship.efficiency * self.ship.thrustBonus \
                    * effectiveexspeed.get_length() * self.exmass / self.ship.mass / self.fps
                self.ship.delta = self.ship.delta.rotatedd(dir, accel)
            else:
                self.ship.delta *= 0.99
                
            
            self.ship.energy -= self.energyCost / self.fps
            self.animatedtime = self.animatedspeed

class Gyro(Part):
    
    image = None
    
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/gyro.png")
        Part.__init__(self, universe)
        
        self.ports = [Port(Vec2d(0, self.height / 2 ), 270, self), \
                Port(Vec2d(-self.width / 2 , 0), 0, self), \
                Port(Vec2d(0, -self.height / 2 ), 90, self)]
        self.functions.extend([self.turnLeft,self.turnRight])
        self.functionDescriptions.extend(\
                [self.turnLeft.__doc__,self.turnRight.__doc__])
        self.name = "Gyro"
        self.torque = 180000 #N m degrees== m m kg degrees /s /s
        self.energyCost = .8
                
    def stats(self):
        stats = (self.torque, self.energyCost)
        statString = ("\nTorque: %s N*m\nCost: %s " +
                    "energy/second of turning")
        return Part.stats(self) + statString % stats
        
    def shortStats(self):
        stats = (self.torque,)
        statString = """\n%s N*m"""
        return Part.shortStats(self) + statString % stats
        
    def turnLeft(self, angle = None, index=0):
        """rotates the ship counter-clockwise."""
        if self.acted or angle and abs(angle) < 2*index: return
        self.acted = True
        if angle:
            angle = max(- self.torque / self.ship.moment / self.fps \
                    * self.ship.efficiency * self.ship.torqueBonus, -abs(angle) )
        else:
            angle = -  self.torque / self.ship.moment / self.fps \
                    * self.ship.efficiency * self.ship.torqueBonus
        if self.ship and self.ship.energy >= self.energyCost:
            self.ship.dir = angleNorm(self.ship.dir + angle)
            self.ship.energy -= self.energyCost / self.fps
        
    def turnRight(self, angle = None, index=0):
        """rotates the ship clockwise."""
        if self.acted or angle and abs(angle) < 2*index: return
        self.acted = True
        if angle:
            angle = min(self.torque / self.ship.moment / self.fps \
                    * self.ship.efficiency * self.ship.torqueBonus, abs(angle) )
        else:
            angle = self.torque / self.ship.moment / self.fps \
                    * self.ship.efficiency * self.ship.torqueBonus
        if self.ship and self.ship.energy >= self.energyCost:
            self.ship.dir = angleNorm(self.ship.dir + angle)
            self.ship.energy -= self.energyCost / self.fps
    
class Generator(Part):
    
    image = None


    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/generator.png")
        Part.__init__(self, universe)
        
        self.name = "Generator"
        self.rate = 6.
        
    def stats(self):
        stats = (self.rate,)
        statString = """\nEnergy Produced: %s/second"""
        return Part.stats(self) + statString % stats
        
    def shortStats(self):
        stats = (self.rate,)
        statString = """\n%s E/s"""
        return Part.shortStats(self) + statString % stats
        
    def update(self):
        if self.ship and self.ship.energy < self.ship.maxEnergy:
            self.ship.energy = min(self.ship.maxEnergy, \
                    self.ship.energy + self.rate * self.ship.efficiency \
                    * self.ship.generatorBonus / self.fps)
        Part.update(self)

class Interconnect(Part):
    
    image = None
    

    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/interconnect.png")
        Part.__init__(self, universe)
        
        self.ports = [Port(Vec2d(0, self.height / 2 ), 270, self), \
                Port(Vec2d(-self.width / 2 , 0), 0, self), \
                Port(Vec2d(0, -self.height / 2 ), 90, self)]
        self.name = "Interconnect"
    def update(self):
        Part.update(self)

class Quarters(Part):
    
    image = None

    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/quarters.png")
        Part.__init__(self, universe)
        self.crewCap = 2
        self.repair = 0
        self.name = "Crew Quarters"

    def stats(self):
        stats = (self.repair,)
        statString = "\nRepairy: %s hp/s"
        return Part.stats(self) + statString % stats

    def shortStats(self):
        stats = (self.repair,)
        statString = "\n%s hp/s"
        return Part.shortStats(self)+statString%(stats)

    def update(self):
        if self.ship:
            #keep track for the amount of quarts. since repair rate is dependant.
            #on the amount of crew/quarters there are around.
            #find out how many quarters there are.
            quarters = 0
            for part in self.ship.parts:
                if part.name == self.name:
                    quarters += 1

            self.ship.crewsize = quarters*self.crewCap
            self.repair = self.ship.crewsize/10.
            
            #for every part on the ship
            #the first one that has it's hp < max
            #gets to be fixed.
            #only one at a time.
            for part in self.ship.parts:
                if part.hp < part.maxhp:
                    part.hp = part.hp+self.repair*self.ship.efficiency/self.fps
                    break

        Part.update(self)

class GatewayFocus(Part):
    
    image = None


    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/gateway_focus.png")
        Part.__init__(self, universe)
        
        self.ports = []
        self.name = "Gateway Focus"
        self.neededenergy = 100
        self.jumpenergy = 0
        self.enabled = False
        self.energyCost = 10
        startradius = 60
        stopradius = 100
        startvelocity = 40
        stopvelocity = 50
        startcolor = (10,20,30)
        stopcolor = (255,255,255)
        startlife = 1
        stoplife = 0
        maximum = 10
        startsize = 10
        stopsize = 2
        relative = True
        self.emitters.append(RingCollector(self, self.condActive, startradius, stopradius, startvelocity, stopvelocity, startcolor, stopcolor, startlife, stoplife, maximum, startsize, stopsize, relative))

    def condActive(self):
        return self.enabled

    def stats(self):
        statString = "Will jump to other system"
        return statString

    def shortStats(self):
        return "Nothing\n"

    def toggle(self):
        if self.jumpenergy >= self.neededenergy:
                self.jump()
                return

        if self.enabled:
            self.enabled = False    
        else:
            self.enabled = True

    def update(self):
        if self.ship:
            if self.enabled and self.ship.energy > self.energyCost:
                self.ship.energy -= (self.energyCost / self.ship.efficiency) / self.fps
                self.jumpenergy += (self.ship.efficiency * self.energyCost) / self.fps
            if self.jumpenergy >= self.neededenergy:
                self.enabled = False
        Part.update(self)

    def jump(self):
        
        if self.ship.atgateway:
            if self.universe.curSystem == self.ship.atgateway.sister.starsystem:
                self.ship.pos = Vec2d(self.ship.atgateway.sister.pos)
                for camera in self.universe.cameras:
                    camera.setPos(self.ship.pos)

                # self.universe.camera.setPos(self.ship.pos)
            else:
                newsystem = self.ship.atgateway.sister.starsystem
                newsystem.player = self.ship
                newsystem.floaters.add(self.ship)
                newsystem.ships.add(self.ship)
                self.universe.curSystem.player = None
                self.universe.curSystem.ships.remove(self)
                self.universe.curSystem.floaters.remove(self)
                self.universe.curSystem = newsystem
                self.ship.pos = self.ship.atgateway.sister.pos
                for camera in self.universe.cameras:
                    camera.setPos(self.ship.pos)
                # self.camera.setPos(self.ship.pos)
            self.jumpenergy = 0


class Battery(Part):
    
    image = None


    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/battery.png")
        Part.__init__(self, universe)
        
        self.name = "Battery"
        self.capacity = 100
    
    def stats(self):
        stats = (self.capacity,)
        statString = """\nCapacity: %s energy"""
        return Part.stats(self) + statString % stats
        
    def shortStats(self):
        stats = (self.capacity,)
        statString = """\n%s E"""
        return Part.shortStats(self) + statString % stats
        
    def attach(self):
        self.ship.maxEnergy += self.capacity * self.ship.batteryBonus
        Part.attach(self)

class Shield(Part):
    
    image = None

    def __init__(self, universe):
        Part.__init__(self, universe)
        self.baseImage = loadImage("res/parts/shield.png")
        self.ports = []
        self.name = "Shield"
        self.shieldhp = 10
        self.shieldRegen = .30
        self.energyCost = 1.5
    
    def stats(self):
        stats = (self.shieldhp, self.shieldRegen, self.energyCost)
        statString = ("\nMax Shield: %.2f \nRegeneration Rate: %.2f/sec"
                "\nCost: %.2f energy/sec of regen")
        return Part.stats(self) + statString % stats
        
    def shortStats(self):
        stats = (self.shieldhp, self.shieldRegen)
        statString = """\n%.2f max \n%.2f regen"""
        return Part.shortStats(self) + statString % stats
        
    def attach(self):
        self.ship.maxhp += self.shieldhp * self.ship.shieldMaxBonus
        Part.attach(self)
        
    def update(self):
        if self.ship and self.ship.hp <= self.ship.maxhp\
        and self.ship.energy > self.energyCost:
            if self.ship.hp == 0:
                self.ship.hp = .0001
            else:
                self.ship.hp = min(self.ship.maxhp, \
                        self.ship.hp + self.shieldRegen \
                        * self.ship.shieldRegenBonus/ self.fps)
                self.ship.energy -= self.energyCost / self.fps
        Part.update(self)


class BigShield(Shield):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/shield.png")
        # gives lots of problems if you init Part and not Shield ... yea
        Shield.__init__(self, universe)


class Chip(Part):
    def __init__(self, universe):
        Part.__init__(self, universe)
        self.name = "Chip"
    def stats(self):
        pass
    def shortstats(self):
        pass
    def update(self):
        Part.update(self)

class CargoHold(Part):
    
    image = None

    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/cargo.png")
        Part.__init__(self, universe)
        self.ports = [  Port(Vec2d(0, self.height / 2 ), 270, self), \
                        Port(Vec2d(-self.width / 2 , 0), 0, self), \
                        Port(Vec2d(0, -self.height / 2 ), 90, self)]
        self.name = "CargoHold"
        self.energyCost = 10
        self.mass = 1
        self.gargocapacity = 4
    def stats(self):
        stats = (self.energyCost,)
        statString = "\nCosts for carrying cargo per part: %s E/p"
        return Part.stats(self)+statString%(stats)

    def shortStats(self):
        stats = (self.energyCost,)
        statString = "\n %s E/p"
        return Part.shortStats(self)+statString%(stats)
        
    def update(self):
        """check how many cargholds are attached and calculate capacity on that."""
        if self.ship:
            gargoholdcount = 0
            cockpitGargoSize = 0
            for part in self.ship.parts:
                #cockpit has storage too. 
                if isinstance(part, Cockpit):
                    cockpitGargoSize = part.gargocapacity
                elif part.name == self.name:
                    gargoholdcount += 1
            #calculate the gargohole count from the amount of gargoholds * capacity plus cockpit amount.
            self.ship.gargoholdsize = (gargoholdcount*self.gargocapacity)+cockpitGargoSize
            
            if len(self.ship.inventory) > (self.ship.gargoholdsize):
                part = self.ship.inventory[-1]
                part.scatter(self.universe.player)
                self.universe.player.reset()
                self.universe.player.inventory.remove(part)
        Part.update(self)



class Cockpit(Radar, Battery, Generator, Gyro, CargoHold):
    

    
    def __init__(self, universe):
        # self.baseImage = loadImage("res/parts/cockpit.png")
        Part.__init__(self, universe)
        Radar.init_extra(self)
        # self.image = None
        self.energyCost = .2 #gyro
        self.torque = 35000 #gyro
        self.radarrange = 5000 #radar
        self.capacity = 5 #battery
        self.rate = .5 #generator
        self.gargocapacity = 6
        self.ports = [Port(Vec2d(self.width / 2 - 2, 0), 180, self), \
                    Port(Vec2d(0, self.height / 2 - 2), 270, self), \
                    Port(Vec2d(-self.width / 2 + 2, 0), 0, self), \
                    Port(Vec2d(0, -self.height / 2 + 2), 90, self)]
        self.name = "Cockpit"

    def stats(self):
        stats = (self.torque, self.energyCost, self.capacity, self.rate, self.ship.gargoholdsize)
        statString = ("\nTorque: %s N*m\nCost: %s energy/second of turning" +
                    "\nCapacity: %s energy" +
                    "\nEnergy Produced: %s/second"+
                    "\nGargo Capacity: %s")
        return Part.stats(self) + statString % stats

    def update(self):
        Generator.update(self)
        Battery.update(self)
        Gyro.update(self)
        Radar.update(self)
        CargoHold.update(self)

class StrafebatCockpit(Cockpit):

    def __init__(self, universe): 
        self.baseImage = loadImage("res/parts/cockpit.png")
        Cockpit.__init__(self, universe)
        
class Interceptor(Cockpit):#move to config

    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/interceptor.png")
        Cockpit.__init__(self, universe)
        self.mass = 20
        self.hp = 15
        self.ports = [Port(Vec2d(4, 10), 180, self),
                      Port(Vec2d(4, -10), 180, self),
                      Port(Vec2d(-3, -17), 90, self),
                      Port(Vec2d(-3, 17), -90, self),
                      Port(Vec2d(-6, 12), 0, self),
                      Port(Vec2d(-6, -12), 0, self)]
        self.name = 'Interceptor Cockpit'


class Destroyer(Cockpit):# move to config
    
    
    
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/destroyer.png")
        Cockpit.__init__(self, universe)
        self.mass = 60
        self.hp = 30
        self.energyCost = .6
        self.ports = [
                    Port(Vec2d(25, 0), 180, self),
                    Port(Vec2d(8, -8), 90, self),
                    Port(Vec2d(8, 8), -90, self),
                    Port(Vec2d(-14, -13), 90, self),
                    Port(Vec2d(-14, 13), -90, self),
                    Port(Vec2d(-25, -8), 0, self),
                    Port(Vec2d(-25, 8), 0, self)]
        self.name = 'Destroyer Cockpit'
                    
class Fighter(Cockpit):#move to config


    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/fighter.png")
        Cockpit.__init__(self, universe)
        self.mass = 10
        self.hp = 10
        self.energyCost = .2 #gyro
        self.torque = 60000 #gyro
        self.capacity = 30 #battery
        self.rate = 10 #generator
        self.ports = [
                    Port(Vec2d(9, 0), 180, self),
                    Port(Vec2d(-5, -7), 90, self),
                    Port(Vec2d(-5, 7), -90, self),
                    Port(Vec2d(-9, 0), 0, self)]
        self.name = 'Fighter Cockpit'
