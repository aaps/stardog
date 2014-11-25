Stardog readme.txt

Stardog, by Shanti Pothapragada
rgbdreamer@gmail.com
http://code.google.com/p/stardog


To run stardog, use:
python stardog.py
or
python stardog.py mode x y

where mode is f for fullscreen, w for windowed, at resolution x,y.  Omit x,y for max resolution. 
Stardog requires Python 2.6ish and Pygame.  Stardog will run faster if Psyco is installed.
(This assumes python is in your path variable.)

Controls:

Enter: menu
Tab: radar
Del: self-destruct
wasd/arrows: thrust and turn
q/e: strafe
ctrl: shoot
space: launch missiles
Mouse: move to turn, left click to shoot, right click to thrust

Keys can be changed in the menu. If you want to use the keyboard, you should probably disable mouse control in the keys menu (otherwise your ship will keep turning towards the mouse).

This is still pre-alpha code.  I'm releasing it with hopes of attracting critism and contributers.
If you are interested in contributing to the code, graphics, art, AI, plot, etc., please email me.

This source is given only under the GPL General Public License.  If you are interested in other licensing, please contact me. 


CHANGES:
since 0.2011.01.18:
Adds stores to planets.  When landed on a planet, you can trade with it.  Each planet starts with a few random parts, and keeps any parts that fall into it from space.  Currently, there is no money, so "trading" is more like giving and taking.
Fixes several PartsMenu errors.
Parts menu layout changed.
Parts now drag and drop onto the selected part, like you would expect.
Destroyer is longer.
Left or Right parts can now be flipped.
Adds background image.
Adds message system.
Adds trigger-based scripting system. 

since 0.2011.01.14:
Separate Fighter, Destroyer, and Interceptor types!
Type chooser added to intro menu.  Intro menu shows after each death.
Adds Flak Cannons and smaller Fighter Shields. 
Missiles mapped to the spacebar by default.
SolarSystem is now smaller.  So is the sun.  There are boundaries that stop the ship, and a warning is shown when trying to pass them.
Gyroscope made smaller.

since 0.2010.11.30:
Player's parts no longer fall off when hit. (Enemies' still do.)
Lasers!
Missiles!
Explosions push back ships. 
Cockpits now generate energy, store energy, and can turn the ship.  Only a tiny bit of each.  Before a ship that lost a generator, battery, or gyro was useless.  Cockpits still cannot thrust (so keep a spare engine handy!).
Parts menu drag-and-drop interface fixed & added.  This interface is much, much easier to use. Description panels update imperfectly.


since 0.2010.11.20:
Adds mouse control.  Click to shoot, right click to thrust.  Can be disabled in Keys menu. 
Ship loses efficiency if it has more than 10 parts. 
Fighters drop a variety of items, but with low-level adjectives. 
Fighters tweaked. 
ctrl-q or alt-F4 to quit (instead of ESC).


