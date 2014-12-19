#game.py

from utils import *
from menus import *
from scripts import *
from solarSystem import *
from gui import *
from planet import *
from spaceship import *
from strafebat import *
from dialogs import *
from camera import *
import plot
from vec2d import Vec2d
try:
	from swampy.Lumpy import Lumpy
except ImportError:
	print "no way to build a class diagram now!! "
#command parsing
from commandParse import *

FPS = 300

class Game:
	"""Game(resolution = None, fullscreen = False)
	-> new game instance. Multiple game instances
	are probably a bad idea."""
	menu = None
	def __init__(self, screen):
		self.pause = False
		self.console = False
		self.debug = False
		self.player = None
		self.fps = FPS
		self.screen = screen
		self.top_left = 0, 0
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.mouseControl = True
		self.timer = 0
		self.systems = []
		self.triggers = []
		self.camera = Camera(self)
		#messenger, with controls as first message:
		self.messenger = Messenger(self, 1)
		self.camera.layerAdd(self.messenger)
		self.camera.layerAdd(MiniInfo(self, 1))
		# self.miniinfo = 
		
		#key polling:
		self.keys = [False]*322
		#mouse is [pos, button1, button2, button3,..., button6].
		#new Apple mice think they have 6 buttons.
		self.mouse = [(0, 0), 0, 0, 0, 0, 0, 0]
		#pygame setup:
		self.clock = pygame.time.Clock()
		
		# self.hud =  # the heads up display
		self.camera.layerAdd(HUD(self, 1))
		
		#create a chatconsole for text input capabilities
		self.chatconsole = ChatConsole(self, Rect(int(self.width/ 8), self.height-50, self.width - int(self.width/ 8) , 50))
		#create a parser that parses chatconsole input for command and such.
		self.commandParse = CommandParse(self, self.chatconsole)
	def run(self):
		"""Runs the game."""
		
		self.running = True
		while self.running:
			# game setup:
			intro = IntroMenu(self, Rect((self.width - 800) / 2,
										(self.height - 600) / 2,
										800,600))
			self.messenger.empty()
			while self.running and intro.running:
			# 	#event polling:
				pygame.event.pump()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						return
					intro.handleEvent(event)
				intro.update()
				self.screen.fill((0, 0, 0, 0))
				intro.draw(self.screen)
				pygame.display.flip()
			#setup initial state:
			self.playerScript = InputScript(self)
			self.player = playerShip(self, Vec2d(0,0),Vec2d(0,0), script = self.playerScript,
							color = self.playerColor, type = self.playerType)
			self.curSystem = SolarA1(self)
			self.camera.setBG(self.curSystem.bg)
			self.nextsystem = SolarB2(self)
			# self.systems = [self.curSystem]
			self.curSystem.add(self.player)
			
			self.menu = Menu(self, Rect((self.width - 800) / 2,	(self.height - 600) / 2, 800, 600))
			for x in range(10):
				self.clock.tick()
			
			self.triggers = plot.newGameTriggers(self)
				
			#The in-round loop (while player is alive):
			while self.running and self.curSystem.ships.has(self.player):
				#event polling:
				pygame.event.pump()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.running = 0
					if not self.pause and not self.console:
						if event.type == pygame.MOUSEBUTTONDOWN:
							self.mouse[event.button] = 1
							self.mouse[0] = event.pos
						elif event.type == pygame.MOUSEBUTTONUP:
							self.mouse[event.button] = 0
							self.mouse[0] = event.pos
						elif event.type == pygame.MOUSEMOTION:
							self.mouse[0] = event.pos
						elif event.type == pygame.KEYDOWN:
							self.keys[event.key % 322] = 1
						elif event.type == pygame.KEYUP:
							self.keys[event.key % 322] = 0
					if self.pause:
						self.menu.handleEvent(event)
					if self.console:
						self.chatconsole.handleEvent(event)


				#game-level key input:
				if self.keys[K_DELETE % 322]:
					self.keys[K_DELETE % 322] = False
					self.player.kill() #suicide
				if self.keys[K_RETURN % 322]:
					self.pause = True #pause/menu
					self.keys[K_RETURN % 322] = False
					if self.pause:
						self.menu.reset()
				if self.keys[K_6 % 322]:
					self.console = True
					self.keys[K_6 % 322] = False
					if self.console:
						self.chatconsole.reset()
				self.debug = False
				if self.keys[K_BACKSPACE % 322]:
					self.debug = True #print debug information
					self.keys[K_BACKSPACE % 322] = False
					print "Debug:"
				#ctrl+q or alt+F4 quit:
				if self.keys[K_LALT % 322] and self.keys[K_F4 % 322] \
				or self.keys[K_RALT % 322] and self.keys[K_F4 % 322] \
				or self.keys[K_LCTRL % 322] and self.keys[K_q % 322] \
				or self.keys[K_RCTRL % 322] and self.keys[K_q % 322]:
					self.running = False
					

				for trigger in self.triggers:
					trigger.update()
				self.curSystem.update()

				self.camera.update()
							
				#draw the layers:
				self.screen.fill((0, 0, 0, 0))

				self.camera.draw(self.screen)


				#paused:
				if self.pause:
					self.menu.update()
					self.menu.draw(self.screen)

				if self.console:
					self.chatconsole.update()
					self.chatconsole.draw(self.screen)
				
				self.commandParse.update()
				
				#frame maintainance:
				pygame.display.flip()
				self.clock.tick(FPS)#aim for FPS but adjust vars for self.fps.
				self.fps = max(1, int(self.clock.get_fps()))
				self.timer += 1. / self.fps
			#end round loop (until gameover)
		#end game loop

# lumpy.class_diagram()
