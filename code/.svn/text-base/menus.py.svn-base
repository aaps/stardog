
from utils import *
from menuElements import *
from parts import Dummy, PART_OVERLAP, DEFAULT_IMAGE, FlippablePart
from spaceship import Ship

DEFAULT_SELECTED_IMAGE = loadImage("res/defaultselected.bmp")

class Menu(TopLevelPanel):
	"""The top level menu object. Menu(mouse, rect) -> new Menu"""
	activeMenu = None
	color = (100, 100, 255, 250)
	def __init__(self, game, rect, player):
		TopLevelPanel.__init__(self, rect)
		subFrameRect = Rect(0, 0, \
					self.rect.width, self.rect.height)
		self.player = player
		self.parts = PartsPanel(subFrameRect, player)
		self.keys = Keys(subFrameRect, player)
		self.skills = Skills(subFrameRect, player)
		x = 2
		y = 2
		h = 24
		w = 80
		#TODO: rewrite these buttons as one Selecter.
		self.panels.append(Button(Rect(x,y,w,h), \
				lambda : self.setActiveMenu(self.parts), "Parts", BIG_FONT))
		y += h + 2
		self.panels.append(Button(Rect(x,y,w,h), \
				lambda : self.setActiveMenu(self.keys), "Keys", BIG_FONT))
		y += h + 2
		self.panels.append(Button(Rect(x,y,w,h), \
				lambda : self.setActiveMenu(self.skills), "Skills", BIG_FONT))
		y += h + 2
		y += h + 2
		self.setActiveMenu(self.parts)

	def setActiveMenu(self, menu):
		if self.activeMenu:
			self.panels.remove(self.activeMenu)
		self.activeMenu = menu
		self.panels.append(menu)

	def update(self):
		Panel.update(self)
		if self.activeMenu:
			self.activeMenu.update()

