BEFORE WE CONTINU THIS NEEDS TO BE DONE
========================================
1 write documentation for all functions and classes
2 write tests for parts and floaters
3 put txt files in a separate dir [done]
4 remove all global class variables (there is a proper name for this) (Ship in code/spaceship.py next)
5 make sure code doesn't run on imports [done, utils can stay the way it is]


INTRODUCTION STUFF
====
Things you can do if you want to start devving for stardog, easy stuff.
find a part that has to be made from this file and make it.(code/parts.py)
tweak the particles that come from damaged parts.(code/parts.py)
add particles to the gateways.(code/planets.py)
make a ship to choose in the beginning. (code/spaceship.py, code/menus.py)
Update this text file, put the this that are done from main dish en side dish in the done part
make a one or two graphics for the cargo, with the magic pink real below
make a story trigger (code/dialogs.py) based on your own condition (code/plot.py) perhaps ship damage
Bonus: make a second set of color bars in the intro menu and give ship parts a secondary color.
(code/menu.py, code/spaceship.py)
Bonus: make tests for plot.py and dialogs.py




main dish
==========

(warning this file could describe things in faul language, cursing and poor grammar !)

* quad trees (hardmode, after vector and view split-out, will replace current collision check mess)

* wormholes/star gates to other systems. (medium mode ?, after Gravless class) [can travel to other star systems via direct travel now, star gates next] [done]

* make jump part(takes energy to load), bind to j, time out and some effect like explosion after timeout addplayer to other system. [done]

* make everything looser coupled, it seems everything is dependent on game for some reason, this should be avoided and factored, lets begin with the following classes.
# particles (done)
# parts (done)
# floaters (done)
# planets (done)
# starsystem (done)
# camera should be part of universe [done]


* multi-player [hard mode, dependent on code structure] !!
http://pygame.org/project-planes-2392-405.html get version 0.6
* A save function ? [a sqllite file for now with sqlalchemy]
* replace the part - port system with a part - grid system [first implement part collition checking to temp eliminate problem]
* sounds also need to be in views ?
* put the collide logic in the things that collide, planets, floaters, parts etc. [1/2 done]
* it needs an economy not yust parts for static $$, [ harder ]
* nebula and atmosphere
* sometime in future convert the entity views to something like this:
http://www.pygame.org/project-OpenGL+Library+(glLib*)-877-.html
http://www.pygame.org/project-glLib+Reloaded-1326-4684.html
* the possibility for stations and planets to have facility's, like bars, trading hubs, etc [initial facility's, shop, refitter, smelter]
* power management system for propulsion, weapons, shields and sensors

side dish
============
* remake the lineout functionality [done]
* InputField had drawing stuff in update put it in draw [done]
* jump portals different colors to show in what system you have transported to (the wormhole thing y)
* make the color shifter able to shift from other color than magic pink [done]

