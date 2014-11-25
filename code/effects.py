#effects.py

def leak(ship):
	if ship.energy >= 5:
		ship.energy -= 5 / ship.game.fps
leak.__name__ = 'Leaky Part'
leak.__doc__ = 'ship loses .5 energy each second'

