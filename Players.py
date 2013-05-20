import pygame, math, random, Abilities
from Globals import *
from pygame.locals import *

class Players:
	def __init__(self, profiles):
		if getConst("MODE") != "VS":
			self.players = [None, None]
		else:
			self.players = [profiles[0].getPlayer(), profiles[1].getPlayer()]
		self.deaths = [0, 0]
		self.profiles = profiles
		
	def getPlayers(self):
		return [k for k in self.players if k != None]
		
	def forceQuit(self):
		for p in [0, 1]:
			if self.players[p]:
				self.profiles[p].save()
	
	def handleEvent(self, ev, grid, ballStruct):
		if getConst("MODE") != "VS":
			if self.players[0] == None and ev.type == MOUSEBUTTONDOWN:
				if ev.button == 1:
					self.players[0] = self.profiles[0].getPlayer()
				elif ev.button == 3:
					self.profiles[0].selectNextClass()
			elif self.players[1] == None and ev.type == KEYDOWN:
				if ev.key == K_SPACE:
					self.players[1] = self.profiles[1].getPlayer()
				elif ev.key == K_v:
					self.profiles[1].selectNextClass()
			
		for p in self.getPlayers():
			if p:
				p.handleEvent(ev, grid, ballStruct)
				
	def beatLevel(self, levelOn):
		for p in [0, 1]:
			if self.players[p]:
				self.profiles[p].beatLevel(levelOn)
				self.profiles[p].save()
		self.players = [None, None]
			
	def update(self, grid, ballStruct):
		for p in [0, 1]:
			if self.players[p]:
				self.players[p].update(grid, ballStruct)
				if self.players[p].readyToDelete():
					self.profiles[p].addDeath()
					self.profiles[p].save()
					self.players[p] = None
			
	def drawMe(self):
		for p in self.getPlayers():
			if p:
				p.drawMe()
		for p in self.profiles:
			p.drawMe()
			
