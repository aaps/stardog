#spaceship.py
    
from utils import *
from parts import *
from partCatalog import *
from floaters import *

from pygame.locals import *
import stardog
from adjectives import addAdjective
from skills import *

def makeFighter(game, pos, delta, dir = 270, script = None, \
                color = (255, 255, 255), player = False):
    """starterShip(x,y) -> default starting ship at x,y."""
    if player:
        ship = Player(game, pos, delta, dir = dir, \
                script = script, color = color)
    else:
        ship = Ship(game, pos, delta, dir = dir, \
                script = script, color = color)
    cockpit = Fighter(game)
    gun = MachineGun(game)
    engine = Engine(game)
    shield = FighterShield(game)
    for part in [cockpit, gun, engine, shield]:
        if rand() > .8:
            addAdjective(part)
            if rand() > .6:
                addAdjective(part)
        part.color = color
    ship.addPart(cockpit)
    cockpit.addPart(engine, 3)
    cockpit.addPart(gun, 0)
    cockpit.addPart(shield, 2)
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship
    
def makeDestroyer(game, pos, delta, dir = 270, script = None, \
                color = (255, 255, 255), player = False):
    """starterShip(x,y) -> default starting ship at x,y."""
    if player:
        ship = Player(game, pos, delta, dir = dir, \
                script = script, color = color)
    else:
        ship = Ship(game, pos, delta, dir = dir, \
                script = script, color = color)
    gyro = Gyro(game)
    generator = Generator(game)
    battery = Battery(game)
    cockpit = Destroyer(game)
    gun = RightLaser(game)
    engine = Engine(game)
    shield = Shield(game)
    for part in [gyro, generator, battery, cockpit, gun, engine, shield]:
        if rand() > .8:
            addAdjective(part)
            if rand() > .6:
                addAdjective(part)
        part.color = color
    ship.addPart(cockpit)
    
    cockpit.addPart(gun, 2)
    cockpit.addPart(battery, 3)
    cockpit.addPart(generator, 4)
    cockpit.addPart(gyro, 5)
    cockpit.addPart(shield, 6)
    
    gyro.addPart(engine, 1)
    
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship	
    
def makeInterceptor(game, pos, delta, dir = 270, script = None, \
                color = (255, 255, 255), player = False):
    """starterShip(x,y) -> default starting ship at x,y."""
    if player:
        ship = Player(game, pos, delta, dir = dir, \
                script = script, color = color)
    else:
        ship = Ship(game, pos, delta, dir = dir, \
                script = script, color = color)
    cockpit = Interceptor(game)
    gyro = Gyro(game)
    generator = Generator(game)
    battery = Battery(game)
    gun = LeftFlakCannon(game)
    gun2 = RightFlakCannon(game)
    missile = MissileLauncher(game)
    engine = Engine(game)
    engine2 = Engine(game)
    quarter = MineDropper(game)#Quarters(game)
    for part in [gyro, generator, battery, cockpit, gun, gun2, engine, engine2,
                missile, quarter]:
        if rand() > .8:
            addAdjective(part)
            if rand() > .6:
                addAdjective(part)
        part.color = color
    ship.addPart(cockpit)
    cockpit.addPart(missile, 0)
    cockpit.addPart(gun, 2)
    cockpit.addPart(gun2, 3)
    cockpit.addPart(generator, 4)
    cockpit.addPart(gyro, 5)
    generator.addPart(battery, 0)
    battery.addPart(engine, 0)
    gyro.addPart(engine2, 1)
    gyro.addPart(quarter, 2)
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship

def makeJuggernaut(game, pos, delta, dir=27, script = None, \
                color = (255,255,255), player=False):
    if player:
        ship = Player(game, pos, delta, dir=dir, \
            script = script, color = color)
    else:
        ship = Ship(game, pos, delta, dir=dir, \
            script = script, color = color)
    
    cockpit = Interceptor(game)
    gyro = Gyro(game)
    generator = Generator(game)
    battery = Battery(game)
    gun = LeftFlakCannon(game)
    gun2 = RightFlakCannon(game)
    engine = Engine(game)
    engine2 = Engine(game)
    quarter = Quarters(game)
    shield = Shield(game)
    
    for part in [gyro, generator, battery, cockpit, gun, gun2, engine, engine2, quarter, shield]:
        if rand() > .8:
            addAdjective(part)
            if rand() > .6:
                addAdjective(part)
        part.color = color
    ship.addPart(cockpit)
    
    cockpit.addPart(quarter, 1)
    cockpit.addPart(gun, 2)
    cockpit.addPart(gun2, 3)
    cockpit.addPart(generator, 4)
    cockpit.addPart(gyro, 5)
    cockpit.addPart(shield, 0)
    
    generator.addPart(battery, 0)
    
    battery.addPart(engine, 0)
    
    gyro.addPart(engine2, 1)
    
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship

