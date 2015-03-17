# camera.py

from vec2d import Vec2d
from planet import *
from multysprites import *


class Camera(object):
    """A camera class that can keep screen dimentions, and has a location, not much more for now, used to view the game"""

    def __init__(self, universe, spritesystem, pos=Vec2d(0, 0)):
        self.universe = universe
        self.spritesystem = spritesystem
        self.spritesystem.camera = self
        self.pos = pos
        self.width = universe.game.width
        self.height = universe.game.height
        self.transcurve = None
        self.transitioning = False
        self.transtime = 10
        self.layers = []
        self.target = None
        self.zoom = 1

    def zoomOut(self):
        if self.zoom > 1:
            self.zoom -= 1
        self.spritesystem.zoom(self.zoom)

        for layer in self.layers:
            layer.zoomTo(self.zoom)

    def zoomIn(self):
        if self.zoom < 6:
            self.zoom += 1
        self.spritesystem.zoom(self.zoom)
        for layer in self.layers:
            layer.zoomTo(self.zoom)

    def update(self):
        """Update all the layers in this camera"""
        for layer in self.layers:
            if layer.enabled:
                layer.update()

    def draw(self, surface):
        """draw all the layers in this camera"""
        for layer in self.layers:
            if layer.enabled:
                layer.draw(surface)

    def easeOutQuart(self, t, b, c, d):
        t /= d
        t -= 1
        return -c * (t*t*t*t - 1) + b

    def linear(self, t, b, c, d):
        return c*t/d + b

    def setPos(self, pos):
        self.pos = pos

    def setTransTime(self, time):
        self.transtime = time

    def setTarget(self, target):
        self.target = target

    def gotoTarget(self):
        self.transitioning = True

    def layerAdd(self, drawable, zindex, zoomable=False):
        layer = Layer(drawable, zindex, self, zoomable)
        self.layers.append(layer)
        self.layers = sorted(self.layers, key=lambda layy: layy.zindex)

    def setLayersPlayer(self, player):
        for layer in self.layers:
            if not isinstance(layer.drawable, SpaceView):
                layer.drawable.setPlayer(player)

    def getLayer(self, zindex=0):
        for layer in self.layers:
            if layer.zindex == zindex:
                return layer
        return None

    def layerRemove(self, zindex=0):
        self.layers[zindex] = None
        self.layers = sorted(self.layers, key=lambda layer: layer.zindex)

    def layerReplace(self, layer, zindex=0):
        self.layers[zindex] = layer


# this could be somewhat overkill, and refactored in an other structures,
# i just dont want drawabled be dependant on
# drawing height and other stuff that dont concerns these things


class Layer(object):

    def __init__(self, drawable, zindex, camera, zoomable=False):
        self.zoomable=zoomable
        self.zindex = zindex
        self.drawable = drawable
        self.camera = camera
        self.enabled = True
        self.zoom = None
        if zoomable:
            self.zoom = 3
        if isinstance(drawable, SpaceView):
            self.drawable.camera = camera

    def zoomTo(self, zoom):
        if self.zoomable:
            self.zoom = zoom


    def setEnabled(self, enabled):
        self.enabled = enabled

    def setZindex(self, index):
        self.zindex = index

    def setZoomable(self, zoom):
        self.zoomable = zoom

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

    
    def __init__(self, game):
        self.game = game

        self.onScreen = []
        self.camera = None
        self.offset = Vec2d(0, 0)

    def update(self):
        self.game.universe.curSystem.update()
        self.onScreen = []
        self.offset = Vec2d(self.camera.pos.x - self.camera.width / 2,
                            self.camera.pos.y - self.camera.height / 2)

        for floater in self.game.universe.curSystem.floaters:
            r = floater.radius
            leftRight = (r + floater.pos.x > self.offset.x and
                         floater.pos.x-r < self.offset.x + self.camera.width)
            upDown = (r + floater.pos.y > self.offset.y and
                      floater.pos.y-r < self.offset.y + self.camera.height)
            if leftRight and upDown:
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
