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
import plot
# import yaml
# import yamlpygame

FPS = 300

class Game:
	"""Game(resolution = None, fullscreen = False)
	-> new game instance. Multiple game instances
	are probably a bad idea."""
	menu = None
	def __init__(self, screen):
		self.pause = False
		self.debug = False
		self.pause = False
		self.fps = FPS
		self.screen = screen
		self.top_left = 0, 0
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.mouseControl = True
		self.timer = 0
		self.systems = []
		self.triggers = []
		#messenger, with controls as first message:
		self.messenger = Messenger(self)
		
		#key polling:
		self.keys = []
		for _i in range (322):
			self.keys.append(False)
		#mouse is [pos, button1, button2, button3,..., button6].
		#new Apple mice think they have 6 buttons.
		self.mouse = [(0, 0), 0, 0, 0, 0, 0, 0]
		#pygame setup:
		self.clock = pygame.time.Clock()
		
		self.hud = HUD(self) # the heads up display
				
	def run(self):
		"""Runs the game."""
		
		self.running = True
		while self.running:
			# game setup:
			intro = IntroMenu(self, Rect((self.width - 800) / 2,
										(self.height - 600) / 2,
										800, 600))
			self.messenger.empty()
			while self.running and intro.running:
				#event polling:
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
			self.player = playerShip(self, 0,0, script = self.playerScript,
							color = self.playerColor, type = self.playerType)
			self.curSystem = SolarA1(self, self.player)
			self.systems = [self.curSystem]
			self.curSystem.add(self.player)
			
			self.menu = Menu(self, Rect((self.width - 800) / 2,
										(self.height - 600) / 2,
										800, 600), self.player)
			for x in range(10):
				self.clock.tick()
			
			self.triggers = plot.newGameTriggers(self)
				
			#The in-round loop (while player is alive):
			while self.running and self.curSystem.ships.has(self.player):
				#event polling:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.running = 0
					elif event.type == pygame.MOUSEBUTTONDOWN:
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
						
				#game-level key input:
				if self.keys[K_DELETE % 322]:
					self.keys[K_DELETE % 322] = False
					self.player.kill() #suicide
				if self.keys[K_RETURN % 322]:
					self.pause = not self.pause #pause/menu
					self.keys[K_RETURN % 322] = False
					if self.pause:
						self.menu.reset()
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
					
				#unpaused:
				if not self.pause:
					#update action:
					for trigger in self.triggers:
						trigger.update()
					self.curSystem.update()
					self.top_left = self.player.x - self.width / 2, \
							self.player.y - self.height / 2
					self.messenger.update()
							
				#draw the layers:
				self.screen.fill((0, 0, 0, 0))
				self.curSystem.draw(self.screen, self.top_left)
				self.hud.draw(self.screen, self.player)
				self.messenger.draw(self.screen)
				
				#paused:
				if self.pause:
					self.menu.update()
					self.menu.draw(self.screen)
					
				#frame maintainance:
				pygame.display.flip()
				self.clock.tick(FPS)#aim for FPS but adjust vars for self.fps.
				self.fps = max(1, int(self.clock.get_fps()))
				self.timer += 1. / self.fps
			#end round loop (until gameover)
		#end game loop