def makeScout(game, pos, delta, dir=27, script=None, \
                color = (255,255,255), player=False):
    if player:
        ship = Player(game, pos, delta, dir = dir, \
                script = script, color = color)
    else:
        ship = Ship(game, pos, delta, dir = dir, \
                script = script, color = color)
    cockpit = Fighter(game)
    battery = Battery(game)
    cannon = RightFlakCannon(game)
    radar = Radar(game)
    engine = Engine(game)
    #gun = MachineGun(game)
    #engine = Engine(game)
    #shield = FighterShield(game)
    for part in [cockpit, battery, cannon, radar, engine]:
        if rand() > .8:
            addAdjective(part)
            if rand() > .6:
                addAdjective(part)
        part.color = color
    ship.addPart(cockpit)
    cockpit.addPart(battery, 1)
    cockpit.addPart(cannon, 2)
    cockpit.addPart(radar, 3)
    radar.addPart(engine, 0)
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship

def makeFreighter(game, pos, delta, dir=27, script=None, \
                    color = (255,255,255), player=False):
    pass

def playerShip(game, pos, delta, dir = 270, script = None, \
                color = (255, 255, 255), type = 'fighter'):
    """starterShip(x,y) -> default starting ship at x,y."""
    if type == 'destroyer':
        ship = makeDestroyer(game, pos, delta, dir, 
                script, color, player=True)
    elif type == 'interceptor':
        ship = makeInterceptor(game, pos, delta, dir, 
                script, color, player=True)
    elif type == 'juggernaut':
        ship = makeJuggernaut(game, pos, delta, dir, script, color, player=True)
    elif type == 'scout':
        ship = makeScout(game, pos, delta, dir, script, color, player=True)
    else:
        ship = makeFighter(game, pos, delta, dir, 
                script, color, player=True)
    #default controls:
    # key, function, toggle or not
    script.initbind(K_DOWN, ship.reverse,False)
    script.initbind(K_UP, ship.forward,False)
    script.initbind(K_RIGHT, ship.turnRight,False)
    script.initbind(K_LEFT, ship.turnLeft,False)
    script.initbind(K_RCTRL, ship.shoot,False)
    script.initbind(K_s, ship.reverse,False)
    script.initbind(K_r, ship.toggleRadar,True)
    script.initbind(K_t, ship.targetNextShip,True)
    script.initbind(K_y, ship.targetPrefShip,True)
    script.initbind(K_g, ship.targetNextPlanet,True)
    script.initbind(K_h, ship.targetPrefPlanet,True)
    script.initbind(K_b, ship.targetNextPart,True)
    script.initbind(K_n, ship.targetPrefPart,True)
    script.initbind(K_j, ship.toggleGatewayFocus,True)
    script.initbind(K_w, ship.forward,False)
    script.initbind(K_e, ship.left,False)
    script.initbind(K_q, ship.right,False)
    script.initbind(K_d, ship.turnRight,False)
    script.initbind(K_a, ship.turnLeft,False)
    #script.initbind(K_LCTRL, ship.shoot,False)
    script.initbind(K_SPACE, ship.shoot,False)
    script.initbind(K_m, ship.launchMines,False)
    
    return ship

