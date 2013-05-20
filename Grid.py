import os, pygame, Balls, random, math
from Globals import *

#1 - basic block
#2 - attacking block
#3 - armour block
#4 - regen block
#5 - heal-other blocks (probably shouldn't be used)
#6 - lava block
#7 - explody block
#Difficulties range from 0 to 5
gridPics = {}
gridStats = {"BaseStats":{"Health":5, "NeedsUpdates":False, "Armour":0, "Damage":1, "Destructable":True, 
						 "FireRate":200, "FireChance":0.01, "RegenRate":200, "RegenChance":1, "RegenAmount":1, 
						 "ShotBounces":1, "NumShots":1, "HealRate":100, "HealAmount":1, "HealChance":0.1, "NumFragments":5, 
						 "FragmentBounces":1, "Points":1},
						 "1":{0:{"Health":2 * 3, "Points":1}, 1:{"Health":4 * 3, "Points":2}, 2:{"Health":6 * 3, "Points":3}, 
						      3:{"Health":9 * 3, "Points":4}, 4:{"Health":11 * 3, "Points":5}, 5:{"Health":14 * 3, "Points":6}},
						 "2":{0:{"Health":1 * 3, "Points":1,  "NeedsUpdates":True, "Armour":1, "Damage":1, "FireRate":200},
									1:{"Health":3 * 3, "Points":2,  "FireRate":180},
									2:{"Health":5 * 3, "Points":3,  "FireRate":160, "FireChance":0.05},
									3:{"Health":8 * 3, "Points":4, "FireRate":130, "FireChance":0.05},
									4:{"Health":10 *3, "Points":5, "FireRate":110, "FireChance":0.1},
									5:{"Health":13 *3, "Points":6, "FireRate":90, "FireChance":0.1, "ShotBounces":2, "NumShots":3},
									6:{"Health":20 *3, "Points":6, "FireRate":45, "FireChance":0.5, "ShotBounces":4, "NumShots":1}},
						 "3":{0:{"Health":10, "Points":1,  "Armour":1}, #5
									1:{"Health":8 , "Points":2,  "Armour":2}, #8
									2:{"Health":12, "Points":3,  "Armour":4}, #12
									3:{"Health":17, "Points":4,  "Armour":6},
									4:{"Health":20, "Points":5,  "Armour":8},
									5:{"Health":24, "Points":6,  "Armour":10},
									6:{"Health":30, "Points":6,  "Armour":15}
									},
						 "4":{0:{"Health":3 * 3, "Points":1, "RegenRate":400, "NeedsUpdates":True},
									1:{"Health":5 * 3, "Points":2, "RegenRate":380},
									2:{"Health":7 * 3, "Points":3, "RegenRate":380},
									3:{"Health":10 *3, "Points":4, "Armour":1, "RegenRate":360},
									4:{"Health":11 *3, "Points":5, "Armour":1, "RegenRate":340},
									5:{"Health":10 *3, "Points":6, "Armour":2, "RegenRate":340, "RegenAmt":2},
									6:{"Health":20 *3, "Points":6, "Armour":3, "RegenRate":250}},
							"5":{0:{"Health":2  * 3, "Points":1, "HealRate":200, "NeedsUpdates":True},
									 1:{"Health":3  * 3, "Points":2, "HealRate":190},
									 2:{"Health":5  * 3, "Points":3, "HealRate":190},
									 3:{"Health":7  * 3, "Points":4, "HealRate":180},
									 4:{"Health":9  * 3, "Points":5, "HealRate":180},
									 5:{"Health":11 * 3, "Points":6, "HealRate":200, "HealAmount":2}},
							"6":{0:{"Health":3  * 3, "Points":1},
									 1:{"Health":4  * 3, "Points":2, "Armour":1, "NumShots":2},
									 2:{"Health":5  * 3, "Points":3, "Armour":2, "NumShots":3},
									 3:{"Health":7  * 3, "Points":4, "Armour":2, "NumShots":3, "ShotBounces":2},
									 4:{"Health":8  * 3, "Points":5, "Armour":3, "NumShots":4, "ShotBounces":2},
									 5:{"Health":9  * 3, "Points":6, "Armour":4, "NumShots":3, "ShotBounces":4}},
							"7":{0:{"Health":1 * 3, "Points":1, "NumFragments":5},
									 1:{"Health":2 * 3, "Points":2, "NumFragments":6},
									 2:{"Health":3 * 3, "Points":3, "NumFragments":8},
									 3:{"Health":3 * 3, "Points":4, "NumFragments":10},
									 4:{"Health":4 * 3, "Points":5, "NumFragments":14, "FragmentBounces":2},
									 5:{"Health":4 * 3, "Points":6, "NumFragments":18, "FragmentBounces":2}}
						}

