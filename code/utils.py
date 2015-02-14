import random
import math
from pygame.locals import *
import pygame
from vec2d import *
from os import listdir
from os.path import isfile, join
import os
import re

hardwareFlag = pygame.HWSURFACE

SUPER_WHITE = (255,255,255)
WHITE = (250,250,250)
BLACK = (0,0,0)
MIN_BLACK = (10,10,10)
NAME_INPUT_BLUE = (100, 100, 200)
TYPE_BUTTON_GREEN = (100,255,100)
CONSOLE_BLUE = (100, 100, 255, 250)
SHIP_PANEL_BLUE = (100,200,0)
PDP_GREEN = (0, 150, 0)
PDP2_GREEN = (100, 200, 0)
SELECTED_COLOR = (255,200,200)
BGACTIVE = (110, 110, 75)
BGSELECTED = (80, 50, 110)
DS_SELECTED = (255,75,51)
BS1 = (100,200,100)
BS3 = (200,100,100)
ST = (200,200,255)
DRAGGABLE = (50, 150, 50)
DRAGGABLE2 = (75,175,75)
BUTTON_ACTIVE = (200,255,200)
SBUTTON_ACTIVE = (255,140,0)
SBUTTON_INACTIVE = (200,100,0)
INPUTFIELD = (100, 200, 100)
FLOATER = (200, 200, 0)
HUD1 = (20, 25, 130)
HUD2 = (0, 50, 230)
HUD3 = (0, 180, 80)
HUD6 = (200, 20, 255)
RADAR2 = (0, 0, 80)
RADAR3 = (0,0,150)
RADAR4 = (0, 250, 250)
RADAR6 = (250, 250, 0)
RADAR7 = (0, 250, 250)
RADAR8 = (150,40,0)
RADAR9 = (200,200,0)
RADAR10 = (0, 250, 250)
RADAR11 = (0,0,80)
RADAR12 = (0, 255, 255)
MINI1 = (100, 100, 255)
MINI2 = (0,255,255)
SHIPDAMAGE = (0, 0, 80, 200)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PART1 =  (150,150,150)
PARTICLE1 =  (150,150,150,50)
PARTICLE2 = (0,0,0,255)
PARTICLE3 = (255,255,0,255)
PARTICLE4 = (255,0,0,255)
PARTICLE5 = (75,75,255,255)
PARTICLE6 = (255,100,100,0)
SOME = (200,200,100)


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

sqrt = math.sqrt
#random generators:
r = random.Random()
rand = r.random
randint = r.randint
randnorm = r.normalvariate
def randColor(min, max):
	return (randint(min[0],max[0]), randint(min[1],max[1]), \
			randint(min[2],max[2]))

#setup fonts
try:
	pygame.font.init()  
	SMALL_FONT = pygame.font.Font("res/hardfont.ttf", 14)    
	FONT = pygame.font.Font("res/hardfont.ttf", 18)
	BIG_FONT = pygame.font.Font("res/hardfont.ttf", 24)
	fontModule = True

except:
	FONT = None
	BIG_FONT = None
	SMALL_FONT = None
	fontModule = False
	print "Font module not found. Text will not be printed."

#setup sounds	
try:
	pygame.mixer.init(44100)

	shootSound = pygame.mixer.Sound("res/sound/lazer.ogg")
	hitSound = pygame.mixer.Sound("res/se_sdest.wav")
	explodeSound = pygame.mixer.Sound("res/se_explode03.wav")
	missileSound =  pygame.mixer.Sound("res/se_explode02.wav")
	messageSound =  pygame.mixer.Sound("res/sound/message pip.ogg")

	travelMusicDir = "res/sound/ambientSound/"
	travelMusic = []
	print os.listdir(travelMusicDir)
	for musicfile in os.listdir(travelMusicDir):
		sound = pygame.mixer.Sound(travelMusicDir+str(musicfile))
		travelMusic.append(sound)
	travelMusic[6].play()
	soundModule = True
except (ImportError, NotImplementedError):
	soundModule = False
	print "Sound module not found. Sounds disabled."
	