class PartsPanel(Panel):
	image = loadImage('res/menus/partsmenubg.bmp')
	#tradeImage = loadImage('res/menus/partstrademenubg.bmp')
	dirtyParts = False
	def __init__(self, rect, player):
		Panel.__init__(self, rect)
		self.addPanel(Label(Rect(self.rect.width / 2 - 60, 2, 0, 0),\
			"Parts", BIG_FONT))
		self.player = player
		inventoryColor = (20,50,35)
		shipColor = (50,20,70)
		flip = Button(Rect(506, 572, 62, 14), self.flip, " FLIP")
		remove = Button(Rect(570, 572, 62, 14), self.remove, " REMOVE")
		add = Button(Rect(100, 572, 62, 14), self.attach, " ATTACH")
		paint = Button(Rect(164, 572, 62, 14), self.paint, " PAINT")
		repair = Button(Rect(300, 572, 62, 14), self.repair, " REPAIR")
		refill = Button(Rect(364, 572, 62, 14), self.refill, " REFILL")
		self.inventoryPanel = InventoryPanel(
				Rect(100, 30, 130, 540),
				self, self.player.inventory)
		self.tradePanel = None
		self.shipPanel = ShipPanel(Rect(232, 30, 400, 300), self, self.player)
		self.descriptionShip = PartDescriptionPanel(
					Rect(232, 332, 400, 238), self.shipPanel)
		self.descriptionInventory = PartDescriptionPanel(
					Rect(636, 332, 400, 238), self.inventoryPanel)
		self.addPanel(self.descriptionShip)
		self.addPanel(self.descriptionInventory)
		self.addPanel(self.shipPanel)
		self.addPanel(self.inventoryPanel)
		self.addPanel(flip)
		self.addPanel(remove)
		self.addPanel(add)
		self.addPanel(paint)
		self.addPanel(repair)
		self.addPanel(refill)

	def update(self):
		Panel.update(self)
		if (self.tradePanel and not self.player.landed
		or self.player.landed and not self.tradePanel):
			self.dirtyParts = True
		if self.dirtyParts:
			self.dirtyParts = False
			self.reset()

	def reset(self):
		if self.player.landed and not self.tradePanel:
			#self.image = self.tradeImage
			self.removePanel(self.tradePanel)
			self.tradePanel = InventoryPanel(Rect(660, 30, 130, 570),
								self, self.player.landed.inventory)
			self.addPanel(self.tradePanel)
		elif not self.player.landed:
			#self.image = self.baseImage
			self.removePanel(self.tradePanel)
			self.tradePanel = Label(Rect(660, 30, 130, 570),
								"Not Docked", FONT)
			self.addPanel(self.tradePanel)
			self.tradePanel = None
		Panel.reset(self)


	def flip(self):
		"""flips the selected part if it is a FlippablePart."""
		if self.shipPanel.selected and self.shipPanel.selected.part:
			part = self.shipPanel.selected.part
			if isinstance(part, FlippablePart):
				part.flip()
				part.unequip()
				self.shipPanel.selected.port.addPart(part)
				self.descriptionShip.setPart(self.shipPanel.selected.part)
				self.shipPanel.reset()

	def remove(self):
		"""removes the selected part from the ship and updates menus"""
		selected = self.shipPanel.selected
		if selected and selected.part \
		and selected.part.parent != selected.part.ship: #not cockpit
			self.descriptionInventory.setPart(self.shipPanel.selected.part)
			self.descriptionShip.setPart(None)
			self.shipPanel.selected.part.unequip()
			self.shipPanel.reset()
			self.inventoryPanel.reset()

	def attach(self):
		"""adds the selected part to the ship and updates menus"""
		if self.shipPanel.selected and self.inventoryPanel.selected:
			self.player.inventory.remove(self.inventoryPanel.selected.part)
			self.descriptionInventory.setPart(self.shipPanel.selected.part)
			if self.shipPanel.selected.part:
				self.shipPanel.selected.part.unequip()
			self.shipPanel.selected.port.addPart(
						self.inventoryPanel.selected.part)
			self.descriptionShip.setPart(self.inventoryPanel.selected.part)
			self.shipPanel.reset()
			self.inventoryPanel.reset()

	def paint(self):
		"""paints the selected part to match this ship."""
		if self.inventoryPanel.selected:
			part = self.inventoryPanel.selected.part
			part.color = self.player.color
			part.image = colorShift(pygame.transform.rotate(part.baseImage, \
						-part.dir), part.color).convert()
			part.image.set_colorkey((255,255,255))
			self.inventoryPanel.reset()

	def repair(self):
		"""repairs the selected part, if player is landed and has enough money"""
		if (self.shipPanel.selected or self.inventoryPanel.selected) and self.player.landed:
			if self.shipPanel.selected:
				part = self.shipPanel.selected.part
			else:
				part = self.inventoryPanel.selected.part
			if hasattr(part, "propellant"):
				cost = round(part.value * (1 - part.hp / part.maxhp) * 0.4, 2)
			else:
				cost = round(part.value * (1 - part.hp / part.maxhp) * 0.8, 2)
			if self.player.money < cost:
				print "not enough money"
			else:
				self.player.money -= cost
				part.hp = part.maxhp
				part.appraise()
				self.shipPanel.reset()
				self.inventoryPanel.reset()
				print part.name, "has been repaired"

	def refill(self):
		"""refills with propellant the selected tank, if player is landed and has enough money"""
		if self.shipPanel.selected and self.player.landed \
		and hasattr(self.shipPanel.selected.part, "propellant"):
			tank = self.shipPanel.selected.part
			cost = round((tank.maxPropellant - tank.propellant) / 90, 2)
			if self.player.money < cost:
				prop = self.player.money * 90
				cost = self.player.money
			else:
				prop = tank.maxPropellant - tank.propellant
			self.player.money -= cost
			tank.propellant += prop
			tank.appraise()
			self.shipPanel.reset()
			self.inventoryPanel.reset()
			print tank.name, "has been refilled with %.1f propellant" % prop
			if tank.ship:
				temp = self.player.usingTank
				self.player.usingTank = tank
				tank.update(tank.ship.dt)
				self.player.usingTank = temp

