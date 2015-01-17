from types import *
from spaceship import playerShip
from vec2d import Vec2d
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WHITE = '\033'

# RED = (255,0,0)
# GREEN = (0,255,0)
# BLUE = (0,0,255)

class AttributeFilter(object):
    def __init__(self):
        pass
    def getFilteredList(self):
        pass

class CommandParse(object):
    helpText = [
    "!print <object...> <attributes> <...>\n"
    "wil print all the atributes of the object\n"
    "or atributes specified, and or the elements\n"
    "in that atributes list\n"
    ]
    
    def __init__(self, game, chatconsole, messenger):
        self.game = game
        self.player = game.player
        self.messenger = messenger
        self.chatconsole = chatconsole
        self.textColor = (244,244,200)
        #a reference to a function that gets the text from the chatconsole
        self.getText = self.chatconsole.console.inputfield.getText
        #a reference to a function that is able to set that text.
        #for for example auto complete (future)
        self.setText = self.chatconsole.console.inputfield.setText
        self.text = []
        self.reload = False
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
        self.game.player = playerShip(self, Vec2d(0,0),Vec2d(0,0),
                            color = self.game.playerColor, name = self.game.PlayerName, type = self.game.playerType)
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
        
    def printAttrVal(self, attribute, value):
        self.printout(str(attribute)+" = "+str(value))
        
    def printAttributes(self, obj):
        for element in obj.__dict__:
            self.printAttrVal(element, obj.__dict__[element])
        
    def execFunc(self, args):
        try:
            exec ' '.join(args)
        except Exception, e:
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
        #if only one argument just print that ones value or attribute list.
        if len(args) == 1:
            try:
                self.printAttributes(attribute)
            except Exception, e:
                self.printAttrVal(last_argument, getattr(self, last_argument))
        #else if we got more arguments traverse list and print value/attribute list.
        else:
            for index in range(1, len(args)-1):
                attribute = getattr(attribute, args[index])
            try:
                self.printAttributes(getattr(attribute, last_argument))
            except Exception, e:
                self.printAttrVal(last_argument, getattr(attribute, last_argument) )
        self.printout("")
    
    def setFunc(self, args):
        if not args:
            return
        try:
            temp = args[0].split('.') #split the attributes
            temp.append(args[1])
            args = temp #rejoin the attributes with the arguments.
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
                self.printout("attr: %s, arg: %s"%(str(attribute), args[index]))
            setattr(attribute, sec_last_argument, eval(last_argument) )
    
    def update(self):
        #get console input
        text = self.getText()
        if text:
            try:
                #if the first character is a ! then it's a command
                if text[0] == '!':
                    #remove the ! and split the text up in a list of words.
                    text = text[1:].split(' ')
                    #remove any to many spaces. or empty slots.
                    while '' in text:
                        text.remove('')
                    #extract the command from the text.
                    command = text[0]
                    #extract arguments.
                    #if arguments available.
                    if len(text) > 1:
                        args = text[1:]
                    else:
                        args = None
                    #self.printout("input: %s \ncommand: %s \narguments: %s"%(text, command, args))
                    if command == 'print':
                        self.printFunc(args)
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
                    elif command == "insertItem":
                        pass
                    elif command == "removeItem":
                        pass
                    elif command == "setTextColor":
                        self.setColor(args)
                    elif command == "setShipColor":
                        self.setShipColor(args)
                    elif command == "convertShip":
                        self.convertShip(args)
                    elif command == 'printdbg':
                        self.printout("input: %s \ncommand: %s \narguments: %s"%(text, command, args))
                    else:
                        self.printout("Invalid input.")
                else:
                    self.printout(self.player.firstname + " " + self.player.secondname +": "+text)
            except Exception, e:
                self.printout(e)
                print e
