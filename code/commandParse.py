from types import *
from spaceship import *
from parts import *
from vec2d import Vec2d
from SoundSystem import *
import sys
import os

# try and import tools for memory usage reporting.
# so these will not be imported if not installed and will not mess up the
# system.
try:
    from pympler import summary
    from pympler import muppy
    from pympler import tracker
    import types as Types
    all_objects = muppy.get_objects()
    tr = tracker.SummaryTracker()
except Exception as e:
    print(e)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WHITE = '\033'


class AttrFilter(object):
    def __init__(self):
        parseFilterInput = "parseFilter.txt"
        path = os.getcwd()+"/code/"+parseFilterInput
        self.fconfig = open(path, "r")

    def getFiltered(self):
        filtered = []
        for line in self.fconfig.readlines():
            # remove \r\n from input.
            line = ''.join(line.split())
            filtered.append(line)
        return filtered


class CommandParse(object):
    helpText = [
                "!help [shows this help text]\n"
                "!print <object...> <attributes> <...> [for example: !print game.player , or !print game.averagefps ]\n"
                "!printPymplerStats [prints listings and sizes for objects] \n"
                "!set <object.attr> <value> [sets object attribute to value]\n"
                "!reload [invokes a reload of the command parse code. so coding is easier and can be tested while in game]\n"
                "!exit [exits the game]\n"
                "!insertPart <part> <amount> [inserts a amount of parts into the players inventory]\n"
                "!parts [lists parts available W.I.P]\n"
                "!removeItem <part> <amount> [removes a amount of parts from the player inventory W.I.P]\n"
                "!func <code> [runs python code] \n"
                "!setTextColor <color> [sets the print out text to color in formate (r,g,b) \n"
                "!setShipColor <color> [colors your ship to the specified color W.I.P]\n"
                "!convertShip <ship type> [convert your ship to ship type W.I.P]\n"
                "!printdbg [toggles debug printing to the ingame console]\n"
                "!setSfxVolume <0-100> [set all sfx sound volume e.g. bullets]\n"
                "!setMusicVolume <0-100> [set music volume ]\n"
    ]

    def __init__(self, game, chatconsole, messenger):
        self.game = game
        self.player = game.player
        self.messenger = messenger
        self.chatconsole = chatconsole

        self.textColor = (244, 244, 200)
        # a reference to a function that gets the text from the chatconsole
        self.getText = self.chatconsole.console.inputfield.getText
        # a reference to a function that is able to set that text.
        # for for example auto complete (future)
        self.setText = self.chatconsole.console.inputfield.setText
        self.text = []
        self.reload = False
        self.debug = False

    def setSfxVolume(self, args):
        if not args:
            return
        volume = eval(args[0])
        setSFXVolume(volume)
        print("sfx vol:"+str(SFX_VOLUME))

    def setMusicVolume(self, args):
        if not args:
            return
        volume = eval(args[0])
        setMusicVolume(volume)
        print("music vol:"+str(MUSIC_VOLUME))

    # prints pympler stats.
    def printListingUsage(self, args):
        all_objects = muppy.get_objects()
        sum1 = summary.summarize(all_objects)
        summary.print_(sum1)
        print(" ")
        print("Summary: ")
        tr = tracker.SummaryTracker()
        tr.print_diff()

    def setColor(self, args):
        if not args:
            return
        self.textColor = eval(args[0])

    def setShipColor(self, args):
        if not args:
            return
        raise Exception("Exception: not implemented yet")

    def convertShip(self, args):
        shipType = args[0]
        if shipType == "Scout":
            pass
        raise Exception("Exception: Not implemented.")

    def insertPart(self, args):
        if not args:
            return
        part = None
        amount = 1
        if len(args) == 1:
            part = args[0]
        else:
            part, amount = args[0], int(args[1])
        self.player.insertPart(eval(part), amount)
        self.printout("inserted %d %s's into inventory." % (amount, str(part)))

    def handleInput(self, event):
        pass

    def printout(self, text):
        text = str(text)
        if '\n' in text:
            text = text.split('\n')
            for item in text:
                self.messenger.message(str(item), self.textColor)
        else:
            self.messenger.message(str(text), self.textColor)
    # print a single value,
    # also check if that value is in the filter list.
    # if so don't print it.

    def printAttrVal(self, attribute, value):
        # attrfilter = AttrFilter()
        filtered_list = AttrFilter().getFiltered()
        if str(attribute) not in filtered_list:
            self.printout(str(attribute)+" = "+str(value))

    def printAttributes(self, obj):
        for element in obj.__dict__:
            self.printAttrVal(element, obj.__dict__[element])

    def execFunc(self, args):
        try:
            exec(' '.join(args))
        except Exception as e:
            self.printout(e)

    def printFunc(self, args):
        if not args:
            return
        try:
            args = args[0].split('.')
            attribute = getattr(self, args[0])
            last_argument = args[-1:][0]
        except:
            self.printout("invalid input")
            return
        # if only one argument just print that ones value or attribute list.
        if len(args) == 1:
            try:
                self.printAttributes(attribute)
            except Exception as e:
                self.printAttrVal(last_argument, getattr(self, last_argument))
        # else if we got more arguments traverse list
        # and print value/attribute list.
        else:
            for index in range(1, len(args)-1):
                attribute = getattr(attribute, args[index])
            try:
                self.printAttributes(getattr(attribute, last_argument))
            except Exception as e:
                self.printAttrVal(last_argument,
                                  getattr(attribute, last_argument))
        self.printout("")

    def setFunc(self, args):
        if not args:
            return
        try:
            # split the attributes
            temp = args[0].split('.')
            temp.append(args[1])
            # rejoin the attributes with the arguments.
            args = temp
        except:
            self.printout("Invalid input")
            return
        attribute = getattr(self, args[0])
        last_argument = args[-1:][0]
        sec_last_argument = args[-2:][0]

        if len(args) == 2:
            setattr(attribute, sec_last_argument, eval(last_argument))
        else:
            for index in xrange(1, len(args)-2):
                attribute = getattr(attribute, args[index])
                self.printout("attr: %s, arg: %s" % (str(attribute),
                              args[index]))
            setattr(attribute, sec_last_argument, eval(last_argument))

    def update(self):
        # get console input
        text = self.getText()
        if text:
            try:
                # if the first character is a ! then it's a command
                if text[0] == '!':
                    # remove the ! and split the text up in a list of words.
                    text = text[1:].split(' ')
                    # remove any to many spaces. or empty slots.
                    while '' in text:
                        text.remove('')
                    # extract the command from the text.
                    command = text[0]
                    # extract arguments.
                    # if arguments available.
                    if len(text) > 1:
                        args = text[1:]
                    else:
                        args = None

                    if command == 'print':
                        self.printFunc(args)
                    elif command == 'printPymplerStats':
                        print "this"
                        self.printListingUsage(args)
                    elif command == 'set':
                        self.setFunc(args)
                    elif command == 'func':
                        self.execFunc(args)
                    elif command == 'reload':
                        self.printout('reload invoked')
                        self.reload = True
                    elif command == 'exit' or command == 'quit':
                        self.game.running = False
                    elif command == 'help':
                        for text in self.helpText:
                            self.printout(text)
                    elif command == "insertPart":
                        self.insertPart(args)
                    elif command == "setSfxVolume":
                        self.setSfxVolume(args)
                    elif command == "setMusicVolume":
                        self.setMusicVolume(args)
                    elif command == "removeItem":
                        pass
                    elif command == "setTextColor":
                        self.setColor(args)
                    elif command == "setShipColor":
                        self.setShipColor(args)
                    elif command == "convertShip":
                        self.convertShip(args)
                    elif command == 'printdbg':
                        self.debug = not self.debug
                    else:
                        self.printout("Invalid input.")

                    if self.debug:
                        self.printout("input: %s \ncommand: %s \narguments: %s"
                                      % (text, command, args))

                else:
                    self.printout(self.player.firstname + " " +
                                  self.player.secondname + ": "+text)
            except Exception as e:
                # self.printout(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(e)
                print(exc_type, str(fname)+":"+str(exc_tb.tb_lineno))
