from types import *
from utils import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WHITE = '\033'

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

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
        #a reference to a function that gets the text from the chatconsole
        self.getText = self.chatconsole.console.inputfield.getText
        #a reference to a function that is able to set that text.
        #for for example auto complete (future)
        self.setText = self.chatconsole.console.inputfield.setText
        self.text = []
        
    def handleInput(self, event):
        pass
    
    def printout(self, text):
        #if '\n' in text:
        #    text = text.split('\n')
        #    for item in text:
        #        self.messenger.message(str(item), (244,244,200))
        #else:
        self.messenger.message(str(text), (244,244,200))
        
    def printAttrVal(self, attribute, value):
        self.printout(str(attribute)+" = "+str(value))
        
    def printAttributes(self, obj):
        for element in obj.__dict__:
            self.printAttrVal(element, obj.__dict__[element])
            
    def update(self):
        #get console input
        text = self.getText()
        if text:
            try:
                #if the first character is a ! then it's a command
                if text[0] == '!':
                    #remove the ! and split the text up in a list of words.
                    text = text[1:].split(' ')
                    while '' in text:
                        text.remove('')
                    #extract the command from the text.
                    command = text[0]
                    #extract a list of arguments.
                    args = text[1:]
                    #self.printout("input: %s \ncommand: %s \narguments: %s"%(text, command, args))
                    if command == 'print':
                        if not args:
                            return
                        attribute = getattr(self, args[0])
                        last_argument = args[-1:][0]
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
                    elif command == 'func':
                        print ' '.join(args)
                        exec ' '.join(args)
                    elif command == 'set':
                        if not args:
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
                    elif command == 'reload':
                        self.printout('reload invoked')
                    elif command == 'exit' or command == 'quit':
                        self.game.running = False
                    elif command == 'help':
                        for text in self.helpText:
                            self.printout(text)
                    elif command == 'printdbg':
                        self.printout("input: %s \ncommand: %s \narguments: %s"%(text, command, args))
                else:
                    self.printout("me: "+text)
            except AttributeError, e:
                print e
