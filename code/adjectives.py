#adjectives.py
from parts import *
from partCatalog import *
PARTS = [LeftCannon, RightCannon, Engine, Gyro, Generator, Battery, Shield,
		LeftLaser, RightLaser, MissileLauncher, MachineGun, FighterShield, 
		LeftFlakCannon, RightFlakCannon]
		
def randItem(game, level = 1):
	roll = randint(0, len(PARTS) -1)
	if roll == rand() * level / 2 < .8:
		return None
	part = PARTS[roll](game)
	return addAdjective(part, level)
	
def addAdjective(part, level = 1):
	choice = adjectives[randint(0,len(adjectives) - 1)]
	if choice.level <= level:
		for type in choice.types:
			if isinstance(part, type):
				adj = choice()
				adj.effect(part)
				part.name = choice.__name__ + ' ' + part.name
				part.adjectives.append(adj)
				return part
	#TODO: make a better data structure for these.
	#for now, if this adjective doesn't fit, pick another at random.
	return addAdjective(part, level)
	
ENERGY_USING = [Gun, Engine, Gyro, Shield]

class Adjective:
	level = 1
	types = [Gun, Engine, Gyro, Battery, Generator, Cockpit, Shield]
	def effect(self, part):
		pass
		
class Sturdy(Adjective):
	"""HP * 1.6"""
	def effect(self, part):
		part.maxhp *= 1.6
		part.hp *= 1.6

class Durable(Adjective):
	"""HP * 1.2"""
	def effect(self, part):
		part.maxhp *= 1.2
		part.hp *= 1.2

class Solid(Adjective):
	"""HP * 2"""
	def effect(self, part):
		part.maxhp *= 2
		part.hp *= 2
		
class Fragile(Adjective):
	"""HP * .4"""
	level = 0
	def effect(self, part):
		part.maxhp *= .4
		part.hp *= .4
		
class Titanium(Adjective):
	"""HP * 1.5, mass * 1.2"""
	def effect(self, part):
		part.maxhp *= 1.5
		part.hp *= 1.5
		part.mass *= 1.2

class Carbonfiber(Adjective):
	"""HP * .4, mass * .4"""
	def effect(self, part):
		part.maxhp *= .4
		part.hp *= .4
		part.mass *= .4

class Nanosteel(Adjective):
	"""HP * .8, mass * .6"""
	def effect(self, part):
		part.maxhp *= .8
		part.hp *= .8
		part.mass *= .6

class Nanosilk(Adjective):
	"""mass * .5"""
	def effect(self, part):
		part.mass *= .5

class Doublesilk(Adjective):
	"""HP * 2"""
	def effect(self, part):
		part.maxhp *= 2
		part.hp *= 2
		
class Plated(Adjective):
	"""HP + 10, Mass + 6"""
	def effect(self, part):
		part.maxhp += 10
		part.hp += 10
		part.mass += 6
		
class Reinforced(Adjective):
	"""HP + 15, Mass + 9"""
	def effect(self, part):
		part.maxhp += 15
		part.hp += 15
		part.mass += 9
		
class Armored(Adjective):
	"""HP + 20, Mass + 12"""
	def effect(self, part):
		part.maxhp += 20
		part.hp += 20
		part.mass += 12
		
class _50_Megawatt(Adjective):
	"""Damage * .5, Cost * .5"""
	types = [Cannon]
	def effect(self, part):
		part.damage *= .5
		part.energyCost *= .5

class _200_Megawatt(Adjective):
	"""Damage * 2, Cost * 2"""
	types = [Cannon]
	def effect(self, part):
		part.damage *= 2
		part.energyCost *= 2
		
class _300_Megawatt(Adjective):
	"""Damage * 3, Cost * 3"""
	types = [Cannon]
	def effect(self, part):
		part.damage *= 3
		part.energyCost *= 3
		
class _400_Megawatt(Adjective):
	"""Damage * 4, Cost * 4"""
	types = [Cannon]
	def effect(self, part):
		part.damage *= 4
		part.energyCost *= 4

