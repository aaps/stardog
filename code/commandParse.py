class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WHITE = '\033'

class CommandParse(object):
	helpText = [
	"!print <object> <attributes> <...>\n"
	"wil print all the atributes of the object\n"
	"or atributes specified, and or the elements\n"
	"in that atributes list\n"
	]
	def __init__(self, game, chatconsole):
		self.game = game
		self.chatconsole = chatconsole
		#a reference to a function that gets the text from the chatconsole
		self.getText = self.chatconsole.console.inputfield.getText
		#a reference to a function that is able to set that text.
		#for for example auto complete (future)
		self.setText = self.chatconsole.console.inputfield.setText
		self.text = []
	def handleInput(self, event):
		pass
	def printWithColor(self, first, second):
		print "%s%s %s%s"%(bcolors.OKBLUE,first, \
			bcolors.OKGREEN, second)
	def update(self):
		#get console input
		text = self.getText()
		if text:
			#if the first character is a ! then it's a command
			if text[0] == '!':
				#remove the ! and split the text up in a list of words.
				text = text[1:].split(' ')
				#extract the command from the text.
				command = text[0]
				#extract a list of arguments.
				args = text[1:]
				if command == 'print':
					if 'game' in args:
						for element in self.game.__dict__:
							self.printWithColor(element, self.game.__dict__[element])
					elif 'player' in args:
						for element in self.game.player.__dict__:
							self.printWithColor(element, self.game.player.__dict__[element])
				if command == 'set':
					attribute = getattr(self, args[0])
					if len(args) > 1:
						attribute.__dict__[args[1]] = int(args[2])
				elif command == 'help':
					for text in self.helpText:
						print text
				elif command == 'printdbg':
					print "input: %s \ncommand: %s \narguments: %s"%(text, command, args)
			else:
				print "text: "
				print text
