#effects.py

def leak(ship):
	if ship.energy >= 0:
		ship.energy -= .5 * ship.game.dt
leak.__name__ = 'Leaky Part'
leak.__doc__ = 'ship loses .5 energy each second'

