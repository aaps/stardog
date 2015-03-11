# camera.py
from utils import *

class spriteSystem(object):

    def __init__(self):
        self.sprites = []
        self.spritesheets = {}

    def addspritesheet(self, spritesheet, xnum, ynum):
        image = loadImage(str(filename))
        dims = (xnum, ynum, round(image.get_width()/xnum), round(image.get_height()/ynum))
        self.spritesheets.update({str(filename):{'image':image,'dimentions':dims}})


    def registerss(self, name, (x,y) ,zoomable=False):
        spritesheet = filter(lambda x: x.location == name, self.spritesheets)
        if len(spritesheet) > 0:
            spritesheet[0].dimentions
            rect = Rect(spritesheet[0].dimentions[0]*spritesheet[0].dimentions[2], spritesheet[0].dimentions[1]*spritesheet[0].dimentions[3], spritesheet[0].dimentions[2], spritesheet[0].dimentions[3] )
            self.spritesheets.subsurface(rect)
            self.sprites.append(multysprite(name,color,zoomable))
            return True

        return False
        
        self.sprites.append(self.spritesheets)

    def registerimg(self, name, zoomable=False):
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

    def __init__(self, filename, color=(255,255,255,255), zoomable = False):
        self.color = color
        self.location = str(filename)
        self.norm = loadImage(self.location)
        self.scaled = self.norm.copy()
        self.scalecolor = colorShift(self.norm, self.color)
        self.zoomable = zoomable

    def zoom(self, zoom):
        zoom = zoom * self.sprites['norm'][sprite].get_rect().width
        self.scaled = pygame.transform.smoothscale(self.sprites[sprite]['norm'],(zoom, zoom))
        self.scalecolor = colorShift(self.scaled, self.color)

    def setColor(self, color):
        self.scalecolor = colorShift(self.scaled, self.color)