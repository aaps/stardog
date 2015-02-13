import legume
import messages
import time

class GameServer(object):

	def __init__(self):
		self._server = legume.Server()
		self._server.OnConnectRequest += self.on_connect_request
		self._server.OnMessage += self.on_message
		self.port = messages.PORT
		self.entity_updates = [ ]
		self.network_timer = time.time()
		self.network_interval = 0.2 #10 fps
		self.network_frames_per_second = 1.0 / self.network_interval #partial updates
		self.full_network_update_every_n_frames = int(self.network_frames_per_second*3) #full updates, every 3 seconds

	def get_entity_as_message(self, entity):

		msg = messages.EntityCreate()

		# msg.x.value = entity.x
		# msg.y.value = entity.y
		# msg.vx.value = entity.vx
		# msg.vy.value = entity.vy
		# msg.ax.value = entity.ax
		# msg.ay.value = entity.ay
		# msg.tx.value = entity.tx
		# msg.ty.value = entity.ty
		return msg


	def send_entity_updates(self, server):
		partial_list = list(self.entity_updates)
		self.entity_updates = set(["a","b","c"])
		for e in partial_list:
			# e.sync_time = self.world._world_frame_number
			try: server.send_message_to_all(self.get_entity_as_message(e))
			except: raise

	def run(self):
		self._server.listen(('', self.port))

		while True:
			if time.time() > self.network_timer + self.network_interval:
				self.network_timer = time.time()
				try:
					self.send_entity_updates(self._server)
				except ValueError:
					print "Oops!  That was no valid number.  Try again..."
					raise
				self._server.update()
		self._server.disconnect()


	def on_connect_request(self, sender, args):
		print args

	def on_message(self, sender, msg):
		# pass
		print msg.x.value , msg.y.value , msg.dx.value , msg.dy.value
		print

def main():
	server = GameServer()
	server.run()

main()