* part attach blocker doesn't give feedback, should say something like parts overlap so no place
* make the color shifter able to shift from other color than magic pink [done]
* make the planet textures into more magic colors and shift them from planet primary color and secondary color
* if floater reaches edgerad also make it go from one system to another so split camera and player specific functionality from only floater functionality
* make sure part inherit from cargo, [todo]
* a text scroll panel that will show text scrolling down (if that is a thing) perhaps with some effect of fade in and out. [done - fade in out]
* a function that could get called on a panel move in of out of panel, like a help on moveover element there is a official name for such an element but i be damned if i know.
* what to do with the mouse hover branch [delete it]
* make a function in game or stardog that will check the version of game of stardog in the github repo, if repo is newer give instructions how to update via installer. [done]
* the ui margins and locations should be dependent on camera size and location ?
* ai can use an fsm to flee attack, explore [using simplefsm] [initial ai states, atack, flee, idle]
* make 2 gateways in the start system to test jumping [done]
* make text able to left center right line-out [done]
* does ship still need hp is not all hp contained in the parts ? parts have hp cockpit has hp, so do we ned ship hp.
* a sentence construction kit for the ai so it can taunt you for example
* plot triggers wont retrigger of don't have the option to. !!
* partcount in menu doesn't show the actual part limit. [Done]
* a list in a ship of who is targeting you. targeting target should not go into player or enemy but in ship !!
* there are good points to use turrets with modules on it, like weapons on turrets, shields on turrets and engines on it.[after chip ai stuff implementation]
* make sure that enabled is a property of part not of subparts/classes !!
* does a ship has a reference to the current star-system if no does it need one [no done]
* the console , input chat console panel hierarchy is a bit much !!
* really a better way to reset stuff on death, like radar error thing, engine trust should be off menus all inactive !!!
* a game intro screen [done]
* make a screen effect class, that will flash the screen white or something, for jump effect
* ai can talk to player, when targeting player for example and disengaging [after FSM and better brains ai, and sentence construction kitt]
* a ai that trys to collect parts and deposit them on his planet [after smarter ai]
* an small adaptation that makes this standout from other stardog. The accounting software  [NovaBlasters it is for now]
* make the screen-shots have a incremental number like : screenshot-1, screenshot-2, etc [done]
* make factory's for planets starsystems and ships, the design pattern [after multi-player]
* a random seed for extra fun !!
* split out parts and cargo ,different files, part inherits from cargo !!
* a Cockpit inherits from some classed to have initial functionality, like gyro, battery, but you cant as of yet have different energy consumptions for different parts
* the menu binding script part is not finished, there are still raw keys in there and a cleanup is needed [done]
* some sessions of bug hunting !!
* some buttons should not be rebind-able in game, like quit, menu and console
* make a start menu with: start, options [done]
* make a options menu with, sound [done]
* make a sound menu with music volume and fx volume [done]
* commenting code !!!
* instead of flippable part change shoot direction, and mirror image, and make flippable a property of class

* more to vec2d vector work. [almost done]
* engines that are good for space travel but bad for landing and visa versa
* other sound for bullet impact on shield and plating and on planet !!!
* instead of restart directly, wait for key press and see your lifeless ship float into the distance. !!
* make the camera so that it can smoothly transition from one place to another
* make the game run from the beginning, so if choosing ship and color the game is already running !!
* cargo container and cargo will work as follows: cargo go's in every container on your ship. in future you can only fit parts on your ship when on planet or structure, when container gets destroyed or disconnected from ship you lose parts until you are at capacity. [done]
* in camera split out functionality make a layer class for the layers that will not do the drawing but perhaps the updating, anyhow updates doesn't belong in camera ? [take from multi-player branch and put in master branch] !!!

* adding info from weapon used on part to part, like plasma burns, impact damage etc. [a list of 3 things that append last, future plans]
* deciding what GUI graphics to update:
* put certain things into threads like : update cycle and draw cycle, also the drawing of mini info panel.
* a globe image for planet that is transparent and go's over planet circle, some scaling needed 5 or so images.
* a shadow for a planet in the night side
* change font for things that need be read like chat. or part details.
* compile a list of games like this one to 'loan' elements from
- naev
- hardwar
- Transcendence
- void infinity
- independance war II

* use inno setup to maker this game runnable on windows [done]
* make a tag on github that the inno setup gets the game from [done]
* make inno setup run a python and pygame test after install and return a good or bad install !
* put the inno setup script in the git repo [done]
* FunctionLabel need to have a color option !!!


