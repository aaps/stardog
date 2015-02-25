import legume
import messages
import time


class Server(object):

	def __init__(self, universe):
		self.universe = universe
		self._server = legume.Server()
		self._server.OnConnectRequest += self.on_connect_request

		self._server.OnMessage += self.on_message
		self.port = messages.PORT
		self.entity_updates = [ ]
		self.client_entity_count = 0
		self.network_timer = time.time()
		self.network_interval = 2 #10 fps
		self.network_frames_per_second = 1.0 / self.network_interval #partial updates
		self.full_network_update_every_n_frames = int(self.network_frames_per_second*3) #full updates, every 3 seconds

		self._server.listen(('', self.port))

	def getPlanetUpdateMessage(self, entity):
		msg = messages.PlanetUpdate()
		return msg

	def getPlanetSpawnMessage(self, entity):
		msg = messages.PlanetSpawn()
		msg.x.value = entity.pos.x
		msg.y.value = entity.pos.y
		msg.radius.value = entity.pos.radius
		return msg

	def getShipUpdateMessage(self, entity):
		msg = messages.ShipUpdate()
		return msg

	def getShipUpdateFullMessage(self, entity):
		msg = messages.ShipUpdateFull()
		return msg

	def getShipSpawnMessage(self, entity):
		msg = messages.ShipSpawn()
		return msg

	def getFloaterUpdateMessage(self, entity):
		msg = messages.FloaterUpdate()
		msg.id.value = entity.id
		msg.x.value = entity.pos.x
		msg.y.value = entity.pos.y
		msg.dx.value = entity.delta.x
		msg.dy.value = entity.delta.y
		return msg

	def getFloaterUpdateFullMessage(self, entity):
		msg = messages.FloaterUpdateFull()
		msg.id.value = entity.id
		msg.x.value = entity.pos.x
		msg.y.value = entity.pos.y
		return msg

	def getFloaterSpawnMessage(self, entity):
		msg = messages.FloaterSpawn()
		msg.id.value = entity.id
		msg.x.value = entity.pos.x
		msg.y.value = entity.pos.y
		return msg

	def getFloaterKillMessage(self, entity):
		msg = messages.FloaterKill()
		msg.id.value = entity.id
		return msg

	def getPartUpdateMessage(self, entity):
		msg = messages.PartUpdate()
		return msg


	def getPartUpdateFullMessage(self, entity):
		msg = messages.PartUpdateFull()
		return msg

	def getPartSpawnMessage(self, entity):
		msg = messages.PartSpawn()
		return msg

	def getSystemUpdateMessage(self, entity):
		msg = messages.SystemUpdate()
		return msg

	def getSystemSpawnMessage(self, entity):
		msg = messages.SystemSpawn()
		return msg

	def send_player_message(self, server):
		msg = messages.PlayerMessage()
		return msg


	def send_entity_spawn(self, server):
		# loop trough a list of entitys that need to get spawned
		# put them in the life list and send the spawn over network
		pass

	def send_all_entitys(self, endpoint):
		
		for floater in self.universe.curSystem.floaters:
			try: 
				message = self.getFloaterSpawnMessage(floater)
				endpoint.send_reliable_message(message)
			except:
				raise

	def send_entity_spawns(self, server):
		for floater in self.universe.curSystem.toSpawn:
			try: 
				message = self.getFloaterSpawnMessage(floater)
				server.send_reliable_message_to_all(message)
			except:
				raise
				
	def send_entity_updates(self, server):
		# 
		for floater in self.universe.curSystem.floaters:
			
			try: 
				message = self.getFloaterUpdateMessage(floater)
				
				server.send_message_to_all(message)
			except:
				raise

	def send_entity_kills(self, server):
		for floater in self.universe.curSystem.floaters:
			
			if floater.send < 2 and floater.hp <= 0:
				try: 
					message = self.getFloaterKillMessage(floater)
					server.send_reliable_message_to_all(message)
				except:
					raise


	def update(self):
		if time.time() > self.network_timer + self.network_interval:
			self.network_timer = time.time()
			try:
				self.send_entity_updates(self._server)
				self.send_entity_spawns(self._server)
				self.send_entity_kills(self._server)
			except ValueError:
				print "Oops!  That was no valid number.  Try again..."
				raise

			self._server.update()



	def __exit__(self, type, value, traceback):
		self._server.disconnect()

	def on_connect_request(self, sender, args):
		self.send_all_entitys(sender)

	def on_message(self, sender, msg):
		pass
