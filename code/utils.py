#utils.py

import random
import math
from pygame.locals import *
import pygame
from vec2d import *
from os import listdir
from os.path import isfile, join
import os
import re

BLACK = (0,0,0)
MIN_BLACK = (10,10,10)
SHIPDAMAGE = (0,0,50,200)
SHIPDAMAGE2 = (0,0,70,200)
HUD3 = (0,150,50)
HUD2 = (0,50,250)
HUD1 = (0,0,150)
RED = (250,0,0)
GREEN = (0,250,0)
BLUE = (0,0,250)
SHIP_PANEL_BLUE = (100,200,0)
CONSOLE_BLUE = (100,100,250,250)
BGSELECTED = (100,50,100)
DRAGGABLE = (50,150,50)
BGACTIVE = (110,100,50)
DS_SELECTED = (250,50,50)
SELECTED_COLOR = (250,200,200)
ST = (200,200,250)
BUTTON_ACTIVE = (200,250,200)
SBUTTON_ACTIVE = (250,150,0)
BS1 = (100,200,100)
BS3 = (200,100,100)
SBUTTON_INACTIVE = (200,100,0)
FLOATER = (200,200,0)
HUD6 = (200,0,250)
MINI2 = (0,250,250)
PART1 =  (150,150,150)
PARTICLE1 = (150,150,150,50)
WHITE = (250,250,250)
PARTICLE3 = (250,250,0,250)
PARTICLE5 = (75,100,250,250)
PARTICLE6 = (250,100,100,0)
SUPER_WHITE = (255,255,255)

def col12row9(game, xcol,yrow, withcol, heightrow):
    rows = 12
    cols = 12
    x = int(game.width / cols) * xcol
    y = int(game.height / rows) * yrow
    width = int(game.width / cols) * withcol
    height = int(game.width / rows) * heightrow

    return Rect(x,y,width,height)

hardwareFlag = pygame.HWSURFACE

# setup fonts
try:
    pygame.font.init()
    font_name = "hardfont.ttf"
    font_dir = "res/fonts/"
    font_path = font_dir+font_name
    SMALL_FONT = pygame.font.Font((font_path), 14)
    FONT = pygame.font.Font((font_path), 18)
    BIG_FONT = pygame.font.Font((font_path), 24)
    fontModule = True

except:
    FONT = None
    BIG_FONT = None
    SMALL_FONT = None
    fontModule = False
    print("Font module not found. Text will not be printed.")

# if pygame.image.get_extended():
#     ext = ".gif"
# else:
#     ext = ".bmp"

sqrt = math.sqrt
# random generators:
r = random.Random()
rand = r.random
randint = r.randint
randnorm = r.normalvariate


#TODO: write fast sloppy trig functions. 
def sin(theta):
    return math.sin(math.radians(theta))

def cos(theta):
    return math.cos(math.radians(theta))
    
def atan2(rise, run):
    return math.degrees(math.atan2(rise, run))

def angleNorm(angle):
    """returns an equivilant angle between -180 and 180."""
    return (angle + 180) % 360 - 180

def angleNormPlus(angle):
    """returns an equivilant angle between -180 and 180."""
    return ((angle + 180) % 360 - 180) + 180

def rotate(x, y, angle):
    """rotation transformation for a point."""
    cost = cos(angle) #cost is short for cos(theta)
    sint = sin(angle)
    newx = x  * cost - y * sint
    newy = x  * sint + y * cost
    return (newx, newy)
    
def dist(x1, y1, x2, y2):
    return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2)

def dist2(floater1, floater2):
    """returns the squared distance between two floaters (center to center)."""
    return  floater1.pos.get_dist_sqrd(floater2.pos)

def sign(num):
    """returns the sign of the number, -1, 0, or 1."""
    if num < 0 : return -1
    if num > 0 : return 1
    return 0
    
