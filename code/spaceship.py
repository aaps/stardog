#spaceship.py
    
from utils import *
from parts import *
from cargo import *
from partCatalog import *
from floaters import *
from pygame.locals import *
from adjectives import addAdjective
from skills import *
from particles import *
from scripts import Controllable

def makeFighter(game, pos, delta, direction = 270, \
                color = (255, 255, 255),name=("Shippy","mcShipperson"), player = False, partlim=8):
    """starterShip(x,y) -> default starting ship at x,y."""
    if player:
        ship = Player(game, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    else:
        ship = Ship(game.universe, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    cockpit = Fighter(game.universe)
    gun = MachineGun(game.universe)
    engine = Engine(game.universe)
    shield = FighterShield(game.universe)
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

def makeFreighter(game, pos, delta, direction=270, color = SUPER_WHITE, name=("Shippy","mcShipperson"), player=False, partlim=8):
    if player:
        ship = Player(game, pos, delta, direction=direction, color=color, name=name, partlimit=partlim)
    else:
        ship = Ship(game.universe, pas, delta, direction=direction, color=color, name=name, partlimit=partlim)

    cockpit = Destroyer(game.universe)
    battery = Battery(game.universe)
    generator = Generator(game.universe)
    engine_left = Engine(game.universe)
    engine_right = Engine(game.universe)
    interc_left = Interconnect(game.universe)
    interc_right = Interconnect(game.universe)
    gyro_left = Gyro(game.universe)
    gyro_right = Gyro(game.universe)
    gun_left = LeftFlakCannon(game.universe)
    gun_right = RightFlakCannon(game.universe)
    ship.addPart(cockpit)

    chold1 = CargoHold(game.universe)
    chold2 = CargoHold(game.universe)
    chold3 = CargoHold(game.universe)
    chold4 = CargoHold(game.universe)
    chold5 = CargoHold(game.universe)
    chold6 = CargoHold(game.universe)
    chold7 = CargoHold(game.universe)
    chold8 = CargoHold(game.universe)

    #put a Gyro on either back-sides of the cockpit 
    cockpit.addPart(gyro_left, 3)
    cockpit.addPart(gyro_right, 4)
    #put a interconnect left and right attached to the gyro
    gyro_left.addPart(interc_left, 1)
    gyro_right.addPart(interc_right, 1)
    #put a engine left and right under the inter connect
    interc_left.addPart(engine_left, 0)
    interc_right.addPart(engine_right, 2)

    #build a stack of interconnects (to be replaced by cargoholds) 
    cockpit.addPart(chold1, 5)
    cockpit.addPart(chold2, 6)
    chold1.addPart(chold3, 1)
    chold2.addPart(chold4, 1)
    chold3.addPart(chold5, 1)
    chold4.addPart(chold6, 1)
    chold5.addPart(chold7, 1)
    chold6.addPart(chold8, 1)

    #put a battery and generator on either front-side of the cockpit.
    cockpit.addPart(battery, 2)
    cockpit.addPart(generator, 1)
    #put a flak cannon on either side.
    generator.addPart(gun_left, 0)
    battery.addPart(gun_right, 0)

    ship.reset()
    ship.energy = ship.maxEnergy * .8

    return ship

def makeDestroyer(game, pos, delta, direction = 270, color = (255, 255, 255),name=("Shippy","mcShipperson"), player = False, partlim=8):
    """starterShip(x,y) -> default starting ship at x,y."""

    if player:
        ship = Player(game, pos, delta, direction = direction, color = color, name=name, partlimit=partlim)
    else:
        ship = Ship(game.universe, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    gyro = Gyro(game.universe)
    generator = Generator(game.universe)
    battery = Battery(game.universe)
    cockpit = Destroyer(game.universe)
    gun = RightLaser(game.universe)
    engine = Engine(game.universe)
    shield = BigShield(game.universe)
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
    
def makeInterceptor(game, pos, delta, direction = 270, color = (255, 255, 255),name=("Shippy","mcShipperson"), player = False, partlim=8):
    """starterShip(x,y) -> default starting ship at x,y."""
    if player:
        ship = Player(game, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    else:
        ship = Ship(game.universe, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    cockpit = Interceptor(game.universe)
    gyro = Gyro(game.universe)
    generator = Generator(game.universe)
    battery = Battery(game.universe)
    gun = LeftFlakCannon(game.universe)
    gun2 = RightFlakCannon(game.universe)
    missile = MissileLauncher(game.universe)
    engine = Engine(game.universe)
    engine2 = Engine(game.universe)
    for part in [gyro, generator, battery, cockpit, gun, gun2, engine, engine2,
                missile]:
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
    # engine.addEmitter(Emitter(game, engine, 5, 10, 10, (100,100,255,255), (255,50,50,255), 1, 3, 10, 3, 1))
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship

def makeJuggernaut(game, pos, delta, direction=27, color = SUPER_WHITE, name=("Shippy","mcShipperson"), player=False, partlim=8):
    if player:
        ship = Player(game, pos, delta, direction=direction, color = color, name=name, partlimit=partlim)
    else:
        ship = Ship(game.universe, pos, delta, direction=direction, color = color, name=name, partlimit=partlim)
    
    cockpit = Interceptor(game.universe)
    gyro = Gyro(game.universe)
    generator = Generator(game.universe)
    battery = Battery(game.universe)
    gun = LeftFlakCannon(game.universe)
    gun2 = RightFlakCannon(game.universe)
    engine = Engine(game.universe)
    engine2 = Engine(game.universe)
    quarter = Quarters(game.universe)
    shield = BigShield(game.universe)
    
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

def makeScout(game, pos, delta, direction=27, color = SUPER_WHITE, name=("Shippy","mcShipperson"), player=False, partlim=8):
    if player:
        ship = Player(game, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    else:
        ship = Ship(game.universe, pos, delta, direction = direction, color = color,name=name, partlimit=partlim)
    cockpit = Fighter(game.universe)
    battery = Battery(game.universe)
    cannon = RightFlakCannon(game.universe)
    radar = Radar(game.universe)
    engine = Engine(game.universe)
    gatewayfocus = GatewayFocus(game.universe)
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
    cockpit.addPart(gatewayfocus, 0)
    radar.addPart(engine, 0)
    ship.reset()
    ship.energy = ship.maxEnergy * .8
    return ship

def playerShip(game, pos, delta, direction = 270, \
                color = (255, 255, 255), name = ("Shippy","mcShipperson"), type = 'fighter'):
    """starterShip(x,y) -> default starting ship at x,y."""
    name = name.split(" ")
    if len(name) == 1:
         name.append("Unknown")
    name = (name[0],name[1])

    if type == 'destroyer':
        ship = makeDestroyer(game, pos, delta, direction, color, name, player=True, partlim=12)
    elif type == 'freighter':
        ship = makeFreighter(game, pos, delta, direction, color, name, player=True, partlim=15)
    elif type == 'interceptor':
        ship = makeInterceptor(game, pos, delta, direction, color, name, player=True, partlim=10)
    elif type == 'juggernaut':
        ship = makeJuggernaut(game, pos, delta, direction, color, name, player=True, partlim=10)
    elif type == 'scout':
        ship = makeScout(game, pos, delta, direction, color, name, player=True, partlim=6)
    elif type == 'fighter':
        ship = makeFighter(game, pos, delta, direction, color, name, player=True, partlim=6)

    return ship



class Ship(Floater, Controllable):
    """Ship(x, y, dx = 0, dy = 0, direction = 270,
    script = None, color = SUPER_WHITE) 
    script should have an update method that 
    returns (moveDir, target, action)."""
    

    

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

    def __init__(self, game, pos, delta, direction = 270, \
                color = (255, 255, 255), name=("shippy","Mcshipperson"), partlim=8):
        Floater.__init__(self, game.universe, pos, delta, direction, 1)
        Controllable.__init__(self, game)
        self.partLimit = 8
        self.penalty = .1
        self.bonus = .05
        self.efficiency = 1.
        self.gyros = []
        self.number = 0
        self.numParts = 0
        self.curtarget = None
        self.firstname = None
        self.secondname = None
        self.skills = []
        self.level = 1
        self.partEffects = []
        self.effects = []
        self.skillEffects = []
        self.crewsize = 1
        self.gargoholdsize = 5
        self.torque = 0
        self.reverseEngines = []
        self.leftEngines = []
        self.rightEngines = []
        self.guns = []
        self.missiles = []
        self.torque = 0
        self.reverseEngines = []
        self.leftEngines = []
        self.rightEngines = []
        self.guns = []
        self.missiles = []
        self.gyros = []
        self.forwardEngines = []
        self.maxhp = 0
        self.hp = 0
        self.landed = None
        self.forwardThrust = 0
        self.reverseThrust = 0
        self.leftThrust = 0
        self.rightThrust = 0
        self.overedge = False
        self.atgateway = None
        self.attention = 0
        self.detectionscore = 0
        self.mass = 0
        self.moment = 0
        self.parts = []
        self.script = None
        self.universe = game.universe
        self.spawncost = 10
        self.surespawn = False
        self.inventory = []
        self.firstname = name[0]
        self.secondname = name[1]
        self.ports = [Port((0,0), 0, self)]
        self.energy = 0
        self.maxEnergy = 0
        self.color = color
        self.part = None
        self.partLimit = partlim
        self.knownsystems = dict()
        self.__dict__.update(self.baseBonuses)


        self.functions = [self.forward, self.reverse, self.left, self.right, \
                self.turnLeft, self.turnRight, self.shoot, self.launchMissiles, self.launchMines, self.toggleGatewayFocus, self.toggleRadar]
        self.functionDescriptions = []
        for function in self.functions:
            self.functionDescriptions.append(function.__doc__)
        self.baseBonuses = self.baseBonuses.copy()
        # register our explosion sound
        self.soundsys = self.universe.game.soundSystem
        self.explosionSound = 'se_explode03.wav'
        self.soundsys.register(self.explosionSound)


    def insertPart(self, part, amount=1):
        for i in range(amount):
            self.inventory.append(part(self.universe))

    def addPart(self, part, portIndex = 0):
        """ship.addPart(part) -> Sets the main part for this ship.
        Only used for the base part (usually a cockpit), other parts are added to parts."""
        part.parent = self
        part.direction = 0
        part.offset = Vec2d(0, 0)
        part.ship = self

        if part.image:
            part.image = colorShift(pygame.transform.rotate(part.baseImage, \
                        0), part.color)
        elif part.spritename:
            part.spritename['color'] = part.color
            part.spritename['direction'] = 0

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
        self.__dict__.update(Ship.baseBonuses)
        #recalculate stats:
        self.dps = 0
        self.partRollCall(self.ports[0].part) 
        minX, minY, maxX, maxY = 0, 0, 0, 0
        #TODO: ? make the center of the ship the center of mass instead of the 
        #center of the radii. 
        for part in self.parts:
            offset = part.offset
            part.reset()
            for port in part.parent.ports:
                if port.part == self:
                    offset = port.offset * self.spritename['zoom']

            # print part
            offset = part.offset #* Vec2d(part.sprite.get_height() / 2, part.sprite.get_width() / 2)
            if isinstance(part, Dummy): continue
            minX = min(offset[0] - part.radius, minX)
            minY = min(offset[1] - part.radius, minY)
            maxX = max(offset[0] + part.radius, maxX)
            maxY = max(offset[1] + part.radius, maxY)
            self.detectionscore += part.hp
        self.radius = max(maxX - minX, maxY - minY) / 2
        self.rect = Rect(0,0,self.radius*2,self.radius*2)

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

        size = int(self.radius * 2)
        self.baseImage = pygame.Surface((size, size), \
                    hardwareFlag | SRCALPHA).convert_alpha()
        self.greyImage = pygame.Surface((size, size), \
                    hardwareFlag | SRCALPHA).convert_alpha()
        # self.baseImage.set_colorkey(BLACK)
        if self.ports[0].part:
            self.ports[0].part.draw(self.baseImage)
            self.ports[0].part.draw(self.greyImage, grey=True)


    def partRollCall(self, part):
        """adds parts to self.parts recursively."""
        if part:
            self.parts.append(part)
            if isinstance(part, Engine):
                if part.direction == 180 or  part.direction == -180:
                    self.reverseEngines.append(part)
                    self.reverseThrust += part.exspeed * part.exmass
                if part.direction == 0 or part.direction == 360:
                    self.forwardEngines.append(part)
                    self.forwardThrust += part.exspeed * part.exmass
                if part.direction == 90 or part.direction == -270:
                    self.rightEngines.append(part)
                    self.rightThrust += part.exspeed * part.exmass
                if part.direction == 270 or part.direction == -90:
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
            gyro.turnLeft(angle,self.gyros.index(gyro))

    def turnRight(self, angle = None):
        """Turns cw using all gyros."""
        for gyro in self.gyros:
            gyro.turnRight(angle, self.gyros.index(gyro))

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
        for radar in self.radars:
            radar.targetNextShip()

    def targetPrefShip(self):
        for radar in self.radars:
            radar.targetPrefShip()

    def targetNextPlanet(self):
        for radar in self.radars:
            radar.targetNextPlanet()

    def targetPrefPlanet(self):
        for radar in self.radars:
            radar.targetPrefPlanet()

    def targetNextPart(self):
        for radar in self.radars:
            radar.targetNextPart()

    def targetPrefPart(self):
        for radar in self.radars:
            radar.targetPrefPart()

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
        
        resultList = []
        for radar in self.radars:
            resultList= list(set(radar.detected)|set(resultList))
        if self.attention > 0:
            self.attention -= 0.1 / self.universe.game.fps
        # actual updating:
        Floater.update(self)
        Controllable.update(self)
        
        #parts updating:
        if self.ports[0].part:
            self.ports[0].part.setFPS(self.universe.game.fps)
            self.ports[0].part.update()
        
        #active effects:
        for effect in self.effects:
            effect(self)
        for effect in self.partEffects:
            effect(self)

        if self.atgateway and dist2(self, self.atgateway) > (self.atgateway.radius * 1.1) ** 2:
            self.atgateway = False
        if self.landed and dist2(self, self.landed) > (self.landed.radius * 1.1) ** 2:
            self.landed = False

        if self.pos.get_distance(Vec2d(0,0)) > self.universe.curSystem.boundrad:
            self.overedge = True
        else:
            self.overedge = False

        if self.pos.get_distance(Vec2d(0,0)) > self.universe.curSystem.edgerad:
            posdifflist = self.universe.curSystem.getNeighborposdiff()
            
            posdiff = (self.pos - self.universe.curSystem.star.pos)
            nearest = sorted(posdifflist, key=lambda diff: diff[1].get_distance(posdiff))[-1]

            if len(posdifflist) == 1 and (nearest[1].normalized()*10 + self.delta.normalized()*10).get_length() > 10:
                self.direction = -nearest[1].get_angle()-90
                self.delta = -self.delta.rotated(nearest[1].get_angle()+90)
            newpos =  Vec2d(0,0).rotatedd(self.delta.get_angle()+180, nearest[0].edgerad-50)

            
            nearest[0].player = self
            nearest[0].floaters.add(self)
            nearest[0].ships.add(self)
            self.universe.curSystem.player = None
            self.universe.curSystem.ships.remove(self)
            self.universe.curSystem.floaters.remove(self)
            self.universe.curSystem = nearest[0]
            self.pos = newpos
            for camera in self.universe.cameras:
                camera.setPos(self.pos)

            self.overedge = False



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

        self.image = pygame.transform.rotate(self.baseImage, \
                                    -self.direction).convert_alpha()

        if self.spritename:
            self.spritename['direction'] = -self.direction

        
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


                            
        #draw to input surface:
        pos[0] += - imageOffset[0] - self.radius
        pos[1] += - imageOffset[1] - self.radius
        surface.blit(buffer, pos) 
        
    def takeDamage(self, damage, other):
        self.attention += 5
        self.hp = max(self.hp - damage, 0)
        if isinstance(other, Bullet) and other.ship == self.universe.player:
            self.universe.player.xpDamage(self, damage)

    def kill(self):
        """play explosion effect than call Floater.kill(self)"""
        self.soundsys.play(self.explosionSound)
        # setVolume(explodeSound.play(), self, self.universe.player)
        for part in self.inventory:
            part.scatter(self)
        Floater.kill(self)

    def planetCollision(self, planet):
        shipangle = (planet.pos - self.pos).get_angle()
        planetangle = (self.pos - planet.pos).get_angle()

        speed = (self.delta-planet.delta).get_length()
        if speed > planet.landing_speed:
            if planet.damage.has_key(self):
                damage = planet.damage[self]
            else:
                self.soundsys.play(self.crashSound)
                #set damage based on incoming speed and mass.
                damage = speed * self.mass * planet.planet_damage
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
            if self == planet.starSystem.universe.player and not self.landed:
                #planet.game.pause = True
                self.landed = planet
                self.universe.game.menu.parts.reset()
            self.delta.x, self.delta.y = planet.delta.x, planet.delta.y

    def gatewayCollision(self, gateway):
        self.atgateway = gateway
        
    def freepartCollision(self, part):
        if part.pickuptimeout <= 0:
            part.direction = 0
            part.image = colorShift(pygame.transform.rotate(part.baseImage, part.direction), part.color).convert_alpha()
            self.inventory.append(part)
            part.kill()
            if self.universe.player == self:
                self.universe.game.menu.parts.inventoryPanel.reset() #TODO: make not suck


class Player(Ship):

    def __init__(self, game, pos, delta, direction = 270, color = (255, 255, 255), name = ("Shippy","mcShipperson"), partlimit=8):
        Ship.__init__(self, game, pos, delta, direction, color, name, partlimit)
        self.skills = [Modularity(self), Agility(self), Composure(self)]
        self.xp = 0
        self.developmentPoints = 12
        self.surespawn = True

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
        if self.xp >= self.next():
            self.level += 1
            self.developmentPoints += 1
            self.xp = 0
        Ship.update(self)
    
    def next(self):
        return 1.1 ** self.level * 10

    def kill(self):
        for part in self.parts:
            part.enabled = False
        Ship.kill(self)


