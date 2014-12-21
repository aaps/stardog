#plot.py
from dialogs import *
def newGameTriggers(game):
	triggers = [
		Trigger(game, timerCondition(game, 5), 
			messageAction(game,
			'You: I should turn on the RADAR, where is the R button ?')),
		Trigger(game, timerCondition(game, 10), 
			messageAction(game,
			'You: Wow, the stars are beautiful.')),
		Trigger(game, timerCondition(game, 20), 
			messageAction(game, 
			"You: I'm thinking thoughts! Have I always had thoughts?  I don't know.")),
		# Trigger(game, [seePlanetCondition(game), timerCondition(game, 20)], 
		# 	[messageAction(game, 
		# 	"You: Hey, I see planets.  I wonder what they're like."), cameraAction(game, random.choice(game.player.knownplanets)
		# 	)]),
		# Trigger(game, timerCondition(game, 25),cameraAction),
		Trigger(game, timerCondition(game, 25), cameraAction(game, game.curSystem.sun
		)),
		# messageAction(game, 
		# 	"You: Look!  Other ships!  I wonder if they'll be my friend!")),
		Trigger(game, solarSystemCondition(game,'Qbert'),
			messageAction(game, "You: I have arived at the " + game.curSystem.name + " system at last, the question is . . . How ?") )
		]
	return triggers