#setup images
 #if there is extended image support, load .gifs, otherwise load .bmps.
 #.bmps do not support transparency, so there might be black clipping.
 
if pygame.image.get_extended():
	ext = ".gif"
else:
	ext = ".bmp"
	
def loadImage(filename, colorkey=BLACK):
	try:
		image = pygame.image.load(filename).convert_alpha()
	except pygame.error:
		image = pygame.image.load("res/parts/default.png").convert_alpha()

	# s = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32).convert_alpha()
	return image
	
def colorShift(surface, color, colorkey = (0,0,0)):
	"""Converts every pixel with equal red and blue values to a shade of 
	color.  Attempts to maintain value and saturation of surface. 
	Returns a new Surface."""

	s = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32).convert_alpha()
	s.set_colorkey(colorkey)
	s.blit(surface, (0,0))
	pa = pygame.PixelArray(s)
	for i in range(len(pa)):
		for j in range(len(pa[i])):
			newColor = oldColor = s.get_at((i, j))
			
			if oldColor[0] == oldColor[2]: #a shade of magic pink
				newColor = [0, 0, 0, 0]
				for k in [0,1,2]:
					newColor[k] = int(oldColor[0] * color[k] / 255 + oldColor[1] * (255 - color[k]) / 255)
			newColor[3] = oldColor[3]
			s.set_at((i, j),newColor)
	del pa
	del surface
	del oldColor
	del newColor
	return s

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
	if damage >= 0 and damage <= 2:
		return (255, int(125*damage), int(125*damage), 125)
	if damage <= 10 and damage >= 2:
		return (255-(20*damage+50), 255-(20*damage+50), 255, 125)
	else:
		return (0,255,0, 125)

def targetRect(surface, color, mincolor, pos, radius, spacing):

	pygame.draw.rect(surface, color, (pos[0]-radius-spacing,pos[1]-radius-spacing,radius*2+(spacing*2),radius*2+(spacing*2)), 1)
	
	pygame.draw.rect(surface, mincolor, (pos[0]-radius-spacing,pos[1]-int(radius/2)-int(spacing/2),(radius*2)+(spacing*2),radius+spacing), 1)
	pygame.draw.rect(surface, mincolor, (pos[0]-int(radius/2)-int(spacing/2),pos[1]-radius-spacing,radius+spacing,(radius*2)+(spacing*2)), 1)

def diamond(surface, color, pos, size):
	pygame.draw.polygon(surface, color,[(0+pos[0],0+pos[1]-(size*2)-2),(4*size+pos[0],4*size+pos[1]-(size*2)-2),(0+pos[0],8*size+pos[1]-(size*2)-2), (-4+pos[0],4*size+pos[1]-(size*2)-2)],1)

def ddiamond(surface, color, pos, size):
	pygame.draw.polygon(surface, color,[(0+pos[0],0+pos[1]-(size*2)-2),(4*size+pos[0],4*size+pos[1]-(size*2)-2),(0+pos[0],8*size+pos[1]-(size*2)-2), (-4+pos[0],4*size+pos[1]-(size*2)-2)],1)
	pygame.draw.polygon(surface, color,[(0+pos[0],0+pos[1]-(size*2)),(2*size+pos[0],2*size+pos[1]-(size*2)),(0+pos[0],4*size+pos[1]-(size*2)), (-2+pos[0],2*size+pos[1]-(size*2))])


def diamondRect(surface, color, rect, corners=[]):
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
	return str(max(round((floaterx.pos.get_distance(floatery.pos)-floaterx.radius-floatery.radius)/10,1),0))


def makeKMs(floater):
	return str(round(floater.delta.get_length()/10,1))

def find_nearest(array, value):
    n = [abs(i-value) for i in array]
    idx = n.index(min(n))
    return array[idx]

def saveScreenShot(mypath, screen):
	number = 0
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	for filename in onlyfiles:
		temp = re.findall(r'\d+', filename)

		if len(temp) > 0 and int(temp[-1]) > number:
			number = int(temp[-1])

	number+=1

	pygame.image.save(screen, "Screen-shots/screenshot" + str(number) + ".jpeg")