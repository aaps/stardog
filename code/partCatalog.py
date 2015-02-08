#partCatalogue
from parts import *

class LeftFlakCannon(FlakCannon, FlippablePart): 
	baseImage = loadImage("res/parts/leftflak.png"); shootPoint = 0, - 20;
	shootDir = 270; name = "Left Flak Cannon"	
class MachineGun(Cannon):
	baseImage = loadImage('res/parts/machinegun.png')
	damage = .25;reloadTime = .1;energyCost = .35;shootDir = 180
	shootPoint = -14, 0;range = 1;speed = 600;name = 'Machine Gun'	
class RightFlakCannon(FlakCannon, FlippablePart):
	baseImage = loadImage("res/parts/rightflak.png")
	shootPoint = 0, 20;	shootDir = 90;	name = "Right Flak Cannon"	
class LeftLaser(Laser, FlippablePart):
	baseImage = loadImage("res/parts/leftlaser.png")
	shootPoint = 0, - 15; shootDir = 270;	name = "Left Laser"	
class RightLaser(Laser, FlippablePart):
	baseImage = loadImage("res/parts/rightlaser.png")
	shootPoint = 0, 15;	shootDir = 90;	name = "Right Laser"
class LeftCannon(Cannon, FlippablePart):
	baseImage = loadImage("res/parts/leftgun.png")
	shootPoint = 0, - 30; shootDir = 270;name = "Left Cannon"
class RightCannon(Cannon, FlippablePart):
	baseImage = loadImage("res/parts/rightgun.png")
	shootPoint = 0, 30;	shootDir = 90;	name = "Right Cannon"		
class StrafebatCannon(Cannon):
	baseImage = loadImage("res/parts/strafebatgun.png")
	shootDir = 180;	shootPoint = -20, 0;	damage = .5
	energyCost = 1;	name = "Fore Gun";	
class FighterShield(Shield):
	baseImage =  loadImage("res/parts/fightershield.png")
	mass = 4;	shieldhp = .6;	shieldRegen = .1;	energyCost = .5
	name = 'Fighter Shield'

generalSellable = [LeftFlakCannon, MachineGun, LeftLaser, LeftCannon, 
	StrafebatCannon, FighterShield, MissileLauncher, Engine, Generator,
	Gyro, Battery, Shield]
