
main dish
==========

(warning this file could describe things in faul language, cursing and poor grammar !)

* quad trees (hardmode, after vector and view splitout, wil replace current collision check mess)

* wormholes/star gates to other systems. (medium mode ?, after Gravless class) [might be soon done]!!! [more work than anticipated]

* make jump part(takes energy to load), bind to j, time out and some effect like explotion after timeout addplayer to other system. [functional part done apart from the actual jump]

* multyplayer [hard mode, dependant on code structure]
* a particle engine for explotions, engine stuff. [medium stuff] !!!

http://pygame.org/project-planes-2392-4051.html get version 0.6
* A save function ? [a sqllite file for now with sqlalchemy]
* replace the part - port system with a part - grid system [first implement part collition checking to temp eliminate problem]
* sounds also need to be in views
* put the collide logic in the things that collide, planets, floaters, parts etc. [1/2 done]
* it needs an economy not yust parts for static $$, [ harder ]
* nebula and atmosphere
* sometime in future convert the entity views to something like this:
http://www.pygame.org/project-OpenGL+Library+(glLib*)-877-.html
http://www.pygame.org/project-glLib+Reloaded-1326-4684.html
* the posibility for stations and planets to have facilitys, like bars, trading hubs, etc

side dish
==========

* minelayer part get color automaticly, fix that !!!
* a random seed for xtra fun
* some parts ont get a delta upon ejecting
* the radar range circle doesnt yet scale
* mini game explotion push stuff, space socker ?
* when opening part the radar will be reset to the ockpit radar
* time to consider a differen graph lib like gfxdraw
* draw out the design of the mini panel
* plitout parts and cargo , different files, is part cargo or cargo part ?
* see if it is posible to get part and dummy collition in parts panel !!!
* a Cockpit inherits from some classed to have initial functionality, like gyro, battery, but you cant as of yet have different energy consumptions for different parts
* the intro menu doesnt calculate with fps, and that is why the curor speed is off, fix that
* make sure a ship cant spawn in planet, count for player
* the menu binding script part is not finished, there are still raw keys in there and a cleanup is needed
* now that more keys can rebound/binded ? with the goal to bind all the keys that way, there should be the option to restrict some key rebinding or unsetting, or there is the posibility to rebind the quit key or something like that, or to rebind the menu key in the menu itself
* rework of menu active and keybindings, activemenu and active better differenciation, update part en draw part if active, the var active in toplevelpanel.
* inputscript in scripts.py should be playerinputscript, also scripts needed for chatconsole and for menu, this makes it posible to have keys for inflight and for menu command on the same key.
* the on mini tagetting field the distance to target and angle to target [done]
* player should go into univese and not into game ?
* systems now have a seperate list for planets and structures and perhaps portals, should be one list of statics !!!
* make a script that will install the requirements, like pygame, etc
* radar detects stuff when it is in the middle make it so it detects the edges or some average [first remove the part that renews the radar disk] [ok done and then some]
* implement backspace and cursor back front in input field !!!
* implement the new font
* names of ship selection should come from ship it self, if posible, intro menu !!!
* some buttons should not be rebindable ingame, like quit, menu and console
* center the text in the input box
* a slider button for the ui !!!
* make a startmenu with: start, options
* make a options menu with, sound
* make a sound menu with music volume and fx volume
* comments in code and keeping the standards
* merging the allto2dvector into master, or even replace master [ok done, aat]
* making the universe class to hold starsystems [WIP]
* making the rest of screen changeable ?, posibility to chage window with and or height ?
* instead of flippable part chage shoot direction, and mirror image, and make flipable a property of class
* more collision handeling refactor !!! [still need more refactoring]
* more to vec2d verctor work. !!! [can alwais use some work]
* zoom in out option for radar [medium mode ?] [doneish]
* weapon heat generation [easy mode]
* engines that are good for space travel but bad for landing and visaversa
* other sound for bullet impact on shield and plating and on planet
* palaxing background, the image
* make bullets that dont impact just disapear
* instead of restart directly, wait for keypress and see your lifeless ship float into the distance.
* make the camera so that it can smoothly transition from one place to another
* make the game run from the beginning, so if choosing ship and color the game is already running
* make camera translatable instead of direct snap
* the portal stargate warp dent could use some drag inside it, for temp usability
* cargo container and cargo will work as follows: cargo go's in every container on your ship. in future you can only fitt parts on your ship when on planet or structure, when container gets destroyed or dissconnected from ship you lose parts untill you are at capacity !!!
* when special key than lifebars on parts and some effect for parts that are on, or some extra type of ship info. [move drawing of arc from parts to ui] !!!
* in camera splitout functionality make a layer class for the layers that will not do the drawing but perhaps the updating, anyhow updates doesnt belong in camera ?

* ai could use some more bains and variation
* also add the chat console and menu to the camera
* when destroyed a part has a change it will become scrap [done]
* parts that disconnect/scatter have a change they will be destroyed
* adding info from weapon used on part to part, like plasma burns, impact damage etc.
* deciding what gui graphics to update:
- part menu background
- some way to texture menu borders and buttons in a dynamic way
* put certain things into threads like : update cycle and draw cycle, also the drawing of mini info panel.
* the planet's and structure's and same kind of problem, when landed one can fly into a planet and gravity can pull you from a structure, need something for that
* compile a list of games like this one to 'loan' elements from
- naev
- hardwar
- Transcendence


