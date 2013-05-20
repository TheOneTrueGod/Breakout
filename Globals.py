import pygame, os
pygame.font.init()
VERSION = 1
CONSTANTS = {"PROFILES":["Player1", "Player2"], "SCREENSIZE":[500, 400], "FULLSCREEN":1, "SURFACE":None, "SQUARESIZE":[50, 20],
						 "PLAYERMINYPOS":300, "INCREASINGMINY":True, "BALLSPEED":10, "PLAYERSPEED":8, "MODE":"VS", 
						 "BASEABILCOST":20, "STEPABILCOST":20}
FONTS = {"MENUFONT":pygame.font.Font(os.path.join("Data", "Fonts", "MenuFont.ttf"), 14),
				 "SMALLFONT":pygame.font.Font(os.path.join("Data", "Fonts", "MenuFont.ttf"), 8),
				 "MEDIUMFONT":pygame.font.Font(os.path.join("Data", "Fonts", "MenuFont.ttf"), 10),
				 "LARGEFONT":pygame.font.Font(os.path.join("Data", "Fonts", "MenuFont.ttf"), 12)}
						 
def getConst(constant):
	if constant in CONSTANTS:
		return CONSTANTS[constant]
	print "Error:  Constant doesn't exist:'" + constant + "'"
	return 0
	
CONSTANTS["SURFACE"] = pygame.display.set_mode(getConst("SCREENSIZE"), getConst("FULLSCREEN"))

def isInt(i):
	try:
		int(i)
		return True
	except:
		return False

def posToCoord(pos):
	return [int(pos[0]) / getConst("SQUARESIZE")[0], int(pos[1]) / getConst("SQUARESIZE")[1]]
	
def coordToPos(coord):
	return [int((coord[0] + .5) * getConst("SQUARESIZE")[0]), 
					int((coord[1] + .5) * getConst("SQUARESIZE")[1])]
					
def getSign(i):
	if i >= 0:
		return 1
	return -1
	
def dist(p1, p2):
	return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def drawTextBox(surface, pos, size, text, drawBorder, bckClr = [0, 0, 0], txtClr = [255, 255, 255], font="MENUFONT"):
	textSpacing = 5
	if drawBorder:
		if bckClr:
			pygame.draw.rect(surface, bckClr, (pos,size))
		pygame.draw.rect(surface, txtClr, (pos[0], pos[1],size[0], size[1]),2)
	currPos = [pos[0] + 6,pos[1] + 6]
	for lines in text.split("\n"):
		currText = lines.split(" ")
		for i in currText:
			if currPos[1] < pos[1] + size[1]:
				if i.find('\n') != -1:
					toDraw = FONTS[font].render(i[:i.find('\n')], False, txtClr)
				else:
					toDraw = FONTS[font].render(i, False, txtClr)
				if currPos[0] + toDraw.get_width() - pos[0] + textSpacing > size[0]:
					currPos[0] = pos[0] + 6
					currPos[1] = currPos[1] + 12
				surface.blit(toDraw,(currPos))
				currPos[0] += toDraw.get_width() + textSpacing
		currPos[0] = pos[0] + 6
		currPos[1] = currPos[1] + 12
		
def buttonHit(mousePos, butPos):
	if butPos[0][0] <= mousePos[0] <= butPos[1][0] and butPos[0][1] <= mousePos[1] <= butPos[1][1]:
		return True
	return False
	
def calcDamage(amount, armour, minDmg = 1):
	if armour <= 0:
		return amount
	newAmount = max(amount - armour, minDmg)
	newArmour = max(armour - (amount - minDmg), 0) * 0.1
	return calcDamage(newAmount, newArmour, minDmg * 0.1)
	
#Printing armour table.
"""
print "ARMOUR"
toPrint = ""
for armour in range(20):
	toPrint += str(armour / 2.0) + ","
print toPrint
toPrint = ""
for amount in range(20):
	toPrint = str(amount / 2.0) + ","
	for armour in range(20):
		toPrint += str(calcDamage(amount / 2.0, armour / 2.0)) + ","
	print toPrint
	"""