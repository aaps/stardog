"""updater.py
maintains two lists of Floaters: frame and slow.  Calls Floater.update()
each frame on everything in frame, runs a scheduler that gurantees each 
Floater in slow is updated at least once every .25 seconds.  Moves Floaters
between the lists based on the value of Floater.frameUpdating.

For Stardog by Shanti Pothapragada, rgbDreamer@rgbDreams.com"""

from heapq import heappush, heappop, heapreplace

import pygame

from utils import *

pygame.init()

class Updater:
	fps = 60
	maxWait = .25	#sprites in slow are updated this often in seconds.
	dangerRadius = 200	#sprites within this distance of other sprites 
						#are added to self.frame for accurate collision
						#checking.
	
	def __init__(self, system = None):
		self.time = time()
		self.count = 0
		self.system = system
		self.frame = []	#a list to update every frame and check collisions
		self.slow = []	#all sprites, updated every maxWait. 
						#frame is selected from this pool.
						#Maintained as a heap of (time, count, sprite) tuples
						#priority queue style. 
		self.ordered = []	#a list of all sprites sorted by x. Used to move
							#sprites near collision into self.frame.
		
	def update(self, dt, screen = None):
		"""update(screen = None) -> updates sprites in this updater.
		
		If screen is provided it should be have a x,y,w,h. Sprites on the 
		screen are updated each frame.  Objects within updater.dangerRadius are
		updated every frame.  Objects that set their .frameUpdating to True
		are updated every frame (needs to be set to True each update). Other 
		objects are updated at least once every updater.maxWait seconds."""
		self.time += dt
		#update these each frame:
		for sprite in self.frame[:]:
			if not sprite.dead:
				sprite.update(dt)
			else:
				heapRemove(self.slow, sprite)
				self.frame.remove(sprite)
				self.system.remove(sprite)

		if not self.slow:
			return
				
		# self.slow is a priority queue.  Calc the number of sprites to update:
		fraction = max(dt / self.maxWait, 1. / self.maxWait / self.fps)
		numUpdates = min(int(len(self.slow) * fraction) + 1, len(self.slow))
		
		lastUpdate,count,sprite = heappop(self.slow) #count is never read.
		for i in range(numUpdates):
			# remove sprites that have been marked dead:
			if sprite.dead:
				if sprite in self.frame:
					self.frame.remove(sprite)
				if self.system:
					self.system.remove(sprite)
				# and don't replace dead sprites:
				lastUpdate,count,sprite = heappop(self.slow)
				continue
			# call updating subroutine:
			self._updateSprite(sprite, self.time - lastUpdate, screen)
			if len(self.slow) < 1: break
			lastUpdate,count,sprite = heapreplace(
								self.slow, (self.time, self.count, sprite))
			self.count += 1
		if numUpdates > 0:
			heappush(self.slow, (self.time, self.count, sprite))
			self.count += 1

	def add(self, sprite):
		if not hasattr(sprite, 'dead'):
			sprite.dead = 0
		if not hasattr(sprite, 'frameUpdating'):
			sprite.frameUpdating = 0
		if sprite.frameUpdating or 1:
			self.frame.append(sprite)
		heappush(self.slow, (self.time, self.count, sprite))
		self.count += 1
		added = False
		for i in range(len(self.ordered) + 1):
			if not added:
				if i >= len(self.ordered) or self.ordered[i].left() < sprite.left():
					self.ordered.insert(i, sprite)
					sprite.orderedIndex = i
					added = True
			else:
				self.ordered[i].orderedIndex = i

	def _updateSprite(self, sprite, dt, screen = None):
		self._reorderSprite(sprite)
		i = sprite.orderedIndex + 1
		end = sprite.x + sprite.radius + self.dangerRadius
		s = sprite
		while i < len(self.ordered) and self.ordered[i].left() < end:
			other = self.ordered[i]
			o = other
			if (s.y < o.y + o.radius * 2 + self.dangerRadius 
			and s.y + s.radius * 2 + self.dangerRadius > o.y):
				sprite.frameUpdating = True
				other.frameUpdating = True
			i += 1
		if screen:
			if (s.x < screen.x + screen.w + self.dangerRadius + s.radius
			and s.x + s.radius + self.dangerRadius > screen.x
			and s.y < screen.y + screen.h + self.dangerRadius + s.radius
			and s.y + s.radius + self.dangerRadius > screen.y):
				sprite.frameUpdating = True
		if sprite in self.frame:
			#this means it has already been updated this frame.
			if not sprite.frameUpdating:
				#must no longer be critical, so remove from self.frame.
				self.frame.remove(sprite)
			else:
				#set it to False. If it's still critical something will set
				#it to True before it gets here again.
				sprite.frameUpdating = False
		else:
			sprite.update(dt)
			if sprite.frameUpdating:
				self.frame.append(sprite)
				sprite.frameUpdating = False
			
	def _reorderSprite(self, sprite):
		i = sprite.orderedIndex
		order = self.ordered 
		assert(order[i] == sprite)
		while (i < len(order) - 1 
		and sprite.left() > order[i+1].left()):
			order[i] = order[i+1]
			order[i].orderedIndex = i
			i += 1
		if i != sprite.orderedIndex:
			order[i] = sprite
			sprite.orderedIndex = i
			
	def sprites(self):
		return [entry[2] for entry in self.slow]
		
	def __iter__(self):
		return iter([entry[2] for entry in self.slow])
	
	def remove(self, sprite):
		if sprite in self.frame:
			self.frame.remove(sprite)
		heapRemove(self.slow, sprite)
				
	def empty(self):
		self.slow = []
		self.frame = []
		self.ordered = []
				
	def collisions(self):
		frame = self.frame
		#insertion sort frame:
		i = 1
		while i < len(frame):
			j = i - 1
			key = frame[i]
			while j >= 0 and key.left() < frame[j].left():
				frame[j + 1] = frame[j]
				j -= 1
			frame[j + 1] = key
			i += 1
		#find collisions:
		hits = []
		numTests = 0
		for i,sprite in enumerate(frame):
			end = sprite.x + sprite.radius
			j = i + 1
			s = sprite
			while j < len(frame) and frame[j].left() < end:
				other = frame[j]
				o = other
				r = sprite.radius + other.radius
				if (s.x < o.x + r \
				and o.x < s.x + r \
				and s.y < o.y + r \
				and o.y < s.y + r \
				and (o.x - s.x) ** 2 + (o.y - s.y) ** 2 < r ** 2):
					hits.append((sprite, other))
				j += 1
			numTests += j - i
		return hits
	
