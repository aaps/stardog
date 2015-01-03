#game.py

from utils import *
from menus import *
from scripts import *
from starSystem import *
from gui import *
from planet import *
from spaceship import *
from strafebat import *
from dialogs import *
from camera import *
from universe import *
import plot
from vec2d import Vec2d
import datetime
try:
    from swampy.Lumpy import Lumpy
except ImportError:
    print "no way to build a class diagram now!! "
#command parsing
import commandParse
from pympler import muppy


FPS = 300

class Game(object):
    """Game(resolution = None, fullscreen = False)
    -> new game instance. Multiple game instances
    are probably a bad idea."""
    menu = None
    def __init__(self, screen):
        self.pause = False
        self.console = False
        self.debug = False
        self.player = None
        self.starttime = 1899463445
        self.fps = FPS
        self.screen = screen
        self.top_left = 0, 0
        self.universe = Universe(self)
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.mouseControl = True
        self.timer = 0
        # self.systems = []
        self.triggers = []
        self.camera = Camera(self)
        #messenger, with controls as first message:
        self.messenger = Messenger(self.universe)
        self.universe.addStarSystem(SolarA1(self.universe, "theone"))
        self.universe.addStarSystem(SolarA1(self.universe, "thesecond"))
        
        self.camera.layerAdd(self.messenger,7)
        self.camera.layerAdd(MiniInfo(self),6)
        
        #key polling:
        self.keys = [False]*322
        #mouse is [pos, button1, button2, button3,..., button6].
        #new Apple mice think they have 6 buttons.
        self.mouse = [(0, 0), 0, 0, 0, 0, 0, 0]
        #pygame setup:
        self.clock = pygame.time.Clock()
        self.hud = HUD(self)
        self.camera.layerAdd(self.hud,4)
        self.camera.layerAdd(SpaceView(self),3)
        #create a chatconsole for text input capabilities
        self.chatconsole = ChatConsole(self, Rect(int(self.width/ 8), self.height-50, self.width - int(self.width/ 8) , 50))
        
    def run(self):
        """Runs the game."""
        
        self.running = True
        while self.running:
            # game setup:
            intro = IntroMenu(self, Rect((self.width - 800) / 2,
                                        (self.height - 600) / 2,
                                        800,600))
            self.messenger.empty()
            while self.running and intro.running:
            # 	#event polling:
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    intro.handleEvent(event)
                intro.update()
                self.screen.fill((0, 0, 0, 0))
                intro.draw(self.screen)
                pygame.display.flip()
            #setup initial state:
            self.playerScript = InputScript(self)
            self.player = playerShip(self, Vec2d(0,0),Vec2d(0,0),
                            color = self.playerColor, name = self.PlayerName, type = self.playerType)
            
            self.camera.layerAdd(shipDamage(self),5)
            self.camera.layerAdd(StarField(self),2)
            self.universe.setCurrentStarSystem("theone")
            self.camera.layerAdd(self.universe.curSystem.bg,1)
            
            self.universe.setPlayer(self.player)
            self.camera.setPos(self.player.pos)
            makePlayerBindings(self.playerScript, self.player)

            self.menu = Menu(self, Rect((self.width - 800) / 2,    (self.height - 600) / 2, 800, 600))
            makeGameBindings(self.playerScript , self)
            
            self.player.setScript(self.playerScript)

           
            for x in range(10):
                self.clock.tick()
            
            self.triggers = plot.newGameTriggers(self.universe)
            #create a parser that parses chatconsole input for command and such.
            self.commandParse = commandParse.CommandParse(self, self.chatconsole, self.messenger)
            #The in-round loop (while player is alive):
            while self.running and self.universe.curSystem.ships.has(self.player):
                #event polling:
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = 0
                    # if not self.pause and not self.console:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse[event.button] = 1
                        self.mouse[0] = event.pos
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse[event.button] = 0
                        self.mouse[0] = event.pos
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse[0] = event.pos
                    elif event.type == pygame.KEYDOWN:
                        self.keys[event.key % 322] = 1
                        if event.key == pygame.K_m:
                            all_objects = muppy.get_objects()
                    elif event.type == pygame.KEYUP:
                        self.keys[event.key % 322] = 0

                    if self.menu.active:
                        self.menu.handleEvent(event)
                    if self.chatconsole.active:
                        self.chatconsole.handleEvent(event)
                # game-level key input:
                # somehow delete key will destroy ship and when back out of menu will again destroy ship
                # when this schript part is in scripts thats why it is still here.
                if self.keys[K_DELETE % 322]:
                    self.keys[K_DELETE % 322] = False
                    self.player.kill() #suicide

                self.debug = False
                if self.keys[K_BACKSPACE % 322]:
                    self.debug = True #print debug information
                    self.keys[K_BACKSPACE % 322] = False
                    print "Debug:"
                #ctrl+q or alt+F4 quit:
                if self.keys[K_LALT % 322] and self.keys[K_F4 % 322] \
                or self.keys[K_RALT % 322] and self.keys[K_F4 % 322] \
                or self.keys[K_LCTRL % 322] and self.keys[K_q % 322] \
                or self.keys[K_RCTRL % 322] and self.keys[K_q % 322]:
                    self.running = False

                for trigger in self.triggers:
                    trigger.update()

                self.camera.update()
                self.camera.draw(self.screen)

                # paused:
                if self.menu.active:
                    self.menu.update()
                    self.menu.draw(self.screen)

                if self.chatconsole.active:
                    self.chatconsole.update()
                    self.chatconsole.draw(self.screen)
                    
                #update actually parses input.
                #and does actions based upon that.
                self.commandParse.update()
                #reloading logic, couldn't make it work from inside the commandParse class
                if self.commandParse.reload:
                    self.commandParse.reload = False
                    reload(commandParse)
                    self.commandParse = commandParse.CommandParse(self, self.chatconsole, self.messenger)
                
                #frame maintainance:
                pygame.display.flip()
                self.clock.tick(FPS)#aim for FPS but adjust vars for self.fps.
                self.fps = max(1, int(self.clock.get_fps()))
                self.timer += 1. / self.fps
            #end round loop (until gameover)
        #end game loop

# lumpy.class_diagram()
