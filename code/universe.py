#universe.py

from starSystem import *

class Universe(object):
	starSystems = []
	curSystem = None
	game = None
	player = None

	def __init__(self, game):
		self.game = game
		player = game.player

	def setPlayer(self, player):
		self.player = player
		self.curSystem.add(self.player)

	def getSystemByName(self, name):
		for system in self.starSystems:
			if system.name == name:
				return system

	def addStarSystem(self, system):
		self.starSystems.append(system)
	
	def getAllNeighbors(self, name)		:
		portals = []
		systems = []
		for system in self.starSystems:
			if system.name == name:
				portals = system.getAllPortals()

		if portals:
			for portal in portals:

				systems.append(portal.getSister())

		return systems


	def removeStarSystem(self, name):
		for system in self.starSystems:
			if system.name == name:
				del self.starSystems[system]
				# self.starSystems[system] = None

	def setCurrentStarSystem(self, name):
		self.curSystem = self.getSystemByName(name)

	def getCurrentStarSystem(self):
		return self.curSystem
