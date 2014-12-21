#skills.py

class Skill:
	"""A skill."""
	def __init__(self, ship, level = 0):
		self.level = level
		self.ship = ship
		
	def shipReset(self):
		pass
		
	def levelUp(self):
		self.level += 1
		self.ship.reset()
		
	def cost(self):
		return 1

class Modularity(Skill):
	("Increases the number of parts a ship can have before losing efficiency.\n"
	"levels 1-6: +1 part per level\n"
	"levels 7-12: +2 parts per level\n"
	"levels 12+: +3 parts per level")
	def __init__(self, ship, level = 0):
		Skill.__init__(self, ship, level)
		self.extraParts = 0
		if level > 12:
			self.extraParts += (level - 12) * 3
			level = 12
		if self.level > 6:
			self.extraParts += (self.level - 6) * 2
			self.level = 6
		self.extraParts += level
	
	def shipReset(self):
		self.ship.partLimit += self.extraParts
		
	def levelUp(self):
		self.level += 1
		self.extraParts += min(self.level // 6 + 1, 3)
		self.ship.reset()
		
class Agility(Skill):
	"""Increases a ship's torque, allowing it to turn faster.
	+5% torque per level"""
	def shipReset(self):
		self.ship.torqueBonus += .05 * self.level
		
class Organization(Skill):
	"""Reduces the efficiency penalty per extra part.
	penalty = .95^level"""
	def shipReset(self):
		self.ship.penalty *= .95 ** self.level
		
class Composure(Skill):
	"""Increases a ship's maximum shields.
	+5% maximum shield per level"""
	def shipReset(self):
		self.ship.shieldMaxBonus += .05 * self.level
		
class Efficiency(Skill):
	"""Gives a ship a bonus to efficiency for each part less than the limit it has.
	bonus = 1 - .95^level"""
	def shipReset(self):
		self.ship.bonus = 1 - .95 ** self.level
		
class Speed(Skill):
	"""Increases a ship's thrust, allowing it to accelerate faster.
	+5% thrust per level"""
	def shipReset(self):
		self.ship.thrustBonus += .05 * self.level
		
		
		
		
		
		
		
		
		
		
		