import Players, os, Abilities
from Globals import *
class Profile:
	def __init__(self, file, controls, skipLoad = False):
		self.file = file
		self.controls = controls
		self.stats = {"Deaths":0, "Class":"Blaster"}
		self.classLevels = {"Brute":[0] * 10, "Blaster":[0] * 10}#, "Enchanter":[0] * 10}
		self.classChangedTimer = 0
		self.levelsBeaten = {}
		if not skipLoad:
			self.load()
			
	def getPoints(self):
		return len(self.levelsBeaten) - sum(self.classLevels[self.stats["Class"]])
			
	def beatLevel(self, level):
		self.levelsBeaten[level] = True
		
	def hasBeatenLevel(self, level):
		return str(level) in self.levelsBeaten
			
	def getName(self):
		return self.file
		
	def getAbilities(self):
		toRet = []
		if self.stats["Class"] in self.classLevels and len(self.classLevels[self.stats["Class"]]) == 10:
			abils = Abilities.getAbilities(self.stats["Class"])
			levels = self.classLevels[self.stats["Class"]]
			return [abils[0](levels[0:3]), abils[1](levels[3:6]), abils[2](levels[6:10])]
		else:
			return [Abilities.ExplodeBalls([0, 0, 0]), Abilities.SplitBalls([0, 0, 0]), Abilities.CreateBall([0, 0, 0, 0])]
		
	def getPlayer(self):
		if getConst("MODE") != "VS":
			return Players.Player(1, self.controls, self.getAbilities())
		return Players.Player(self.controls, self.controls, self.getAbilities(), pos = [getConst("SCREENSIZE")[0] / 2, getConst("SCREENSIZE")[1] * (self.controls % 2)])
		
	def getClassLevels(self):
		return self.classLevels[self.stats["Class"]]
		
	def getCost(self, abilNum):
		return 1
		if 0 <= abilNum <= 9:
			return getConst("BASEABILCOST") + self.classLevels[self.getStat("Class")][abilNum] * getConst("STEPABILCOST")
		return 9999999999
	
	def convertAbilNumToArrayPos(self, num):
		abil = None
		if 0 <= num <= 9:
			abilList = self.getAbilities()
			abil = abilList[2]
			if num < 3:
				abil = abilList[0]
			elif 3 <= num < 6:
				abil = abilList[1]
				num -= 3
			else:
				num -= 6
		return abil, num
		
	def getUpgradeName(self, num):
		toRet = ""
		if 0 <= num <= 9:
			abil, num = self.convertAbilNumToArrayPos(num)
			if abil:
				toRet += abil.getUpgradeName(num)
		return toRet	
		
	def getDescription(self, abilNum):
		toRet = ""
		if 0 <= abilNum <= 9:
			abil, num = self.convertAbilNumToArrayPos(abilNum)
				
			if abil:
				toRet += abil.getDescription(num) + "\n"
			toRet += "Cost " + str(self.getCost(abilNum))
		return toRet
			
	def getClass(self):
		return self.stats["Class"]
		
	def getStat(self, stat):
		if stat in self.stats:
			return self.stats[stat]
		return 0
		
	def tryToUpgradeAbil(self, abilNum):
		if 0 <= abilNum <= 9 and self.getCost(abilNum) <= self.getPoints() and len(self.levelsBeaten) / 3 + 2 > self.classLevels[self.getStat("Class")][abilNum]:
			self.classLevels[self.getStat("Class")][abilNum] += 1
		self.save()
		
	def selectNextClass(self):
		list = [k for k in self.classLevels]
		if self.stats["Class"] in self.classLevels:
			listLoc = list.index(self.stats["Class"])
			listLoc = (listLoc + 1) % len(list)
			self.stats["Class"] = list[listLoc]
		else:
			self.stats["Class"] = list[0]
		self.classChangedTimer = 100
		
	def addDeath(self):
		self.stats["Deaths"] += 1
		
	def load(self):
		path = os.path.join("Data", "Profiles", self.file + ".prof")
		if os.path.exists(path):
			fileIn = open(path)
			versionNumber = fileIn.readline()
			assert(len(versionNumber) > 0)
			assert(isInt(versionNumber))
			versionNumber = int(versionNumber)
			line = fileIn.readline()
			while line:
				line = line.strip().split()
				if len(line) >= 2:
					if line[0] in self.stats and isInt(line[1]):
						self.stats[line[0]] = int(line[1])
					elif line[0] in self.classLevels:
						for i in range(1, min(len(line), 12)): #Cap the line when we have 10 upgrades.
							if isInt(line[i]):
								self.classLevels[line[0]][i - 1] = int(line[i])
					elif line[0] == "levelsBeaten":
						for lev in line[1:]:
							self.levelsBeaten[lev] = True
				line = fileIn.readline()
			
		else:
			self.__init__(self.file, self.controls, skipLoad = True)
		
	def save(self):
		fileOut = open(os.path.join("Data", "Profiles", self.file + ".prof"), 'w')
		fileOut.write(str(VERSION) + "\n")
		for stat in self.stats:
			fileOut.write(stat + " " + str(self.stats[stat]) + "\n")
		for c in self.classLevels:
			fileOut.write(c + " ")
			for lev in self.classLevels[c]:
				fileOut.write(str(lev) + " ")
			fileOut.write("\n")
		levels = []
		for k in self.levelsBeaten:
			levels += [str(k)]
		fileOut.write("levelsBeaten " + " ".join(levels))
		fileOut.write("\n")
		fileOut.close()
		
	def drawMe(self):
		if self.classChangedTimer > 0:
			pos = [10 + (self.controls - 1) * (getConst("SCREENSIZE")[0] - 120), getConst("SCREENSIZE")[1] - 30]
			clr = [int(255 * self.classChangedTimer / 100.0)] * 3
			drawTextBox(getConst("SURFACE"), pos, [100, 30], self.stats["Class"], False, txtClr = clr)
			self.classChangedTimer -= 1
			
descriptions = {"Blaster":{0:"", 
												 1:"",
												 2:"",
												 3:"",
												 4:"",
												 5:"",
												 6:"",
												 7:"",
												 8:"",
												 9:""},
								"Brute":{0:"", 
												 1:"",
												 2:"",
												 3:"",
												 4:"",
												 5:"",
												 6:"Strength: Increases ball damage.",
												 7:"Rejuvinate: Recovers more of the balls health when it hits you.",
												 8:"Endurance: Increases your health, and the staying power of your ball.",
												 9:"Critical: Chance of the ball dealing extra damage."}}