class ShipPanel(Selecter):
	selected = None
	text = None
	#drawBorder = False
	def __init__(self, rect, parent, player, descriptionPanel = None):
		Selecter.__init__(self, rect)
		self.player = player
		self.parent = parent
		self.reset()

	def reset(self):
		s = self.player
		self.setSelected(None)
		self.player.reset()
		self.panels = []
		self.selectables = []
		if not s.parts:
			dummy = Dummy(s.game)
			self.selectables.append(ShipPartPanel(dummy, self))
			self.selectables[-1].port = s.ports[0]
		for part in s.parts:
			self.selectables.append(ShipPartPanel(part, self))
			for port in part.ports:
				if port.part is None:
					dummy = Dummy(part.game)
					#calculate dummy offsets:
					dummy.dir = port.dir + part.dir
					cost = cos(part.dir) #cost is short for cos(theta)
					sint = sin(part.dir)
					dummy.offset = (part.offset[0] + port.offset[0] * cost
						- port.offset[1] * sint
						- cos(dummy.dir) * (dummy.width - PART_OVERLAP) / 2,
						part.offset[1] + port.offset[0] * sint
						+ port.offset[1] * cost
						- sin(dummy.dir) * (dummy.width - PART_OVERLAP) / 2)
					#rotate takes a ccw angle.
					dummy.image = colorShift(pygame.transform.rotate(
							dummy.baseImage, -dummy.dir), dummy.color).convert()
					dummy.image.set_colorkey((0,0,0))
					self.selectables.append(ShipPartPanel(dummy, self))
					self.selectables[-1].port = port
		#update ship stats display:
			#tabs not displaying correctly, so using spaces.
		text = ("Money: $%.2f\nParts: %i/%i\nEfficiency: %.3f\nMass: %.1f T\n" +
			"Forward Thrust: %i MN\nMoment: %i MG m^2\nTorque: %i MN m\n" +
			"Max DPS: %.2f\nEnergy: %.1f/%i\nPropellant: %.1f/%.f\nShields: %.1f/%.1f")
		values = (s.money, s.numParts, s.partLimit, s.efficiency, s.mass,
				s.forwardThrust/1000, s.moment, s.torque/1000,
				s.dps, s.energy, s.maxEnergy, s.propellant, s.maxPropellant, s.hp, s.maxhp)
		self.text = (TextBlock(Rect(20,10,400,100), text%values,
					color = (100,200,0), font = SMALL_FONT))
		self.addPanel(self.text)
		Panel.reset(self)
		#not Selectable.reset(), because that rearranges the selectables.

class PartDescriptionPanel(Panel):
	#drawBorder = False
	"""displays descriptions of parts."""
	def __init__(self, rect, selecter = None):
		Panel.__init__(self, rect)
		self.part = None
		self.text = None
		self.name = None
		self.selecter = selecter

	def setPart(self, part):
		self.part = part
		self.removePanel(self.text)
		self.removePanel(self.name)
		if not part or isinstance(part, Dummy):
			if self.image:
				self.image.fill((0,0,0,0))
			return
		self.image = pygame.Surface((self.rect.width, self.rect.height),
					hardwareFlag).convert()
		self.image.set_colorkey((0,0,0))
		bigImage = pygame.transform.scale2x(self.part.image)
		bigImage.set_colorkey((255,255,255)) # idk why this one's white.
		self.image.blit(bigImage,
				(self.rect.width / 2 - bigImage.get_width() / 2, 5))
		string = part.stats()
		string += '\nFunctions: '
		for function in part.functions:
			string += function.__name__+' '
		if not part.functions: string += 'None'
		string += '\n'
		for adj in part.adjectives:
			string += "\n  %s: %s"%(str(adj.__class__).split('.')[-1],
														adj.__doc__)
		x, y = self.rect.left, self.rect.top
		w, h = self.rect.width, self.rect.height
		self.name = Label(Rect(x + 4, y + 44, w, 20), part.name, FONT,
				(100, 200, 0))
		self.text = TextBlock(Rect(x + 4, y + 64, w, h), string, SMALL_FONT,
				(0, 150, 0))
		self.addPanel(self.name)
		self.addPanel(self.text)

	def update(self):
		if (self.selecter
		and self.selecter.selected
		and self.selecter.selected.part != self.part):
			self.setPart(self.selecter.selected.part)
		elif self.selecter and self.selecter.selected is None:
			self.setPart(None)
		Panel.update(self)

	def reset(self):
		self.setPart(self.part)
		Panel.reset(self)

