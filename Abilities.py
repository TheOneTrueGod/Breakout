import random, Balls, math, pygame
from Globals import *
class Ability:
	def __init__(self, upgrades):
		self.cooldown = [0, 50]
		self.upgrades = upgrades
		self.childInit()
		
	def childInit(self):
		self.cooldown = [0, 50]
		
	def getHealAmt(self):
		return 0
		
	def getUpgradeName(self, upgradeNum):
		return ""
		
	def getDescription(self, upgradeNum):
		return ""
		
	def getPlayerHealth(self):
		return 4 + int(sum(self.upgrades) / 2.5)
		
	def update(self, owner, grid, ballStruct):
		if self.cooldown[0] > 0:
			self.cooldown[0] -= 1
			
	def hitBlock(self, ball, block, grid, players, effects, ballStruct):
		pass
		
	def activate(self, owner, grid, ballStruct):
		pass
		
	def drawMe(self, player):
		pass
#Classes	
class CreateBall(Ability):
	def childInit(self):
		self.cooldown = [50, 200]
		self.maxBalls = -1
		self.damage = 3.0
		self.health = 25
		self.healAmt = 7
		
	def getBallDamage(self, levelOffset = 0):
		return 3.0
		
	def getBallHealth(self, levelOffset = 0):
		return 25
		
	def getHealAmt(self, levelOffset = 0):
		return 7
		
	def update(self, owner, grid, ballStruct):
		if self.cooldown[0] > 0 and (self.cooldown[0] > self.cooldown[1] / 2 or self.maxBalls == -1 or len(owner.getBallsControlled()) < self.maxBalls):
			self.cooldown[0] -= 1
			
		if self.cooldown[0] <= 0:
			self.activate(owner, grid, ballStruct)
			self.cooldown[0] += self.cooldown[1]
			
	def hitBlock(self, ball, block, grid, players, effects, ballStruct):
		pass
			
	def hitBall(self, owner, ball, ballStruct):
		pass
		
	def activate(self, owner, grid, ballStruct):
		pos = owner.getPos()
		hlth = self.getBallHealth()
		speed = getConst("BALLSPEED")
		size = 5
		owner.addBallCreated(ballStruct.addBall(
			Balls.Ball([pos[0] + random.uniform(-2, 2), pos[1] - 5 * (((owner.getTeam() % 2) * 2) - 1)], owner, self.getBallDamage(), size, speed=speed, health = hlth, 
									colourCode = owner.controls, isControlled = True, team = owner.getTeam())))
		
	def drawMe(self, player):
		surface = getConst("SURFACE")
		if 1 < self.cooldown[0] < self.cooldown[1] * 0.5:
			size = int(player.getSize() * (1 - (self.cooldown[0] / (self.cooldown[1] * 0.5))))
			if size > 2:
				pos = [int(player.getPos()[0]), int(player.getPos()[1])]
				pygame.draw.circle(surface, [60, 60, 60], pos, size, 2)
				
