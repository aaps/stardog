#plot.py
from dialogs import *
def newGameTriggers(universe):
	triggers = [
		Trigger(universe, timerCondition(universe, 5), 
			messageAction(universe,
			'You: I should turn on the RADAR, where is the R button ?')),
		Trigger(universe, timerCondition(universe, 10), 
			messageAction(universe,
			'You: Wow, the stars are beautiful.')),
		Trigger(universe, timerCondition(universe, 20), 
			messageAction(universe, 
			"You: I'm thinking thoughts! Have I always had thoughts?  I don't know.")),
		Trigger(universe, [seePlanetCondition(universe), timerCondition(universe, 20)], 
			messageAction(universe, 
			"You: Hey, I see planets.  I wonder what they're like.")),
		Trigger(universe, seeShipCondition(universe), 
			messageAction(universe, 
			"You: Look!  Other ships!  I wonder if they'll be my friend!")),
		Trigger(universe, solarSystemCondition(universe,'Qbert'),
			messageAction(universe, "You: I have arived at the " + universe.curSystem.name + " system at last, the question is . . . How ?") )
		]
	return triggers