def limit(min, num, max):
    """Returns num if min < num <max.  
    Returns min if num < min or max if num > max."""
    if num > max: return max
    if num < min: return min
    return num

def not0(num):
    """if num is 0, returns .001.  To prevent div by 0 errors."""
    if num:
        return num
    return .000001




def randColor(min, max):
    return (randint(min[0], max[0]), randint(min[1], max[1]),
            randint(min[2], max[2]))



def randImageInDir(directory):
    
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        
        f.extend(filenames)
        break
    return directory + "/" + random.choice(f)


def loadImage(filename):
    try:
        image = pygame.image.load(filename).convert_alpha()
    except pygame.error:
        image = pygame.image.load("res/parts/default.png").convert_alpha()

    return image
    
def colorShift(surface, color, first = 0, second = 2):
    """Converts every pixel with equal red and blue values to a shade of 
    color.  Attempts to maintain value and saturation of surface. 
    Returns a new Surface."""

    s = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32).convert_alpha()
    # s.set_colorkey(colorkey)
    s.blit(surface, (0,0))
    pa = pygame.PixelArray(s)
    for i in range(len(pa)):
        for j in range(len(pa[i])):
            newColor = oldColor = s.get_at((i, j))
            
            if oldColor[first] == oldColor[second]: #a shade of magic pink
                newColor = [0, 0, 0, 0]
                for k in [0,1,2]:
                    # print newColor, old
                    newColor[k] = int(oldColor[0] * color[k] / 255 + oldColor[1] * (255 - color[k]) / 255)
            newColor[3] = oldColor[3]
            s.set_at((i, j),newColor)
    del pa
    del surface
    del oldColor
    del newColor
    return s

def totalColorVal(surface):
    pa = pygame.PixelArray(surface)
    colscore = 0
    for i in range(len(pa)):
        for j in range(len(pa[i])):
            col = surface.get_at((i, j))
            colscore += col[0] + col[1] + col[2]
    return colscore

def collisionTest(a, b):
    """test spatial collision of Floaters a and b"""
    return a != b and a.pos.get_distance(b.pos) < (a.radius + b.radius)


def linePointDist(linePoint1, linePoint2, point, infinite = False):
    line = linePoint2[0] - linePoint1[0], linePoint2[1] - linePoint1[1]
    lineDist = sqrt(line[0] ** 2 + line[1] ** 2)
    toPoint = point[0] - linePoint1[0], point[1] - linePoint1[1]
    projectionDist = (line[0] * toPoint[0] + line[1] * toPoint[1]) / lineDist
    if projectionDist < 0 and not infinite:
        closest = linePoint1
    elif projectionDist > lineDist and not infinite:
        closest = linePoint2
    else: 
        ratio = projectionDist / lineDist
        closest = (line[0] * ratio + linePoint1[0],
                      line[1] * ratio + linePoint1[1])
        
    return dist(closest[0], closest[1], point[0], point[1])
    

def bulletColor(damage):
    """generates a color based on how much energy it needs to express"""
    if damage >= 0 and damage <= 2:
        return (255, int(125*damage), int(125*damage), 125)
    if damage <= 10 and damage >= 2:
        return (255-(20*damage+50), 255-(20*damage+50), 255, 125)
    else:
        return (0,255,0, 125)

def targetRect(surface, color, mincolor, pos, radius, spacing):
    """A radar targeting rectangle drawing function"""
    pygame.draw.rect(surface, color, (pos[0]-radius-spacing,pos[1]-radius-spacing,radius*2+(spacing*2),radius*2+(spacing*2)), 1)
    pygame.draw.rect(surface, mincolor, (pos[0]-radius-spacing,pos[1]-int(radius/2)-int(spacing/2),(radius*2)+(spacing*2),radius+spacing), 1)
    pygame.draw.rect(surface, mincolor, (pos[0]-int(radius/2)-int(spacing/2),pos[1]-radius-spacing,radius+spacing,(radius*2)+(spacing*2)), 1)

