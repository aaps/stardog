# floaters.py

from utils import *
from pygame.locals import *
import stardog
from vec2d import Vec2d
import math
from particles import *

FPS = 200
MISSILE_RADIUS = 50
SOUND_RADIUS = 3000


def setVolume(channel, floater1, floater2):
    from spaceship import Player
    """sets volume for a channel based on the distance between
     the player and floater."""
    distance = floater2.pos.get_distance(floater1.pos)
    if channel and floater1 and floater2:
        volume = 0.0
        if distance < SOUND_RADIUS and (isinstance(floater1, Player) or
           isinstance(floater2, Player)):
            volume = math.sqrt((SOUND_RADIUS - distance)**1.8 /
                               (SOUND_RADIUS + .001)**1.8)
        channel.set_volume(volume)

BULLET_IMAGE = loadImage("res/ammo/shot.png")
MISSILE_IMAGE = loadImage("res/ammo/missile.png")
DEFAULT_IMAGE = loadImage("res/parts/default.png")


class Ballistic(object):
    """an abstraction of a Floater.  Just has a Vec2d,Vec2d."""
    def __init__(self, pos, delta):
        self.pos = pos
        self.delta = delta


class Floater(pygame.sprite.Sprite, Ballistic):
    """creates a floater with position (x,y) in pixels, speed (dx, dy)
    in pixels per second, direction dir
    where 0 is pointing right and 270 is pointing up, radius radius
    (for collision testing), and with the image image.  Image should be a
    string of a file name without an axtension- there should be both a .gif
    and a .bmp, which is used depends on the pygame support on the run
    system."""
    baseImage = None

    def __init__(self, universe, pos, delta, dir=270, radius=10,
                 image=None):
        pygame.sprite.Sprite.__init__(self)
        self.universe = universe
        self.dir = dir
        self.pos = pos
        self.delta = delta
        self.emitters = []
        self.color = FLOATER
        self.hp = 1
        self.mass = 1
        self.tangible = True
        self.lastDamageFrom = None
        self.fps = 10
        self.radius = radius
        if (not image):
            image = DEFAULT_IMAGE
        self.image = pygame.transform.rotate(image, -self.dir).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        """updates this floater based on its variables"""
        self.pos += self.delta / self.fps
        self.rect.center = self.pos.inttup()
        for emitter in self.emitters:
            emitter.update()

    def takeDamage(self, damage, other):

        self.lastDamageFrom = other
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def draw(self, surface, offset=Vec2d(0, 0)):
        """Blits this floater onto the surface. """
        poss = (self.pos.x - self.image.get_width() / 2 - offset.x,
                self.pos.y - self.image.get_height() / 2 - offset.y)
        surface.blit(self.image, poss)
        for emitter in self.emitters:
            emitter.draw(surface, offset)

    def crash(self, other):
        if soundModule:
            setVolume(hitSound.play(), self, other)
        hpA = self.hp
        hpB = other.hp
        if hpB > 0:
            self.takeDamage(hpB, other)
        if hpA > 0:
            other.takeDamage(hpA, self)

    def addEmitter(self, emitter):
        self.emitters.append(emitter)

    def condHalfDamage(self):
        return self.hp <= self.maxhp/2

    def condThQuarterDamage(self):
        return self.hp <= self.maxhp/4

    def condAlways(self):
        return True

    def setFPS(self, fps):
        self.fps = fps


class Bullet(Floater):
    def __init__(self, universe, gun, damage, speed, range, image=None):
        dir = gun.dir + gun.ship.dir
        # cost is short for cos(theta)
        # cost = cos(dir)
        # sint = sin(dir)
        pos = (gun.pos + Vec2d(gun.shootPoint).rotated(dir) +
               gun.ship.delta / universe.game.fps)
        # not needed for the offset, but needed for the dir.
        dir += gun.shootDir
        self.speed = speed
        delta = gun.ship.delta.rotatedd(dir, self.speed)
        if image is None:
            image = BULLET_IMAGE
        Floater.__init__(self, universe, pos, delta,
                         dir=dir, radius=gun.bulletRadius,
                         image=image)
        self.range = range
        self.hp = damage
        self.life = 0.
        self.ship = gun.ship
        if 'target' in gun.ship.__dict__:
            self.curtarget = gun.ship.curtarget

    def update(self):
        self.life += 1. / self.fps
        Floater.update(self)
        if self.life > self.range:
            self.softkill()

    def detonate(self):
        if self.lastDamageFrom:
            delta = (self.lastDamageFrom.delta + self.delta) / 2
        else:
            delta = self.delta
        impact = Impact(self.universe.game, self.pos, delta, 20, 14)
        self.universe.curSystem.add(impact)

    def kill(self):
        if soundModule:
            setVolume(missileSound.play(), self, self.universe.player)
        self.detonate()
        Floater.kill(self)

    def softkill(self):
        # self.detonate()
        Floater.kill(self)