class Ship(Floater):
    """Ship(x, y, dx = 0, dy = 0, dir = 270,
    script = None, color = (255,255,255)) 
    script should have an update method that 
    returns (moveDir, target, action)."""
    mass = 0
    moment = 0
    parts = []
    atgateway = False
    attention = 0
    forwardEngines = []
    maxhp = 0
    hp = 0
    forwardThrust = 0
    reverseThrust = 0
    leftThrust = 0
    rightThrust = 0
    torque = 0
    reverseEngines = []
    leftEngines = []
    rightEngines = []
    guns = []
    missiles = []
    gyros = []
    number = 0
    numParts = 0
    curtarget = None
    firstname = None
    secondname = None
    skills = []
    level = 1
    partEffects = []
    effects = []
    skillEffects = []
    
    partLimit = 8
    penalty = .1
    bonus = .05
    efficiency = 1.
    #bonuses:
    baseBonuses = {\
    'thrustBonus' : 1., 'torqueBonus' : 1.,\
    'shieldRegenBonus' : 1., 'shieldMaxBonus' : 1.,\
    'generatorBonus' : 1., 'batteryBonus' : 1., 'regeneration' : 0, 'energyUseBonus' : 1.,\
    'massBonus' : 1., 'sensorBonus' : 1., 'hiddenBonus' : 1., 'fireRateBonus' : 1.,\
    'damageBonus' : 1., 'cannonBonus' : 1., 'laserBonus' : 1., 'missileBonus' : 1.,\
    'cannonRateBonus' : 1., 'laserRateBonus' : 1., 'missileRateBonus' : 1.,\
    'cannonRangeBonus' : 1., 'laserRangeBonus' : 1., 'missileRangeBonus' : 1.,\
    'cannonDefenseBonus' : 1., 'laserDefenseBonus' : 1., 'missileDefenseBonus' : 1.,\
    'cannonSpeedBonus' : 1., 'missileSpeedBonus' : 1.\
    }

    
    def __init__(self, game, pos, delta, dir = 270, script = None, \
                color = (255, 255, 255), name=("shippy","Mcshipperson")):
        Floater.__init__(self, game, pos, delta, dir, 1)
        self.inventory = []
        """
        self.insertInInventory(Gyro, 3)
        self.insertInInventory(MineDropper, 2)
        self.insertInInventory(Generator, 4)
        self.insertInInventory(Battery, 4)
        """
        self.firstname = name[0]
        self.secondname = name[1]
        self.ports = [Port((0,0), 0, self)]
        self.energy = 0
        self.maxEnergy = 0
        self.color = color
        self.part = None
        if hasattr(self, 'knownplanets'):
            self.knownplanets[:] = []
        else:
            self.knownplanets = []
        self.__dict__.update(self.baseBonuses)
        if script: self.script = script
        else: self.script = Script(game)
        self.baseImage = pygame.Surface((200, 200), hardwareFlag | SRCALPHA).convert_alpha()
        self.baseImage.set_colorkey((0,0,0))
        self.functions = [self.forward, self.reverse, self.left, self.right, \
                self.turnLeft, self.turnRight, self.shoot, self.launchMissiles, self.launchMines, self.toggleGatewayFocus, self.toggleRadar]
        self.functionDescriptions = []
        for function in self.functions:
            self.functionDescriptions.append(function.__doc__)
        self.baseBonuses = self.baseBonuses.copy()

    def insertInInventory(self, part, amount=1):
        for i in range(amount):
            self.inventory.append(part(self.game))

    def addPart(self, part, portIndex = 0):
        """ship.addPart(part) -> Sets the main part for this ship.
        Only used for the base part (usually a cockpit), other parts are added to parts."""
        part.parent = self
        part.dir = 0
        part.offset = Vec2d(0, 0)
        part.ship = self
        part.image = colorShift(part.baseImage, self.color).convert()
        part.image.set_colorkey((0,0,0))
        self.ports[0].part = part
        self.reset()

    def reset(self):
        self.parts = []
        self.forwardEngines = []
        self.forwardThrust = 0
        self.reverseThrust = 0
        
        self.leftThrust = 0
        self.rightThrust = 0
        self.torque = 0
        self.reverseEngines = []
        self.leftEngines = []
        self.rightEngines = []
        self.guns = []
        self.missiles = []
        self.radars = []
        self.gwfocusus = []
        self.mines = []
        self.gyros = []
        self.partLimit = Ship.partLimit
        self.__dict__.update(Ship.baseBonuses)
        #recalculate stats:
        self.dps = 0
        self.partRollCall(self.ports[0].part) 
        minX, minY, maxX, maxY = 0, 0, 0, 0
        #TODO: ? make the center of the ship the center of mass instead of the 
        #center of the radii. 
        for part in self.parts:
            if isinstance(part, Dummy): continue
            minX = min(part.offset[0] - part.radius, minX)
            minY = min(part.offset[1] - part.radius, minY)
            maxX = max(part.offset[0] + part.radius, maxX)
            maxY = max(part.offset[1] + part.radius, maxY)
        self.radius = max(maxX - minX, maxY - minY) / 2
        #recenter:
        # xCorrection = (maxX + minX) / 2
        # yCorrection = (maxY + minY) / 2
        Correction = Vec2d( (maxX + minX) / 2, (maxY + minY) / 2)
        self.partEffects = []
        self.mass = 1
        self.moment = 1
        self.maxEnergy = 1
        self.maxhp = 0
        partNum = 1
        for part in self.parts:
            if not isinstance(part, Dummy):
                part.number = partNum
                partNum += 1
                part.offset = part.offset - Correction		
                part.attach()
        partNum -= 1
        if partNum > self.partLimit:
            self.efficiency = (1 - self.penalty) ** (partNum - self.partLimit)
        else:
            self.efficiency = 2 - (1 - self.bonus) ** (self.partLimit - partNum)
        self.numParts = partNum
        self.energy = min(self.energy, self.maxEnergy)
        self.hp = min(self.hp, self.maxhp)
        for skill in self.skills:
            skill.shipReset()
        #redraw base image:
        if self.game.pause:
            size = int(self.radius * 2 + 60)
        else: 
            size = int(self.radius * 2)
        self.baseImage = pygame.Surface((size, size), \
                    hardwareFlag | SRCALPHA).convert_alpha()
        self.baseImage.set_colorkey((0,0,0))
        if self.ports[0].part:
            self.ports[0].part.draw(self.baseImage)



    def partRollCall(self, part):
        """adds parts to self.parts recursively."""
        if part:
            self.parts.append(part)
            if isinstance(part, Engine):
                if part.dir == 180:
                    self.reverseEngines.append(part)
                    self.reverseThrust += part.exspeed * part.exmass
                if part.dir == 0 or part.dir == 360:
                    self.forwardEngines.append(part)
                    self.forwardThrust += part.exspeed * part.exmass
                if part.dir == 90:
                    self.rightEngines.append(part)
                    self.rightThrust += part.exspeed * part.exmass
                if part.dir == 270:
                    self.leftEngines.append(part)
                    self.leftThrust += part.exspeed * part.exmass
            if isinstance(part, Gyro):
                self.gyros.append(part)
                self.torque += part.torque
            if isinstance(part, Radar):
                self.radars.append(part)
            if isinstance(part, GatewayFocus):
                self.gwfocusus.append(part)
            if isinstance(part, Gun):
                if isinstance(part, MissileLauncher):
                    self.missiles.append(part)
                if isinstance(part, MineDropper):
                    self.mines.append(part)
                else:
                    self.guns.append(part)
                self.dps += part.getDPS()
            for port in part.ports:
                if port.part:
                    self.partRollCall(port.part)
                
    def forward(self):
        """thrust forward using all forward engines"""
        for engine in self.forwardEngines:
            engine.thrust()
    def reverse(self):
        """thrust backward using all reverse engines"""
        for engine in self.reverseEngines:
            engine.thrust()
    def left(self):
        """strafes left using all left engines"""
        for engine in self.leftEngines:
            engine.thrust()
    def right(self):
        """strafes right using all right engines"""
        for engine in self.rightEngines:
            engine.thrust()
    def turnLeft(self, angle = None):
        """Turns ccw using all gyros."""
        for gyro in self.gyros:
            gyro.turnLeft(angle)
    def turnRight(self, angle = None):
        """Turns cw using all gyros."""
        for gyro in self.gyros:
            gyro.turnRight(angle)
    def shoot(self):
        """fires all guns."""
        self.attention += 1
        for gun in self.guns:
            gun.shoot()
    def launchMissiles(self):
        self.attention += 2
        for missle in self.missiles:
            missle.shoot()
    def launchMines(self):
        self.attention += 0.5
        for mine in self.mines:
            mine.shoot()
    def toggleRadar(self):
        for radar in self.radars:
            radar.toggle()

    def targetNextShip(self):
        # from planet import Planet
        resultList = []
        
        for radar in self.radars:
            resultList= list(set(radar.detected)|set(resultList))
        resultList =  filter(lambda f: isinstance(f, Ship), resultList)
        length = len(resultList)


        if self.curtarget and self.curtarget in resultList  and length-1 > resultList.index(self.curtarget):
            self.curtarget = resultList[resultList.index(self.curtarget)+1]
        elif length > 0:
            self.curtarget = resultList[0]
        else:
            self.curtarget = None


    def targetPrefShip(self):
        # from planet import Planet
        resultList = []
        
        for radar in self.radars:
            resultList= list(set(radar.detected)|set(resultList))
        resultList = filter(lambda f: isinstance(f, Ship), resultList)
        length = len(resultList)


        if self.curtarget and self.curtarget in resultList  and  resultList.index(self.curtarget) > 0:
            self.curtarget = resultList[resultList.index(self.curtarget)-1]
        elif length > 0:
            self.curtarget = resultList[length-1]
        else:
            self.curtarget = None

    def targetNextPlanet(self):
        from planet import Planet

        length = len(self.knownplanets)


        if self.curtarget and self.curtarget in self.knownplanets  and length-1 > self.knownplanets.index(self.curtarget):
            self.curtarget = self.knownplanets[self.knownplanets.index(self.curtarget)+1]
        elif length > 0:
            self.curtarget = self.knownplanets[0]
        else:
            self.curtarget = None

    def targetPrefPlanet(self):
        from planet import Planet

        length = len(self.knownplanets)


        if self.curtarget and self.curtarget in self.knownplanets  and self.knownplanets.index(self.curtarget) > 0:
            self.curtarget = self.knownplanets[self.knownplanets.index(self.curtarget)-1]
        elif length > 0:
            self.curtarget = self.knownplanets[length-1]
        else:
            self.curtarget = None

    def targetNextPart(self):
        resultList = []
        
        for radar in self.radars:
            
            resultList= list(set(radar.detected)|set(resultList))
        resultList =  filter(lambda f: isinstance(f, Part), resultList)
        length = len(resultList)


        if self.curtarget and self.curtarget in resultList  and length-1 > resultList.index(self.curtarget):
            self.curtarget = resultList[resultList.index(self.curtarget)+1]
        elif length > 0:
            self.curtarget = resultList[0]
        else:
            self.curtarget = None

    def targetPrefPart(self):
        resultList = []
        
        for radar in self.radars:
            
            resultList= list(set(radar.detected)|set(resultList))
        resultList =  filter(lambda f: isinstance(f, Part), resultList)
        length = len(resultList)


        if self.curtarget and self.curtarget in resultList  and resultList.index(self.curtarget) > 0:
            self.curtarget = resultList[self.knownplanets.index(self.curtarget)-1]
        elif length > 0:
            self.curtarget = resultList[length-1]
        else:
            self.curtarget = None

    def toggleGatewayFocus(self):
        for gwfocus in self.gwfocusus:
            gwfocus.toggle()

    def combineLists(self, atype):
        pass
    
    
    def update(self):
        #check if dead:
        if not self.parts or self.parts[0].hp <= 0:
            self.kill()
        #run script, get choices.
        
        if self.game.player == self:
             if not self.game.pause and not self.game.console:
                self.script.update(self)
        else:
            self.script.update(self)

        resultList = []
        for radar in self.radars:
            resultList= list(set(radar.detected)|set(resultList))
        if not self.curtarget in resultList:
            self.curtarget = None


        if self.attention > 0:
            self.attention -= 0.1 / self.game.fps
        # actual updating:
        Floater.update(self)
        #parts updating:
        if self.ports[0].part:
            self.ports[0].part.update()
        
        #active effects:
        for effect in self.effects:
            effect(self)
        for effect in self.partEffects:
            effect(self)

        if self.atgateway and dist2(self, self.atgateway) > (self.atgateway.radius * 1.1) ** 2:
            self.atgateway = False


    def draw(self, surface, offset = None, pos = (0, 0)):
        """ship.draw(surface, offset) -> Blits this ship onto the surface. 
         offset is the (x,y) of the topleft of the surface, pos is the
         position to draw the ship on the surface, where pos=(0,0) is the
         center of the surface. If offset is none, the ship will be drawn down 
         and right from pos where pos(0,0) is the topleft of the surface."""
        #image update:
        #note: transform is counter-clockwise, opposite of everything else.
        buffer = pygame.Surface((self.radius * 2, self.radius * 2), \
                flags = hardwareFlag | SRCALPHA).convert_alpha()
        buffer.set_colorkey((0,0,0))
        self.image = pygame.transform.rotate(self.baseImage, \
                                    -self.dir).convert_alpha()
        self.image.set_colorkey((0,0,0))
        
        #imageOffset compensates for the extra padding from the rotation.
        imageOffset = [- self.image.get_width() / 2,\
                       - self.image.get_height() / 2]
        #offset is where on the input surface to blit the ship.
        if offset:
            pos = self.pos  - offset + pos + imageOffset
                  
        #draw to buffer:
        surface.blit(self.image, pos)
        for part in self.parts:
            part.redraw(surface, offset)
        
        #shield:
        if self.hp > .0002:
            r = int(self.radius)
            shieldColor = (50,100,200, int(255. / 3 * self.hp / self.maxhp) )
            pygame.draw.circle(buffer, shieldColor, \
                        (r, r), r, 0)
            pygame.draw.circle(buffer, (50,50,0,50), \
                        (r, r), r, 5)
            rect = (0,0, r * 2, r * 2)
            pygame.draw.arc(buffer, (50,50,200,100), rect, + math.pi/2,\
                            math.pi * 2 * self.hp / self.maxhp + math.pi/2, 5)
                            
        #draw to input surface:
        pos[0] += - imageOffset[0] - self.radius
        pos[1] += - imageOffset[1] - self.radius
        surface.blit(buffer, pos) 
        
    def takeDamage(self, damage, other):
        self.attention += 5
        self.hp = max(self.hp - damage, 0)
        if isinstance(other, Bullet) and other.ship == self.game.player:
            self.game.player.xpDamage(self, damage)

    def kill(self):
        """play explosion effect than call Floater.kill(self)"""
        if soundModule:
            setVolume(explodeSound.play(), self, self.game.player)
        for part in self.inventory:
            part.scatter(self)
        Floater.kill(self)

        

    def planetCollision(self, planet):
        shipangle = (planet.pos - self.pos).get_angle()
        planetangle = (self.pos - planet.pos).get_angle()

        dx, dy = rotate(self.delta.x-planet.delta.y, self.delta.y-planet.delta.y, shipangle-planetangle)
        speed = sqrt(dy ** 2 + dx ** 2)
        if speed > planet.LANDING_SPEED:
            if planet.damage.has_key(self):
                damage = planet.damage[self]
            else:
                if soundModule:
                    setVolume(hitSound.play(), planet, planet.game.player)
                #set damage based on incoming speed and mass.
                damage = speed * self.mass * planet.PLANET_DAMAGE
            for part in self.parts:
                if collisionTest(planet, part):
                    temp = part.hp
                    part.takeDamage(damage, planet)
                    damage -= temp
                    if damage <= 0:
                        r = self.radius + planet.radius
                        self.delta = self.delta * (self.pos - planet.pos) + self.delta * -(self.pos - planet.pos)
                        if planet.damage.has_key(self):
                            del planet.damage[self]
                        return
            if damage > 0:
                planet.damage[self] = damage
        else:
            #landing:
            if self == planet.game.player and not self.landed:
                planet.game.pause = True
                self.landed = planet
                self.game.menu.parts.reset()
            self.delta.x, self.delta.y = planet.delta.x, planet.delta.y

    def gatewayCollision(self, gateway):
        self.atgateway = gateway

    def freepartCollision(self, part):
        if part.pickuptimeout <= 0:
            part.dir = 0
            part.image = colorShift(pygame.transform.rotate(part.baseImage, part.dir), part.color).convert()
            part.image.set_colorkey((0,0,0))
            self.inventory.append(part)
            part.kill()
            if self.game.player == self:
                self.game.menu.parts.inventoryPanel.reset() #TODO: make not suck


class Player(Ship):
    xp = 0
    developmentPoints = 12
    landed = False
    name = "Player X"
    def __init__(self, game, pos, delta, dir = 270, script = None, \
                color = (255, 255, 255)):
        Ship.__init__(self, game, pos, delta, dir, script, color)
        self.skills = [Modularity(self), Agility(self), Composure(self)]

    def xpQuest(self, xp):
        self.xp += xp

    def xpKill(self, ship):
        self.xp +=  10. * ship.level / self.level

    def xpDamage(self, target, damage):
        if isinstance(target, Part) and target.parent:
            target = target.parent #count the ship, not the part.
        self.xp += 1. * target.level / self.level * damage

    def xpDestroy(self, target):
        self.xp += 2. * target.level / self.level

    def update(self):
        if self.game.debug: print 'xp:',self.xp
        if self.xp >= self.next():
            self.level += 1
            self.developmentPoints += 1
            self.xp = 0
        if self.landed \
        and dist2(self, self.landed) > (self.landed.radius * 1.1) ** 2:
            self.landed = False
        Ship.update(self)
    
    def next(self):
        return 1.1 ** self.level * 10