def getGridStat(stat, blockType, blockStrength):
	global gridStats
	if blockType in gridStats:
		if blockStrength in gridStats[blockType]:
			if stat in gridStats[blockType][blockStrength]:
				return gridStats[blockType][blockStrength][stat]
			elif 0 in gridStats[blockType] and stat in gridStats[blockType][0]:
				return gridStats[blockType][0][stat]
			elif stat in gridStats["BaseStats"]:
				return gridStats["BaseStats"][stat]
	print "******Warning:", [blockType, blockStrength], "doesn't have a corresponding stat block"
	if stat in gridStats["BaseStats"]:
		return gridStats["BaseStats"][stat]
	print "******Warning:", stat, "is not a valid stat"
	return 0
	
def loadBlockPic(picToLoad):
	path = os.path.join("Data", "Pics", "Blocks", picToLoad + ".PNG")
	if not os.path.exists(path):
		print "ERROR, file not found: '" + path + "'"
		assert(picToLoad != "NoBlock")
		return loadBlockPic("NoBlock")
	pic = pygame.image.load(path)
	if "Damage" in picToLoad:
		pic.set_colorkey([255, 0, 128])
	frames = pic.get_height() / getConst("SQUARESIZE")[1]
	toRet = []
	for y in xrange(frames):
		toRet += [[]]
		for x in xrange(5 - 4 * ("Damage" in picToLoad)):
			newPic = pic.subsurface([0, y * getConst("SQUARESIZE")[1], getConst("SQUARESIZE")[0], getConst("SQUARESIZE")[1]]).copy()
			if "Damage" not in picToLoad:
				drawBlockPic("Damage" + str(picToLoad), [0, 0], x, 0, surface = newPic)
			toRet[y] += [newPic]

	return toRet
	
def drawBlockPic(pic, pos, frame, damageFrame, surface = None):
	global gridPics
	if pic in gridPics:
		if 0 <= frame < len(gridPics[pic]) and ((0 <= damageFrame < 5 and pic != "Damage") or damageFrame == 0 and pic == "Damage"):
			if surface is None:
				surface = getConst("SURFACE")
			toDraw = gridPics[pic][frame][damageFrame]
			surface.blit(toDraw, pos)
		else:
			drawBlockPic("NoBlock", pos, 0, 0, surface)
	else:
		gridPics[pic] = loadBlockPic(pic)
		drawBlockPic(pic, pos, frame, damageFrame, surface)
		
