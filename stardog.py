#stardog.py

import pygame
from pygame.locals import *
import sys
try:
	import psyco
	psyco.full()
except ImportError:
	print 'this game may run faster if you install psyco.'
	
FULL = False; RESOLUTION = 1024, 800 #test
#FULL = True; RESOLUTION = None #play
hardwareFlag = pygame.HWSURFACE


if __name__=="__main__":
	#command line resolution selection:
	if len(sys.argv) > 1:
		try:
			if sys.argv[1] == 'f' or sys.argv[1] == 'full':
				FULL = True
				RESOLUTION = None
			else:
				FULL = False
			if len(sys.argv) == 4 \
			and 300 <= int(sys.argv[2]) < 4000 \
			and	300 <= int(sys.argv[3]) < 4000:
				RESOLUTION = int(sys.argv[2]), int(sys.argv[3])
		except:
			print("bad command line arguments.")
	#set up the disply:
	pygame.init()
	#pygame.display.init()
	if not RESOLUTION:
		RESOLUTION = pygame.display.list_modes()[0]
	if FULL:
		screen = pygame.display.set_mode(RESOLUTION, \
						hardwareFlag | pygame.FULLSCREEN | pygame.SRCALPHA)
	else:
		screen = pygame.display.set_mode(RESOLUTION, \
							hardwareFlag | pygame.SRCALPHA)
	#cursor:
	thickarrow_strings = (            #sized 24x16
	  "X               ",
	  "XX              ",
	  "X.X             ",
	  "X..X            ",
	  "X. .X           ",
	  "X.  .X          ",
	  "X.   .X         ",
	  "X.    .X        ",
	  "X.     .X       ",
	  "X.   ....X      ",
	  "X. ..XXXXXX     ",
	  "X..XXX          ",
	  "X.XX            ",
	  "XX              ",
	  "X               ",
	  "                ")
	#note: black is and white are fliped.
	datatuple, masktuple = pygame.cursors.compile( thickarrow_strings,
									  black='X', white='.', xor='o' )
	pygame.mouse.set_cursor( (16,16), (0,0), datatuple, masktuple )
import code.game
if __name__ == '__main__':
	game = code.game.Game(screen)
	game.run()
