#races.py


class Race:
	planets = []
	parts = []
	adjectives = []
	playerRepute = 0
	playerCredits = 0
	enemies = []
	allies = []
	ships = []
	shipScripts = []
	script = None
	
	def __init__(self, game, name, color = (255,0,0)):
		self.game = game
		self.name = name
		self.color = color
		
	def update(self):
		systems = []
		for system in self.game.systems:
			ownAll = True
			for planet in system:
				if planet.race = self:
					systems.append(system)
				else:
					ownAll = False
				
			
			
			
			
			