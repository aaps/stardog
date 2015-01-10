#parts.py


from utils import *
from scripts import *
from pygame.locals import *
from floaters import *
import stardog
from vec2d import Vec2d
import copy
from particles import *



PART_OVERLAP = 0
DETACH_SPACE = 50
DETACH_SPEED = 100

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
    baseImage = loadImage("res/default.gif", (255,255,255))
    image = None
    height, width = 9, 3
    pickuptimeout = 0
    volume = 1
    equipable = True
    parent = None
    dir = 270
    mass = 10
    ship = None
    # position in relation to the center of the ship
    #and the center of this part:
    offset = Vec2d(0, 0)
    shipoffset = Vec2d(0, 0)
    #whether this should be redrawn each frame:
    color = (150,150,150)
    animated = False
    animatedBaseImage = None
    animatedImage = None
    number = -1
    name = 'part'
    level = 1
    buffer = pygame.Surface((30,30), flags = hardwareFlag | SRCALPHA).convert_alpha()
    buffer.set_colorkey((0,0,0))
    acted = False
    
    #a list of functions that are called on the ship during ship.update:
    shipEffects = []
    #a list of functions that are called on this part at attach time:
    attachEffects = []

    def __init__(self, game):
        self.functions = []
        self.functionDescriptions = []
        self.adjectives = []
        self.maxhp = 10
        self.hp = 10
        radius = max(self.baseImage.get_height() / 2,
                    self.baseImage.get_width() / 2)
        Floater.__init__(self, game, Vec2d(0,0), Vec2d(0,0), dir = 270, radius = radius)
        self.image = colorShift(self.baseImage.copy(), self.color)
        self.width = self.image.get_width() - 4
        self.height = self.image.get_height() - 4
        #the length of this list is the number of connections.
         #each element is the part there, (x,y,dir) position of the connection.
         #the example is at the bottom of the part, pointed down.
        self.ports = [Port(Vec2d(-self.width / 2, 0), 0, self)]
        self.emitters.append(Emitter(self.game, self, self.condHalfDamage , 180, 10, 20, (0,0,0,255), (100,100,100,0), 2, 4, 5, 3, 5, True))
        self.emitters.append(Emitter(self.game, self, self.condThQuarterDamage , 180, 5, 10, (0,0,255,255), (255,255,0,0), 2, 4, 5, 3, 5, True))
        
    
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
        part.offset = self.offset + port.offset.rotated(self.dir) - Vec2d(0,0).rotatedd(part.dir,(part.width - PART_OVERLAP) / 2)

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
        part.image.set_colorkey((0,0,0))
        if part.animatedBaseImage:
            part.animatedImage = colorShift(part.animatedBaseImage, part.color)
            part.animatedImage.set_colorkey((0,0,0))
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
            self.pos = self.ship.pos +  self.offset * DETACH_SPACE

            self.delta = self.ship.delta + Vec2d(0,0).rotatedd(random.randrange(0,360), DETACH_SPEED)
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
                self.game.universe.curSystem.add(self)
        
    def scatter(self, ship):
        """Like detach, but for parts that are in an inventory when a 
        ship is destroyed."""
        self.pickuptimeout = 5
        angle = randint(0,360)
        offset = Vec2d(cos(angle) * DETACH_SPACE, sin(angle) * DETACH_SPACE)
        #set physics to drift away from ship (not collide):
        self.image = colorShift(pygame.transform.rotate(self.baseImage, angle), self.color).convert()
        self.image.set_colorkey((0,0,0))
        self.pos = ship.pos + self.offset
        self.delta.x = ship.delta.x + (rand()  * DETACH_SPEED)

        self.ship = None
        self.game.universe.curSystem.add(self)
        
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
        if self.parent:
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
            self.pickuptimeout -= 1. / self.game.fps

        for emitter in self.emitters:
            emitter.update()


    def draw(self, surface, offset = None, redraw = True):
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

        #draw children:
        for port in self.ports:
            if port.part:
                port.part.draw(surface)
                
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
            image.set_colorkey((0,0,0))
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
        if isinstance(other, Bullet) and other.ship == self.game.player:
            hitByPlayer = True
            self.game.player.xpDamage(self, damage)
        if self.parent and self.parent != self.ship \
        and not isinstance(self.ship, Player)  \
        and rand() <  1. * damage / (self.hp + 1):
            self.detach()
        self.hp -= damage
        if self.hp <= 0:
            if hitByPlayer:
                self.game.player.xpDestroy(self)
                if self.ship:
                    self.game.player.xpKill(self.ship)
            if self.parent:
                self.detach()
            if rand() < 0.3 and not isinstance(self, Scrap):
                scrap = Scrap(self.game)
                scrap.pos = self.pos
                scrap.delta = self.delta

                self.game.universe.curSystem.add(scrap)
            self.kill()

            
            #if dead, make an explosion here.
            self.game.universe.curSystem.add(Explosion(self.game, self.pos, \
                        self.delta, radius = self.radius * 4,\
                        time = self.maxhp / 5))

    def condHalfDamage(self):
        return self.hp <= self.maxhp/2 and self.hp > self.maxhp/4

    def condThQuarterDamage(self):
        return self.hp <= self.maxhp/4

    # def condActive(self):
    #     return False

    def condAlways(self):
        return True




