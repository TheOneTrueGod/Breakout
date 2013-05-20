from Globals import *
class EffectStruct:
	def __init__(self):
		self.effects = []
		
	def addEffect(self, newEffect):
		self.effects += [newEffect]
		
	def update(self):
		i = 0
		while i < len(self.effects):
			self.effects[i].update()
			if self.effects[i].readyToDelete():
				del self.effects[i]
			i += 1
		
	def drawMe(self):
		for effect in self.effects:
			effect.drawMe()
		
class Effect:
	def __init__(self):
		self.time = 0
		
	def readyToDelete(self):
		return self.time <= 0
		
	def update(self):
		self.time -= 1
	
	def drawMe(self):
		pass
		
class FadingBall(Effect):
	def __init__(self, pos, colour, time, size):
		self.time = time
		self.startTime = time
		self.startColour = colour
		self.pos = pos
		self.size = size
		
	def getSize(self):
		return max(int(self.size * ((self.time / float(self.startTime)) * 0.4 + 0.6)), 1)
		
	def drawMe(self):
		surface = getConst("SURFACE")
		clr = []
		for col in self.startColour:
			clr += [col * (self.time / float(self.startTime))]
		pygame.draw.circle(surface, clr, self.pos, self.getSize())
		
class FlyingText(Effect):
	def __init__(self, pos, colour, time, size):
		self.time = time
		self.startTime = time
		self.startColour = colour
		self.pos = pos
		self.size = size
		
	def getSize(self):
		return max(int(self.size * ((self.time / float(self.startTime)) * 0.4 + 0.6)), 1)
		
	def drawMe(self):
		surface = getConst("SURFACE")
		clr = []
		for col in self.startColour:
			clr += [col * (self.time / float(self.startTime))]
		pygame.draw.circle(surface, clr, self.pos, self.getSize())