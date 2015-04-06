#game.py

from menus import *
from scripts import *
from gui import *
from dialogs import *
from camera import *
from universe import *
from plot import *
import datetime
import sys
from utils import *
from multysprites import *

# command parsing (a command line interface for the game)
# that supports multiple commands, and functions.
from commandParse import CommandParse

# import librarie for showing mem usage in caption
try:
    import resource
    import gc
except Exception as e:
    print(e)

FPS = 3e6


class Game(object):
    """Game(resolution = None, fullscreen = False)
    -> new game instance. Multiple game instances
    are probably a bad idea."""
    menu = None

    def __init__(self, screen, FPS):
        self.console = False
        self.debug = False
        self.player = None
        self.starttime = 1899463445
        self.fps = FPS
        self.fpscounter = 0
        self.fpses = range(0, 30)
        self.averagefps = 0
        self.screen = screen
        self.top_left = 0, 0
        self.mouseControl = True
        self.timer = 0
        self.triggers = []

        self.universe = Universe(self)
        self.width = screen.get_width()
        self.height = screen.get_height()
        # initialize the the music system.
        self.musicSystem = MusicSystem('res/sound/ambientMusic/')
        self.musicSystem.play(self.musicSystem.getRandomMusic())
        # initialize the sound system.
        # every part has to register with this system.
        self.soundSystem = SoundSystem('res/sound/sfxSounds/')
        self.spritesystem = spriteSystem()
        self.spritesystem.addspritesheet("res/parts/default.png", 1, 1)
        self.spritesystem.addspritesheet("res/ammo/shot.png", 1,1)
        self.spritesystem.addspritesheet("res/parts/misilelauncher.png", 1, 1)
        self.spritesystem.addspritesheet("res/ammo/missile.png", 1, 1)
        self.spritesystem.addspritesheet("res/ammo/mine.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/radar.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/engine.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/gyro.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/generator.png", 1, 1)

        self.spritesystem.addspritesheet("res/parts/interconnect.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/quarters.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/gateway_focus.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/battery.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/shield.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/cargo.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/minelayer.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/interceptor.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/fighter.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/destroyer.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/leftflak.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/machinegun.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/rightflak.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/leftlaser.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/rightlaser.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/leftgun.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/rightgun.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/strafebatgun.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/fightershield.png", 1, 1)
        self.spritesystem.addspritesheet("res/parts/cockpit.png", 1,1 )
        self.spritesystem.addspritesheet("res/goods/goods.png", 5, 5)
        self.camera = Camera(self.universe, self.spritesystem)
        self.universe.addCamera(self.camera)

        # messenger, with controls as first message:
        self.messenger = Messenger(self.universe, BIG_FONT)
        theone = SolarA1(self.universe, "theone", Vec2d(1, 100))
        thesecond = SolarA1(self.universe, "thesecond", Vec2d(1, -100), 2, 1)
        thethird = SolarA1(self.universe, "thethird", Vec2d(1, 200), 2, 1)
        theone.addNeighbor(thesecond)
        theone.addNeighbor(thethird)

        self.universe.addStarSystem(theone)
        self.universe.addStarSystem(thesecond)
        self.universe.addStarSystem(thethird)

        self.camera.layerAdd(self.messenger, 7)
        self.camera.layerAdd(MiniInfo(self.universe, FONT), 6)

        # key polling:
        self.keys = [False]*322
        # mouse is [pos, button1, button2, button3,..., button6].
        # new Apple mice think they have 6 buttons.
        self.mouse = [(0, 0), 0, 0, 0, 0, 0, 0]
        # pygame setup:
        self.clock = pygame.time.Clock()
        self.hud = HUD(self.universe)
        self.tageting = TargetingRect(self.universe)
        self.radarfield = RadarField(self.universe)
        self.camera.layerAdd(self.hud, 4)
        self.camera.layerAdd(self.radarfield, 4)
        self.camera.layerAdd(self.tageting, 4)
        self.spaceview = SpaceView(self)
        self.camera.layerAdd(self.spaceview, 3, True)
        # create a chatconsole for text input capabilities
        # self.chatconsole = ChatConsole(self, col12row9(self,1,1,4,8))
        # does the universe have a player present in it?
        self.hasPlayer = None

    def quit(self):
        pygame.quit()

    def run(self):
        """Runs the game."""
        self.running = True
        while self.running:
            # game setup:
            intro = IntroMenu(self, Rect((self.width - 800) / 2,
                                         (self.height - 600) / 2,
                                         800, 600))
            self.messenger.empty()
            while self.running and intro.running:
                # event polling:
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    intro.handleEvent(event)
                intro.update()
                self.screen.fill((0, 0, 0, 0))
                intro.draw(self.screen)
                pygame.display.flip()
                # aim for FPS but adjust vars for self.fps.
                self.clock.tick(self.fps)
                self.fps = max(1, int(self.clock.get_fps()))
                self.timer += 1. / self.fps
            # handle if running is false
            if not self.running:
                break

            # setup initial state:
            self.playerScript = InputScript(self)
            self.menuScript = Script(self)
            self.consoleScript = Script(self)
            self.player = playerShip(self, Vec2d(0, 0), Vec2d(0, 0),
                                     color=self.playerColor,
                                     name=self.PlayerName,
                                     type=self.playerType)
            self.playerid = id(self.player)

            self.camera.layerAdd(shipDamage(self.universe, FONT), 5)
            self.camera.layerAdd(StarField(self.universe), 2)
            self.universe.setCurrentStarSystem("theone")
            self.camera.layerAdd(self.universe.curSystem.bg, 1)
            self.camera.setLayersPlayer(self.player)
            self.universe.setPlayer(self.player)
            self.camera.setPos(self.player.pos)
            makePlayerBindings(self.playerScript, self.player)

            self.menu = Menu(self, Rect((self.width - 800) / 2,
                             (self.height - 600) / 2, 800, 600))

            self.chatconsole = ChatConsole(self, col12row9(self,2,11,10,1)
)
            makeMenuBindings(self.menuScript, self)
            makeGameBindings(self.playerScript, self)
            makeConsoleBindings(self.consoleScript, self)

            # two rules below should be integrated into their classes
            # self.menu.keys.bindings.bindings = self.playerScript.bindings
            self.menu.keys.bindings.reset()
            self.menu.addScript(self.menuScript)

            self.chatconsole.addScript(self.consoleScript)
            self.player.addScript(self.playerScript)
            for x in range(10):
                self.clock.tick()

            self.triggers = Triggers(self)
            self.storytriggers = self.triggers.StoryTriggers(self.universe)
            # create a parser that parses chatconsole input
            # for command and such.
            self.commandParse = CommandParse(self, self.chatconsole,
                                             self.messenger)
            # check once wether the universe still has a player.
            self.hasPlayer = self.player in self.universe.curSystem.floaters
            # The in-round loop (while player is alive):
            # print self.hasPlayer, self.running

            while self.running and self.hasPlayer:
                # check wether the universe still has a player.
                self.hasPlayer = self.player in self.universe.curSystem.floaters
                # event polling:
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
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

                    elif event.type == pygame.KEYUP:
                        self.keys[event.key % 322] = 0
                    if self.menu.active:
                        self.menu.handleEvent(event)
                    if self.chatconsole.active:
                        self.chatconsole.handleEvent(event)
                # game-level key input:
                # somehow delete key will destroy ship and when back out of
                # menu will again destroy ship
                # when this schript part is in scripts thats
                # why it is still here.
                if self.keys[K_DELETE % 322]:
                    self.keys[K_DELETE % 322] = False
                    # suicide
                    self.player.kill()

                if self.keys[K_BACKSLASH % 322]:
                    saveScreenShot("Screen-shots", self.screen)

                self.debug = False
                L_ALT_F4 = (self.keys[K_LALT % 322] and self.keys[K_F4 % 322])
                R_ALT_F4 = (self.keys[K_RALT % 322] and self.keys[K_F4 % 322])
                L_CTRL_Q = (self.keys[K_LCTRL % 322] and self.keys[K_q % 322])
                R_CTRL_Q = (self.keys[K_RCTRL % 322] and self.keys[K_q % 322])
                if (L_ALT_F4 or R_ALT_F4 or L_CTRL_Q or R_CTRL_Q):
                    self.running = False
                    
                for strigger in self.storytriggers:
                    strigger.update()

                self.universe.update()
                self.universe.draw(self.screen)

                # paused:

                if self.menu.active:
                    self.menu.update()
                    self.menu.draw(self.screen)

                if self.chatconsole.active:
                    self.chatconsole.update()
                    self.chatconsole.draw(self.screen)

                # update actually parses input.
                # and does actions based upon that.
                self.commandParse.update()
                # reloading logic, couldn't make it work
                # from inside the commandParse class
                # reloads the module so it imports new code.
                if self.commandParse.reload:
                    self.commandParse.reload = False
                    reload(commandParse)
                    self.commandParse = CommandParse(self, self.chatconsole,
                                                     self.messenger)

                # frame maintainance:
                pygame.display.flip()
                if self.fpscounter >= 30:
                    self.fpscounter = 0
                self.fpses[self.fpscounter] = self.fps
                self.fpscounter += 1
                self.averagefps = reduce(lambda x, y: x+y, self.fpses)/30

                # aim for FPS but adjust vars for self.fps.
                self.clock.tick(FPS)
                self.fps = max(1, int(self.clock.get_fps()))
                self.timer += 1. / self.fps

                self.spritesystem.setFPS(self.fps)
                self.spritesystem.update()

                # try and print debuging caption
                try:
                    disp_str = 'Memory usage: %d(KB) %d(MB) %d(GB) FPS: %d'
                    memUse = int(resource.getrusage(
                                 resource.RUSAGE_SELF).ru_maxrss)
                    memUseMB = memUse/1024
                    memUseGB = memUseMB/1024
                    fps = self.averagefps
                    pygame.display.set_caption(disp_str % (memUse, memUseMB,
                                               memUseGB, fps))
                except Exception:
                    pygame.display.set_caption('FPS: %d' % (self.averagefps))
            # end round loop (until gameover)
        # end game loop
        # self.__init__(self.screen)