class Dummy(Part):
    """A dummy part used by the parts menu."""
    mass = 0
    def __init__(self, game):
        Part.__init__(self, game)
        self.ports = []
        
    def update(self):
        if self.parent: 
            #a Dummy should never be a base part, so ignore that case.
            for port in self.parent.ports:
                if port.part == self:
                    port.part = None
                    self.kill()
                    self.ship.reset()

class Scrap(Part):
    name = "Scrap"
    baseImage = loadImage("res/goods/scrap" + ext)
    image = None
    damage = 1
    equipable = False


    def __init__(self, game):
        Part.__init__(self, game)

    def update(self):
        Part.update(self)

    def shortStats(self):
        return "Scrap"

    def stats(self):
        return "It is Scrap"

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
    baseImage = loadImage("res/default" + ext)
    image = None
    damage = 2
    range = 4
    name = "Gun"
    shootPoint = -30, 0 
    shootDir = 180
    reloadTime = .5 #in seconds
    reload = 0
    energyCost = 3
    bulletRadius = 2
    
    def __init__(self, game):
        Part.__init__(self, game)
        self.functions.append(self.shoot)
        self.functionDescriptions.append("shoot")
        self.ports = []
    
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
            self.reload -= 1. / self.game.fps
        Part.update(self)
    
    def getDPS(self):
        return 1.0 * self.damage / self.reloadTime
        
class Cannon(Gun):
    bulletImage = None
    speed = 300
    name = "Cannon"
    
    def __init__(self, game):
        if self.bulletImage == None:
            self.bulletImage = BULLET_IMAGE.copy()
        Gun.__init__(self, game)
        
    def stats(self):
        stats = (self.speed,)
        statString = ("\nBullet Speed: %s m/s")
        return Gun.stats(self) + statString % stats
                
    def attach(self):
        self.bulletImage = colorShift(BULLET_IMAGE, bulletColor(self.damage))
        Part.attach(self)
            
    def shoot(self):
        """fires a bullet."""
        if self.acted: return
        self.acted = True
        s = self.ship
        if self.reload <= 0 and s.energy > self.energyCost:
            self.reload = self.reloadTime / s.efficiency * s.cannonRateBonus
            s.energy -= self.energyCost
            if soundModule:
                setVolume(shootSound.play(), self, self.game.player)
            self.game.universe.curSystem.add( 
                    Bullet(self.game, self, 
                    self.damage * s.efficiency * s.damageBonus * s.cannonBonus, 
                    self.speed * s.cannonSpeedBonus,
                    self.range * s.cannonRangeBonus, image = self.bulletImage))

class MineDropper(Gun):
    baseImage = loadImage("res/parts/minelayer"+ext)
    mineImage = loadImage("res/mine"+ext)
    damage = 10
    speed = 0
    reloadTime = 2
    acceleration = 0
    range = 1
    turning = 0
    percision = 0
    explosionRadius = 120
    explosionTime = .6
    force = 6000
    name = "Mine-Layer"
    
    def __init__(self, game):
        Gun.__init__(self, game)

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
            if soundModule:
                setVolume(shootSound.play(), self, self.game.player)
            self.game.universe.curSystem.add(Mine(self.game, self,
                    self.damage*s.efficiency*s.damageBonus,
                    self.speed,
                    self.acceleration,
                    self.range, self.explosionRadius,
                    image = self.mineImage))

