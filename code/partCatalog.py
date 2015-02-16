#partCatalogue
from parts import *

class LeftFlakCannon(FlakCannon, FlippablePart): 
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/leftflak.png")
        FlakCannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.ports = []
        self.shootPoint = 0, - 20;
        self.shootDir = 270
        self.name = "Left Flak Cannon"  

class MachineGun(Cannon):
    def __init__(self, universe):
        self.baseImage = loadImage('res/parts/machinegun.png')
        Cannon.__init__(self, universe)
        self.ports = []
        self.damage = .25
        self.reloadTime = 0.7
        self.energyCost = .35*8
        self.shootDir = 180
        self.shootPoint = -14, 0
        self.range = 1
        self.speed = 600
        self.name = 'Machine Gun'   

class RightFlakCannon(FlakCannon, FlippablePart):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/rightflak.png")
        FlakCannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.ports = []
        self.shootPoint = 0, 20
        self.shootDir = 90
        self.name = "Right Flak Cannon" 

class LeftLaser(Laser, FlippablePart):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/leftlaser.png")
        Laser.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.ports = []
        self.shootPoint = 0, - 15
        self.shootDir = 270
        self.name = "Left Laser"    

class RightLaser(Laser, FlippablePart):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/rightlaser.png")
        Laser.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.ports = []
        self.shootPoint = 0, 15
        self.shootDir = 90
        self.name = "Right Laser"

class LeftCannon(Cannon, FlippablePart):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/leftgun.png")
        Cannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.ports = []
        self.shootPoint = 0, - 30
        self.shootDir = 270
        self.name = "Left Cannon"

class RightCannon(Cannon, FlippablePart):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/rightgun.png")
        Cannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.ports = []
        self.shootPoint = 0, 30
        self.shootDir = 90
        self.name = "Right Cannon"      

class StrafebatCannon(Cannon):
    def __init__(self, universe):
        self.baseImage = loadImage("res/parts/strafebatgun.png")
        Cannon.__init__(self, universe)
        self.ports = []
        self.shootDir = 180
        self.shootPoint = -20, 0
        self.damage = .5
        self.energyCost = 1
        self.name = "Fore Gun"  

class FighterShield(Shield):
    def __init__(self, universe):
        self.baseImage =  loadImage("res/parts/fightershield.png")
        Shield.__init__(self, universe)
        self.ports = []
        self.mass = 4
        self.shieldhp = .6
        self.shieldRegen = .1
        self.energyCost = .5
        self.name = 'Fighter Shield'

generalSellable = [LeftFlakCannon, MachineGun, LeftLaser, LeftCannon, 
    StrafebatCannon, FighterShield, MissileLauncher, Engine, Generator,
    Gyro, Battery, Shield]
