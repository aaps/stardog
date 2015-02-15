#gameserver.py

from server import *
from universe import *

class Server(object):

	def __init__(self, screen):
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.player = None
		self.universe = Universe(self)
		self.screen = screen
		self.server = GameServer(self.universe)
		self.running = True
		self.fps = 25
		theone = SolarA1(self.universe, "theone", Vec2d(1,100))
		self.universe.addStarSystem(theone)
		self.clock = pygame.time.Clock()


	def run(self):

		while self.running:
			self.clock.tick()
			self.universe.update()
			self.server.update()

