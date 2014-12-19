
from vec2d import Vec2d

class Camera:
	game = None
	pos = None
	width = 100
	height = 100
	transcurve = None
	transitioning = False
	transtime = 10
	onScreen = []
	layers = []
	target = None
	bg = None

	def __init__(self, game, pos = Vec2d(0,0)):
		self.game = game
		pos = Vec2d(0,0)
		self.width = game.width
		self.height = game.height
		self.onScreen = []


	def update(self):
		self.onScreen = []
		self.offset = Vec2d(self.game.player.pos.x - self.width / 2, 
				self.game.player.pos.y - self.height / 2)
		for floater in self.game.curSystem.floaters:
			r = floater.radius
			if (r + floater.pos.x > self.offset.x \
				and floater.pos.x - r < self.offset.x + self.width)\
			and (r + floater.pos.y > self.offset.y \
				and floater.pos.y - r < self.offset.y + self.height):
					self.onScreen.append(floater)

		for layer in self.layers:
			if layer.enabled:
				layer.update()


	def draw(self, surface):
		self.bg.draw(surface, self.game.player)
		for floater in self.onScreen:
			floater.draw(surface, self.offset)

		for layer in self.layers:
			if layer.enabled:
				layer.draw(surface)

	def easeOutQuart(self, t, b, c, d):
		t /= d
		t -= 1
		return -c * (t*t*t*t - 1) + b

	def linear(self, t, b, c, d): 
		return c*t/d + b

	def setBG(self, bg):
		self.bg = bg

	def setTransTime(self, time):
		self.transtime = time

	def setTarget(self, target):
		self.target = target

	def gotoTarget(self):
		self.transitioning = True

	def layerAdd(self, layer):
		self.layers.append(layer)
		sorted(self.layers, key=lambda layer: layer.zindex)