class MissileLauncher(Gun):
    baseImage = loadImage("res/parts/missilelauncher" + ext)
    missileImage = None
    damage = 20
    speed = 40
    reloadTime = 5
    acceleration = 600
    range = 1

    turning = 0
    percision = 0
    explosionRadius = 120
    explosionTime = .6
    force = 6000
    name = 'Missile Launcher'
    
    def __init__(self, game):
        if self.missileImage == None:
            self.missileImage = MISSILE_IMAGE.copy()
        Gun.__init__(self, game)
    
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
            if soundModule:
                setVolume(shootSound.play(), self, self.game.player)
            self.game.universe.curSystem.add( Missile(self.game, self, 
                    self.damage * s.efficiency * s.damageBonus * s.missileBonus,
                    self.speed * s.missileSpeedBonus,
                    self.acceleration * s.missileSpeedBonus,
                    self.range * s.missileRangeBonus, self.explosionRadius,
                    image = MISSILE_IMAGE))

class Laser(Gun):
    baseImage = loadImage("res/parts/leftlaser" + ext)
    damage = 10
    range = 300
    name = "Laser"
    reloadTime = .8 #in seconds
    energyCost = 8
    beamWidth = 1
    imageDuration = .08
    
    def __init__(self, game):
        Gun.__init__(self, game)
                
    def shoot(self):
        """fires a laser"""
        if self.acted: return
        self.acted = True
        s = self.ship
        if self.reload <= 0 and self.ship.energy > self.energyCost:
            self.reload = self.reloadTime / s.efficiency * s.cannonRateBonus
            self.ship.energy -= self.energyCost
            if soundModule:
                setVolume(shootSound.play(), self, self.game.player)
            self.game.universe.curSystem.add( \
                    LaserBeam(self.game, self, \
                    self.damage * s.efficiency * s.damageBonus * s.laserBonus, \
                    self.range * s.laserRangeBonus))
    
class FlakCannon(Cannon):
    spread = 18.75
    damage = 0.5
    energyCost = 1
    reloadTime = 0.2
    burstSize = 8
    reloadBurstTime = 4
    range = 6
    speed = 150

    def __init__(self, game):
        self.burst = self.burstSize
        self.reloadBurst = self.reloadBurstTime
        Cannon.__init__(self, game)
        
    def stats(self):
        stats = (self.speed, self.burstSize, self.reloadBurstTime, self.spread)
        statString = ("\nBullet Speed: %i m/s\nBurst Size: %i"
                    "\nBurst reload: %i seconds\nBullet Spread: %i degrees")
        return Gun.stats(self) + statString % stats

    def update(self):
        Gun.update(self)
        self.reloadBurst -= 1. / self.game.fps
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
            if soundModule:
                setVolume(shootSound.play(), self, self.game.player)
            #shoot several bullets, changing shootDir for each:
            baseDir = self.shootDir
            self.shootDir = baseDir + rand() * self.spread - self.spread / 2
            self.game.universe.curSystem.add( 
                Bullet(self.game, self, 
                self.damage * s.efficiency * s.damageBonus * s.cannonBonus, 
                self.speed * s.cannonSpeedBonus,
                self.range * s.cannonRangeBonus, image = self.bulletImage))
            self.shootDir = baseDir # restore shootDir.
            if self.burst <= 0:
                self.reloadBurst = self.reloadBurstTime

