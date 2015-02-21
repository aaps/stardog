#gameserver.py

from server import *
from universe import *
from SoundSystem import *

class GameServer(object):

	def __init__(self, screen):
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.player = None
		self.musicSystem = DummyMusicSystem('res/sound/ambientMusic/')
		self.soundSystem = DummySoundSystem('res/sound/sfxSounds/')
		self.universe = Universe(self)
		self.screen = screen
		self.server = Server(self.universe)
		self.running = True
		self.keys = [False]*322
		self.fps = 25

		theone = SolarA1(self.universe, "theone", Vec2d(1,100))
		self.universe.addStarSystem(theone)
		self.universe.setCurrentStarSystem("theone")
		self.clock = pygame.time.Clock()


	def run(self):

		while self.running:
			self.clock.tick()
			self.universe.update()
			self.server.update()