class Grid:
	def __init__(self, levelOn = 1):
		self.grid = []
		self.updateList = []
		self.numSquares = 0
		self.levelOn = levelOn
		self.noLevelLoaded = False
		self.updatedOnce = False
		if levelOn == "VS":
			self.setupVS()
		else:
			self.loadFromFile("Level" + str(levelOn))
		
	def skipLevel(self):
		if getConst("MODE") != "VS":
			self.numSquares = 0
		
	def isDone(self):
		return self.noLevelLoaded
		
	def goBackALevel(self):
		if getConst("MODE") != "VS":
			self.levelOn -= 2
			self.numSquares = 0
		
	def getNumSquares(self):
		return self.numSquares
		
	def setupVS(self):
		self.grid = []
		self.numSquares = [0, 0]
		CONSTANTS["SCREENSIZE"] = [600, 400] # 12 x 20
		CONSTANTS["MINYPOS"] = 350
		CONSTANTS["SURFACE"] = pygame.display.set_mode(getConst("SCREENSIZE"), pygame.FULLSCREEN * (getConst("FULLSCREEN") != 0))
		for y in range(4):
			newRow = []
			for x in range(12):
				newRow += [EmptySquare()]
			self.grid += [newRow]
			
		for t in [2, 1]:
			for y in range(6):
				newRow = []
				for x in range(12):
					if t == 1:
						type = "1" + str(y / 2)
					else:
						type = "1" + str(2 - y / 2)
					newSquare = Square(type, [len(newRow)    * getConst("SQUARESIZE")[0],
																 len(self.grid) * getConst("SQUARESIZE")[1]], self, team = t)
					newRow += [newSquare]
					self.numSquares[t - 1] += 1
				self.grid += [newRow]
				
		for y in range(4):
			newRow = []
			for x in range(12):
				newRow += [EmptySquare()]
			self.grid += [newRow]
				
	def loadFromFile(self, levelFile):
		CONSTANTS["MODE"] = "MAIN"
		path = os.path.join("Data", "Levels", levelFile + ".lev")
		if not os.path.exists(path):
			print "Error:  Level file not found: '" + path + "'"
			self.numSquares = 1
			self.noLevelLoaded = True
			return
		numRows = (getConst("SCREENSIZE")[1] / getConst("SQUARESIZE")[1])
		numCols = (getConst("SCREENSIZE")[0] / getConst("SQUARESIZE")[0])
		fileIn = open(path)
		self.grid = []
		self.updateList = []
		line = fileIn.readline()
		while line:
			line = line.strip().split(" ")
			#Allow changing of constants
			if line and line[0] in CONSTANTS:
				if line[0] == "SCREENSIZE" and len(line) >= 3 and isInt(line[1]) and isInt(line[2]):
					CONSTANTS["SCREENSIZE"] = [int(line[1]) * getConst("SQUARESIZE")[0], int(line[2]) * getConst("SQUARESIZE")[1]]
				elif line[0] not in ["SURFACE", "SQUARESIZE"]:
					if type(getConst(line[0])) is type([]):
						i = 1
						while i < len(line) and i - 1 < len(CONSTANTS[line[0]]):
							constType = type(CONSTANTS[line[0]][i - 1])
							if constType == type(1) and isInt(line[i]):
								CONSTANTS[line[0]][i - 1] = int(line[i])
							elif constType == type("1"):
								CONSTANTS[line[0]][i - 1] = line[i]
							i += 1
					elif type(getConst(line[0])) is type(1) and len(line) >= 2 and isInt(line[1]):
						CONSTANTS[line[0]] = int(line[1])
				if line[0] == "SCREENSIZE":
					numRows = (getConst("SCREENSIZE")[1] / getConst("SQUARESIZE")[1])
					numCols = (getConst("SCREENSIZE")[0] / getConst("SQUARESIZE")[0])
			#If they're not trying to change a constant, load a line.
			else:
				newRow = []
				for i in line:
					if len(newRow) < numCols and isInt(i):
						if len(i) >= 2 and i[0] != "0":
							newSquare = Square(i, [len(newRow)    * getConst("SQUARESIZE")[0],
																		 len(self.grid) * getConst("SQUARESIZE")[1]], self)
							newRow += [newSquare]
							if newSquare.requiresUpdates():
								self.updateList += [newSquare]
							if newSquare.canBeDestroyed():
								self.numSquares += 1
						else:
							newRow += [EmptySquare()]
				for i in range(numCols - len(newRow)): #Blank out the right side of the row
					newRow += [EmptySquare()]
				self.grid += [newRow]
			line = fileIn.readline()
		#Blank out whatever isn't included
		for i in range(numRows - len(self.grid)):
			self.grid += [[]]
			for j in range(numCols):
				self.grid[len(self.grid) - 1] += [EmptySquare()]
				
		CONSTANTS["SURFACE"] = pygame.display.set_mode(getConst("SCREENSIZE"), pygame.FULLSCREEN * (getConst("FULLSCREEN") != 0))
				
	def blankOutGrid(self):
		for i in range((getConst("SCREENSIZE")[1] / getConst("SQUARESIZE")[1])):
			self.grid += [[]]
			for j in range((getConst("SCREENSIZE")[0] / getConst("SQUARESIZE")[0])):
				self.grid[i] += [EmptySquare()]
			
	def getType(self, coord):
		if 0 <= coord[1] < len(self.grid):
			if 0 <= coord[0] < len(self.grid[coord[1]]):
				return self.grid[coord[1]][coord[0]].getType()
		return 1
		
	def getAt(self, coord):
		if 0 <= coord[1] < len(self.grid):
			if 0 <= coord[0] < len(self.grid[coord[1]]):
				return self.grid[coord[1]][coord[0]]
		return None
		
	def addHealth(self, coord):
		if 0 <= coord[1] < len(self.grid):
			if 0 <= coord[0] < len(self.grid[coord[1]]):
				self.grid[coord[1]][coord[0]].addHealth(1)
				
	def markSquareDeath(self, square):
		if square.canBeDestroyed():
			if getConst("MODE") == "VS":
				self.numSquares[square.getTeam() - 1] -= 1
				self.numSquares[(square.getTeam() - 1) % 2] += 1
			else:
				self.numSquares -= 1
				
	def update(self, players, ballStruct, effects):
		if getConst("MODE") != "VS" and self.numSquares <= 0:
			players.beatLevel(self.levelOn)
			self.levelOn += 1
			self.loadFromFile("Level" + str(self.levelOn))
			ballStruct.beatLevel()
		for block in self.updateList:
			block.update(self, players, ballStruct, effects)
				
	def drawMe(self):
		#Draws the image/damage permutations
		#for y in [0, 1, 2]:
			#for x in [0, 1, 2, 3, 4]:
				#drawBlockPic("1", [x * 50, y * 20], y, x)
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				self.grid[y][x].drawMe([x, y])
					
