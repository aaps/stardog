import legume
import messages
import time



class GameServer(object):

	def __init__(self, universe):
		self.universe = universe
		self._server = legume.Server()
		self._server.OnConnectRequest += self.on_connect_request

		self._server.OnMessage += self.on_message
		self.port = messages.PORT
		self.entity_updates = [ ]
		self.network_timer = time.time()
		self.network_interval = 0.2 #10 fps
		self.network_frames_per_second = 1.0 / self.network_interval #partial updates
		self.full_network_update_every_n_frames = int(self.network_frames_per_second*3) #full updates, every 3 seconds

		self._server.listen(('', self.port))

	def getPlanetUpdateMessage(self, entity):
		msg = messages.PlanetUpdate()
		return msg

	def getPlanetSpawnMessage(self, entity):
		msg = messages.PlanetSpawn()
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
		return msg

	def getFloaterUpdateFullMessage(self, entity):
		msg = messages.FloaterUpdateFull()
		return msg

	def getFloaterSpawnMessage(self, entity):
		msg = messages.FloaterSpawn()
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


	def send_entity_updates(self, server):
		for system in self.universe.starSystems:

			for floater in system.floaters:
				# e.sync_time = self.world._world_frame_number
				# if floater is star:
				# get_star_as_message
				# if floater is ship:
				# get_ship_as_message
				try: server.send_message_to_all(self.getFloaterUpdateMessage(floater))
				except: raise

	def update(self):
		if time.time() > self.network_timer + self.network_interval:
			self.network_timer = time.time()
			try:
				self.send_entity_updates(self._server)
			except ValueError:
				print "Oops!  That was no valid number.  Try again..."
				raise
			self._server.update()





	def __exit__(self, type, value, traceback):
		self._server.disconnect()

	def on_connect_request(self, sender, args):
		print args

	def on_message(self, sender, msg):
		# pass
		print msg.x.value , msg.y.value , msg.dx.value , msg.dy.value
		print
