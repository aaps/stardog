
from vec2d import Vec2d

class Camera:
	game = None
	pos = None
	width = 100
	height = 100
	transcurve = None
	transitioning = False
	transtime = 10
	# onScreen = []
	layers = []
	target = None
	# bg = None

	def __init__(self, game, pos = Vec2d(0,0)):
		self.game = game
		pos = Vec2d(0,0)
		self.width = game.width
		self.height = game.height
		# self.onScreen = []


	def update(self):
		for layer in self.layers:
			if layer.enabled:
				layer.update()

	def draw(self, surface):
		for layer in self.layers:
			if layer.enabled:
				layer.draw(surface)


	def easeOutQuart(self, t, b, c, d):
		t /= d
		t -= 1
		return -c * (t*t*t*t - 1) + b

	def linear(self, t, b, c, d): 
		return c*t/d + b


	def setTransTime(self, time):
		self.transtime = time

	def setTarget(self, target):
		self.target = target

	def gotoTarget(self):
		self.transitioning = True


	def layerAdd(self, drawable, zindex):
		layer = Layer(drawable, zindex)

		self.layers.append(layer)

		self.layers = sorted(self.layers, key=lambda layy: layy.zindex)
	
	def getLayer(self, zindex=0):
		for layer in self.layers:
			if layer.zindex == zindex:
				return layer
		return None
		

	
	def layerRemove(self, zindex=0):
		self.layers[zindex] = None
		self.layers = sorted(self.layers, key=lambda layer: layer.zindex)

	def layerReplace(self,layer, zindex=0):
		self.layers[zindex] = layer

# this could be somewhat overkill, and refactored in an other structures, i just dont want drawabled be dependant on
# drawing height and other stuff that dont concerns these things
class Layer:
	zindex = 0
	enabled = True
	drawable = None

	def __init__(self, drawable ,zindex):
		self.zindex = zindex
		self.drawable = drawable

	def setEnabled(self, enabled):
		self.enabled = enabled

	def setZindex(self, index):
		self.zindex = index

	def setDrawable(self, drawable):
		self.drawable = drawable

	def update(self):
		if self.enabled:
			self.drawable.update()

	def draw(self, surface):
		if self.enabled:
			self.drawable.draw(surface)


class SpaceView:

	onScreen = []
	game = None
	width = 100
	height = 100

	def __init__(self, game):
		self.game = game
		pos = Vec2d(0,0)
		self.width = game.width
		self.height = game.height


	def update(self):
		self.game.curSystem.update()

		self.onScreen = []
		self.offset = Vec2d(self.game.player.pos.x - self.width / 2, 
				self.game.player.pos.y - self.height / 2)
		for floater in self.game.curSystem.floaters:
			r = floater.radius
			if (r + floater.pos.x > self.offset.x and floater.pos.x - r < self.offset.x + self.width)\
			and (r + floater.pos.y > self.offset.y 	and floater.pos.y - r < self.offset.y + self.height):
					self.onScreen.append(floater)

	def draw(self, surface):
		for floater in self.onScreen:
			floater.draw(surface, self.offset)