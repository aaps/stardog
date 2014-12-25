
main dish
==========

* quad trees (hardmode, after vector and view splitout, wil replace current collision check mess)

* wormholes/star gates to other systems. (medium mode ?, after Gravless class) [might be soon done]!!!
make jump part(takes energy to load), bind to j, time out and some effect like explotion after timeout addplayer to other system.

* multyplayer [hard mode, dependant on code structure, vectors and views split, also a better ui]
* a particle engine for explotions, engine stuff. [medium stuff, after view splitout]

http://pygame.org/project-planes-2392-4051.html get version 0.6
* A save function ? [a sqllite file for now with sqlalchemy] [Robert ?]
* replace the part - port system with a part - grid system
* sounds also need to be in views
* put the collide logic in the things that collide, planets, floaters, parts etc. [1/4 done]
* it needs an economy not yust parts for static $$, [ harder ]
* nebula and atmosphere
* sometime in future convert the entity views to something like this:
http://www.pygame.org/project-OpenGL+Library+(glLib*)-877-.html
http://www.pygame.org/project-glLib+Reloaded-1326-4684.html


side dish
==========

* making the rest of screen changeable ?, posibility to chage window with and or height ?
* instead of flippable part chage shoot direction, and mirror image, and make flipable a property of class
* more collision handeling refactor !! [still need more refactoring]
* more to vec2d verctor work. !!! [can alwais use some work]
* remember planets that where on radar in list [done , aat]
* some way to target ships, parts and planets !!! [easy mode]
* zoom in out option for radar [medium mode ?]
* weapon heat generation [easy mode]
* engines that are good for space travel but bad for landing and visaversa
* a name to give yourself [as a precursor of network play and to get familiair with gui, after view spitout and vectors] [gui is not nice, but overhaul costs to much time, lets keep it for now]
* Display solar system name somewhere [was suposed to be in menu untill the no pause game refactor]
* other sound for bullet impact on shield and plating and on planet
* palaxing background, the image
* menu volume controll for music and effects
* instead of restart directly, wait for keypress and see your lifeless ship float into the distance.
* a camera to capture different places, in stead of only player. [done and then some, aat]
* make the camera so that it can smoothly transition from one place to another
* make the game run from the beginning, so if choosing ship and color the game is already running
* give ships a atention score that goes up when ships are sooting and dying drops off over time. [done, aat]
* the portal stargate warp dent could use some drag inside it, for temp usability
* grav anomalys are easy to make, game element ?
* cargo container and cargo will work as follows: cargo go's in every container on your ship. in future you can only fitt parts on your ship when on planet or structure, when container gets destroyed or dissconnected from ship you lose parts untill you are at capacity
* when special key than lifebars on parts and some effect for parts that are on, or some extra type of ship info.
* in camera splitout functionality make a layer class for the layers that will not do the drawing but perhaps the updating, anyhow updates doesnt belong in camera ?
* landed can go to ship class so the ai can do extra stuff
* ai could use some more bains and variation
* also add the chat console and menu to the camera
* draw planets over things like explotions, and other ships.
* make the color of the color of the star dependant on the size of the star, bigger is blueer, smaller redisher [done could use some tweaking]
* when destroyed a part has a change it will become scrap



Housekeeping
===
* cleanup class diagram
* impost original stagdog svn
* integrate wishlist of: http://code.google.com/p/stardog/