class Missile(Bullet):
    hp = 1

    def __init__(self, universe, launcher, damage, speed, acceleration, range,
                 explosionRadius, image=None):
        Bullet.__init__(self, universe, launcher, self.hp, speed, range, image)
        self.damage = damage
        self.turning = launcher.turning
        self.percision = launcher.percision
        self.acceleration = launcher.acceleration
        self.explosionRadius = explosionRadius
        self.time = launcher.explosionTime
        self.force = launcher.force
        self.life = 0
        self.turning = 0
        self.percision = 0
        self.impacted = None
        self.explode = False
        self.emitters.append(Emitter(self, self.condAlways, 5, 100, 200,
                             (255, 255, 255, 255), (255, 255, 255, 0), 2,
                             4, 100, 2, 5, True))

    def update(self):
        self.life += 1. / self.fps
        self.dir = (self.dir + 180) % 360 - 180
        self.delta += (Vec2d(0, 0).rotatedd(self.dir, self.acceleration)
                       / self.fps)
        if self.life > self.range:
            self.kill()
        Floater.update(self)

    def detonate(self):
        delta = self.delta.rotatedd(self.dir, -(self.acceleration * self.life))
        explosion = Explosion(self.universe, self.pos, delta,
                              self.explosionRadius, self.time, self.damage,
                              self.force)
        self.universe.curSystem.add(explosion)

    def kill(self):
        self.detonate()
        if soundModule:
            setVolume(missileSound.play(), self, self.universe.player)
        Floater.kill(self)

    def takeDamage(self, damage, other):
        self.impacted = other
        Floater.takeDamage(self, damage, other)


class Mine(Bullet):
    hp = 1

    def __init__(self, universe, launcher, damage, speed, acceleration, range,
                 explosionRadius, image=None):
        Bullet.__init__(self, universe, launcher, self.hp, speed, range, image)
        self.damage = damage
        self.turning = launcher.turning
        self.percision = launcher.percision
        self.acceleration = launcher.acceleration
        self.explosionRadius = explosionRadius
        self.time = launcher.explosionTime
        self.force = launcher.force
        self.radius = 15
        self.impacted = None
        self.explode = False
        self.tangible = True
        self.turning = 0
        self.percision = 0

    def update(self):
        self.dir = (self.dir+180) % 360 - 180
        self.delta = self.delta / 1.05
        if self.life > self.range:
            self.kill()
        Floater.update(self)

    def detonate(self):
        delta = self.delta.rotatedd(self.dir, -(self.acceleration*self.life))
        explosion = Explosion(self.universe, self.pos, delta,
                              self.explosionRadius, self.time, self.damage,
                              self.force)
        self.game.universe.curSystem.add(explosion)

    def kill(self):
        self.detonate()
        if soundModule:
            setVolume(missileSound.play(), self, self.game.player)
        Floater.kill(self)

    def takeDamage(self, damage, other):
        self.impacted = other
        Floater.takeDamage(self, damage, other)


class Explosion(Floater):
    life = 0

    def __init__(self, universe, pos, delta, radius=10,
                 time=5, damage=0, force=6000):
        image = pygame.Surface((radius * 2, radius * 2),
                               flags=hardwareFlag).convert()
        image.set_colorkey(BLACK)
        Floater.__init__(self, universe, pos, delta, radius=0,
                         image=image)
        self.maxRadius = int(radius)
        self.delta = delta
        self.force = force
        self.radius = 0
        self.time = time
        self.damage = damage
        self.hp = damage / (self.time * self.fps)
        if damage == 0:
            self.tangible = False
        self.emitters.append(RingEmitter(self, self.condAlways, 0, 50, 20, 50,
                                         (255, 200, 0, 250), (251, 0, 0, 1), 1,
                                         2, 30, 30, 10, 50, True))

    def update(self):
        self.life += 1. / self.fps
        if self.life > self.time:
            Floater.kill(self)
        self.hp = self.damage / (self.time * self.fps)
        # grow or shrink: size peaks at time / 2:
        if self.life < self.time / 4:
            self.radius = int(self.maxRadius * self.life * 4 / self.time)
        else:
            self.radius = int(self.maxRadius * (self.time * 4 / 3 -
                              self.life * 4 / 3) / self.time)
        Floater.update(self)

    def kill(self):
        pass

    def takeDamage(self, damage, other):
        pass