class Radar(Part):
    baseImage = loadImage("res/parts/radar" + ext)
    image = None
    disk = None
    name = "Radar"
    energyCost = 0.5
    radarrange = 18000
    radarspeed = 1
    radartime = 0
    detected = []
    enabled = False

    def __init__(self, game):

        self.radartime = 0
        self.game = game
        self.detected = []
        Part.__init__(self, game)
    
    def toggle(self):
        
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True
        
        self.ship.radars = sorted(self.ship.radars, key=lambda radar: radar.radarrange, reverse=True)

        for radar in self.ship.radars:
            if not radar == self:
                radar.enabled = self.enabled

        
    def shortStats(self):
        return "nothing"

    def shortStats(self):
        return "nothing yet"

    def stats(self):
        return "nothing yet"
     
    def update(self):
        from planet import Planet
        if self.enabled and self.ship.energy > self.energyCost:
            self.radartime -= 1. / self.game.fps
            if self.radartime <= 0:

                self.detected = []
                self.disk = RadarDisk(self.game, self.ship.pos, self.ship.delta, self.dir, self.radarrange)
                self.radartime = self.radarspeed
                for floater in self.game.universe.curSystem.floaters:
                    if collisionTest(self.disk, floater) and floater != self.ship:
                        self.detected.append(floater)
                        if floater not in self.ship.knownplanets and isinstance (floater,Planet):
                            self.ship.knownplanets.append(floater)
            self.ship.energy -= self.energyCost / self.game.fps
        else:
            self.detected = []
        Part.update(self)

    def targetNextShip(self):
        from spaceship import Ship
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
        self.ship.knownplanets = sorted(self.ship.knownplanets, key = self.radarDistance)
        
        if self.ship.curtarget in self.ship.knownplanets:
            index = self.ship.knownplanets.index(self.ship.curtarget)
            if index+1 < len(self.ship.knownplanets):
                self.ship.curtarget = self.ship.knownplanets[index+1]
            else:
                self.ship.curtarget = self.ship.knownplanets[0]
        elif len(self.ship.knownplanets) > 0:
            self.ship.curtarget = self.ship.knownplanets[0]
        else:
            self.ship.curtarget = None



    def targetPrefPlanet(self):
        from planet import Planet
        self.ship.knownplanets = sorted(self.ship.knownplanets, key = self.radarDistance)

        if self.ship.curtarget in self.ship.knownplanets:
            index = self.ship.knownplanets.index(self.ship.curtarget)
            if index > 0:
                self.ship.curtarget = self.ship.knownplanets[index-1]
            else:
                self.ship.curtarget = self.ship.knownplanets[len(self.ship.knownplanets)-1]
        elif len(self.ship.knownplanets) > 0:
            self.ship.curtarget = self.ship.knownplanets[len(self.ship.knownplanets)-1]
        else:
            self.ship.curtarget = None

    def targetNextPart(self):
        resultList = []
        for radar in self.ship.radars:
            resultList= list(set(radar.detected)|set(resultList))
        resultList =  filter(lambda f: isinstance(f, Part), resultList)
        resultList = sorted(resultList, key = self.radarDistance)
        length = len(resultList)
        if self.ship.curtarget and self.ship.curtarget in resultList  and length-1 > resultList.index(self.ship.curtarget):
            self.ship.curtarget = resultList[resultList.index(self.ship.curtarget)+1]
        elif length > 0:
            self.ship.curtarget = resultList[0]
        else:
            self.ship.curtarget = None

    def targetPrefPart(self):
        resultList = []
        for radar in self.ship.radars: 
            resultList= list(set(radar.detected)|set(resultList))
        resultList =  filter(lambda f: isinstance(f, Part), resultList)
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
    baseImage = loadImage("res/parts/engine" + ext)
    image = None
    name = "Engine"
    animatedtime = 0
    animatedspeed = 0.5
    exspeed = 5000
    exmass = 10
    thrusting = False
    energyCost = 1.
    
    def __init__(self, game):
        if Engine.animatedImage == None:
            Engine.animatedImage = loadImage(\
                    "res/parts/engine thrusting" + ext)
        self.baseAnimatedImage = Engine.animatedImage
        Part.__init__(self, game)
        self.width -= 6	#move the engines in 6 pixels.
        self.ports = []
        self.functions.append(self.thrust)
        self.functionDescriptions.append('thrust')
        self.emitters.append(Emitter(self.game, self, self.condActive , 5, 50, 100, (75,75,255,255), (255,100,100,0), 2, 4, 100, 2, 5, True))
        
    
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
            self.animatedtime -= 1. / self.game.fps
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
                    * effectiveexspeed.get_length() * self.exmass / self.ship.mass / self.game.fps
                self.ship.delta = self.ship.delta.rotatedd(dir, accel)
            else:
                self.ship.delta *= 0.99
                
            
            self.ship.energy -= self.energyCost / self.game.fps
            self.animatedtime = self.animatedspeed