Housekeeping
===
* cleanup class diagram
* impost original stagdog svn

bugs
=====

* when blowing up an enemy error could happen
* cargo part doesnt update and does not accelerate fall etc. [done]
* the binded keys dont display annymore, check it out and fix. !!!
* on branch viewsinview an explotion will make another one.[so what for now]
* the laser is broken, ;( [It is fixed, Aat]
* make binding keys actually works. they bind but don't do anything. and moste of the time. it bugs out the guns so they fire randomly or continously. [it works]
* after menu and chat console prototype independance of game pause the menu will not 
* engines seem to light up nice, but the purple color of the engines doesnt color to ship color. [will be done with implementation of animated sprites class]
* known planets is a list of all the known planets not the known planets in the current system
* In case of open planet part panel and parts 'land' on planet they will not show up at the parts panel right away. only after a menu out/in
* planets should be targetable when not in radar range, couse they are remembered, still it doesnt work out that way, check it out
* processing of ship image on mini screen is a slow afair perhaps first: https://github.com/Mekire/pygame-image-outline/blob/master/outline.py and after that a thred that will fill in the ship part by part ?


parts
======

* A radar that will eventualy suport raytracing. [easy for initial radar, perhaps use laser code for raytrace]

* bigger detonation range. for mines
* a coloniser part
* a cargo part to hold the cargo
* a gravity well part.
* a dockingport part [can be hardmode]
* a disable beam part [easymode]
* ship lights [easy mode once particles is done]
* a part with a cog/chip on it that will keep a copy of the ship it is in and refreshes that every x seconds [can only read ship values, not hange them, also needs filter list on what props to make avalable, might be hardmode food for tought]
* make images for ships in the menu to choose from. [and make them better, color to shift]


unknowns
=========

* if you will travel long enough you will also reach the next solar system, as in stargate travel.
* The edge of the system is a stupid idea, and can be replaced with a: when over boundry go to next star system independent of direction, will alwais travel to next star system even is only one ajacent
* a cource line for a ship that will include gravity pulls. [depends on simulator ception]
* astroids in orbits (hard mode, depends on quad trees)
* test if planet orbit is posible and if no what is needed to make it so !
* a orbit calculator so your ship can go into orbit [depends on simulator ception]
* simulator ception for calculation of trajectorys, targeting and future positions [hard ?]
* imports in methods, do we want that ? [cant always find a way around that]



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
* remember planets that where on radar in list [done , aat]
* some way to target ships, parts and planets [easy mode,done Aat]
* a name to give yourself [as a precursor of network play and to get familiair with gui, after view spitout and vectors] [gui is not nice, but overhaul costs to much time, lets keep it for now, Done Aat]
* a camera to capture different places, in stead of only player. [done and then some, aat]
* give ships a atention score that goes up when ships are sooting and dying, drops off over time. [done, aat]
* make the color of the color of the star dependant on the size of the star, bigger is blueer, smaller redisher [done could use some tweaking]
* the engines dont animate after radar addition, meh [ok this was a timing problem , when more code time in programm passes differently, it was done in a messy way, this will come back in a different form and place, fixed this however, ok done]
* Canons don't work anymore they don't shoot. [done , aat] 
* putting a engine on a radar "part" it doesn't fire [done aat].
* putting an engine on crew quarters part it doesnt fire [done aat]
* radar will still work when there is no energy [done, aat]
* remove the self.kill(other) thing see master branch, this is not working should be other way of both coliders to know about each other. [done, aat]
* I can make a crash by blowing up my own ship in missile difference collision on branch * all2vector [Fixed Aat]
* engines will sometimes not fire in case of multyple forward. [fixed , Aat]
* show info, skills etc the right way. [fixed aat]
* still cant land on strucutre class. [fixed Aat]
* radar enabled states are seperate, should be synced ? [done, aat]
* more randomization of enemy ships [done, 2 x extra ships]
* Make mine's de accelerate till they hit their target spot
so you can get out of the way in time. [done, aat]
* implement game time in menu, some fictional time [done, could perhaps use a reference future date]
* mke sure planets have a minimum distance from each other [done]
* in case of button pressed when you open menu, the ship will continue to do that action. [done, for now]
* when ejecting parts planet inventory will not put them at 0 degrees when caught [done]
* when in console up / down to browse history [done]
* draw planets over things like explotions, and other ships. [done]
 improve name input with a box around name [done]
 * rename solarsystems to starsystems sun to stars etc [done]
 * landed can go to ship class so the ai can do extra stuff [done]

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
or only give the destroyer that capability? [implemented by duality the mine laying device part]
* display ship stats closer to the ship like health energy xp bar can stay where it is? [yes health bars can stay where they are, need to look better tho, aat, enemy health bars can be removed]
* make a scout ship [done duality] 
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
