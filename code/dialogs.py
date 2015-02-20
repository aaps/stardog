# dialogs.py
from utils import *
from menuElements import *
from spaceship import Ship
from planet import *
from gui import *


class Messenger(Drawable):
    # not capitalized in stand lib
    queue = deque()
    font = FONT

    def __init__(self, universe, font=FONT, dir=1):
        Drawable.__init__(self, universe)
        # -1 means the messages stack upward.
        self.dir = dir
        self.image = pygame.Surface((universe.game.width-204,
                                    self.font.get_linesize()))
        # characters per second
        self.speed = 40
        self.image.set_alpha(200)
        self.topleft = 0, 0
        self.maxMessages = 100
        # seconds after each message
        self.messageDelay = 9
        # line width
        self.maxChars = 200
        self.universe = universe
        self.game = universe.game

        self.soundSys = self.universe.game.soundSystem
        self.popupSound = 'message pip.ogg'
        self.soundSys.register(self.popupSound)

    def chunks(self, the_list, length):
        """ Yield successive n-size chucks from the_list.
        """
        for i in xrange(0, len(the_list), length):
            yield the_list[i:i+length]

    def message(self, text, color=SUPER_WHITE):
        """message(text,color) -> add a message to the Messenger."""
        text = '   ' + text
        # line length limit
        if len(text) > self.maxChars:
            for sentence in self.chunks(text, self.maxChars):
                linger = (self.game.timer+1.*len(sentence)/self.speed
                          + self.messageDelay)
                queueItem = (self.font.render(sentence, True, color), linger)
                self.queue.append(queueItem)
            return
        linger = (self.game.timer + 1. * len(text) / self.speed
                  + self.messageDelay)
        queueItem = (self.font.render(text, True, color), linger)
        self.queue.append(queueItem)
        self.soundSys.play(self.popupSound)


class Trigger(object):
    def __init__(self, universe, conditions, actions, repeat=False):
        self.repeat = repeat
        # if type(conditions) != type([]):
        if not isinstance(conditions, list):
            conditions = [conditions]
        self.conditions = conditions
        # if type(actions) != type([]):
        if not isinstance(actions, list):
            actions = [actions]
        self.actions = actions
        self.game = universe.game

    def update(self):
        for condition in self.conditions:
            if not condition():
                return
        for action in self.actions:
            action()
        if not self.repeat:
            self.game.triggers.remove(self)


def timerCondition(universe, time, relative=True):
    if relative:
        time = universe.game.timer + time
    return lambda: universe.game.timer >= time


def levelCondition(universe, level):
    return lambda: universe.curSystem.player.level >= level


def planetCondition(universe, planet):
    return lambda: universe.curSystem.player.landed == planet


def solarSystemCondition(universe, solarSystem):
    return lambda: universe.curSystem.name == solarSystem


def seePlanetCondition(universe):
    def see():
        for radar in universe.player.radars:
            for floater in radar.detected:
                if (isinstance(floater, Planet) and not isinstance(floater, Star)):
                    return True
        return False
    return see


def seeShipCondition(universe):
    def see():
        for radar in universe.player.radars:
            for floater in radar.detected:
                if isinstance(floater, Ship):
                    return True
        return False

    return see


def farAwayCondition(universe):
    return lambda: universe.curSystem.player.overedge


def messageAction(universe, text, color=(200, 200, 100)):
    return lambda: universe.game.messenger.message(text, color)