def heapRemove(heap, item):
	for i,sprite in enumerate(heap):
		if sprite[2]  == item:
			heapDel(heap, i)
			return
	
def heapDel(heap, index):
	last = len(heap) - 1
	if last == index:	#base case
		del heap[index]
	elif last == index * 2 + 1:
		heap[index] = heap[index * 2 + 1]
		heapDel(heap, index * 2 + 1)	#recurse
	elif last > index * 2 + 1:
		if heap[index * 2 + 1] < heap[index * 2 + 2]:
			heap[index] = heap[index * 2 + 1]
			heap[index * 2 + 1] = heap[index * 2 + 2]
		else:
			heap[index] = heap[index * 2 + 2]
		heapDel(heap, index * 2 + 2)	#recurse
	else:# last < index * 2 + 1:
		if heap[-1] < heap[index // 2]:
			heap[index] = heap[-1]
		else:
			heap[index] = heap[index // 2]
			heap[index // 2] = heap[-1]
		del heap[-1]
	
class Updatable:
	num = 0
	def __init__(self):
		self.id = Updatable.num
		Updatable.num += 1
		self.frameUpdating = False
		self.dead = False
		
	def update(self, dt):
		print self.id
		
	def __repr__(self):
		return "Updatable with id " + str(self.id)

def test():
	u = Updater()
	pygame.time.wait(500)
	u.update()
	u.add(Updatable())
	u.add(Updatable())
	u.add(Updatable())
	u.add(Updatable())
	framey = Updatable()
	framey.frameUpdating = True
	u.add(framey)
	for x in range(100):
		u.update()
		pygame.time.wait(50)
	return u
