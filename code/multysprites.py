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
        

    def getsprite(self, sprited, spriteid):
        if not spriteid['zoom']:
             spriteid['zoom'] =  self.camera.zoom
        ahash = zlib.adler32(spriteid.get('name') + str(spriteid.get('pos')) +  str(spriteid.get('color')) + str(spriteid.get('direction')) + str(spriteid.get('zoom')))
        result = self.sprites.get(ahash)
        if result:
            return result
        else:
            spritesheet = self.spritesheets.get(spriteid.get('name'))
            if spritesheet:
                dimentions = spritesheet.get('dimentions')
                rect = Rect(spriteid.get('pos')[0]*dimentions[2], spriteid.get('pos')[1]*dimentions[3], dimentions[2], dimentions[3] )
                surface = spritesheet.get('image').subsurface(rect)


                amultysprite = multysprite( spriteid.get('name'), surface, sprited, spriteid.get('pos'), spriteid.get('color'), spriteid.get('direction'), spriteid.get('zoom'))
                self.sprites.update({ahash:amultysprite}) 
                return amultysprite

            return multysprite(self.defname,self.default,sprited,(0,0))


    def zoom(self, zoom):
        for sprite in self.sprites:
            if self.sprites[sprite].sprited and self.sprites[sprite].sprited.spritename:
                self.sprites[sprite].sprited.spritename['zoom'] = zoom

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

    def __init__(self, filename, surface, sprited=None, pos=(1,1), color=(255,255,255), direction = 0, zoom = 1):
        
        self.image = surface
        self.sprited = sprited
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

