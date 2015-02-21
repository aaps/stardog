#!/usr/bin/python

import pygame

from pygame.locals import *
import sys
try:
  from updater import *
except:
  from utils.updater import *


FULL = False; RESOLUTION = 1024, 768 #test
# FULL = True; RESOLUTION = None
# FULL = True; RESOLUTION = None #play
hardwareFlag = pygame.HWSURFACE|pygame.DOUBLEBUF



if __name__=="__main__":
    #command line resolution selection:
    run = 'client'
    if len(sys.argv) > 1:
        print sys.argv
        try:
            if sys.argv[1] == 'client':
              
              if sys.argv[2] == 'f' or sys.argv[2] == 'full':
                  FULL = True
                  RESOLUTION = None
              else:
                  FULL = False
              if len(sys.argv) == 4 \
              and 300 <= int(sys.argv[2]) < 4000 \
              and 300 <= int(sys.argv[3]) < 4000:
                  RESOLUTION = int(sys.argv[2]), int(sys.argv[3])

            elif sys.argv[1] == 'server':
                run = 'server'
                RESOLUTION = (100,100)

         

        except Exception, err:
            print err
            print("bad command line arguments.")
    #set up the disply:
    pygame.init()
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
      "X.o.X           ",
      "X.oo.X          ",
      "X.ooo.X         ",
      "X.oooo.X        ",
      "X.ooooo.X       ",
      "X.ooo....X      ",
      "X.o..XXXXXX     ",
      "X..XXX          ",
      "X.XX            ",
      "XX              ",
      "X               ",
      "                ")
    #note: black is and white are fliped.
    datatuple, masktuple = pygame.cursors.compile( thickarrow_strings,
                                      black='X', white='.', xor='o' )
    pygame.mouse.set_cursor( (16,16), (0,0), datatuple, masktuple )




if __name__ == '__main__':

    if run is 'client':
      import code.game
      game = code.game.Game(screen)
      game.GGV = getGitVersion
      game.GLV = getLogVersion
      game.CV = checkVersion
      game.CRED = getCredits
      game.run()
    else:
      import code.gameserver
      game = code.gameserver.Server(screen)
      game.run()

