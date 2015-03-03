# universe.py
# 
from starSystem import *

class Universe(object):
    
    def __init__(self, game = None):
        self.starSystems = []
        self.curSystem = None
        self.player = None
        self.game = game

        if game:
            self.player = game.player
        self.cameras = []

    def setPlayer(self, player):
        self.player = player
        self.curSystem.add(self.player)

    def getSystemByName(self, name):
        for system in self.starSystems:
            if system.name == name:
                return system

    def addStarSystem(self, system):
        self.starSystems.append(system)

    def addCamera(self, camera):
        self.cameras.append(camera)

    def update(self):
        for camera in self.cameras:
            camera.update()

    def draw(self, surface):
        for camera in self.cameras:
            camera.draw(surface)

    # def getAllNeighbors(self, name):
    #   portals = []
    #   systems = []
    #   for system in self.starSystems:
    #       if system.name == name:
    #           portals = system.getAllPortals()
    #   if portals:
    #       for portal in portals:
    #           systems.append(portal.getSister())
    #   return systems

    def neighborsTo(self, starsystem):
        pass

    def removeStarSystem(self, name):
        for system in self.starSystems:
            if system.name == name:
                del self.starSystems[system]
                # self.starSystems[system] = None

    def setCurrentStarSystem(self, name):
        self.curSystem = self.getSystemByName(name)

    def getCurrentStarSystem(self):
        return self.curSystem
