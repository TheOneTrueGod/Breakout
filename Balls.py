import math, Effects
from Globals import *

class BallStruct:
	def __init__(self):
		self.balls = []
		
	def update(self, grid, players, effects):
		b = 0
		while b < len(self.balls):
			self.balls[b].update(grid, players, effects, self)
			if self.balls[b].readyToDelete():
				self.balls[b].delete()
				del self.balls[b]
			else:
				b += 1
				
	def beatLevel(self):
		b = 0
		while b < len(self.balls):
			del self.balls[b]
			
	def addBall(self, newBall):#pos, team, damage, size):
		self.balls += [newBall]
		return newBall
		
	def getBalls(self):
		return self.balls
			
	def drawMe(self):
		for b in self.balls:
			b.drawMe()
			
class Ball:
	def __init__(self, pos, controller, damage, size, health = 16, direction = math.pi / 2.0, speed = 10, colourCode = 0, isControlled = False, team = 1, numWallHits = 7, isSplitBall = False):
		self.pos = [pos[0], pos[1]]
		self.speed = [math.cos(direction) * speed, math.sin(direction) * speed]
		self.size = size
		self.controller = controller
		self.damage = damage
		self.health = health
		self.maxHealth = health
		self.markedForDelete = False
		self.colourCode = colourCode
		self.isControlled = isControlled
		self.isEnchanted = False
		self.damaged = False
		self.team = team
		self.isSplitBall = isSplitBall
		self.damageTakenFromWalls = self.maxHealth * (1 / float(numWallHits))
		self.childInit()
	
	def childInit(self):
		pass
	
	def getTeam(self):
		return self.team
	
	def getPos(self):
		return [int(self.pos[0]), int(self.pos[1])]
		
	def getController(self):
		return self.controller
		
	def getDamage(self):
		return self.damage
		
	def getSize(self):
		return self.size
		
	def getHealth(self):
		return [self.health, self.maxHealth]
		
	def getDirection(self):
		return math.atan2(self.speed[1], self.speed[0])
		
	def getSpeed(self):
		return math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
		
	def getDamageTakenFromWalls(self):
		return self.damageTakenFromWalls
		
	def getDamageTakenFromBlocks(self):
		return self.damage
		
	def wasDamaged(self):
		return self.damaged
		
	def enchant(self):
		self.isEnchanted = True
		
	def setColourCode(self, newCC):
		self.colourCode = newCC
		
	def delete(self):
		self.markedForDelete = True
		if self.isControlled:
			self.controller.deleteControlledBall(self)
			self.isControlled = False
			
	def reduceHealth(self, amt):
		self.health -= amt
		if amt > 0:
			self.damaged = True
		
	def readyToDelete(self):
		return self.health <= 0 or self.markedForDelete
		
	def hitBlock(self, block, grid, players, effects, ballStruct):
		if block.getTeam() != self.getTeam():
			if block.getHealth()[0] <= 0:
				self.controller.addPoints(block.getPointValue())
			self.controller.hitBlock(self, block, grid, players, effects, ballStruct)
			block.damage(self, self.damage, ballStruct)
			self.reduceHealth(self.getDamageTakenFromBlocks())
			
	def collideWithPlayer(self, player):
		direction = math.atan2(self.pos[1] - player.getPos()[1], self.pos[0] - player.getPos()[0])
		speed = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
		self.speed = [math.cos(direction) * speed, math.sin(direction) * speed]
		player.collideWithBall(self)
		
	def collidesWithBlocks(self):
		return True
		
	def update(self, grid, players, effects, ballStruct):
		for player in players.getPlayers():
			if dist(self.pos, player.getPos()) <= (self.size + player.getSize()) ** 2:
				self.collideWithPlayer(player)
				#player.pos = [player.pos[0] - self.speed[0] / float(speed * 2), player.pos[1] - self.speed[1] / float(speed * 2)]
		
		xCoord = posToCoord((int(self.pos[0] + self.size * getSign(self.speed[0]) + self.speed[0]), int(self.pos[1])))
		yCoord = posToCoord((int(self.pos[0]), int(self.pos[1] + self.size * getSign(self.speed[1]) + self.speed[1])))
		xCollide = grid.getAt(xCoord); yCollide = grid.getAt(yCoord)
		
		if xCollide:
			if xCollide.getType():
				self.hitBlock(xCollide, grid, players, effects, ballStruct)
		else:
			self.reduceHealth(self.getDamageTakenFromWalls())
		
		if xCollide != yCollide != None:
			if yCollide.getType():
				self.hitBlock(yCollide, grid, players, effects, ballStruct)
		if yCollide == None:
			self.reduceHealth(self.getDamageTakenFromWalls())
			
		if (not xCollide or (xCollide.getType() and self.collidesWithBlocks() and xCollide.getTeam() != self.getTeam())) and self.health > 0:
			self.speed[0] *= -1
			
		if (not yCollide or (yCollide.getType() and self.collidesWithBlocks() and yCollide.getTeam() != self.getTeam())) and self.health > 0:
			self.speed[1] *= -1
			
		self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
		
	def heal(self, amt):
		self.health = min(max(self.health + amt, 0), self.maxHealth)
		
	def getColour(self):
		clr = [0, 0, 0]
		if self.colourCode == 0:
			clr = [int(50 + 100 * self.health / float(self.maxHealth))] * 3
		elif self.colourCode == 1:
			clr = [int(100 + 155 * self.health / float(self.maxHealth)), 0, int(100 + 155 * self.health / float(self.maxHealth))]
		elif self.colourCode == 2:
			clr = [0, int(100 + 155 * self.health / float(self.maxHealth)), 0]
		elif self.colourCode == 3:
			clr = [int(50 + 100 * self.health / float(self.maxHealth))] * 3
		return clr
		
	def drawMe(self):
		if self.health > 0:
			pos = (int(self.pos[0]), int(self.pos[1]))
			clr = self.getColour()
			if self.isEnchanted:
				pygame.draw.circle(getConst("SURFACE"), [150 + int(105 * self.health / float(self.maxHealth))] * 3, pos, int(self.size + 1), 1)
			pygame.draw.circle(getConst("SURFACE"), clr, pos, int(self.size))

