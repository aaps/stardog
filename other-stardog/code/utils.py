import random
import math
from pygame.locals import *
import pygame

hardwareFlag = pygame.HWSURFACE# | DOUBLEBUF

#not to do: write fast sloppy trig functions. These would be slower!
#sinTable = [math.sin(math.radians(x)) for x in range(360)]
#cosTable = [math.cos(math.radians(x)) for x in range(360)]
#maybe write them in c?
def sin(theta):
	return math.sin(math.radians(theta))

def cos(theta):
	return math.cos(math.radians(theta))

def atan2(rise, run):
	"""slope to angle, takes signed rise and run to get correct quadrant."""
	return math.degrees(math.atan2(rise, run))

def asin(x):
	"""asin, takes a value in [0,1] (opposite/hypotenuse), returns degrees."""
	return math.degrees(math.asin(x))

pi = math.pi


def angleNorm(angle):
	"""returns an equivalent angle between -180 and 180."""
	return (angle + 180) % 360 - 180

def rotate(x, y, angle):
	"""rotation transformation for a point."""
	cost = cos(angle) #cost is short for cos(theta)
	sint = sin(angle)
	newx = x  * cost - y * sint
	newy = x  * sint + y * cost
	return (newx, newy)

def dist(x1, y1, x2, y2):
	"""dist(x1, y1, x2, y2) -> the distance from (x1, y1) to (x2, y2)"""
	return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2)

def dist2(floater1, floater2):
	"""returns the squared distance between two floaters (center to center)."""
	return ((floater1.x - floater2.x) * (floater1.x - floater2.x) +
			(floater1.y - floater2.y) * (floater1.y - floater2.y))

def relDist(floater1, floater2):
	"""returns relative distance between two floaters"""
	return math.sqrt(dist2(floater1, floater2))

def relativeDir(floater1, floater2):
	"""absolute angle of floater2 treating floater1 as the origin."""
	return atan2(floater2.y - floater1.y, floater2.x - floater1.x)

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

def getPos(floater):
	"""object -> (object.x, object.y)"""
	return floater.x, floater.y

sqrt = math.sqrt
log = math.log
#random generators:
r = random.Random()
rand = r.random
randint = r.randint
randnorm = r.normalvariate
choice = random.choice

time = pygame.time.get_ticks

def randColor(min, max):
	return (randint(min[0],max[0]), randint(min[1],max[1]), \
			randint(min[2],max[2]))

#setup fonts
try:
	pygame.font.init()
	#SHADOW_FONT = pygame.font.SysFont(name = None, size = 20, bold = True)
	SMALL_FONT = pygame.font.SysFont(name = None, size = 16)
	FONT = pygame.font.SysFont(name = None, size = 20)
	MED_FONT = pygame.font.SysFont(name = None, size = 28)
	BIG_FONT = pygame.font.SysFont(name = None, size = 36)
	fontModule = True
except:
	FONT = None
	BIG_FONT = None
	fontModule = False
	print "Font module not found. Text will not be printed."

#setup sounds
try:
	pygame.mixer.init(44100)
	pygame.mixer.set_num_channels(63)
	shootSound = pygame.mixer.Sound("res/sound/lazer.ogg")
	hitSound = pygame.mixer.Sound("res/se_sdest.wav")
	explodeSound = pygame.mixer.Sound("res/sound/ship explosion.ogg")
	missileSound =  pygame.mixer.Sound("res/se_explode02.wav")
	messageSound =  pygame.mixer.Sound("res/sound/message pip.ogg")
	thrustSound = pygame.mixer.Sound("res/sound/thrust.ogg")
	pygame.mixer.set_reserved(1)
	#channel 0: thrust sound
	pygame.mixer.Channel(0).set_volume(.2)
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

def loadImage(filename, colorkey=(0,0,0)):
	try:
		image = pygame.image.load(filename).convert()
		image.set_colorkey(colorkey)
	except pygame.error:
		image = pygame.image.load("res/default.bmp").convert()
		image.set_colorkey((255,255,255))
	return image

def colorShift(surface, color, colorkey = (0,0,0)):
	"""Converts every pixel with equal red and blue values to a shade of
	color.  Attempts to maintain value and saturation of surface.
	Returns a new Surface."""
	s = pygame.Surface(surface.get_size(), flags = hardwareFlag).convert()
	s.set_colorkey(colorkey)
	s.blit(surface, (0,0))
	pa = pygame.PixelArray(s)
	alpha = surface.get_alpha()
	for i in range(len(pa)):
		for j in range(len(pa[i])):
			oldColor = s.unmap_rgb(pa[i][j])
			if oldColor[0] == oldColor[2]: #a shade of magic pink
				newColor = [0, 0, 0, 0]
				for k in [0,1,2]:
					#oldColor[0] = oldColor[2] = main color
					#oldColor[1] = unsaturation
					newColor[k] = int(oldColor[0] * color[k] / 255 \
								+ oldColor[1] * (255 - color[k]) / 255)
				newColor[3] = oldColor[3]
				pa[i][j] = s.map_rgb(tuple(newColor))
	del pa
	return s

def collisionTest(a, b):
	"""test spatial collision of Floaters a and b"""
	r = a.radius + b.radius
	return a != b \
	and a.x < b.x + r \
	and b.x < a.x + r \
	and a.y < b.y + r \
	and b.y < a.y + r \
	and dist2(a, b) < r ** 2

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








