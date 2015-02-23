# dialogs.py
from utils import *
from menuElements import *
from spaceship import Ship
from planet import *
from gui import *


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
            self.game.storytriggers.remove(self)

class Conditions(object):


    def timerCondition(self, universe, time, relative=True):
        if relative:
            time = universe.game.timer + time
        return lambda: universe.game.timer >= time


    def levelCondition(self,universe, level):
        return lambda: universe.curSystem.player.level >= level


    def planetCondition(self,universe, planet):
        return lambda: universe.curSystem.player.landed == planet


    def solarSystemCondition(self,universe, solarSystem):
        return lambda: universe.curSystem.name == solarSystem


    def seePlanetCondition(self,universe):
        def see():
            for radar in universe.player.radars:
                for floater in radar.detected:
                    if (isinstance(floater, Planet) and not isinstance(floater, Star)):
                        return True
            return False
        return see


    def seeShipCondition(self,universe):
        def see():
            for radar in universe.player.radars:
                for floater in radar.detected:
                    if isinstance(floater, Ship):
                        return True
            return False

        return see


    def farAwayCondition(self,universe):
        return lambda: universe.curSystem.player.overedge

class Actions(object):

    def messageAction(self,universe, text, color=(200, 200, 100)):
        return lambda: universe.game.messenger.message(text, color)
