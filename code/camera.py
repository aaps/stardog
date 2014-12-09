class Camera:
	

	def __init__(self, screen):
		self.screen = screen
		pos = Vec2d(0,0)
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.onScreen = []

	def draw(self):
		self.screen.fill((0, 0, 0, 0))
		intro.draw(self.screen)
		pygame.display.flip()

	def set_pos(pos = Vec2d(0,0)):
		self.pos = pos

	def add_pos(pos = Vec2d(0,0)):
		self.pos =+ pos