class PlayerIgnoringBall(Ball):
	def getDamageTakenFromBlocks(self):
		return self.health
		
	def collideWithPlayer(self, player):
		pass
		
class LanceHead(PlayerIgnoringBall):
	def hitBlock(self, block, grid, players, effects, ballStruct):
		if block.getTeam() != self.getTeam():
			if not self.readyToDelete():
				Ball.hitBlock(self, block, grid, players, effects, ballStruct)
				for i in [1, 2]:
					ballStruct.addBall(Ball(self.getPos(), self.getController(), self.damage / 2.0, self.getSize(), 
																						self.getHealth()[1] / 2.0, math.pi / 4.0 + math.pi / 2.0 * (i - 1), self.getSpeed(), team = self.getTeam()))
			self.delete()
		
class ExplodingBall(Ball):
	def childInit(self):
		self.explosionRadius = 0
		
	def getDamageTakenFromWalls(self):
		return Ball.getDamageTakenFromWalls(self) * 2.0
		
	def getDamageTakenFromBlocks(self):
		return self.health
	
	def setUpgradeStats(self, primaryDamagePct, secondaryDamagePct, explosionRadius):
		self.explosionRadius = explosionRadius
		self.primaryDamagePct = primaryDamagePct
		self.secondaryDamagePct = secondaryDamagePct
		
	def getExplosionCoords(self):
		return [[-1,  0], [ 1,  0], [ 0,  1], [ 0, -1]] + \
					 [[ 1,  1], [-1,  1], [-1, -1], [ 1, -1]] * (self.explosionRadius >= 1) + \
					 [[-2,  0], [ 2,  0], [ 0,  2], [ 0, -2]] * (self.explosionRadius >= 2) + \
					 [[ 2,  1], [-2,  1], [-2, -1], [ 2, -1]] * (self.explosionRadius >= 3) + \
					 [[ 1,  2], [-1,  2], [-1, -2], [ 1, -2]] * (self.explosionRadius >= 4) + \
					 [[-3,  0], [ 3,  0], [ 0,  3], [ 0, -3]] * (self.explosionRadius >= 5) + \
					 [[ 3,  1], [-3,  1], [ 3, -1], [-3, -1]] * (self.explosionRadius >= 6) + \
					 [[ 1,  3], [ 1, -3], [-1,  3], [-1, -3]] * (self.explosionRadius >= 7) + \
					 [[-4,  0], [ 4,  0], [ 0,  4], [ 0, -4]] * (self.explosionRadius >= 8) + \
					 [[ 2,  2], [-2,  2], [ 2, -2], [-2, -2]] * (self.explosionRadius >= 9)
		
	def hitBlock(self, block, grid, players, effects, ballStruct):
		if not self.readyToDelete() and block.getTeam() != self.getTeam():
			damage = self.damage
			self.damage *= self.primaryDamagePct
			Ball.hitBlock(self, block, grid, players, effects, ballStruct)
			
			#Hit nearby targets
			maxDist = (self.explosionRadius + 4) / 5 + 1 #Gets the pattern 1, 2, 2, 3, 3, 3
			coord = posToCoord(block.getPos())
			for modCoord in self.getExplosionCoords():
				dist = (math.fabs(modCoord[0]) + math.fabs(modCoord[1]))
				#Make it deal less damage to farther away targets in the explosion
				self.damage = damage * 1.0 - (dist / float(maxDist)) * self.secondaryDamagePct
				explosionCoord = [coord[0] + modCoord[0], coord[1] + modCoord[1]]
				square = grid.getAt(explosionCoord)
				if square and square.getType():
					Ball.hitBlock(self, square, grid, players, effects, ballStruct)
			self.delete()
		
	def update(self, grid, players, effects, ballStruct):
		Ball.update(self, grid, players, effects, ballStruct)
		if self.health > 0:
			effects.addEffect(Effects.FadingBall(self.getPos(), self.getColour(), 8, int(self.size)))
					