class Player:
	def __init__(self, team, controls, abilities, pos = -1):
		self.team = team
		self.controls = controls
		self.size = 20
		if pos == -1:
			self.pos = [getConst("SCREENSIZE")[0] / 2, getConst("SCREENSIZE")[1] - self.size]
		else:
			self.pos = pos
		self.target = self.pos
		self.speed = getConst("PLAYERSPEED")
		self.abilities = abilities#[Abilities.ExplodeBalls(), Abilities.SplitBalls(), Abilities.CreateBall()]
		self.keys = Keys()
		self.ballsCreated = []
		self.health = self.abilities[2].getPlayerHealth(); self.maxHealth = self.health
		self.points = 0
		self.ptrToBallStruct = None
		
	def getTeam(self):
		return self.team
		
	def getPos(self):
		return [self.pos[0], self.pos[1]]
		
	def getSize(self):
		return self.size
		
	def getAbilities(self):
		return self.abilities
		
	def getBallsControlled(self):
		return self.ballsCreated
		
	def getMaxBalls(self):
		return 1
	
	def addBallCreated(self, newBall):
		self.ballsCreated += [newBall]
		
	def deleteControlledBall(self, ball):
		b = 0
		while b < len(self.ballsCreated):
			if self.ballsCreated[b] is ball:
				del self.ballsCreated[b]
				return
			b += 1
		print "Not Found!", ball, self.ballsCreated
		
	def addPoints(self, amt):
		self.points += amt
		
	def getPoints(self):
		return self.points
		
	def readyToDelete(self):
		return self.health <= 0
		
	def getBallHealAmt(self):
		return self.abilities[2].getHealAmt()
		
	def collideWithBall(self, ball):
		if ball.getTeam() == self.team:
			amt = self.getBallHealAmt()

			if ball.getController() == self:
				ball.heal(amt)
			else:
				ball.heal(amt / 2)
		else:
			self.damage(ball.getDamage())
			ball.delete()
			
		self.abilities[2].hitBall(self, ball, self.ptrToBallStruct)
		
	def damage(self, amt):
		self.health -= max(amt, 0)
		if self.health <= 0:
			for b in self.ballsCreated:
				b.setColourCode(3)
				
	def hitBlock(self, ball, block, grid, players, effects, ballStruct):
		self.abilities[2].hitBlock(ball, block, grid, players, effects, ballStruct)
		
	def handleEvent(self, ev, grid, ballStruct):
		self.keys.handleEvent(ev)
				
	def update(self, grid, ballStruct):
		self.ptrToBallStruct = ballStruct
		for abil in self.abilities:
			abil.update(self, grid, ballStruct)
			
		if self.controls == 1:
			self.target = self.keys.getMousePos()
			if 1 in self.keys.getMouseButtons():
				self.abilities[0].activate(self, grid, ballStruct)
			if 3 in self.keys.getMouseButtons():
				self.abilities[1].activate(self, grid, ballStruct)
		elif self.controls == 2:
			self.target = [self.pos[0] + self.speed * self.keys.keyPressed(K_d) - self.speed * self.keys.keyPressed(K_a),
										 self.pos[1] + self.speed * self.keys.keyPressed(K_s) - self.speed * self.keys.keyPressed(K_w)]
			if self.keys.keyPressed(K_SPACE):
				self.abilities[1].activate(self, grid, ballStruct)
			if self.keys.keyPressed(K_v):
				self.abilities[0].activate(self, grid, ballStruct)
			
		direction = math.atan2(self.target[1] - self.pos[1], self.target[0] - self.pos[0])
		#speed = [self.target[0] - self.pos[0], self.target[1] - self.pos[1]]
		speed = [math.cos(direction) * self.speed, math.sin(direction) * self.speed]
		
		xCoord = posToCoord((self.pos[0] + self.size * getSign(speed[0]), self.pos[1]))
		yCoord = posToCoord((self.pos[0], self.pos[1] + self.size * getSign(speed[1])))
		xCollide = grid.getAt(xCoord); yCollide = grid.getAt(yCoord)
		
		if xCollide and not xCollide.getType():
			if math.fabs(self.pos[0] - self.target[0]) < math.fabs(speed[0]):
				self.pos[0] = self.target[0]
			else:
				self.pos = [self.pos[0] + speed[0], self.pos[1]]
			
		if yCollide and not yCollide.getType():
			if math.fabs(self.pos[1] - self.target[1]) < math.fabs(speed[1]):
				self.pos[1] = self.target[1]
			else:
				self.pos = [self.pos[0], self.pos[1] + speed[1]]
				
		if self.team == 1 and self.pos[1] < getConst("PLAYERMINYPOS"):
				self.pos[1] = getConst("PLAYERMINYPOS")
		elif self.team == 2 and self.pos[1] > getConst("SCREENSIZE")[1] - getConst("PLAYERMINYPOS"):
				self.pos[1] = getConst("SCREENSIZE")[1] - getConst("PLAYERMINYPOS")
				
	def drawMe(self):
		for abil in self.abilities:
			abil.drawMe(self)
		pos = (int(self.pos[0]), int(self.pos[1]))
		pct = (self.health / float(self.maxHealth)) * 0.7 + 0.3
		if self.controls == 1:
			clr = [int(255 * pct), 0, int(255 * pct)]
		else:
			clr = [0, int(255 * pct), 0]
		pygame.draw.circle(getConst("SURFACE"), clr, pos, int(self.size), 2)
		
class Keys:
	def __init__(self):
		self.pressed = {}
		self.mousePos = [0, 0]
		self.mouseButtons = []

	def getMousePos(self):
		return self.mousePos
		
	def getMouseButtons(self):
		return self.mouseButtons
		
	def keyPressed(self, key):
		return key in self.pressed
		
	def getKeys(self):
		return self.pressed
	
	def handleEvent(self, ev):
		if ev.type == KEYDOWN:
			self.pressed[ev.key] = True
		elif ev.type == KEYUP:
			if ev.key in self.pressed:
				del self.pressed[ev.key]
		elif ev.type == MOUSEMOTION:
			self.mousePos = ev.pos
		elif ev.type == MOUSEBUTTONDOWN:
			self.mousePos = ev.pos
			self.mouseButtons += [ev.button]
		elif ev.type == MOUSEBUTTONUP:
			self.mousePos = ev.pos
			if ev.button in self.mouseButtons:
				self.mouseButtons.remove(ev.button)