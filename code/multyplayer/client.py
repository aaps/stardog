import legume
import messages
import time
from code.vec2d import Vec2d
from code.floaters import *

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
		
		if legume.messages.message_factory.is_a(msg, 'FloaterSpawn'): 
			pos = Vec2d(msg.x.value, msg.y.value)
			floater = ServerFloaterDisk(self.universe, pos, Vec2d(0,0), radius = 50)
			floater.id = msg.id.value
			
			if self.universe.curSystem and not any(x.id == floater.id for x in self.universe.curSystem.floaters):
				self.universe.curSystem.floaters.add(floater)

		elif legume.messages.message_factory.is_a(msg, 'FloaterUpdate'):
			if self.universe.curSystem:
				
				floater = self.universe.curSystem.getFloater(msg.id.value)
				if len(floater) > 0 and isinstance(floater[0], ServerFloaterDisk):
					floater[0].pos = Vec2d(msg.x.value,msg.y.value)
					floater[0].delta = Vec2d(msg.dx.value,msg.dy.value)

		elif legume.messages.message_factory.is_a(msg, 'FloaterKill'):
			print "receved floter kill", msg
			if self.universe.curSystem:
				floater = self.universe.curSystem.getFloater(msg.id.value)
				if len(floater) > 0:
					floater[0].send = -1
					

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