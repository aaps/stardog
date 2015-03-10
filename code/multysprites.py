# camera.py
from utils import *

class spriteSystem(object):

    def __init__(self):
        self.sprites = []

    def register(self, name, zoomable=False):
        self.sprites.append(multysprite(name,color,zoomable))

    def getsprite(self, name):
        return filter(lambda x: x.location == name, self.sprites)

    def zoom(self, zoom):
        for sprite in self.sprites:
            if sprite.zoomable:
                sprite.zoom(zoom)

    def draw(self, sprite):
        pass
                


class multysprite(object):

    def __init__(self, filename, color, zoomable = False):
        self.color = color
        self.location = str(filename)
        self.norm = loadImage(self.location)
        self.scaled = self.norm.copy()
        # print self.color
        self.scalecolor = colorShift(self.norm, self.color)
        self.zoomable = zoomable

    def zoom(self, zoom):
        zoom = zoom * self.sprites['norm'][sprite].get_rect().width
        self.scaled = pygame.transform.smoothscale(self.sprites[sprite]['norm'],(zoom, zoom))
        self.scalecolor = colorShift(self.scaled, self.color)

    def setColor(self, color):
        self.scalecolor = colorShift(self.scaled, self.color)