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
		self.imagenames = {'shot':'res/shot.bmp','missile':'res/missile.bmp','default':'res/default.bmp','defaultselected':'res/defaultselected.bmp','fighter':'res/parts/fighter.bmp','engine':'res/parts/engine.bmp','machinegun':'res/parts/machine_gun.bmp','fightershield':'res/parts/fighter_shield.bmp','gyro':'res/parts/gyro.bmp','battery':'res/parts/battery.bmp','generator':'res/parts/generator.bmp','missilelauncher':'res/parts/missilelauncher.bmp','interceptor': 'res/parts/interceptor.bmp','rightgun':'res/parts/rightgun.bmp','rightlaser':'res/parts/rightlaser.bmp','rightflakcannon':'res/parts/rightflak.bmp','leftflakcannon':'res/parts/leftflak.bmp' }
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

				if floater.image in self.images:
					self.mutatedimages[floater.image] = pygame.transform.rotate(self.images[floater.image], -floater.dir).convert()
				else:
					self.mutatedimages[floater.image] = pygame.transform.rotate(self.images['default'], -floater.dir).convert()
					self.images[floater.image] = self.images['default']

				if isinstance(floater, Part):

					floater.setwithheight(self.images[floater.image].get_width()-1, self.images[floater.image].get_height()-1)

		

	def floaterDraw(self, floater, offset = (0,0)):
		"""Blits this floater onto the surface. """
		pos = floater.x - floater.rect.width  / 2 - offset[0], floater.y - floater.rect.height / 2 - offset[1]
		
		if hasattr(floater, 'parts') and len(floater.parts) > 0:
			for part in floater.parts:
				self.partDraw(part,floater, offset)
		elif hasattr(floater, 'image') and floater.image:
			self.surface.blit(self.mutatedimages[floater.image], pos)
		elif isinstance(floater, Explosion):
			self.explotionDraw(floater, offset)
		elif isinstance(floater, Planet):
			self.PlanetDraw(floater, offset)

		

	def partDraw(self, part, floater,offset = (0,0)):

		if hasattr(part,'dir'):
			self.mutatedimages[part.image] = pygame.transform.rotate(self.images[part.image], - part.dir - floater.dir).convert_alpha()
		pos = part.x - self.mutatedimages[part.image].get_width()  / 2 - offset[0], part.y - self.mutatedimages[part.image].get_height() / 2 - offset[1]
		self.surface.blit(colorShift(self.mutatedimages[part.image],part.color), pos)

	def explotionDraw(self, floater, offset = (0,0)):
		sur = pygame.Surface((250,250))
		sur.fill((0, 0, 0, 0))
		for circle in range(min(floater.radius / 4, 40)):
			color = (randint(100, 155), randint(000, 100), randint(0, 20), \
					randint(100, 255))
			radius = randint(floater.radius / 4, floater.radius / 2)
			r = randint(0, floater.radius - radius)
			theta = randint(0, 360)

			pos = (int(cos(theta) * r + floater.maxRadius ), \
					  int(sin(theta) * r + floater.maxRadius))
			
			pygame.draw.circle(sur, color, pos, radius)
		poss = floater.x - sur.get_width()  / 2 - offset[0], floater.y - sur.get_height() / 2 - offset[1]	
		sur.set_colorkey((0,0,0))
		self.surface.blit(sur, poss)

	def PlanetDraw(self, floater, offset = (0,0)):
		pos = int(floater.x - offset[0]), int(floater.y - offset[1])
		pygame.draw.circle(self.surface, floater.color, pos, int(floater.radius))


	def impactdraw(self):
		pass