class ShipPartPanel(DragableSelectable):
	drawBorder = False
	port = None
	part = None
	def __init__(self, part, parent):
		width = part.image.get_width() * 2
		height = part.image.get_height() * 2
		rect = Rect(
			part.offset[0] * 2 + parent.rect.width / 2 - width / 2,
			part.offset[1] * 2 + parent.rect.height / 2 - height / 2,
			width, height)
		DragableSelectable.__init__(self, rect, parent)
		self.ship = parent.player
		if not isinstance(part, Dummy):
			self.part = part
		if part.parent:
			for port in part.parent.ports:
				if port.part == part:
					self.port = port
		self.image = pygame.transform.scale2x(part.image).convert()
		self.image.set_colorkey((0,0,0))

	def select(self):
		pygame.draw.ellipse(self.image, (1, 1, 1), self.image.get_rect())
		pygame.draw.ellipse(self.image, (255, 0, 0), self.image.get_rect(), 1)
		if self.part:
			color = self.part.color
			color = color[0] // 4 + 192, color[1] // 2 + 128, color[2] // 2 + 128
			color = 250, 0, 200
			self.image.blit(colorShift(pygame.transform.scale2x(\
					pygame.transform.rotate(self.part.baseImage, -self.part.dir)), \
					color), (0,0))
		else:
			dir = self.port.dir + self.port.parent.dir
			self.image.blit(pygame.transform.scale2x(pygame.transform.rotate(
									DEFAULT_SELECTED_IMAGE, -dir)), (0,0))

	def unselect(self):
		if self.part:
			self.image = pygame.transform.scale2x(self.part.image).convert()
			self.image.set_colorkey((0,0,0))
		else:
			dir = self.port.dir + self.port.parent.dir
			self.image = pygame.transform.scale2x(\
						pygame.transform.rotate(DEFAULT_IMAGE, -dir)).convert()
			self.image.set_colorkey((0,0,0))

	def dragOver(self, pos, rel):
		self.parent.setSelected(self)

	def drag(self, start):
		if not self.part or self.part.parent == self.part.ship:
			return None
		if not self.selected:
			self.select()
			self.parent.setSelected(self)
		return (PartTile(self.part, Rect(0, 0, PartTile.width, PartTile.height),
				self), self)

	def drop(self, pos, dropped):
		if isinstance(dropped, PartTile):
			if self.part and self.port.parent == self.part.ship:
				return #do not allow Cockpits to be swapped!
			if self.part and dropped.part == self.part:
				return #dropped on self: do nothing.
			if self.part and self.checkParent(self.part,dropped.part):
				return #trying to drop a part on it's parent.  Do nothing.
			if dropped.parent == self.parent.parent.tradePanel:
				return #avoids to drop a part from trade panel without buying it
			dropped.part.unequip(toInventory = False)
			if not self.port.parent in self.ship.parts:
				#unequiping dropped messed up this node!
				return
			self.port.addPart(dropped.part)
			self.parent.parent.dirtyParts = True
			return 3

	def endDrag(self, dropped, result):
		if result == 1:
			dropped.part.unequip(toInventory = False)
		if result:
			#if child parts were removed, need to reset inventory panel:
			self.parent.parent.dirtyParts = True
		self.parent.setSelected(None)

	def checkParent(self, thisPart, partToMatch):
		"""recursive helper to check if a part is thisPart's parent."""
		if thisPart is None:
			if self.part: thisPart = self.part
			else: thisPart = self.port.parent
		if thisPart == partToMatch:
			return True
		if thisPart is None or isinstance(thisPart.parent, Ship):
			return False
		return self.checkParent(thisPart.parent, partToMatch)

