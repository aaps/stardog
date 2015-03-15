# camera.py
from utils import *
import zlib

class spriteSystem(object):

    def __init__(self):
        self.sprites = {}
        self.spritesheets = {}
        self.defname = "res/parts/default.png"
        self.default = loadImage(self.defname)
        self.fps = 1

    def addspritesheet(self, filename, xnum, ynum):
        image = loadImage(str(filename))
        dims = (xnum, ynum, round(image.get_width()/xnum), round(image.get_height()/ynum))
        self.spritesheets.update({str(filename):{'image':image,'dimentions':dims}})
        

    def getsprite(self, spriteid):
        name = spriteid[0]
        pos = spriteid[1]
        color = spriteid[2]
        direction = spriteid[3]
        zoom = spriteid[4]

        ahash = zlib.adler32(name + str(pos) +  str(color) + str(direction) + str(zoom))
        result = self.sprites.get(ahash)
        if result:
            return result
        else:
            spritesheet = self.spritesheets.get(name)
            if spritesheet:
                dimentions = spritesheet.get('dimentions')
                rect = Rect(pos[0]*dimentions[2], pos[1]*dimentions[3], dimentions[2], dimentions[3] )
                surface = spritesheet.get('image').subsurface(rect)


                amultysprite = multysprite(name, surface, pos, color, direction, zoom)
                self.sprites.update({ahash:amultysprite}) 
                return amultysprite

            return multysprite(self.defname,self.default,(0,0))


    def zoom(self, zoom):
        for sprite in self.sprites:
            if sprite.zoomable:
                sprite.zoom(zoom)

    def setFPS(self, fps):
        self.fps = fps

    def update(self):
        for sprite in self.sprites:
            self.sprites[sprite].notused += 1.0 / self.fps
            if self.sprites[sprite].notused > 10:
                self.sprites = self.removekey(self.sprites, sprite)
                
    def removekey(self, d, key):
        r = d.copy()
        del r[key]
        return r

                
class multysprite(object):

    def __init__(self, filename, surface, pos=(1,1), color=(255,255,255), direction = 0, zoom = 1):
        
        self.image = surface
        self.notused = 0
        if color:
            self.image = colorShift(self.image, color)
        if zoom:
            dims = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (zoom*dims.width, zoom*dims.height))
        if direction:
            self.image = pygame.transform.rotate(self.image, -direction)
        self.image = self.image.convert_alpha()
        
    def getImage(self):
        self.notused = 0
        return self.image

