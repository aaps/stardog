from solarSystem import *
from planet import *
from gui import *
from spaceship import *
from dialogs import *
from spaceship import *
from floaters import *

class View:

	def __init__(self, game,screen):
		self.game = game
		self.bg = BG(self.game)
		self.surface = screen
		self.onScreen = []
		self.imagenames = {'shot':'shot.bmp','missile':'missile.bmp','default':'default.bmp','defaultselected':'defaultselected.bmp' }
		self.images = {}
		self.respath = 'res/'
		for name in self.imagenames:
			self.images[name] =  loadImage(self.respath + self.imagenames[name])

	

	def getAllOnScreen(self,starsystem, offset):
		self.onScreen = []
		offset = (self.game.player.x - self.game.width / 2, 
				self.game.player.y - self.game.height / 2)
		for floater in starsystem.floaters:
			r = floater.radius
			if (r + floater.x > offset[0] \
				and floater.x - r < offset[0] + self.game.width)\
			and (r + floater.y > offset[1] \
				and floater.y - r < offset[1] + self.game.height):
					self.onScreen.append(floater)


	def starSystemDraw(self, starsystem, offset):
		self.getAllOnScreen(starsystem, offset)
		
		self.bg.draw(self.surface, self.game.player)
		for floater in self.onScreen:
				self.floaterDraw(floater, offset)
				# floater.draw(self.surface, offset)

	def floaterDraw(self, floater, offset = (0,0)):
		"""Blits this floater onto the surface. """
		pos = floater.x - floater.image.get_width()  / 2 - offset[0], \
			  floater.y - floater.image.get_height() / 2 - offset[1]
		self.surface.blit(self.images['default'], pos)

	def shipDraw(self, floater, offset = (0,0)):
		pass


	def explotionDraw(self, floater, offset = (0,0)):
		pass

	def partDraw(self, floater, offset = (0,0)):
		pass

