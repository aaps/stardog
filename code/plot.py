#plot.py
from dialogs import *
def newGameTriggers(game):
	triggers = [
		Trigger(game, timerCondition(game, 5), 
			messageAction(game,
			'You: Wow, the stars are beautiful.')),
		Trigger(game, timerCondition(game, 10), 
			messageAction(game, 
			"You: I'm thinking thoughts! Have I always had thoughts?  I don't know.")),
		Trigger(game, timerCondition(game, 15), 
			messageAction(game, 
			"You: Hey, I see planets.  I wonder what they're like.")),
		Trigger(game, seeShipCondition(game), 
			messageAction(game, 
			"You: Look!  Other ships!  I wonder if they'll be my friend!")),
		]
	return triggers