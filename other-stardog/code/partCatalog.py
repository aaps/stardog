#partCatalog.py
from parts import *

class LeftFlakCannon(FlakCannon, FlippablePart):
	baseImage = loadImage("res/parts/leftflak.bmp"); shootPoint = 0, - 6;
	shootDir = 270; name = "Left Flak Cannon"
class MachineGun(Cannon):
	baseImage = loadImage('res/parts/machine gun.bmp')
	damage = .25;reloadTime = .1;energyCost = .35;shootDir = 180
	shootPoint = -4, 0;range = 1;speed = 600;name = 'Machine Gun'; value = 1.5
class RightFlakCannon(FlakCannon, FlippablePart):
	baseImage = loadImage("res/parts/rightflak.bmp")
	shootPoint = 0, 6;	shootDir = 90;	name = "Right Flak Cannon"
class LeftLaser(Laser, FlippablePart):
	baseImage = loadImage("res/parts/leftlaser" + ext)
	shootPoint = 0, - 6; shootDir = 270;	name = "Left Laser"	; value = 1.5
class RightLaser(Laser, FlippablePart):
	baseImage = loadImage("res/parts/rightlaser" + ext)
	shootPoint = 0, 6;	shootDir = 90;	name = "Right Laser"; value = 1.5
class LeftCannon(Cannon, FlippablePart):
	baseImage = loadImage("res/parts/leftgun" + ext)
	shootPoint = 0, - 6; shootDir = 270;name = "Left Cannon"
class RightCannon(Cannon, FlippablePart):
	baseImage = loadImage("res/parts/rightgun" + ext)
	shootPoint = 0, 6;	shootDir = 90;	name = "Right Cannon"
class StrafebatCannon(Cannon):
	baseImage = loadImage("res/parts/strafebatgun" + ext)
	shootDir = 180;	shootPoint = -20, 0;	damage = .5
	energyCost = 1;	name = "Fore Gun";	value = .5
class FighterShield(Shield):
	baseImage =  loadImage("res/parts/fighter shield.bmp")
	mass = 4;	shieldhp = 1;	shieldRegen = .1;	energyCost = .5
	name = 'Fighter Shield';	value = 1.4
class EmergencyEngine(Engine):
	name = "Emergency Engine";	force = 2000;	thrusting = False
	specImpulse = 8000; energyCost = 2.5; value = .1; hp = 3
class TakeOffEngine(Engine):
	name = "Take-Off Engine";	force = 30000;	thrusting = False
	specImpulse = 5000; energyCost = 5; value = .8; hp = 3

generalSellable = [LeftFlakCannon, MachineGun, LeftLaser, LeftCannon,
	StrafebatCannon, FighterShield, MissileLauncher, Engine, Generator,
	Gyro, Battery, Shield, Tank]
