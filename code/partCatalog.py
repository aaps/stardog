#partCatalogue.py

from parts import *

class LeftFlakCannon(FlakCannon, FlippablePart): 
    def __init__(self, universe):
        FlakCannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.spritename = {'name':"res/parts/leftflak.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootPoint = 0, - 20;
        self.shootDir = 270
        self.name = "Left Flak Cannon"  

class MachineGun(Cannon):
    def __init__(self, universe):
        Cannon.__init__(self, universe)
        self.spritename = {'name':"res/parts/machinegun.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None

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
        FlakCannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.spritename = {'name':"res/parts/rightflak.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootPoint = 0, 20
        self.shootDir = 90
        self.name = "Right Flak Cannon" 

class LeftLaser(Laser, FlippablePart):
    def __init__(self, universe):
        Laser.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.spritename = {'name':"res/parts/leftlaser.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootPoint = 0, - 15
        self.shootDir = 270
        self.name = "Left Laser"    

class RightLaser(Laser, FlippablePart):
    def __init__(self, universe):
        Laser.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.spritename = {'name':"res/parts/rightlaser.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootPoint = 0, 15
        self.shootDir = 90
        self.name = "Right Laser"

class LeftCannon(Cannon, FlippablePart):
    def __init__(self, universe):
        Cannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.spritename = {'name':"res/parts/leftgun.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootPoint = 0, - 30
        self.shootDir = 270
        self.name = "Left Cannon"

class RightCannon(Cannon, FlippablePart):
    def __init__(self, universe):
        Cannon.__init__(self, universe)
        FlippablePart.__init__(self, universe)
        self.spritename = {'name':"res/parts/rightgun.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootPoint = 0, 30
        self.shootDir = 90
        self.name = "Right Cannon"      

class StrafebatCannon(Cannon):
    def __init__(self, universe):
        Cannon.__init__(self, universe)
        self.spritename = {'name':"res/parts/strafebatgun.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.shootDir = 180
        self.shootPoint = -20, 0
        self.damage = .5
        self.energyCost = 1
        self.name = "Fore Gun"  

class FighterShield(Shield):
    def __init__(self, universe):
        # self.baseImage =  loadImage("res/parts/fightershield.png")
        Shield.__init__(self, universe)
        self.spritename = {'name':"res/parts/fightershield.png", 'pos':(0,0), 'color':(100,100,100), 'direction':None,'zoom':None}
        self.image=None
        
        self.ports = []
        self.mass = 4
        self.shieldhp = .6
        self.shieldRegen = .1
        self.energyCost = .5
        self.name = 'Fighter Shield'
