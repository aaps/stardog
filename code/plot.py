#plot.py
from dialogs import *
def newGameTriggers(universe):
	player = universe.getCurrentStarSystem().player

	triggers = [
		Trigger(universe, timerCondition(universe, 5), 
			messageAction(universe,
			player.firstname + " " + player.secondname + ': I should turn on the RADAR, where is the R button ?')),
		Trigger(universe, timerCondition(universe, 10), 
			messageAction(universe,
			player.firstname + " " + player.secondname + ': Wow, the stars are beautiful.')),
		Trigger(universe, timerCondition(universe, 20), 
			messageAction(universe, 
			player.firstname + " " + player.secondname + ": I'm thinking thoughts! Have I always had thoughts?  I don't know.")),
		Trigger(universe, [seePlanetCondition(universe), timerCondition(universe, 20)], 
			messageAction(universe, 
			player.firstname + " " + player.secondname + ": Hey, I see planets.  I wonder what they're like.")),
		Trigger(universe, seeShipCondition(universe), 
			messageAction(universe, 
			player.firstname + " " + player.secondname + ": Look!  Other ships!  I wonder if they'll be my friend!")),
		Trigger(universe, solarSystemCondition(universe,'Qbert'),
			messageAction(universe, player.firstname + " " + player.secondname + ": I have arived at the " + universe.curSystem.name + " system at last, the question is . . . How ?") ),
		Trigger(universe, farAwayCondition(universe), 
			messageAction(universe, player.firstname + " " + player.secondname + ": I have traveled quite far from the center of " + universe.curSystem.name + " I wonder where this leads to ?!"))
		]


	return triggers