class Nitrogen_Cooled(Adjective):
	"""Rate * 1.3, Cost + 3"""
	types = [Cannon]
	def effect(self, part):
		part.reloadTime /= 1.3
		part.energyCost += 3

class Helium_Cooled(Adjective):
	"""Rate * 1.5, Cost + 5"""
	types = [Cannon]
	def effect(self, part):
		part.reloadTime /= 1.5
		part.energyCost += 5

class Quantum_Accelerated(Adjective):
	"""Rate * 2., Cost + 9"""
	types = [Cannon]
	def effect(self, part):
		part.reloadTime /= 2
		part.energyCost += 9
		
class Hydrogen_Fusion(Adjective):
	"""Rate * 1.5"""
	types = [Generator]
	def effect(self, part):
		part.rate *= 1.5
		
class Dilithium(Adjective):
	"""Rate * 2"""
	types = [Generator]
	def effect(self, part):
		part.rate *= 2
		
class Antimatter(Adjective):
	"""Rate * 4"""
	types = [Generator]
	def effect(self, part):
		part.rate *= 4
		
class Advanced_Chemical(Adjective):
	"""Capacity * 1.2"""
	types = [Battery]
	def effect(self, part):
		part.capacity *= 1.2
		
class Magnetic(Adjective):
	"""Capacity * 1.6"""
	types = [Battery]
	def effect(self, part):
		part.capacity *= 1.6
		
class Kinetic(Adjective):
	"""Capacity * 2"""
	types = [Battery]
	def effect(self, part):
		part.capacity *= 2
		
class Alpha_Decay(Adjective):
	"""Capacity * 2.5"""
	types = [Battery]
	def effect(self, part):
		part.capacity *= 2.5
		
class Nuclear(Adjective):
	"""Capacity * 3"""
	types = [Battery]
	def effect(self, part):
		part.capacity *= 3
		
class Stored_Antimatter(Adjective):
	"""Capacity * 4"""
	types = [Battery]
	def effect(self, part):
		part.capacity *= 4
		
class Delicate(Adjective):
	"""Cost * .8, HP * .6"""
	types = ENERGY_USING
	def effect(self, part):
		part.energyCost *= .8
		part.maxhp *= .6
		part.hp *= .6
		
class Efficient(Adjective):
	"""Cost *= .6"""
	types = ENERGY_USING
	def effect(self, part):
		part.energyCost *= .6
		
class Miserly(Adjective):
	"""Cost *= .4"""
	types = ENERGY_USING
	def effect(self, part):
		part.energyCost *= .4
		
class Leaky(Adjective):
	"""-.5 energy per second"""
	level = 0
	types = ENERGY_USING
	def effect(self, part):
		from effects import leak
		part.shipEffects.append(leak)
		
class Inefficient(Adjective):
	"""Cost *= 2.5"""
	level = 0
	types = ENERGY_USING
	def effect(self, part):
		part.energyCost *= 2.5
		
class Obsolete(Adjective):
	"""Cost *= 2, Mass *= 2"""
	level = 0
	types = ENERGY_USING
	def effect(self, part):
		part.energyCost *= 2
		part.mass *= 2
		
class Heavy(Adjective):
	"""Mass *= 2.5"""
	level = 0
	types = ENERGY_USING
	def effect(self, part):
		part.mass *= 2.5
		
class Damaged(Adjective):
	"""Starting HP / 2"""
	level = 0
	def effect(self, part):
		part.hp = part.hp / 2
	

adjectives = (Sturdy, Durable, Solid, Fragile, 
 Titanium, Carbonfiber, Nanosteel, 
 Nanosilk, Doublesilk, Plated, Reinforced, 
 Armored, _50_Megawatt, _200_Megawatt, _300_Megawatt, 
 _400_Megawatt, Nitrogen_Cooled, Helium_Cooled, 
 Quantum_Accelerated, Hydrogen_Fusion, Dilithium,
 Antimatter, Advanced_Chemical, Magnetic, 
 Kinetic, Alpha_Decay, Nuclear, Stored_Antimatter,
 Delicate, Efficient, Miserly, Leaky, Inefficient, 
 Obsolete, Damaged, Heavy)
