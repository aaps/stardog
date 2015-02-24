#plot.py

from dialogs import *

class Triggers(object):

	def __init__(self, game):
		self.game = game
		self.conditions = Conditions()
		self.actions = Actions()


	def StoryTriggers(self, universe):
		player = universe.getCurrentStarSystem().player

		triggers = [
			Trigger(universe, self.conditions.timerCondition(universe, 5), 
				self.actions.messageAction(universe,
				player.firstname + " " + player.secondname + ': I should turn on the RADAR, where is the R button ?')),
			Trigger(universe, self.conditions.timerCondition(universe, 10), 
				self.actions.messageAction(universe,
				player.firstname + " " + player.secondname + ': Wow, the stars are beautiful.')),
			Trigger(universe, self.conditions.timerCondition(universe, 20), 
				self.actions.messageAction(universe, 
				player.firstname + " " + player.secondname + ": I'm thinking thoughts! Have I always had thoughts?  I don't know.")),
			Trigger(universe, [self.conditions.seePlanetCondition(universe), self.conditions.timerCondition(universe, 20)], 
				self.actions.messageAction(universe, 
				player.firstname + " " + player.secondname + ": Hey, I see planets.  I wonder what they're like.")),
			Trigger(universe, self.conditions.seeShipCondition(universe), 
				self.actions.messageAction(universe, 
				player.firstname + " " + player.secondname + ": Look!  Other ships!  I wonder if they'll be my friend!")),
			Trigger(universe, self.conditions.solarSystemCondition(universe,'Qbert'),
				self.actions.messageAction(universe, player.firstname + " " + player.secondname + ": I have arived at the " + universe.curSystem.name + " system at last, the question is . . . How ?") ),
			Trigger(universe, self.conditions.farAwayCondition(universe), 
				self.actions.messageAction(universe, player.firstname + " " + player.secondname + ": I have traveled quite far from the center of " + universe.curSystem.name + " I wonder where this leads to ?!")),
			]

		return triggers