class PartTile(DragableSelectable):
	drawBorder = False
	width = 130
	height = 50
	partImageOffset = 0,12
	drawBorderDragging = False
	selectedColor = (255,200,200)
	bgInactive = None
	bgActive = (110, 110, 75)
	bgSelected = (80, 50, 110)
	def __init__(self, part, rect, parent):
		"""PartTile(part, rect) -> new PartTile.
		The menu interface for a part. Display it like a button!"""
		DragableSelectable.__init__(self, rect, parent)
		self.part = part
		bigImage = pygame.transform.scale2x(self.part.image)
		bigImage.set_colorkey((255,255,255)) # idk why this one's white.
		self.hotSpot = (self.partImageOffset[0] + self.part.width,
						self.partImageOffset[1] + self.part.height)
		self.image.blit(bigImage, PartTile.partImageOffset)
		#add text labels:
		rect = Rect(rect)
		self.addPanel(Label(rect, part.name, font = SMALL_FONT))
		self.panels[-1].rect.width = self.rect.width
		string = part.shortStats()
		i = string.find('\n')
		priceString = string[:i]
		string = string[i+1:]
		i = string.find('\n')
		hpString = string[:i]
		statString = string[i+1:]
		rect = Rect(rect)
		rect.x += 38; rect.y += 14
		self.addPanel(Label(rect, priceString, color = (200,200,0),
					font = SMALL_FONT))
		self.panels[-1].rect.width = 35
		rect = Rect(rect)
		rect.x += 45
		self.addPanel(Label(rect, hpString, color = (200,0,0),
					font = SMALL_FONT))
		self.panels[-1].rect.width = self.rect.width - 88
		rect = Rect(rect)
		rect.x -= 45
		rect.y += 12
		self.addPanel(TextBlock(rect, statString, color = (0, 150, 0),
					font = SMALL_FONT))

class InventoryPanel(Selecter):
	#drawBorder = False
	selected = None
	def __init__(self, rect, parent, partList):
		"""InventoryPanel(rect, partList) -> a Selecter that resets to the
		provided list of parts."""
		Selecter.__init__(self, rect, vertical = True)
		self.partList = partList
		self.parent = parent
		self.parent.dirtyParts = True

	def reset(self):
		self.setSelected(None)

		self.selectables = []
		for part in self.partList:
			self.addSelectable(PartTile(part, \
						Rect(0,0,PartTile.width, PartTile.height), self))
		Selecter.reset(self)

	def drop(self, pos, dropped):
		result = Selecter.drop(self, pos, dropped)
		if result: return result
		if isinstance(dropped, PartTile):
			if dropped.part in self.partList:
				#from here to here: ignore
				return
			#add dropped part to partList:
			if not dropped.part in self.partList:
				#check if buying or selling
				if self.parent.tradePanel == self:
					self.parent.player.money += dropped.part.price
				elif dropped.parent == self.parent.tradePanel:
					if dropped.part.price > self.parent.player.money:
						print "not enough money"
						return
					else:
						self.parent.player.money -= dropped.part.price
				self.partList.append(dropped.part)
				self.parent.dirtyParts = True
			#select it:
			for partTile in self.selectables:
				if partTile.part == dropped.part:
					self.setSelected(partTile)
					break
			return 1
		return None

	def endDrag(self, dropped, result):
		if result == 1 or result == 3:
			#it went somewhere else.  Remove from here:
			while dropped.part in self.partList:
				self.partList.remove(dropped.part)
			self.setSelected(None)
			self.parent.dirtyParts = True