class EnemyShot(Ball):
	def __init__(self, pos, team, damage, size, health = 1, direction = math.pi / 2.0, speed = 3):
		Ball.__init__(self, pos, team, damage, size, health = 1, direction = math.pi / 2.0, speed = 3)
		self.pos = [pos[0], pos[1]]
		self.speed = [math.cos(direction) * speed, math.sin(direction) * speed]
		self.size = size
		self.team = team
		self.damage = damage
		self.health = health
		self.maxHealth = health
		self.markedForDelete = False
		self.isControlled = False
		self.controller = None
		
	def hitBlock(self, block, grid, players, effects, ballStruct):
		pass
		
	def collidesWithBlocks(self):
		return False
		
	def getDamageTakenFromWalls(self):
		return 1
		
	def drawMe(self):
		if self.health > 0:
			pos = (int(self.pos[0]), int(self.pos[1]))
			clr = [0, 0, 255]
			pygame.draw.circle(getConst("SURFACE"), clr, pos, int(self.size))

class MiniBallLauncher(Ball):
	def childInit(self):
		self.timer = [0, 2]
		
	#def drawMe(self):
		#pass
	
	def update(self, grid, players, effects, ballStruct):
		self.timer[0] += 1
		if self.timer[0] >= self.timer[1]:
			self.timer[0] = 0
			ballStruct.addBall(PlayerIgnoringBall(self.getPos(), self.getController(), self.damage, self.getSize(), 
																						1, self.getDirection(), self.getSpeed(), team = self.getTeam(), numWallHits=1))
			self.health -= 1

class GhostBall(Ball):
	def childInit(self):
		self.lastHit = []
		
	def collidesWithBlocks(self):
		return False
	
	def hitBlock(self, block, grid, players, effects, ballStruct):
		if block not in self.lastHit and block.getTeam() != self.getTeam():
			block.damage(self, self.damage, ballStruct)
			self.health -= 1
			if self.damage <= 1:
				self.delete()
			if block.getHealth()[0] <= 0:
				self.controller.addPoints(block.getPointValue())
			self.lastHit += [block]
			if len(self.lastHit) > 5:
				del self.lastHit[0]
	
	def drawMe(self):
		if self.health > 0:
			pos = (int(self.pos[0]), int(self.pos[1]))
			clr = self.getColour()
			pygame.draw.circle(getConst("SURFACE"), clr, pos, int(self.size), 1)
			
class BallAttractor(Ball):
	def __init__(self, oldBall, controller, abilCreatedBy):
		Ball.__init__(self, [0, 0], controller, 0, 0)
		self.controlled = oldBall.isControlled
		oldBall.delete()
		self.pos = oldBall.pos
		self.oldBall = oldBall
		self.controller = controller
		self.abilCreatedBy = abilCreatedBy
		self.angle = math.atan2(oldBall.getPos()[1] - controller.getPos()[1], oldBall.getPos()[0] - controller.getPos()[0])
		self.distance = math.sqrt(dist(controller.getPos(), oldBall.getPos()))
		
	def update(self, grid, players, effects, ballStruct):
		self.distance *= 0.95
		self.angle = (self.angle + math.pi / 32.0) % (math.pi * 2)
		self.oldBall.pos = [self.controller.getPos()[0] + math.cos(self.angle) * self.distance, self.controller.getPos()[1] + math.sin(self.angle) * self.distance]
		if self.distance <= self.controller.getSize() / 2:
			self.delete()
			self.abilCreatedBy.ballCollidedWithPlayer(self.oldBall, self.controller, self.controlled, grid, effects, ballStruct)
			
	def drawMe(self):
		self.oldBall.drawMe()