class Square:
	def __init__(self, type, pos, grid, team = 3):
		self.blockType = type[0]
		self.blockStrength = int(type[1:])
		self.health = getGridStat("Health", self.blockType, self.blockStrength)
		if self.blockType == "2":
			self.fireRate = getGridStat("FireRate", self.blockType, self.blockStrength)
			self.fireChance = getGridStat("FireChance", self.blockType, self.blockStrength)
		elif self.blockType == "4":
			self.regenRate = getGridStat("RegenRate", self.blockType, self.blockStrength)
			self.regenChance = getGridStat("RegenChance", self.blockType, self.blockStrength)
			self.regenAmt = getGridStat("RegenAmount", self.blockType, self.blockStrength)
		elif self.blockType == "5":
			self.healRate = getGridStat("HealRate", self.blockType, self.blockStrength)
			self.healAmt = getGridStat("HealAmount", self.blockType, self.blockStrength)
			self.healChance = getGridStat("HealChance", self.blockType, self.blockStrength)
		
		self.maxHealth = self.health
		self.timer = 0
		self.pos = pos
		self.ptrToGrid = grid
		self.team = team
		
	def getPointValue(self):
		return getGridStat("Points", self.blockType, self.blockStrength)
		
	def getTeam(self):
		return self.team

	def getType(self):
		if self.health <= 0:
			return 0
		return self.blockType
		
	def getPos(self):
		return [int(self.pos[0] + getConst("SQUARESIZE")[0] / 2), int(self.pos[1] + getConst("SQUARESIZE")[1] / 2)]
		
	def getHealth(self):
		return [self.health, self.maxHealth]
		
	def getStrength(self):
		return self.blockStrength
		
	def requiresUpdates(self):
		return getGridStat("NeedsUpdates", self.blockType, int(self.blockStrength))
	
	def canBeDestroyed(self):
		return getGridStat("Destructable", self.blockType, int(self.blockStrength))
		
	def addHealth(self, amt):
		self.health = min(self.maxHealth, self.health + amt)
		
	def damage(self, ball, amt, ballStruct):
		prevHealth = self.health
		armour = getGridStat("Armour", self.blockType, self.blockStrength)
		amt = calcDamage(amt, armour)
		if self.getType() == "6" and ball:
			#ball.delete()
			target = ball.controller
			if not target:
				target = random.choice(playerList).getPos()
			else:
				target = target.getPos()
			pos = [self.pos[0] + getConst("SQUARESIZE")[0] / 2, self.pos[1] + getConst("SQUARESIZE")[1] / 2]
			health = getGridStat("ShotBounces", self.blockType, self.blockStrength)
			dmg = getGridStat("Damage", self.blockType, self.blockStrength)
				
			numShots = getGridStat("NumShots", self.blockType, self.blockStrength)
			angStart = math.atan2(target[1] - pos[1], target[0] - pos[0])
			angDiff = math.pi / (8.0 + numShots / 1.0)
			if numShots > 1:
				angStart -= numShots / 2 * angDiff
			#angStart -= angDiff / 2.0 * (numShots % 2)
			for i in range(numShots):
				ang = angStart + angDiff * i
				ballStruct.addBall(Balls.EnemyShot(pos, self.team, dmg, 3, health, ang, 3))
		elif self.getType() == "7" and self.health <= amt:
			numShots = getGridStat("NumFragments", self.blockType, self.blockStrength)
			for i in range(numShots):
				pos = [self.pos[0] + getConst("SQUARESIZE")[0] / 2, self.pos[1] + getConst("SQUARESIZE")[1] / 2]
				dmg = 1; health = getGridStat("FragmentBounces", self.blockType, self.blockStrength)
				ang = math.pi * 2 / float(numShots) * i
				ballStruct.addBall(Balls.EnemyShot(pos, self.team, dmg, 3, health, ang, 3))
		self.health = max(0, self.health - amt)
		if self.health <= 0 and prevHealth > 0:
			if getConst("MODE") == "VS":
				self.team = self.team % 2 + 1
				self.health = self.maxHealth
			else:
				self.ptrToGrid.markSquareDeath(self)
			
	def update(self, grid, players, ballStruct, effects):
		if self.getType() == "2":
			self.timer += (self.timer < self.fireRate)
			c = random.uniform(0, 1)
			if self.timer >= self.fireRate and random.uniform(0, 1) <= self.fireChance:
				playerList = []
				for p in players.getPlayers():
					if p.getTeam() != self.team:
						playerList += [p]
				if playerList:
					target = random.choice(playerList).getPos()
					pos = [self.pos[0] + getConst("SQUARESIZE")[0] / 2, self.pos[1] + getConst("SQUARESIZE")[1] / 2]
					health = getGridStat("ShotBounces", self.blockType, self.blockStrength)
					dmg = getGridStat("Damage", self.blockType, self.blockStrength)
						
					numShots = getGridStat("NumShots", self.blockType, self.blockStrength)
					angStart = math.atan2(target[1] - pos[1], target[0] - pos[0])
					angDiff = math.pi / (8.0 + numShots / 1.0)
					if numShots > 1:
						angStart -= numShots / 2 * angDiff
					#angStart -= angDiff / 2.0 * (numShots % 2)
					for i in range(numShots):
						ang = angStart + angDiff * i
						ballStruct.addBall(Balls.EnemyShot(pos, self.team, dmg, 3, health, ang, 3))
				self.timer = 0
		elif self.getType() == "4":
			self.timer += (self.timer < self.regenRate)
			c = random.uniform(0, 1)
			if self.timer >= self.regenRate and random.uniform(0, 1) <= self.regenChance:
				self.health = min(self.health + self.regenAmt, self.maxHealth)
				self.timer = 0
		elif self.getType() == "5":
			self.timer += (self.timer < self.healRate)
			c = random.uniform(0, 1)
			if self.timer >= self.healRate and random.uniform(0, 1) <= self.healChance:
				coord = posToCoord(self.getPos())
				for x in [-1, 0, 1]:
					for y in [-1, 0, 1]:
						if x != 0 or y != 0:
							square = grid.getAt([coord[0] + x, coord[1] + y])
							if square and square.getType():
								square.addHealth(self.healAmt)
						
	def drawMe(self, pos):	
		pos = [pos[0] * getConst("SQUARESIZE")[0], pos[1] * getConst("SQUARESIZE")[1]]
		if getConst("MODE") != "VS":
			if self.health > 0:
				damageFrame = 4 - int(((self.health / float(self.maxHealth)) * 4))
				drawBlockPic(self.blockType, pos, self.blockStrength, damageFrame)
			else:
				clr = [15, 15, 15]
				pygame.draw.rect(getConst("SURFACE"), clr, [
										pos, 
										[getConst("SQUARESIZE")[0], getConst("SQUARESIZE")[1]]], 2)
		else:
			if self.team in [1, 2]:
				damageFrame = 4 - int(((self.health / float(self.maxHealth)) * 4))
				drawBlockPic("Team" + str(self.team) + self.blockType, pos, self.blockStrength, damageFrame)
									
class EmptySquare(Square):
	def __init__(self):
		self.health = 0
		self.maxHealth = 0
		
	def getType(self):
		return 0
		
	def addHealth(self, amt):
		pass
		
	def damage(self, amt):
		pass

	def drawMe(self, pos):	
		pass
		
		
#Tabitha's Ideas for blocks
#Blocks that explode when they die
#Blocks that don't shoot until you have cleared the square in front of them