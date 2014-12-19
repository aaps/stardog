class CommandParse(object):
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
	def update(self):
		#get console input
		text = self.getText()
		if text:
			#if the first character is a ! then it's a command
			if text[0] == '!':
				print "command"
			else:
				print text