bugs
=====
* remove the self.kill(other) thing see master branch, this is not working should be other way of both coliders to know about each other.
* on branch viewsinview an explotion will make another one.[so what for now]
* I can make a crash by blowing up my own ship in missile difference collision on branch * all2vector [Fixed Aat]
engines will sometimes not fire in case of multyple forward. [fixed , Aat]
in viewsinview ship direction jitters sometimes, more so when it's got a lot of parts.
the laser is broken, ;( [It is fixed, Aat]
* make binding keys actually works. they bind but don't do anything. and moste of the time. it bugs out the guns so they fire randomly or continously. [it works]
* if you bind a key to a engine that isn't in the engine slot. it won't fire if you press that key. [??? hu ???]
* the engines dont animate after radar addition, meh [ok this was a timing problem , when more code time in programm passes differently, it was done in a messy way, this will come back in a different form and place, fixed this however]
* radar enabled states are seperate, should be synced ? 
* after menu and chat console prototype independance of game pause the menu will not show info, skills etc the right way. [fixed aat]
* still cant land on strucutre class. [fixed Aat]
* when ejecting parts planet inventory will not put them streight when caught
* engines seem to light up nice, but the purple color of the engines doesnt color to ship color.
* in case of button pressed when you open menu, the ship will continue to do that action.
* known planets is a list of all the known planets not the known planets in the current system
* In case of open planet part panel and parts 'land' on planet they will not show up at the parts panel right away. only after a menu out/in
* Canons don't work anymore they don't shoot.
* putting a engine on a radar "part" it doesn't fire.

parts
======

* A radar that will eventualy suport raytracing. [easy for initial radar]
* Make mine's de accelerate till they hit their target spot. 
so you can get out of the way in time.
maybe implement a arming period. 
bigger detonation range.

* a coloniser part
* a cargo part to hold the cargo
* a gravity well part.
* a dockingport part [can be hardmode]
* a disable beam part [easymode]
* ship lights [easy mode once particles is done]
* a part with a cog on it that will keep a copy of the ship it is in and refreshes that every x seconds
* make images for ships in the menu to choose from. 


unknowns
=========

* if you will travel long enough you will also reach the next solar system, as in stargate travel.
* The edge of the system is a stupid idea, and can be replaced with a: when over boundry go to next star system independent of direction, will alwais travel to next star system even is only one ajacent

* a cource line for a ship that will include gravity pulls. [depends on simulator ception]
* astroids in orbits (hard mode, depends on quad tree, simulatorception)
* test if planet orbit is posible and if no what is needed to make it so !
* a orbit calculator [depends on simulator ception]
* simulator ception for calculation of trajectorys, targeting and future positions [hard ?]
* imports in methods, do we want that ?



DONE
====
* test if solar orbit is posible, [solar orbit is possible did it twice (duality)]
* finite engine trust speed [it is done, can be tweaked, but is done (Aat)]
* revamp to use vectors [as good as done Aat]
* every planet own part list, nope but fixed [Aat fixed it]
* fixing a bug that made memmory leak during the drawing of the star map (duality)

* splitout views [nasty stuff] [as good as done, for now i want no part of it Aat]
* we have parts not that can be toggled on or off, like the radar, no none asked for it still did it [Aat]
* Space mines [easy mode] [Duality]
make menu work on fullscreen. only fighter is displayed right left corner. [fixed Duality]
* and parts for crew quaters. [part added]
* make the space structure class that will inherit from gravless as well with a custom  [done in other way]

* posibility to eject parts [easy mode, done aat]
* make planet inherit from a Gravless class so stargate will not be effected by graf [done in another way]
* removed names from the code, duality, your name can go here !

[Duality]

Commanline interface
=====
* a command line interface for manipulating the world so that testing is faster. [W.I.P]
* convert all oldstyle classes into new style that is easier to check with type() [done]
* make command interface check against a list of keys that it may ignore for printing or using.
- a command to add parts to a ship
- a command to change name of ship
- a command to change name of planet
- a command to add parts to planets
- a command to make ships / planets
- a command to remove ships / planets
- above also for other floaters/structures ?
- a command to make a star system and link it to existing system
- a command to reate a specific part with x stats on planet or ship, integrate with one of above ?
- a command to manipulate your camera (need work)
- a command for teleporting ships to other starsystem


crew
=====
* add crew?
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
* make a scout ship
* make a juggernaut ship [Done, also increased parts that can be fixed to the ship by 2 because it was 10/8 parts attached]
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
