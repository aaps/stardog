#camera.py
from vec2d import Vec2d
from planet import *
from floaters import *

class Camera(object):
	game = None
	width = 100
	height = 100
	transcurve = None
	transitioning = False
	transtime = 10
	pos = None
	layers = []
	target = None

	def __init__(self, game, pos=Vec2d(0,0)):
		self.game = game
		self.pos = pos
		self.width = game.width
		self.height = game.height

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

	def setPos(self,pos):
		self.pos = pos

	def setTransTime(self, time):
		self.transtime = time

	def setTarget(self, target):
		self.target = target

	def gotoTarget(self):
		self.transitioning = True

	def layerAdd(self, drawable, zindex):

		layer = Layer(drawable, zindex, self)

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
class Layer(object):
	zindex = 0
	enabled = True
	drawable = None
	camera = None

	def __init__(self, drawable ,zindex, camera):
		self.zindex = zindex
		self.drawable = drawable
		self.camera = camera
		if isinstance(drawable, SpaceView):
			self.drawable.camera = camera

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
			if isinstance(self.drawable, SpaceView):
				self.drawable.draw(surface, self.camera.pos)
			else:
				self.drawable.draw(surface)


class SpaceView(object):

	onScreen = []
	game = None
	width = 100
	height = 100
	camera = None
	offset = Vec2d(0,0)

	def __init__(self, game):
		self.game = game
		self.width = 100
		self.height = 100

	def update(self):
		self.game.universe.curSystem.update()

		self.onScreen = []
		self.offset = Vec2d(self.camera.pos.x - self.camera.width / 2, 
				self.camera.pos.y - self.camera.height / 2)


		for floater in self.game.universe.curSystem.floaters:
			r = floater.radius
			if (r + floater.pos.x > self.offset.x and floater.pos.x - r < self.offset.x + self.camera.width)\
			and (r + floater.pos.y > self.offset.y 	and floater.pos.y - r < self.offset.y + self.camera.height):
				self.onScreen.append(floater)




	def sortFloaterHeight(self, onscreen):
		if isinstance(onscreen, Planet):
			return 4
		elif isinstance(onscreen, Impact):
			return 5
		elif isinstance(onscreen, Explosion):
			return 3
		else:
			return 1

	def draw(self, surface, pos):
		self.onScreen = sorted(self.onScreen, key=lambda onscreen: self.sortFloaterHeight(onscreen))
		for floater in self.onScreen:
			floater.draw(surface, self.offset)