class Impact(Floater):
    life = 0
    tangible = False
    mass = 0

    def __init__(self, universe, pos, delta, radius=5,
                 time=1):
        image = pygame.Surface((radius * 2, radius * 2),
                               flags=hardwareFlag).convert()
        image.set_colorkey(BLACK)
        Floater.__init__(self, universe, pos, delta, radius=0,
                         image=image)
        self.maxRadius = int(radius)
        self.radius = 0
        self.time = time
        self.emitters.append(RingEmitter( self, self.condAlways , 0, 5, 5, 10,  (255,255,255,250), (100,100,255,1), 0.5, 1, 10, 10, 1, 5, True))

    def update(self):
        self.life += 1. / self.fps
        if self.life > self.time:
            Floater.kill(self)
        if self.life < self.time / 4:
            self.radius = int(self.maxRadius * self.life * 4 / self.time)
        else:
            self.radius = int(self.maxRadius * (self.time * 4 / 3 - self.life * 4 / 3) / self.time)
        Floater.update(self)




    def takeDamage(self, damage, other):
        pass

    
class LaserBeam(Floater):
    """LaserBeam(game, laser, damage, range) -> new LaserBeam

    A LaserBeam is the projectile of a Laser.  They are line segments
    that reach their end point instantly.  A LaserBeam has a different 
    collision mechanism: they use line/circle collision, and it is checked 
    during initialization."""

    baseImage = loadImage("res/ammo/laser.png").convert_alpha()
    # baseImage.set_colorkey(BLACK)
    
    def __init__(self, universe, laser, damage, range):
        dir = laser.dir + laser.ship.dir
        cost = cos(dir) #cost is short for cos(theta)
        sint = sin(dir)
        pos = laser.pos + Vec2d(laser.shootPoint).rotated(dir) + laser.ship.delta / universe.game.fps

        start = pos
        dir = laser.dir + laser.ship.dir + laser.shootDir
        length = range

        stop = pos.rotatedd(dir, range)

        Floater.__init__(self, universe, (start + stop) / 2, laser.ship.delta, dir,
                        radius = 0)

        self.life = .5 #seconds
        self.hp = 0
        self.tangible = False
        self.damage = damage
        self.start = start
        self.stop = stop
        left = min(start.x, stop.x)
        top = min(start.y, stop.y)
        width = abs(start.x - stop.x)
        height = abs(start.y - stop.y)
        self.rect = Rect(left, top, width, height)
        self.slope = (start.y-stop.y) / not0(start.x - stop.x)
        self.laser = laser
        self.life = laser.imageDuration
        self.ship = laser.ship
        self.width = laser.beamWidth
        self.image = pygame.transform.rotate(
                    pygame.transform.scale(
                    colorShift(self.baseImage, (bulletColor(self.damage))),
                    (int(length), 5)), -dir).convert_alpha()
        if 'target' in laser.ship.__dict__:
            self.curtarget = laser.ship.curtarget
        self.universe.curSystem.specialOperations.append(self.collision)

        
    def intersect(self, floater, skipRect = False):
        #check rect collide:
        if floater != self and (skipRect or self.rect.colliderect(floater.rect)):
            #check line-circle collide:
            dist = linePointDist(self.start, self.stop, (floater.pos.x, floater.pos.y))
            if dist < floater.radius:
                return dist

                
    def collision(self):
        from spaceship import Ship
        colliders = []
        for floater in self.universe.curSystem.floaters:
            if floater.tangible and self.intersect(floater):
                colliders.append(floater)
        if colliders:
            #recurse for parts in a ship:
            for floater in colliders:
                if isinstance(floater, Ship):
                    for part in floater.parts:
                        if self.intersect(part, True):
                            colliders.append(part)
            #sort so that the nearest gets hit first:
            dir = sign(self.stop.y + self.stop.x * self.slope - 
                    self.start.y + self.start.x * self.slope)
            colliders.sort(key = lambda f: 
                    (f.pos.y + f.pos.x * self.slope) * dir - f.radius)
            #hit until damage is used up
            for floater in colliders:
                tmp = floater.hp
                floater.takeDamage(self.damage, self)
                self.damage -= tmp
                if self.damage < 1: #fudge it for effect: 1 not 0
                    #adjust stop based on last hit target:
                    self.stop = (floater.pos.x, (floater.pos.x - self.start.x) 
                                            * self.slope + self.start.y)
                    
                    self.length = self.start.get_distance(self.stop)
                    break
                
                    
    def update(self):
        self.life -= 1. / self.fps
        Floater.update(self)
        self.start = self.start + self.delta / self.fps
        self.stop = self.stop  + self.delta / self.fps
        if self.life < 0:
            self.kill()
    
        
    def takeDamage(self, damage, other):
        pass
    
        
class RadarDisk(Floater):
    baseImage = None
    color = (0, 0, 0)
    mass = 0
    tangible = False

    def __init__(self, universe, pos, delta, dir = 0, radius = 10, image = None):
        # self.game = game
        self.dir = dir
        self.pos = pos
        self.delta = delta
        self.radius = radius

    def draw(self):
        pass

    def update(self):
        pass