class Gyro(FlippablePart):
    baseImage = loadImage("res/parts/gyro" + ext)
    image = None
    name = "Gyro"
    torque = 180000 #N m degrees== m m kg degrees /s /s
    energyCost = .8
    
    def __init__(self, game):
        Part.__init__(self, game)
        self.ports = [Port(Vec2d(0, self.height / 2 ), 270, self), \
                Port(Vec2d(-self.width / 2 , 0), 0, self), \
                Port(Vec2d(0, -self.height / 2 ), 90, self)]
        self.functions.extend([self.turnLeft,self.turnRight])
        self.functionDescriptions.extend(\
                [self.turnLeft.__doc__,self.turnRight.__doc__])
                
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
            angle = max(- self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus, -abs(angle) )
        else:
            angle = -  self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus
        if self.ship and self.ship.energy >= self.energyCost:
            self.ship.dir = angleNorm(self.ship.dir + angle)
            self.ship.energy -= self.energyCost / self.game.fps
        
    def turnRight(self, angle = None, index=0):
        """rotates the ship clockwise."""
        if self.acted or angle and abs(angle) < 2*index: return
        self.acted = True
        if angle:
            angle = min(self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus, abs(angle) )
        else:
            angle = self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus
        if self.ship and self.ship.energy >= self.energyCost:
            self.ship.dir = angleNorm(self.ship.dir + angle)
            self.ship.energy -= self.energyCost / self.game.fps
    
class Generator(Part):
    baseImage = loadImage("res/parts/generator" + ext)
    image = None
    name = "Generator"
    rate = 6.
        
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
                    * self.ship.generatorBonus / self.game.fps)
        Part.update(self)

class Interconnect(Part):
    baseImage = loadImage("res/parts/interconnect" + ext)
    image = None
    name = "Interconnect"

    def __init__(self, game):
        Part.__init__(self, game)
        self.ports = [Port(Vec2d(0, self.height / 2 ), 270, self), \
                Port(Vec2d(-self.width / 2 , 0), 0, self), \
                Port(Vec2d(0, -self.height / 2 ), 90, self)]

class Quarters(Part):
    baseImage = loadImage("res/parts/quarters"+ext)
    image = None
    name = "Crew Quarters"
    repair = .2
    
    def __init__(self, game):
        Part.__init__(self, game)
        # self.detected = []
        Part.__init__(self, game)
        # self.ports = [Port(Vec2d(-self.width/2,0), 0, self)]

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
            for part in self.ship.parts:
                if part.hp < part.maxhp:
                    part.hp = part.hp+self.repair*self.ship.efficiency/self.game.fps
                    break
        Part.update(self)

class GargoHold(Part):
    baseImage = loadImage("res/parts/cargo"+ext)
    image = None
    name = "GargoHold"
    energyCost = 10
    mass = 1
    
    def __init__(self, game):
        Part.__init__(self, game)
        self.ports = [  Port(Vec2d(0, self.height / 2 ), 270, self), \
                        Port(Vec2d(-self.width / 2 , 0), 0, self), \
                        Port(Vec2d(0, -self.height / 2 ), 90, self)]
    def stats(self):
        stats = (self.energyCost,)
        statString = "\nCosts for carrying cargo per part: %s E/p"
        return Part.stats(self)+statString%(stats)

    def shortStats(self):
        stats = (self.energyCost,)
        statString = "\n %s E/p"
        return Part.shortStats(self)+statString%(stats)

    def update(self):
        if self.ship:
            numOfParts = len(self.ship.inventory)
            energyCost = numOfParts
        Part.update(self)