bugs
=====
* explosions and impact clouds are subject to gravity, should not be. [done]
* parts that get targeted will not showup in the mini info [done]
* parts that can stack after flip don't stack or don't go from ship in inventory, strange stuff, test it
* the impact clouds are killing [done]
* somewhere in console there is a max, text field length that is reached to soon [done]
* the slider part is still not slid-able [done]
* pure black should not be a color to choose ship from  [done]
* particle emitters don't have the exact right position in case of part [done]
* putting engines on cockpit and perhaps other parts off ship will prevent the engine of fingering.
* trust of engine has the direction of ship not of slot of part [todo !!!]
* if part targeted and picked up it still exists on target screen  [done]
* still cant rebind keys
* particles also alter delta of part they come from, fix that
* slider buttons should have the option for min max that also should be guarded [done]
* part damage screen HUD has names of parts that are too long, fixit [done]
* radar range wrong radar radius when in and out of menu, chekout [done]
* remove the big radar display, until we have the small display down, then put it in again [done]
* invalid rect assignment bug somewhere same as explosion
* when blowing up an enemy error could happen
* cargo part doesn't update and does not accelerate fall etc. [done]
* the binded keys don't display anymore, check it out and fix. [well they display, but dont bind]
* on branch viewsinview an explosion will make another one.[so what for now]
* the laser is broken, ;( [It is fixed, Aat]
* make binding keys actually works. they bind but don't do anything. and most of the time. it bugs out the guns so they fire randomly or continuously. [it works, done]
* after menu and chat console prototype independance of game pause the menu will not ??? [done]
* engines seem to light up nice, but the purple color of the engines doesn't color to ship color. [will be done with implementation of animated sprites class]
* known planets is a list of all the known planets not the known planets in the current system [done]
* In case of open planet part panel and parts 'land' on planet they will not show up at the parts panel right away. only after a menu out/in
* planets should be target-able when not in radar range, course they are remembered, still it doesn't work out that way, check it out [done]
* processing of ship image on mini screen is a slow affair perhaps first: https://github.com/Mekire/pygame-image-outline/blob/master/outline.py and after that a thread that will fill in the ship part by part ? [done in another way]
* cockpits are named part [so? their name's do show up now so Done ? ]
* damage calculation for health bars is bad now
* ai doesnt update anymore (in what way? Duality)
* massive memory leak (is fixed) [Done]


parts
======

* A radar that will eventual support ray tracing. [easy for initial radar, perhaps use laser code for ray-trace]
* bigger detonation range. for mines
* a colonizer part
* a cargo part to hold the cargo [Done]
* a gravity well part.
* a docking port part [can be hard-mode]
* a disable beam part [easy mode]
* ship lights [easy mode once particles is done]
* a part with a cog/chip on it that will keep a copy of the ship it is in and refreshes that every x seconds [can only read ship values, not change them, also needs filter list on what props to make available, might be hardmode food for tough]
* make images for ships in the menu to choose from. [and make them better, color to shift]


unknowns
=========

* if you will travel long enough you will also reach the next solar system, as in Stargate travel.
* The edge of the system is a stupid idea, and can be replaced with a: when over boundary go to next star system independent of direction, will always travel to next star system even is only one adjacent
* a course line for a ship that will include gravity pulls. [depends on simulator ception]
* asteroids in orbits (hard mode, depends on quad trees)
* test if planet orbit is possible and if no what is needed to make it so !
* a orbit calculator so your ship can go into orbit [depends on simulator ception]
* simulator ception for calculation of trajectory's, targeting and future positions [hard ?]
* imports in methods, do we want that ? [cant always find a way around that]



DONE
====
* test if solar orbit is possible, [solar orbit is possible did it twice (duality)]
* finite engine trust speed [it is done, can be tweaked, but is done (Aat)]
* revamp to use vectors [as good as done Aat]
* every planet own part list, nope but fixed [Aat fixed it]
* fixing a bug that made memory leak during the drawing of the star map (duality)
* split-out views [nasty stuff] [as good as done, for now i want no part of it Aat]
* we have parts not that can be toggled on or off, like the radar, no none asked for it still did it [Aat]
* Space mines [easy mode] [Duality]
make menu work on full-screen. only fighter is displayed right left corner. [fixed Duality]
* and parts for crew quarters. [part added]
* make the space structure class that will inherit from gravless as well with a custom  [done in other way]
* possibility to eject parts [easy mode, done aat]
* make planet inherit from a Gravless class so star-gate will not be effected by graf [done in another way]
* removed names from the code, duality, your name can go here !
* remember planets that where on radar in list [done , aat]
* some way to target ships, parts and planets [easy mode,done Aat]
* a name to give yourself [as a precursor of network play and to get familiar with GUI, after view spitout and vectors] [gui is not nice, but overhaul costs to much time, lets keep it for now, Done Aat]
* a camera to capture different places, in stead of only player. [done and then some, aat]
* give ships a attention score that goes up when ships are sooting and dying, drops off over time. [done, aat]
* make the color of the color of the star dependent on the size of the star, bigger is bluer, smaller redisher [done could use some tweaking]
* the engines dont animate after radar addition, meh [ok this was a timing problem , when more code time in program passes differently, it was done in a messy way, this will come back in a different form and place, fixed this however, ok done]
* Canons don't work anymore they don't shoot. [done , aat] 
* putting a engine on a radar "part" it doesn't fire [done aat].
* putting an engine on crew quarters part it doesn't fire [done aat]
* radar will still work when there is no energy [done, aat]
* remove the self.kill(other) thing see master branch, this is not working should be other way of both coliders to know about each other. [done, aat]
* I can make a crash by blowing up my own ship in missile difference collision on branch * all2vector [Fixed Aat]
* engines will sometimes not fire in case of multiple forward. [fixed , Aat]
* show info, skills etc the right way. [fixed aat]
* still cant land on structure class. [fixed Aat]
* radar enabled states are separate, should be synced ? [done, aat]
* more randomization of enemy ships [done, 2 x extra ships]
* Make mine's de accelerate till they hit their target spot
so you can get out of the way in time. [done, aat]
* implement game time in menu, some fictional time [done, could perhaps use a reference future date]
* make sure planets have a minimum distance from each other [done]
* in case of button pressed when you open menu, the ship will continue to do that action. [done, for now]
* when ejecting parts planet inventory will not put them at 0 degrees when caught [done]
* when in console up / down to browse history [done]
* draw planets over things like explosions, and other ships. [done]
 improve name input with a box around name [done]
 * rename solarsystems to starsystems sun to stars etc [done]
 * landed can go to ship class so the ai can do extra stuff [done]
 * systems now have a separate list for planets and structures and perhaps portals, should be one list of statics [done]
 * the on mini tagetting field the distance to target and angle to target [done]
 * when destroyed a part has a change it will become scrap [done]
* a particle engine for explosions, engine stuff. [medium stuff] [done]
* a slider button for the ui [done]
* move drawing of arc from parts to ui [done]
* implement backspace and cursor back front in input field [done]
* radar and gui are one thing should be two separate things. [done]
* a selection box for targeted floaters on radar and on main screen [done]
* need a file with all the theme's colors to use [done]
* put laser one one color, perhaps same as the plasma cannon colors [done lasers are green now]
* a arrow on radar when targeting a known planet that is out of radar reach. [done]
* the radar range circle doesn't yet scale [done]
* when opening part the radar will be reset to the cockpit radar [done]
* make some formula to convert the pix into m, km  something like that [done 1000 px is 100 km now from floater rim to floater rim, all the rimming all the time]
* make sure a ship cant spawn in planet, count for player [done]
* now that more keys can rebound/binded ? with the goal to bind all the keys that way, there should be the option to restrict some key rebinding or unsetting, or there is the possibility to rebind the quit key or something like that, or to rebind the menu key in the menu itself [done, you cant rebind menu keys ingame only shipping keys]
* names of ship selection should come from ship it self, if possible, intro menu [done]
* merging the allto2dvector into master, or even replace master [ok done, aat]
* zoom in out option for radar [medium mode ?] [done]
* parts that disconnect/scatter have a change they will be destroyed [done]
* the targeting reticule of a selected part of ship should go over planet etc in radar. [done]
* the ai should abide by its own radar range [done, it is still as stupid as can be]
* remove fps measurement and make an average fps for in game, can be read with console [done]
* place energy and xp bars in separate rectfrom rest og gui [done]]
- part menu new background [done]
- tryout a 45 angle on a menu corner [done]
* make bullets that don't impact just disappear [done]
* make sure all the hud elements have a way to be easily re/positioned [yes all drawable have a set_rect method, done]
* see if it is possible to get part and dummy collision in parts panel [done]
* center the text in the input box [done]
* implement the new font [done]
* add some screen shots to the github repo [done]
* make a detection score for a ship, based on the parts, that also need a detection score. [remove totalhp from shipdamage indicatiors and put it in ship, this will be detection score] [done]
* the intro menu doesn't calculate with fps, and that is why the cursor speed is off, fix that done, ugly but done
* all variables if possible in class and not a class global
* remove the shield indication arc and put it on gui. [done]
* make it so that gravity doesn't count when distance from star greater than bound-rad [done]
* a button to make screen shots [done]
* place all menu elements in menuelements.py instead of menu for example [ok nothing wrong here menu has all the menu element compositions, and menu elements all the menu elements, done]
* time to consider a different graph lib like gfxdraw [we did, but we not gonna do it !, ha, done]
* rework of menu active and keybindings, activemenu and active, better differentiation, update part and draw part if active, the var active in toplevelpanel. [done]
* inputscript in scripts.py should be playerinputscript, also scripts needed for chat console and for menu, this makes it possible to have keys for in-flight and for menu command on the same key. [done it is possible]
* making the universe class to hold star systems [done]
* the planet's and structure's and same kind of problem, when landed one can fly into a planet and gravity can pull you from a structure, need something for that [can fix that by making planets ignore floters that are landed unless landed on self] [done]


[Duality]

Progress Bar
=====
* in updater.py show a progress bar, opening a request is fast, downloading with url.read() takes a long time.
* thus place a progress bar there. the placing of files and folders is also done in under a second.

Energy Rerouting.
=====
* like when the laser drains your energy, and then goes on to drain your shields.
* and that you have the ability to reroute power to certain places.

Trading drones
=====
* drones that fly between ships and or planets that are able to trade things.
* see a teleporter would be no fun. this way you got vulnerable drones/shutles.
* if they are destroyed you lose trading capabilities.

Progress Download Source
=====
* make a implementation of the installer.py where it show the progress.
* inspiration: http://stackoverflow.com/questions/2028517/python-urllib2-progress-hook

Creative mode
=====
* implement a creative mode, so testing is easier.

Part making system (code)
=====
* thinking of a way to make a better part system, where you just make parts in parts.py
* and it automatically adds it to the adjectives and such. 
* it´s now just make part add to adjectives array and that one class with attributes thing.

So currently reflecting on the parts code. specifically adjectives.py
and i am wondering a few things that might be better.
At say for example line 29 (ENERGY_USING is list of parts)
shouldn´t a part know of it´s self if energy using.
like attribute of part energy_using = True or something.
and besides that don´t all parts use energy, what parts don´t?
plasma bullets do, rockets don´t ? 

and besides that, on line 33 you have types = [] list of parts.
shouldn´t a part know of it´s self what part type it is?
would make things easier ? if part new if it could have a adjective?

Commanline interface
=====
* convert all oldstyle classes into new style that is easier to check with type() [done]
* a command line interface for manipulating the world so that testing is faster. [W.I.P]

* make command interface check against a list of keys that it may ignore for printing or using.
- a command to add parts to a ship [Done]
- a command to change name of ship
- a command to add parts to planets [Done but parts appear in ship inventory]
- a command to spawn enemy ships
- a command to kill all enemy's
- a command to manipulate your camera (need work)


crew [done]
=====
* add crew?
* more crew more efficient ship.
* maybe if crew then heal x per x seconds.
* crew quarters gives you more crew thus faster healing.

bays
=====
* a part that is a cargo bay, bigger bay more part that can be carried [Done]
- make the gargohold hold parts, instead of that it just increases the size of parts that can be kept in the ship.
- for example you find a abandoned gargohold and it has nice goodies in it :)
* gargholds are very well suited for plot twists, you'll never know what is inside till you pick it up.
* and enemy could be inside, or poisonous things. or radio active things. or other things. you get the point.

* mechBay for forging stuff like parts and gun  and like that. 

Freighter [done]
=====
* use destroyer cockpit.
* from the sides of cockpit interconnects with an engine on the back side of interconnect, and a tail of cargo containers.
* [build it now if any needs to be changed will see.]

ship
=====
* every ship a individual mid section that defines what the ship is.
* implement dropping mines and implement a part for it that does that?
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
* make mass count more realistically. it's not just counted in to heavy.
key-handling:
* some key combinations don't work in menu or other parts of the game.
* thus make key-handling for quiting (for example) be interrupt based.

* if part die/are killed damage vehicle/ship

* particle engine for effects.
