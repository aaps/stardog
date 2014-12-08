
main dish
==========
* splitout views <nasty stuff> !!!
* quad trees (hardmode, after vector and view splitout, wil replace current collision check mess)
* wormholes/star gates to other systems. (medium mode ?, after Gravless class)
* multyplayer <hard mode, dependant on code structure, vectors and views split, also a better ui>
http://code.google.com/p/legume/
* a particle engine for explotions, engine stuff. <medium stuff, after view splitout>
* better ui (nasty mode ?, after view splitout)
* A save function ? <a sqllite file for now with sqlalchemy>
* replace the part - port system with a part - grid system
* sounds also need to be in views

side dish
==========
* make planet inherit from a Gravless class so stargate will not be effected by graf and * not be a planet. !!! also good for space ports, etc.
* make the space structure class that will inherit from gravless as well with a custom 
http://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon shape
* posibility to eject parts <easy mode>
* some way to target ships, parts and planets <easy mode>
* zoom in out option for radar <medium mode ?>
* weapon heat generation <easy mode>
* some early implementation of space $ <easy mode>
* a name to give yourself <as a precursor of network play and to get familiair with gui, after view spitout and vectors>
	http://www.cosc.canterbury.ac.nz/greg.ewing/python/Albow/
	http://ocemp.sourceforge.net/guiwidget.html
* the solarsystm.py has lots of basic functionality in a specific class can be put in parent class. this leaves space for starsystem specific stuff such as names and planet locations. !!!
* other sound for bullet impact on shield and plating and on planet
* palaxing background

bugs
=====
* on branch viewsinview an explotion will make another one.
* I can make a crash by bowing up my own ship in missile difference collision on branch * all2vector <Fixed Aat>
*in case of part flip in equipment screen another mirror part will apear but will replace counterpart when equipt.
engines will sometimes not fire in case of multyple forward.
can a planet have negative gravity ?
in viewsinview ship direction jitters sometimes


parts
======
* Space mines <easy mode> <Robert ?>
* A radar that will eventualy suport raytracing. <easy for initial radar> !!!
* a gravity well part.
* a dockingport part <can be hardmode>
* a disable beam part <easymode>
* ship lights <easy mode once particles is done>
* a part with a cog on it that will keep a copy of the ship it is in and refreshes that every x seconds



unknowns
=========

* if you will travel long enough you will also reach the next solar system, as in stargate travel.
* The edge of the system is a stupid idea, and can be replaced with a: when over boundry go to next star system independent of direction, will alwais travel to next star system even is only one ajacent
* every planet own part list <it is already so ?> <Robert ?>
* a cource line for a ship that will include gravity pulls. <depends on simulator ception>
* astroids in orbits (hard mode, depends on quad tree, simulatorception)
* test if planet orbit is posible and if no what is needed to make it so !
* a orbit calculator <depends on simulator ception>
* simulator ception for calculation of trajectorys, targeting and future positions <hard ?>
* integrate wishlist of: http://code.google.com/p/stardog/


DONE
====
* test if solar orbit is posible, <solar orbit is possible did it twice (duality)>
* finite engine trust speed <it is done, can be tweaked, but is done (Aat)>
* revamp to use vectors <as good as done Aat>

<Duality>

make menu work on fullscreen. only fighter is displayed right left corner. <fixed Duality>

crew
=====
* add crew?
* and parts for crew quaters.					<part added>
* more crew more efficient ship.
* maybe if crew then heal x per x seconds.

bays
=====
* a part that is mechanic bay
* a part that is weapons bay
* a part that is the armory
* a part that is a cargo bay

ship
=====
* every ship a individual mid section that defines what the ship is.
* implement droping mines and implement a part for it that does that?
or only give the destroyer that capability?
* display ship stats closer to the ship like health energy xp bar can stay where it is?

parts
======
* blocks with different shapes so that you can better position parts.
* maybe implement hull plating. some things are worth protecting.

universe
=========
* make mass count more realisticly. it's not just counted in to heavy.
key-handling:
* some key combinations don't work in menu or other parts of the game.
* thus make key-handling for quiting (for example) be interupt based.

if part die/are killed damage vehicle/ship

particle engine for effects.