class GatewayFocus(Part):
    baseImage = loadImage("res/parts/gateway_focus"+ext)
    image = None
    name = "Gateway Focus"
    neededenergy = 100
    jumpenergy = 0
    enabled = False
    energyCost = 10

    def __init__(self, game):
        Part.__init__(self, game)
        self.ports = []

    def stats(self):
        statString = "Will jump to other system"
        return statString

    def shortStats(self):
        return "Nothing"

    def toggle(self):
        if self.enabled:
            self.enabled = False
            if self.jumpenergy >= self.neededenergy:
                self.jump()
        else:
            self.enabled = True

    def update(self):
        if self.enabled and self.ship.energy > self.energyCost and self.jumpenergy <= self.neededenergy:
            self.ship.energy -= (self.energyCost / self.ship.efficiency) / self.game.fps
            self.jumpenergy += (self.ship.efficiency * self.energyCost) / self.game.fps

    def jump(self):
        print "gateway",self.ship.atgateway
        print "gateway sister",self.ship.atgateway.sister
        print "jump"

class Battery(Part):
    baseImage = loadImage("res/parts/battery" + ext)
    image = None
    name = "Battery"
    capacity = 100
    
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
    baseImage = loadImage("res/parts/shield" + ext)
    image = None
    name = "Shield"
    shieldhp = 10
    shieldRegen = .30
    energyCost = 1.5
    def __init__(self, game): 
        Part.__init__(self, game)
        self.ports = []
    
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
                        * self.ship.shieldRegenBonus/ self.game.fps)
                self.ship.energy -= self.energyCost / self.game.fps
        Part.update(self)

class Cockpit(Radar, Battery, Generator, Gyro):
    baseImage = loadImage("res/parts/cockpit.gif")
    image = None
    energyCost = .2 #gyro
    torque = 35000 #gyro
    energyCost = 0.01 #radar
    radarrange = 5000 #radar
    capacity = 5 #battery
    rate = .5 #generator
    name = "Cockpit"
    
    def __init__(self, game):
        Part.__init__(self, game)
        self.ports = [Port(Vec2d(self.width / 2 - 2, 0), 180, self), \
                    Port(Vec2d(0, self.height / 2 - 2), 270, self), \
                    Port(Vec2d(-self.width / 2 + 2, 0), 0, self), \
                    Port(Vec2d(0, -self.height / 2 + 2), 90, self)]

    def stats(self):
        stats = (self.torque, self.energyCost, self.capacity, self.rate)
        statString = ("\nTorque: %s N*m\nCost: %s energy/second of turning" +
                    "\nCapacity: %s energy" +
                    "\nEnergy Produced: %s/second")
        return Part.stats(self) + statString % stats

    def update(self):
        Generator.update(self)
        Battery.update(self)
        # Gyro.update(self)
        Radar.update(self)
        
class Interceptor(Cockpit):#move to config
    mass = 20
    hp = 15
    baseImage = loadImage("res/parts/interceptor.bmp")
    name = 'Interceptor Cockpit'
    
    def __init__(self, game):
        Cockpit.__init__(self, game)
        self.ports = [
                    Port(Vec2d(4, 10), 180, self),
                    Port(Vec2d(4, -10), 180, self),
                    Port(Vec2d(-3, -17), 90, self),
                    Port(Vec2d(-3, 17), -90, self),
                    Port(Vec2d(-6, 12), 0, self),
                    Port(Vec2d(-6, -12), 0, self)]
                    
class Destroyer(Cockpit):#move to config
    mass = 60
    hp = 30
    energyCost = .6
    baseImage = loadImage("res/parts/destroyer.bmp")
    name = 'Destroyer Cockpit'
    
    def __init__(self, game):
        Cockpit.__init__(self, game)
        self.ports = [
                    Port(Vec2d(25, 0), 180, self),
                    Port(Vec2d(8, -8), 90, self),
                    Port(Vec2d(8, 8), -90, self),
                    Port(Vec2d(-14, -13), 90, self),
                    Port(Vec2d(-14, 13), -90, self),
                    Port(Vec2d(-25, -8), 0, self),
                    Port(Vec2d(-25, 8), 0, self)]
                    
class Fighter(Cockpit):#move to config
    mass = 10
    hp = 10
    energyCost = .2
    rate = 1.5
    capacity = 5
    baseImage = loadImage("res/parts/fighter.bmp")
    name = 'Fighter Cockpit'
    
    def __init__(self, game):
        Cockpit.__init__(self, game)
        self.ports = [
                    Port(Vec2d(9, 0), 180, self),
                    Port(Vec2d(-5, -7), 90, self),
                    Port(Vec2d(-5, 7), -90, self),
                    Port(Vec2d(-9, 0), 0, self)]
                    
