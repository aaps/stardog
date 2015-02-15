import legume
import messages
import time

class GameClient(object):
	def __init__(self, universe):
		self.universe = universe
		self._client = legume.Client()
		self._client.OnMessage += self.on_message 
		self.frame_nr = 0


	def connect(self, host='localhost'):
		if self._client._state not in [self._client.CONNECTED, self._client.CONNECTING]:
			print('Using host/port: %s %s' % (host, messages.PORT))
			self._client.connect((host, messages.PORT))

	def on_message(self, sender, msg):
		# pass
		if legume.messages.message_factory.is_a(msg, 'FloaterUpdate'): 
			pass
			# put the updates for the planets, floaters and ships here
		elif legume.messages.message_factory.is_a(msg, 'EntityCreate'):
			pass
			#put create planet, floaters, and ships here


		else:
			raise KeyError() #add message typr!
			print('Message: %s' % args)

	def update(self):

		for system in self.universe.starSystems:
			for floater in system.floaters:
				self.showEntity(self._client, floater)
		self._client.update()

	def showEntity(self, endpoint, entity):
		pass
		#dont send annything to the server yet, only after we get the ghost of the server in the clients
		# msg = messages.FloaterUpdate()
		# msg.frame_number.value = 5
		# msg.x.value = entity.pos.x
		# msg.y.value = entity.pos.y
		# msg.dx.value = entity.delta.x
		# msg.dy.value = entity.delta.y
		# try: endpoint.send_message(msg) #fix: check connectivity
		# except: pass 