from solarSystem import *
from planet import *
# from gui import *
from spaceship import *
from menuElements import *
from spaceship import *
from floaters import *

class View:

	def __init__(self, game,screen):
		self.game = game
		self.bg = BG(self.game)
		self.surface = screen
		self.onScreen = []
		self.imagenames = {'shot':'res/shot.bmp','missile':'res/missile.bmp','default':'res/default.bmp','defaultselected':'res/defaultselected.bmp','fighter':'res/parts/fighter.bmp','engine':'res/parts/engine.bmp','machinegun':'res/parts/machine_gun.bmp','fightershield':'res/parts/fighter_shield.bmp' }
		self.images = {}
		self.mutatedimages = {}
		for name in self.imagenames:
			self.images[name] =  loadImage(self.imagenames[name])
		self.mutatedimages['default'] = self.images['default']


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

	def add(self,floater):
			if hasattr(floater, 'image'):

				self.mutatedimages[floater.image] = pygame.transform.rotate(self.images[floater.image], -floater.dir).convert()


	def floaterDraw(self, floater, offset = (0,0)):
		"""Blits this floater onto the surface. """
		pos = floater.x - floater.rect.width  / 2 - offset[0], floater.y - floater.rect.height / 2 - offset[1]
		if hasattr(floater, 'image'):
			self.surface.blit(self.mutatedimages[floater.image], pos)
		if hasattr(floater, 'parts') and len(floater.parts) > 0:
			for part in floater.parts:
				self.partDraw(part, offset)


	def partDraw(self, part, offset = (0,0)):
		pos = part.x - part.rect.width  / 2 - offset[0], part.y - part.rect.height / 2 - offset[1]
		self.surface.blit(self.mutatedimages[part.image], pos)