class Drone(Cockpit, Engine, Cannon):
    baseImage = loadImage("res/ship" + ext)
    mass = 10
    name = "Tiny Fighter Chassis"
    image = None
    energyCost = 1 #this is used as a coefficient everywhere.
    #gun:
    shootDir = 0
    shootPoint = 20, 0
    damage = .2
    reloadTime = .1
    burstSize = 3
    reloadBurstTime = 2
    shotCost = .3
    shot = False
    #engine:
    force = 10000
    thrustCost = .1
    thrusted = False
    #gyro:
    torque = 600
    turnCost = .1
    turned = False
    #generator:
    rate = 30
    #battery:
    capacity = 40
    
    def __init__(self,  game):
        if Drone.animatedImage == None:
            Drone.animatedImage = loadImage("res/shipThrusting" + ext)
        self.baseAnimatedImage = Drone.animatedImage
        self.animated = True
        Part.__init__(self, game)
        self.reload = 0
        self.reloadBurst = 0
        self.burst = self.burstSize
        self.functions = [self.shoot, self.turnLeft, self.turnRight, \
        self.thrust]
        self.functionDescriptions = ['shoot', 'turn left', 'turn right', 'thrust']
    
    def update(self):
        pass
        # self.animated = self.thrusted
        # self.shot = False
        # self.thrusted = False
        # self.turned = False
        # self.reload -= 1. / self.game.fps
        # self.reloadBurst -= 1. / self.game.fps
        # if self.reloadBurst <= 0 :
        # 	self.burst = self.burstSize
        # 	self.reloadBurst = self.reloadBurstTime
        # #generator:
        # if self.ship and self.ship.energy < self.ship.maxEnergy:
        # 	self.ship.energy = min(self.ship.maxEnergy, \
        # 						self.ship.energy + self.rate / self.game.fps)
        # Part.update(self)
        
    def attach(self):
        #battery:
        self.ship.maxEnergy += self.capacity
        Part.attach(self)
        
    def shoot(self):
        """fires a bullet."""
        if self.shot: return
        self.shot = True
        if self.reload <= 0 \
        and self.ship.energy > self.shotCost * self.energyCost\
        and self.burst > 0:
            self.reload = self.reloadTime
            self.burst -= 1
            s = self.ship
            s.energy -= self.shotCost * self.energyCost
            if soundModule:
                self.game.universe.curSystem.floaters.add( 
                    Bullet(self.game, self, 
                    self.damage * s.efficiency * s.damageBonus * s.cannonBonus,
                    self.speed * s.cannonSpeedBonus,
                    self.range * s.cannonRangeBonus, image = self.bulletImage))
            if self.burst <= 0:
                self.reloadBurst = self.reloadBurstTime
                
    def thrust(self):
        """thrust: pushes the ship from the direction this engine points."""
        if self.thrusted: return
        self.thrusted = True
        if self.ship and self.ship.energy >= self.thrustCost * self.energyCost:
            dir = self.ship.dir
            
            self.ship.delta = self.ship.delta.rotatedd(dir, self.force / self.ship.mass / self.game.fps)

            self.ship.energy -= self.thrustCost / self.game.fps * self.energyCost
            self.thrusting = True
            
    def turnLeft(self, angle = None):
        """rotates the ship counter-clockwise."""
        if self.turned: return
        self.turned = True
        if angle:
            angle = max(- self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus, -abs(angle) )
        else:
            angle = - self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus
        if self.ship and self.ship.energy >= self.turnCost * self.energyCost:
            self.ship.dir = angleNorm(self.ship.dir + angle)
            self.ship.energy -= self.turnCost / self.game.fps * self.energyCost
        
    def turnRight(self, angle = None):
        """rotates the ship clockwise."""
        if self.turned: return
        self.turned = True
        if angle:
            angle = min(self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus, abs(angle) )
        else:
            angle = self.torque / self.ship.moment / self.ship.game.fps \
                    * self.ship.efficiency * self.ship.torqueBonus
        if self.ship and self.ship.energy >= self.turnCost * self.energyCost:
            self.ship.dir = angleNorm(self.ship.dir + angle)
            self.ship.energy -= self.turnCost / self.game.fps * self.energyCost



