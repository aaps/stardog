#dialogs.py
from collections import deque

from utils import *
from menuElements import *
from spaceship import Ship
from planet import *


class Messenger(Drawable):
    queue = deque() #not capitalized in stand lib
    speed = 40 #characters per second
    messageDelay = 9 #seconds after each message
    maxChars = 200 #line width
    font = FONT
    topleft = 0,0
    maxMessages = 100
    def __init__(self, universe, font = FONT, dir = 1):
        Drawable.__init__(self, universe.game)
        self.dir = dir# -1 means the messages stack upward.
        self.image = pygame.Surface((universe.game.width - 204, self.font.get_linesize()))
        self.image.set_alpha(200)
        self.universe = universe
        self.game = universe.game
   
    def chunks(self, the_list, length):
        """ Yield successive n-size chucks from the_list.
        """
        for i in xrange(0, len(the_list), length):
            yield the_list[i:i+length]
    
    def message(self, text, color = SUPER_WHITE):
        """message(text,color) -> add a message to the Messenger."""
        text = '   ' + text
        if len(text) > self.maxChars: #line length limit
            for sentence in self.chunks(text, self.maxChars):
                self.queue.append((self.font.render(sentence, True, color),
                    self.game.timer + 1. * len(sentence) / self.speed + self.messageDelay))
            return
        self.queue.append((self.font.render(text, True, color),
                self.game.timer + 1. * len(text) / self.speed + self.messageDelay))
        if soundModule:
            messageSound.play()
        
    def update(self):
        if self.queue and self.game.timer > self.queue[0][1] \
        or len(self.queue) > self.maxMessages:
            self.queue.popleft()
        
    def draw(self, surface):
        y = self.topleft[1]
        for message in self.queue:
            self.image.fill((0, 0, 80))
            self.image.blit(message[0], (0,0))
            surface.blit(self.image, (self.topleft[0], y))
            y += self.font.get_linesize() * self.dir
            
    def empty(self):
        self.queue = deque()
        
class Trigger(object):
    def __init__(self, universe, conditions, actions, repeat = False):
        self.repeat = repeat
        if type(conditions) != type([]):
            conditions = [conditions]
        self. conditions = conditions
        if type(actions) != type([]):
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
        
def timerCondition(universe, time, relative = True):
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
                if isinstance(floater,Planet) and not isinstance(floater,Star):
                    return True
        return False
    return see

def seeShipCondition(universe):
    def see():
        for radar in universe.player.radars:
            for floater in radar.detected:
                if isinstance(floater,Ship):
                    return True
        return False
    return see

    
def messageAction(universe, text, color = (200,200,100)):
    return lambda: universe.game.messenger.message(text, color)

    

        