class Keys(Panel):
	bindingMessage = pygame.image.load("res/menus/keybind.gif")
	"""the Keys panel of the menu."""
	def __init__(self, rect, player):
		Panel.__init__(self, rect)
		self.player = player
		self.keyboardRect = Rect(self.rect.left + 2, self.rect.height - 204, \
							self.rect.width - 4, 202)
		self.functions = FunctionSelecter(\
					Rect(self.rect.width / 2 + self.rect.left,\
					self.rect.top, self.rect.width / 4 - 4,\
					self.rect.height - self.keyboardRect.height - 26), player)
		self.addPanel(self.functions)
		self.bindings = BindingSelecter( \
					Rect(self.rect.width * 3 / 4 + self.rect.left,\
					self.rect.top, self.rect.width / 4 - 4,\
					self.rect.height - self.keyboardRect.height - 26), player)
		self.addPanel(self.bindings)
		buttonTop = self.rect.height - self.keyboardRect.height - 24
		self.addPanel(Button(Rect(self.rect.width - 204, buttonTop, 100, 20), \
					self.bind, "Bind"))
		self.addPanel(Button(Rect(self.rect.width - 106, buttonTop, 100, 20), \
					self.unbind, "Unbind"))
		# self.addPanel(PartFunctionsPanel(Rect(self.rect.left + 2, \
					# self.rect.top + 2, 	self.rect.width / 2 - 4, \
					# self.rect.height - self.keyboardRect.height - 2), self, \
					# player))
		self.toggleMouseButton = Button(Rect(self.rect.left, self.rect.bottom - 20,
								200,20), self.toggleMouse, "Turn Mouse Off")
		self.addPanel(self.toggleMouseButton)


	def toggleMouse(self):
		self.player.game.mouseControl = not self.player.game.mouseControl
		if self.player.game.mouseControl:
			self.toggleMouseButton.image = FONT.render('Turn Mouse Off',\
						True, self.color)
		else:
			self.toggleMouseButton.image = FONT.render('Turn Mouse On',\
						True, self.color)

	def unbind(self):
		"""Removes the currently selected binding."""
		if self.bindings.selected:
			self.player.script.unbind(self.bindings.selected.keyNum, \
						self.bindings.selected.function)
			self.bindings.reset()

	def bind(self):
		"""binds the current function to a key it captures"""
		if self.functions.selected and isinstance(self.functions.selected, \
												FunctionSelectable):
			screen = self.player.game.screen
			screen.blit(self.bindingMessage, (screen.get_width() / 2  \
								- self.bindingMessage.get_width() / 2, \
								screen.get_height() / 2))
			pygame.display.flip()
			key = self.captureKey()
			self.player.script.bind(key, self.functions.selected.function)
			self.bindings.reset()

	def captureKey(self):
		"""Warning: Enters a loop for upto five seconds!
		captures the first pressed key and returns its number."""
		start = pygame.time.get_ticks()
		print 'capturing key'
		while pygame.time.get_ticks() < start + 5000:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = 0
					return
				elif event.type == pygame.KEYDOWN:
					return event.key
		return 0

class PartFunctionsPanel(ShipPanel):
	labels = []

	def reset(self):
		ShipPanel.reset(self)
		for panel in self.labels:
			self.removePanel(panel)
		self.labels = []
		for part in self.player.parts:
			pos = part.offset[0] + self.rect.centerx - 100, \
					part.offset[1] + self.rect.centery
			self.labels.append(Label(Rect(pos,(20,20)), str(part.number), \
					font = BIG_FONT))
			self.addPanel(self.labels[-1])
		Panel.reset(self)

class FunctionSelecter(Selecter):
	def __init__(self, rect, ship):
		Selecter.__init__(self, rect)
		self.partsList = ship.parts
		self.player = ship
		self.reset()

	def reset(self):
		self.selectables = []
		self.addSelectable(PresetSelectable("ship-wide presets", \
					Rect(0, 0, self.rect.width, 16)))
		for function in self.player.functions:
			self.addSelectable(FunctionSelectable(function, \
						Rect(20, 0, self.rect.width, 16)))

		for part in self.partsList:
			self.addSelectable(PartHeaderSelectable(part, \
						Rect(0, 0, self.rect.width, 16)))
			for function in part.functions:
				self.addSelectable(FunctionSelectable(function, \
						Rect(20, 0, self.rect.width - 20, 16)))
		Selecter.reset(self)

class PresetSelectable(Selectable):
	def __init__(self, string, rect):
		self.name = string
		Selectable.__init__(self, rect)
		self.addPanel(Label(rect, string))

