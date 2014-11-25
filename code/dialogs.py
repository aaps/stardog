#dialogs.py
from collections import deque

from utils import *
from menuElements import *

squareWidth = 80
squareSpacing = squareWidth + 10


class IntroMenu(TopLevelPanel):
	color = (100, 100, 255, 250)
	def __init__(self, game, rect):
		TopLevelPanel.__init__(self, rect)
		self.game = game
		self.running = True
		self.colorChoose()
		
	def colorChoose(self):
		self.panels = []
		self.addPanel(Label(Rect(100,30,200,20), \
				"Choose a color:", color = (250,250,250),\
				font = BIG_FONT))
		for x in range((self.rect.width - 100) / (squareSpacing)):
			for y in range((self.rect.height - 120) / (squareSpacing)):
				self.addPanel(ColorButton(self, \
						Rect(x * squareSpacing + 50, y * squareSpacing + 70,\
						squareWidth, squareWidth),\
						(randint(0,255),randint(0,255),randint(0,255))))
						
	def typeChoose(self):
		self.panels = []
		x = self.rect.left + 50
		y = self.rect.top + 100
		self.addPanel(TypeButton(self, Rect(x,y,100,120), 'fighter'))
		x += 200
		self.addPanel(TypeButton(self, Rect(x,y,100,120), 'interceptor'))
		x += 200
		self.addPanel(TypeButton(self, Rect(x,y,100,120), 'destroyer'))
			
	def chooseColor(self, color):
		self.game.playerColor = color
		self.typeChoose()
	
	def chooseType(self, type):
		self.game.playerType = type
		self.running = False
	
class ColorButton(Button):
	def __init__(self, parent, rect, color):
		self.myColor = color
		self.parent = parent
		Button.__init__(self, rect, self.choose, None)
		
	def draw(self, surface, rect):
		pygame.draw.rect(surface, self.myColor, self.rect) 
		Panel.draw(self, surface, rect)
		
	def choose(self):
		self.parent.chooseColor(self.myColor)
		
class TypeButton(Button):
	def __init__(self, parent, rect, type):
		self.image = colorShift(loadImage('res/menus/'+type+'.bmp', None),
						parent.game.playerColor,None)
		self.parent = parent
		self.type = type
		Button.__init__(self, rect, self.choose, None)
		
	def choose(self):
		self.parent.chooseType(self.type)
	
class Messenger:
	queue = deque() #not capitalized in stand lib
	speed = 40 #characters per second
	messageDelay = 9 #seconds after each message
	maxChars = 250 #line width
	font = FONT
	topleft = 2,2
	maxMessages = 8
	def __init__(self, game, font = FONT, dir = 1):
		self.dir = dir# -1 means the messages stack upward.
		self.game = game
		self.image = pygame.Surface((game.width - 202, self.font.get_linesize()))
		self.image.set_alpha(200)
	
	def message(self, text, color = (250,250,250)):
		"""message(text,color) -> add a message to the Messenger."""
		text = '   ' + text
		if len(text) > self.maxChars: #line length limit
			self.message(text[:maxChars], color)
			self.message(text[maxChars:], color)
			return
		self.queue.append((self.font.render(text, True, color),
				self.game.timer + 1. * len(text) / self.speed + self.messageDelay))
		if soundModule:
			messageSound.play()
		
	def update(self):
		if self.queue and self.game.timer > self.queue[0][1] \
		or len(self.queue) > self.maxMessages:
			self.queue.popleft()
		
	def draw(self, surface):
		y = self.topleft[1]
		for message in self.queue:
			self.image.fill((0, 0, 80))
			self.image.blit(message[0], (0,0))
			surface.blit(self.image, (self.topleft[0], y))
			y += self.font.get_linesize() * self.dir
			
	def empty(self):
		self.queue = deque()
		
class Trigger:
	def __init__(self, game, conditions, actions, repeat = False):
		self.repeat = repeat
		if type(conditions) != type([]):
			conditions = [conditions]
		self. conditions = conditions
		if type(actions) != type([]):
			actions = [actions]
		self.actions = actions
		self.game = game
		
	def update(self):
		for condition in self.conditions:
			if not condition():
				return
		for action in self.actions:
			action()
		if not self.repeat:
			self.game.triggers.remove(self)
		
def timerCondition(game, time, relative = True):
	if relative:
		time = game.timer + time
	return lambda: game.timer >= time
	
def levelCondition(game, level):
	return lambda: game.player.level >= level
	
def planetCondition(game, planet):
	return lambda: game.player.landed == planet
	
def solarSystemCondition(game, solarSystem):
	return lambda: game.curSystem == solarSystem

def seeShipCondition(game):
	from spaceship import Ship
	def see():
		for floater in game.curSystem.onScreen:
			if isinstance(floater,Ship) and floater != game.player:
				return True
		return False
	return see
	
def messageAction(game, text, color = (200,200,100)):
	return lambda: game.messenger.message(text, color)
	

		