def diamond(surface, color, pos, size):
    """A function that will draw a diamond for gui radar ussage"""
    pygame.draw.polygon(surface, color,[(0+pos[0],0+pos[1]-(size*2)-2),(4*size+pos[0],4*size+pos[1]-(size*2)-2),(0+pos[0],8*size+pos[1]-(size*2)-2), (-4+pos[0],4*size+pos[1]-(size*2)-2)],1)

def ddiamond(surface, color, pos, size):
    """ A double diamon drawing function"""
    pygame.draw.polygon(surface, color,[(0+pos[0],0+pos[1]-(size*2)-2),(4*size+pos[0],4*size+pos[1]-(size*2)-2),(0+pos[0],8*size+pos[1]-(size*2)-2), (-4+pos[0],4*size+pos[1]-(size*2)-2)],1)
    pygame.draw.polygon(surface, color,[(0+pos[0],0+pos[1]-(size*2)),(2*size+pos[0],2*size+pos[1]-(size*2)),(0+pos[0],4*size+pos[1]-(size*2)), (-2+pos[0],2*size+pos[1]-(size*2))])



def diamondRect(surface, color, rect, corners=[]):
    """A rectangle with shaved off corners drawing function"""
    relrect = (0,0,rect[2],rect[3])
    image = pygame.Surface((rect[2],rect[3])).convert()
    image.fill((0, 0, 0))
    pygame.draw.rect(image, color, relrect, 1)
    if len(corners) == 4:
        for idx, corner in enumerate(corners):
            if corner > 0:
                if idx == 0:
                    points = [(relrect[0],relrect[1]),(relrect[0]+corner,relrect[1]),(relrect[0],relrect[1]+corner)]
                    pygame.draw.polygon(image, BLACK, points)
                    pygame.draw.lines(image, color, False, points[1:]) 
                elif idx == 1:
                    points = [(relrect[2]+relrect[0]-1,relrect[1]),(relrect[2]+relrect[0]-corner-1,relrect[1]),(relrect[2]+relrect[0]-1,relrect[1]+corner)]
                    pygame.draw.polygon(image, BLACK, points)
                    pygame.draw.lines(image, color, False, points[1:]) 
                elif idx == 2:
                    points = [(relrect[2]+relrect[0]-1,relrect[3]+relrect[1]-1),(relrect[2]+relrect[0]-corner-1,relrect[3]+relrect[1]-1),(relrect[2]+relrect[0]-1,relrect[3]+relrect[1]-corner-1)]
                    pygame.draw.polygon(image, BLACK, points)
                    pygame.draw.lines(image, color, False, points[1:]) 
                else:
                    points = [(relrect[0],relrect[1]+relrect[3]-1),(relrect[0],relrect[1]+relrect[3]-corner-1),(relrect[0]+corner,relrect[1]+relrect[3]-1)]
                    pygame.draw.polygon(image, BLACK, points)
                    pygame.draw.lines(image, color, False, points[1:])
    image.set_colorkey(BLACK)
    surface.blit(image, (rect[0], rect[1]))


def makeKMdistance(floaterx, floatery):
    """Convert game pix distance edge to edge into KM's, ships several KM's big, meh"""
    return str(max(round((floaterx.pos.get_distance(floatery.pos)-floaterx.radius-floatery.radius)/10,1),0))


def makeKMs(floater):
    """The soon to be famous pix to km calculator"""
    return str(round(floater.delta.get_length()/10,1))

def saveScreenShot(mypath, screen):
    """It will save a screenshot in a path of choice, also incremental numbers"""
    number = 0
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for filename in onlyfiles:
        temp = re.findall(r'\d+', filename)

        if len(temp) > 0 and int(temp[-1]) > number:
            number = int(temp[-1])
    number+=1
    pygame.image.save(screen, "Screen-shots/screenshot" + str(number) + ".jpeg")