class FunctionSelectable(Selectable):
	def __init__(self, function, rect):
		self.function = function
		Selectable.__init__(self, rect)
		self.addPanel(Label(rect, function.__name__))

class PartHeaderSelectable(Selectable):
	def __init__(self, part, rect):
		self.part = part
		Selectable.__init__(self, rect)
		if part.number != -1:
			self.addPanel(Label(rect, '#' + str(part.number) + ' ' + part.name))
		else:
			self.addPanel(Label(rect, part.name))

class FunctionSelectable(Selectable):
	def __init__(self, function, rect):
		self.function = function
		Selectable.__init__(self, rect)
		self.addPanel(Label(rect, " " + function.__name__))

class BindingSelecter(Selecter):
	def __init__(self, rect, ship):
		Selecter.__init__(self, rect)
		self.bindings = ship.script.bindings
		self.reset()

	def reset(self):
		self.selectables = []
		for binding in self.bindings:
			Selecter.addSelectable(self,BindingSelectable(binding, \
						Rect(0, 0, self.rect.width, 20)))
		self.selectables.sort(cmp = lambda x,y: y.keyNum)
		Selecter.reset(self)

	def addSelectable(self, selectable):
		self.reset()

class BindingSelectable(Selectable):
	def __init__(self, binding, rect):
		self.keyNum = binding[0]
		self.function = binding[1]
		self.partNum = binding[1].im_self.number
		self.name = pygame.key.name(self.keyNum)
		Selectable.__init__(self, rect)
		self.addPanel(Label(rect, \
					" " + self.name + " - ", color = (100,200,100)))
		self.addPanel(Label( \
					Rect(self.panels[-1].rect.right, self.rect.top,0,0), \
					str(self.partNum) + ": ", color = (200,200,100)))
		self.addPanel(Label( \
					Rect(self.panels[-1].rect.right, self.rect.top,0,0), \
					str(self.function.__name__), color = (200,100,100)))

class Skills(Panel):
	def __init__(self, rect, player):
		Panel.__init__(self, rect)
		self.addPanel(Label(Rect(self.rect.width / 2 - 60, 2, 0, 0),\
			"Skills", BIG_FONT))
		rect = Rect(100,0,300,100)
		for skill in player.skills:
			rect = Rect(rect)
			rect.y += 150
			self.addPanel(SkillTile(rect, self, skill, player))


	def skill(self, skillName):
		pass

class SkillTreeTab(Selectable):
	pass
class SkillTreeSelector(Selecter):
	pass

class SkillTile(Button):
	def __init__(self, rect, parent, skill, ship):
		self.skill = skill
		self.parent = parent
		self.ship = ship
		function = self.getSkill
		Button.__init__(self, rect, function, None)
		rect1 = Rect(rect.x + 5, rect.y + 5, 20, rect.width - 10)
		rect2 = Rect(rect.x + 5, rect.y + 25, 20, rect.width - 10)
		rect3 = Rect(rect.x + 5, rect.y + 45, 200, rect.width - 10)
		self.addPanel(Label(rect1, str(skill.__class__), color = (200,200,255)))
		self.levelLabel = Label(rect2, 'level ' + str(skill.level),\
					color = (100,200,0))
		self.addPanel(self.levelLabel)
		self.addPanel(TextBlock(rect3, skill.__doc__, SMALL_FONT, (100,200,0)))

	def getSkill(self):
		if self.ship.developmentPoints >= self.skill.cost():
			self.skill.levelUp()
			self.ship.developmentPoints -= self.skill.cost()
			self.removePanel(self.levelLabel)
			rect = self.levelLabel.rect
			self.levelLabel = Label(rect, 'level ' + str(self.skill.level),\
						color = (100,200,0))
			self.addPanel(self.levelLabel)

class Store(Panel):
	def __init__(self, rect, player):
		self.player = player
		Panel.__init__(self, rect)
		self.addPanel(Label(Rect(self.rect.width / 2 - 60, 2, 0, 0),\
			"Store", BIG_FONT))