class BruteClass(CreateBall):
	def childInit(self):
		self.cooldown = [50, 200]
		self.maxBalls = 2
		
	def getBallDamage(self, levelOffset = 0):
		return 5.0 + (self.upgrades[0] + levelOffset) * 1
		
	def getBallHealth(self, levelOffset = 0):
		return (self.getBallDamage(levelOffset) * (16.0 + (self.upgrades[2] + levelOffset) * 2.0))
		
	def getHealAmt(self, levelOffset = 0):
		return 12 + (self.upgrades[1] + levelOffset) * 3 + (self.upgrades[2] + levelOffset) * 1.5
		
	def getPlayerHealth(self, levelOffset = 0):
		return 4 + (self.upgrades[2] + levelOffset) + sum(self.upgrades) / 2
		
	def getCritDamage(self, levelOffset = 0):
		return 2 + (self.upgrades[3] - 1 + levelOffset) * 0.25
		
	def getCritChance(self, levelOffset = 0):
		return 0.02 * (self.upgrades[3] + levelOffset)

	def hitBlock(self, ball, block, grid, players, effects, ballStruct):
		if random.random() <= self.getCritChance():
			block.damage(ball, self.getBallDamage() * (self.getCritDamage() - 1), ballStruct)
			
	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 3:
			return ["Strength", "Health", "Endurance", "Critical"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		if upgradeNum == 0:
			return "Strength: Increases damage from " + str(self.getBallDamage()) + " to " + str(self.getBallDamage(1))
		elif upgradeNum == 1:
			return "Health: Increases the amount you heal the ball from " + str(self.getBallHealth()) + " to " + str(self.getBallHealth(1)) + " and increases your health from " + str(self.getPlayerHealth()) + " to " + str(self.getPlayerHealth(1))
		elif upgradeNum == 2:
			return "Endurance: Increases ball health from " + str(self.getBallHealth()) + " to " + str(self.getBallHealth(1)) + " and the amount you heal it when you strike it from " + str(self.getHealAmt()) + " to " + str(self.getHealAmt(1))
		elif upgradeNum == 3:
			return "Critical: Increases chance for a critical hit from " + str(int(self.getCritChance() * 100)) + "% to " + str(int(self.getCritChance(1) * 100)) + "% and increases critical damage from " + str(int((self.getCritDamage()) * 100) / 100.0) + "x damage to " + str(round((self.getCritDamage(1)) * 100) / 100.0) + "x damage"
		return ""
		
class BlasterClass(CreateBall):
	def childInit(self):
		self.cooldown = [50, self.getCooldown()]
		self.maxBalls = 6
		self.damage = 3.0 + self.upgrades[1] * 0.2
		self.health = 70 + self.upgrades[1] * 7
		self.healAmt = 10 + self.upgrades[1] * 0.4
		
	def getCooldown(self, levelOffset = 0):
		return 200 - (self.upgrades[2] + levelOffset) * 6
		
	def getBallDamage(self, levelOffset = 0):
		return 3.0 + (self.upgrades[1] + levelOffset) * 1
		
	def getBallHealth(self, levelOffset = 0):
		return 70 + (self.upgrades[1] + levelOffset) * 7
		
	def getHealAmt(self, levelOffset = 0):
		return 10 + (self.upgrades[1] + levelOffset) * 0.5
	
	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 3:
			return ["Creation", "Strength", "Speed", "Destruction"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		if upgradeNum == 0:
			return "Creation: Increases the chance for one of your balls to create a smaller ball each time it hits a block from " + str(int(self.getSplitChance() * 100)) + "% to " + str(int(self.getSplitChance(1) * 100)) + "%"
		elif upgradeNum == 1:
			return "Strength: Increases the damage your balls deal from " + str(self.getBallDamage()) + " to " + str(self.getBallDamage(1))
		elif upgradeNum == 2:
			return "Speed: Decreases the time it takes you to create balls from " + str(self.getCooldown()) + " to " + str(self.getCooldown(1))
		elif upgradeNum == 3:
			return "Destruction: Increases the chance for your ball to damage all nearby blocks from " + str(int(self.getExplodeChance() * 100)) + "% to " + str(int(self.getExplodeChance(1) * 100)) + "%"
		return ""
		
	def getSplitChance(self, levelOffset = 0):
		return (self.upgrades[0] + levelOffset) * 0.02
		
	def getExplodeChance(self, levelOffset = 0):
		return (self.upgrades[3] + levelOffset) * 0.05
		
	def hitBlock(self, ball, block, grid, players, effects, ballStruct):
		if block.getType():
			if random.random() <= self.getExplodeChance():
				coord = posToCoord(block.getPos())
				for x in [-1, 0, 1]:
					for y in [-1, 0, 1]:
						if x != 0 or y != 0:
							explosionCoord = [coord[0] + x, coord[1] + y]
							square = grid.getAt(explosionCoord)
							if square and square.getType():
								square.damage(ball, ball.getDamage() / 2.0, ballStruct)
			elif not ball.isSplitBall and random.random() <= self.getSplitChance():
				direction = ball.getDirection() + math.pi
				pos = [ball.getPos()[0] + math.cos(direction), ball.getPos()[1] + math.sin(direction)]
				dmg = ball.getDamage() / 2.0
				ballStruct.addBall(Balls.Ball(pos, ball.getController(), dmg, ball.getSize() - 2, ball.getHealth()[1] / 2.0, direction, ball.getSpeed(), team = ball.getTeam(), isSplitBall = True))
	
class EnchanterClass(CreateBall):
	def childInit(self):
		self.cooldown = [50, 200 - self.upgrades[2] * 6]
		self.maxBalls = 6 + self.upgrades[2]
		self.damage = 1.5 + self.upgrades[0] * 0.1
		self.health = 160 + self.upgrades[1] * 20
		self.healAmt = 15 + self.upgrades[0] * 0.4 + self.upgrades[1] * 0.5
		
	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 3:
			return ["Strength", "Endurance", "Control", "Clone"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		if upgradeNum == 0:
			return "Strength: Increases the damage your balls deal.  Damage currently at " + str(self.damage)
		elif upgradeNum == 1:
			return "Endurance: Increases ball durability and the amount you heal it when you strike it."
		elif upgradeNum == 2:
			return "Control: Increases the maximum number of balls you can have under control at once to " + str(self.maxBalls)
		elif upgradeNum == 3:
			return "Clone: A " + str(int(self.getCloneChance() * 100)) + "% chance to create a new ball when you hit one of your balls"
		return ""
		
	def getCloneChance(self):
		return (self.upgrades[3] + 0.1) * 0.02
		
	def hitBall(self, owner, ball, ballStruct):
		if ball.isControlled and ball.wasDamaged() and random.random() <= self.getCloneChance():
			pos = owner.getPos()
			hlth = self.health / 2.0
			speed = getConst("BALLSPEED")
			size = 3
			offset = random.uniform(-3, 3)
			ballStruct.addBall(
				Balls.Ball([pos[0] + offset, pos[1] - 5 * (((owner.getTeam() % 2) * 2) - 1)], owner, self.damage / 2.0, 
										size, speed=speed, health = hlth, 
										colourCode = 0, isControlled = False, team = owner.getTeam(), numWallHits = 5))
		
	def activate(self, owner, grid, ballStruct):
		pos = owner.getPos()
		hlth = self.health
		speed = getConst("BALLSPEED")
		size = 5
		offset = random.uniform(0, 2)
		for i in [-1, 1]:
			owner.addBallCreated(ballStruct.addBall(
				Balls.Ball([pos[0] + offset * i, pos[1] - 5 * (((owner.getTeam() % 2) * 2) - 1)], owner, self.damage, size, speed=speed, health = hlth, 
										colourCode = owner.controls, isControlled = True, team = owner.getTeam(), numWallHits = 12)))
		
#Abilities		
class SplitBalls(Ability):
	def childInit(self):
		self.cooldown = [0, 10]
		
	def activate(self, owner, grid, ballStruct):
		if self.cooldown[0] <= 0:
			b = 0
			balls = owner.getBallsControlled()
			while b < len(balls):
				if not balls[b].readyToDelete() and balls[b].wasDamaged():
					numSplits = self.getNumBalls()
					for i in range(numSplits):
						direction = math.pi * 2.0 / float(numSplits) * (i) + 0.5
						pos = [balls[b].getPos()[0] + math.cos(direction), balls[b].getPos()[1] + math.sin(direction)]
						dmg = balls[b].getDamage() * self.getBallDamage()
						ballStruct.addBall(Balls.Ball(pos, balls[b].getController(), dmg, balls[b].getSize() - 2, balls[b].getHealth()[1] * self.getLifespan(), direction, balls[b].getSpeed(), team = balls[b].getTeam(), isSplitBall = True))
					balls[b].delete()
				else:
					b += 1
					
	def getNumBalls(self, levelMod = 0):
		#4 + 1 / lv
		level = self.upgrades[2] + levelMod
		return int(level + 4)
		
	def getBallDamage(self, levelMod = 0):
		#50% + 15% / lv
		level = self.upgrades[0] + levelMod
		return 0.5 + (level / 10.0) * 1.5
		
	def getLifespan(self, levelMod = 0):
		#50% + 20% / lv
		level = self.upgrades[1] + levelMod
		return 0.5 + (level / 10.0) * 2.0

	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 2:
			return ["Ball Damage", "Ball Lifespan", "Number of Balls"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		if upgradeNum == 0:
			return "Ball Damage: Increases the damage of the split balls from "+ str(int(self.getBallDamage() * 100)) + "% to " + str(int(self.getBallDamage(1) * 100)) + "%"
		elif upgradeNum == 1:
			return "Ball Lifespan: Increases lifespan of split balls from " + str(int(self.getLifespan() * 100)) + "% to "+ str(int(self.getLifespan(1) * 100)) + "%"
		elif upgradeNum == 2:
			return "Number of Balls: Increases number of balls split off from " + str(self.getNumBalls()) + " to " + str(self.getNumBalls(1))
		return ""
			
class ExplodeBalls(SplitBalls):
	def childInit(self):
		self.cooldown = [0, 10]
		
	def activate(self, owner, grid, ballStruct):
		if self.cooldown[0] <= 0:
			b = 0
			balls = owner.getBallsControlled()
			while b < len(balls):
				if not balls[b].readyToDelete() and balls[b].wasDamaged():
					health = 10
					newBall = Balls.ExplodingBall(balls[b].getPos(), balls[b].getController(), balls[b].getDamage() + 2, balls[b].getSize(), health, balls[b].getDirection(), balls[b].getSpeed(), team = balls[b].getTeam())
					newBall.setUpgradeStats(self.getPrimaryDamageMod(), self.getSecondaryDamageMod(), self.getExplosionRadius())
					ballStruct.addBall(newBall)
					balls[b].delete()
				else:
					b += 1
					
	def getExplosionRadius(self, levelMod = 0):
		return self.upgrades[2] + levelMod
		
	def getPrimaryDamageMod(self, levelMod = 0):
		#80% + 15% / lv
		return 0.8 + ((self.upgrades[0] + levelMod) / 10.0) * 1.5
		
	def getSecondaryDamageMod(self, levelMod = 0):
		#50% + 10% / lv
		return 0.5 + ((self.upgrades[1] + levelMod) / 10.0) * 1.0

	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 2:
			return ["Primary Damage", "Explosion Damage", "Radius"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		if upgradeNum == 0:
			return "Primary Damage: Increases damage done to primary block hit from " + str(int(self.getPrimaryDamageMod() * 100)) + "% to " + str(int(self.getPrimaryDamageMod(1) * 100)) + "%"
		elif upgradeNum == 1:
			return "Secondary Damage: Increases damage done in the explosion from " + str(int(self.getSecondaryDamageMod() * 100)) + "% to " + str(int(self.getSecondaryDamageMod(1) * 100)) + "%"
		elif upgradeNum == 2:
			return "Radius: Increases the radius of the explosion from " + str(self.getExplosionRadius()) + " to " + str(self.getExplosionRadius(1))
		return ""
					
class EnchantBalls(SplitBalls):
	def childInit(self):
		self.cooldown = [0, 500]
		
	def activate(self, owner, grid, ballStruct):
		if self.cooldown[0] <= 0:
			b = 0
			balls = ballStruct.getBalls()
			while b < len(balls):
				if not balls[b].isEnchanted and balls[b].getController() == owner:
					balls[b].enchant()
					balls[b].maxHealth = balls[b].maxHealth * 1.2
					balls[b].heal(balls[b].maxHealth / 2.0)
					balls[b].damage *= 1.2
				b += 1
				
	def getUpgradeName(self, upgradeNum):
		return ""
		if 0 <= upgradeNum <= 2:
			return ["Ball Damage", "Ball Lifespan", "Number of Balls"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		return ""
		if upgradeNum == 0:
			return "Ball Damage: Increases the damage of the split balls.  Damage at: " + str(int(self.getBallDamage() * 100)) + "%"
		elif upgradeNum == 1:
			return "Ball Lifespan: Lifespan of split balls is " + str(int(self.getLifespan() * 100)) + "% of the old ball."
		elif upgradeNum == 2:
			return "Number of Balls: Number of balls split off: " + str(self.getNumBalls())
		return ""
				
class TargetBalls(SplitBalls):
	def childInit(self):
		self.cooldown = [0, 200]
		
	def activate(self, owner, grid, ballStruct):
		if self.cooldown[0] <= 0:
			b = 0
			balls = ballStruct.getBalls()
			toAdd = []
			while b < len(balls):
				if balls[b].getController() == owner:# and not balls[b].isControlled:
					toAdd += [Balls.BallAttractor(balls[b], owner, self)]
				b += 1
			for ball in toAdd:
				ballStruct.addBall(ball)
			self.cooldown[0] = self.cooldown[1]
			
	def ballCollidedWithPlayer(self, ball, controller, controlled, grid, effects, ballStruct):
		size = 2
		for i in range(1 + (controlled * 2)):
			angle = random.uniform(math.pi * 3 / 2.0 - math.pi / 4.0, math.pi * 3 / 2.0 + math.pi / 4.0)
			ballStruct.addBall(Balls.PlayerIgnoringBall(controller.getPos(), controller, ball.getDamage(), size, health = 1, direction = angle, speed = 15, team = controller.getTeam(), numWallHits = 1))
					
	def getUpgradeName(self, upgradeNum):
		return ""
		if 0 <= upgradeNum <= 2:
			return ["Ball Damage", "Ball Lifespan", "Number of Balls"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		return ""
		if upgradeNum == 0:
			return "Ball Damage: Increases the damage of the split balls.  Damage at: " + str(int(self.getBallDamage() * 100)) + "%"
		elif upgradeNum == 1:
			return "Ball Lifespan: Lifespan of split balls is " + str(int(self.getLifespan() * 100)) + "% of the old ball."
		elif upgradeNum == 2:
			return "Number of Balls: Number of balls split off: " + str(self.getNumBalls())
		return ""
					
class LanceBall(SplitBalls):
	def activate(self, owner, grid, ballStruct):
		if self.cooldown[0] <= 0:
			b = 0
			balls = owner.getBallsControlled()
			while b < len(balls):
				if not balls[b].readyToDelete() and balls[b].wasDamaged():
					direction = balls[b].getDirection()#-math.pi / 2.0
					pos = balls[b].getPos()
					dmg = balls[b].getDamage() * self.getLanceDamage()
					ballStruct.addBall(Balls.LanceHead(pos, balls[b].getController(), dmg, balls[b].getSize(), 
																				balls[b].getHealth()[1], direction, balls[b].getSpeed(), team = balls[b].getTeam(), numWallHits=4))
					dmg = balls[b].getDamage() * self.getTailDamage()
					numToShoot = self.getNumBalls()
					ballStruct.addBall(Balls.MiniBallLauncher(pos, balls[b].getController(), dmg, balls[b].getSize() / 2.0, 
																				numToShoot, direction, balls[b].getSpeed(), team = balls[b].getTeam()))
					balls[b].delete()
				else:
					b += 1
					
	def getLanceDamage(self, levelOffset = 0):
		return 1.0 + (self.upgrades[2] + levelOffset) * 0.2
					
	def getTailDamage(self, levelOffset = 0):
		return 0.25 + (self.upgrades[1] + levelOffset) * 0.05
		
	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 2:
			return ["Tail Size", "Tail Damage", "Lance Power"][upgradeNum]
		return ""
		
	def getNumBalls(self, levelOffset=0):
		return 5 + int((self.upgrades[0] + levelOffset))
		
	def getDescription(self, upgradeNum):
		if upgradeNum == 0:
			return "Tail Size: Increases the number of tail balls from " + str(int(self.getNumBalls())) + " to " + str(int(self.getNumBalls(1)))
		elif upgradeNum == 1:
			return "Tail Damage: Increases the amount of damage each ball in the tail does from " + str(int(self.getTailDamage() * 100)) + "% to "  + str(int(self.getTailDamage(1) * 100)) + "%"
		elif upgradeNum == 2:
			return "Lance Power: Increases the amount of damage the lance head and the lance head fragments deal from " + str(int(self.getLanceDamage() * 100)) + "% to " + str(int(self.getLanceDamage(1) * 100)) + "%"
		return ""
					
class GhostBall(SplitBalls):
	def getUpgradeName(self, upgradeNum):
		if 0 <= upgradeNum <= 2:
			return ["Durability", "Piercing", "Ghost Damage"][upgradeNum]
		return ""
		
	def getDescription(self, upgradeNum):
		return ""
		if upgradeNum == 0:
			return "Ball Damage: Increases the damage of the split balls.  Damage at: " + str(int(self.getBallDamage() * 100)) + "%"
		elif upgradeNum == 1:
			return "Ball Lifespan: Lifespan of split balls is " + str(int(self.getLifespan() * 100)) + "% of the old ball."
		elif upgradeNum == 2:
			return "Number of Balls: Number of balls split off: " + str(self.getNumBalls())
		return ""
		
	def getBallDamage(self, levelOffset):
		return 0.5 + (self.upgrades[2] + levelOffset) * 0.1
		
	def getNumPierces(self, levelOffset):
		return 5 + (self.upgrades[1] + levelOffset)
		
	def getWallBounces(self, levelOffset):
		return 1 + (self.upgrades[0] + levelOffset) * 0.7
		
	def activate(self, owner, grid, ballStruct):
		if self.cooldown[0] <= 0:
			b = 0
			balls = owner.getBallsControlled()
			while b < len(balls):
				if not balls[b].readyToDelete() and balls[b].wasDamaged():
					pos = balls[b].getPos()
					dmg = balls[b].getDamage() * self.getBallDamage(0)
					health = self.getNumPierces(0)
					ballStruct.addBall(Balls.GhostBall(pos, balls[b].getController(), dmg, balls[b].getSize(), 
																				health, balls[b].getDirection(), balls[b].getSpeed(), team = balls[b].getTeam(), numWallHits = self.getWallBounces(0)))
					balls[b].delete()
				else:
					b += 1
				
def getAbilities(className):
	if className == "Brute":
		return [LanceBall, GhostBall, BruteClass]
	elif className == "Enchanter":
		return [EnchantBalls, TargetBalls, EnchanterClass]
	return [ExplodeBalls, SplitBalls, BlasterClass]
	

			#self.cooldown[0] = self.cooldown[1]
	
#Ball that pierces through all blocks (doesn't necessarily destroy them)
#Splitting Ball

#Each character has 2 generic abilities, and 1 class
#Each ability/class has 4(maybe 3?) upgrades.
#Classes (Brute, Controller, Blaster, 
#Blaster: Based on dealing good damage through abilities.  Medium amount of low-md damage balls
	#Class Upgrades -- Speed (Faster creation of balls)
	#									 Power (More damage from abilities)
	#									 
	#Brute: Based on throwing out single powerful balls.  Can only have control a couple of balls at a time.?
	#Class Upgrades  -- Strength (Bonus to ball damage, reduces firing rate)
	#										Rejuvinate (Heals the ball more when it is hit.)
	#										Endurance     (Increases player health, ball health, and heals more to the ball when the player hits it.)
	#										Critical			(Chance of dealing extra damage when ball hits.  (1% at 150% dmg to 10% at 300% dmg)) (Maybe some damage is dealt to block behind hit block as well.)
	
	
#Abilities
	#Exploding Ball (Created already)
		#Increased Damage (100% damage - 200% damage) (Or maybe +1 to + 10 damage)
		#Increased Explosion Damage (50% of primary damage - 100% of primary damage
		#Increased Radius (Takes N points to be effective.  Radius starts at as a plus sign, increases to 3x3 box, then a 5x5 box.)
	#Splitting Ball (Created already)
		#Increased Damage (25% damage - 50% damage) (or maybe 25% primary + 1 to + 5 damage)
		#Increased Splits (More balls per usage)
		#Increased lifespan (Increases the lifespan of the split balls)
	#Lance (Created)
		#Increased Damage (150% - 300% damage on primary, 25% - 50% on secondary)
		#Increased Trail (Increases number of trailing small balls
		#Increased trail lifespan (Increases number of bounces trail can survive for.  Primary ball never survives more than 1 hit.
	#Piercing Ball (Created)
		#Increased piercing (Can only pierce a certain number of blocks.  Starts at 2, ends higher?  They are also limited by their health.
		#Increased damage (75% - 150% damage)
		#Ignore Armour (ignores armour.  starts at 1, ends at some higher number)
	#Magic Ball (Imbues balls with magic, healing them and increasing their damage.  Damage/Health can only be increased once, but this doesn't restrict the usage of other abilities.)
		#Increased healing (5% - 100%)
		#Increased damage (100% - 250%)
		#Increased health (+5 - + 20 or some'n like that)
	#Control Balls (Balls circle around you in tighter and tighter circles.  When they hit you they are destroyed, and a one-shot ball is flung at a random block.
		#Increased Area
		#Increase damage (50% of destroyed ball - 100%)
		#Increased max # of balls (At half level, will affect allied balls.  At max level, will affect enemy shots.)
		
#Unattached Upgrades
	#Create small ball when big ball hits a block or destroys a block
	#Minor area of effect damage on all attacks
	#Ball splits into smaller balls when it destroys a block
	#Dodge: Decreases your size and increases your speed
	
	
#Class Idea; Destroyer.  % chance things will happen when he hits a block.  Abilities do things like buff up the ball for one hit, and if it destroys a block, keep the buff on it. Or heal all of your balls.  Or something.
#Mitch's number: 905 420 0459