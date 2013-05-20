import pygame, Balls, Grid, Players, Effects, sys, Profiles, math
from Globals import *
from pygame.locals import *
pygame.init()
buttons = {"Next":pygame.image.load(os.path.join("Data", "Pics", "Buttons", "Next.bmp")),
					 "TitleBar":pygame.image.load(os.path.join("Data", "Pics", "Buttons", "TitleBar.png"))}
def playGame(startLevel, profiles):
	if startLevel == "VS":
		CONSTANTS["MODE"] = "VS"
	else:
		CONSTANTS["MODE"] = "MAIN"
	grid = Grid.Grid(startLevel)
	players = Players.Players(profiles)
	ballStruct = Balls.BallStruct()
	effects = Effects.EffectStruct()
	_done = False
	
	while not _done:
		for ev in pygame.event.get():
			if ev.type == QUIT:
				players.forceQuit()
				return "QUIT"
			elif ev.type == KEYDOWN and ev.key == K_ESCAPE:
				players.forceQuit()
				return 
			else:
				players.handleEvent(ev, grid, ballStruct)
		
		if grid.isDone():
			return 
		
		effects.update()
		grid.update(players, ballStruct, effects)
		ballStruct.update(grid, players, effects)
		players.update(grid, ballStruct)
		
		grid.drawMe()
		players.drawMe()
		effects.drawMe()
		ballStruct.drawMe()
		#pygame.draw.rect(getConst("SURFACE"), [255, 255, 255], [0, 0, getConst("SCREENSIZE")[0] - 1, getConst("SCREENSIZE")[1] - 1], 1)
		
		pygame.display.update()
		getConst("SURFACE").fill([0] * 3)
		pygame.time.Clock().tick(40)

def drawProfileMenu(profile):
	CONSTANTS["SURFACE"] = pygame.display.set_mode((400, 400))
	buttonPositions = []
	getConst("SURFACE").fill([0] * 3)
	
	levs = profile.getClassLevels()
	centre = [200, 215]
	#Name
	drawTextBox(getConst("SURFACE"), [125, 5], [150, 25], profile.getName(), True)
	#Current Class
	drawTextBox(getConst("SURFACE"), [125, 32], [120, 25], profile.getClass(), True)
	getConst("SURFACE").blit(buttons["Next"], [250, 32])
	drawTextBox(getConst("SURFACE"), [250, 32], [25, 25], "", True, bckClr = None)
	
	#Stats
	drawTextBox(getConst("SURFACE"), [125, 60], [60, 25], "Deaths", True)
	drawTextBox(getConst("SURFACE"), [190, 60], [60, 25], str(profile.getStat("Deaths")), False)
	
	drawTextBox(getConst("SURFACE"), [125, 87], [60, 25], "Points", True)
	drawTextBox(getConst("SURFACE"), [190, 87], [60, 25], str(profile.getPoints()), False)
	
	spread = math.pi * 2 / 13.0
	numSize = [24, 24]
	for i in range(len(levs)):
		ang = spread * i + spread * (i > 2) + spread * (i > 5) + math.pi / 26.0 + math.pi
		pos = [int(centre[0] + math.cos(ang) * 120 - numSize[0] / 2), 
					 int(centre[1] + math.sin(ang) * 90 - numSize[1] / 2)]
		drawTextBox(getConst("SURFACE"), [pos[0], pos[1]], numSize, str(levs[i]), True, font="LARGEFONT")
		toDraw = FONTS["MEDIUMFONT"].render(profile.getUpgradeName(i), False, [200] * 3)
		buttonPositions += [[[pos[0], pos[1]], [pos[0] + numSize[0], pos[1] + numSize[1]]]]
		pos[1] += numSize[1] + 2
		pos[0] -= (toDraw.get_width() / 2 - numSize[0] / 2)
		#print pos
		getConst("SURFACE").blit(toDraw, pos)
	pygame.display.update()
	return buttonPositions
	
def profileMenu(profile):
	_done = False
	buttonPositions = drawProfileMenu(profile)
	while not _done:
		for ev in pygame.event.get():
			if ev.type == QUIT:
				return "QUIT"
			elif ev.type == KEYDOWN and ev.key == K_ESCAPE:
				_done = True
			elif ev.type in [MOUSEMOTION, MOUSEBUTTONDOWN]:
				for i in range(len(buttonPositions)):
					if buttonHit(ev.pos, buttonPositions[i]):
						if ev.type == MOUSEBUTTONDOWN:
							profile.tryToUpgradeAbil(i)
							drawProfileMenu(profile)
						drawTextBox(getConst("SURFACE"), [10, 330], [380, 65], profile.getDescription(i), True, font = "LARGEFONT")
						pygame.display.update()
				if buttonHit(ev.pos, [[250, 32], [275, 57]]):
					if ev.type == MOUSEBUTTONDOWN:
						profile.selectNextClass()
						buttonPositions = drawProfileMenu(profile)
					drawTextBox(getConst("SURFACE"), [10, 330], [380, 65], "Next Profile", True, font = "LARGEFONT")
					pygame.display.update()
	
def drawMainMenu(profiles, menuPos):
	getConst("SURFACE").fill([0] * 3)
	CONSTANTS["SURFACE"] = pygame.display.set_mode((400, 300))
	#TitleBar
	getConst("SURFACE").blit(buttons["TitleBar"], [200 - 154 / 2, 2])
	#Play Button
	drawTextBox(getConst("SURFACE"), [menuPos[0] + 160, menuPos[1] + 20], [80, 30], "Play Game", True)
	#Levels
	#Get number of levels
	files = len(os.listdir(os.path.join("Data", "Levels")))
	for i in range(files):
		x = menuPos[0] + 23 + 36 * (i % 10)
		y = menuPos[1] + 100 + 36 * (i / 10)
		drawTextBox(getConst("SURFACE"), [x, y], [30, 30], str(i + 1), True)
		if profiles[0].hasBeatenLevel(i + 1):
			pygame.draw.rect(getConst("SURFACE"), [255, 0, 255], [x + 2, y + 2, 5, 27])
		if profiles[1].hasBeatenLevel(i + 1):
			pygame.draw.rect(getConst("SURFACE"), [0, 255, 0], [x + 30 - 6, y + 2, 5, 27])
	#Profiles
	for i in [0, 1]:
		drawTextBox(getConst("SURFACE"), [menuPos[0] + 50 + (400 - 150 - 75) * i, menuPos[1] + 60], [125, 30], profiles[i].getName(), True)
	drawTextBox(getConst("SURFACE"), [menuPos[0] + 180, menuPos[1] + 60], [40, 30], "VS Mode", True, font = "MEDIUMFONT")
	pygame.display.update()
	
def mainMenu():
	menuPos = [0, 30]
	level = 1
	profiles = [Profiles.Profile(getConst("PROFILES")[0], 1), Profiles.Profile(getConst("PROFILES")[1], 2)]
	_done = False
	drawMainMenu(profiles, menuPos)
	while not _done:
		for ev in pygame.event.get():
			if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
				_done = True
			elif ev.type == MOUSEBUTTONDOWN:
				for i in [0, 1]:
					if buttonHit(ev.pos, ([menuPos[0] + 50 + 175 * i, menuPos[1] + 60], [menuPos[0] + 175 + 175 * i, menuPos[1] + 60 + 30])):
						result = profileMenu(profiles[i])
						if result == "QUIT":
							_done = True
						drawMainMenu(profiles, menuPos)
				if buttonHit(ev.pos, ([menuPos[0] + 160, menuPos[1] + 20], [menuPos[0] + 240, menuPos[1] + 50])):
					if playGame(1, profiles) == "QUIT":
						_done = True
					drawMainMenu(profiles, menuPos)
				elif buttonHit(ev.pos, ([menuPos[0] + 180, menuPos[1] + 60], [menuPos[0] + 220, menuPos[1] + 90])):
					if playGame("VS", profiles) == "QUIT":
						_done = True
					drawMainMenu(profiles, menuPos)
				else:
					if menuPos[0] + 23 < ev.pos[0] <= menuPos[0] + 383 and menuPos[1] + 100 <= ev.pos[1] <= menuPos[1] + 100 + 36 * 3 \
					and (ev.pos[0] - 23 - menuPos[0]) % 36 - 30 < 0 and (ev.pos[1] - 100 - menuPos[1]) % 36 - 30 < 0:
						level = (ev.pos[0] - 23 - menuPos[0]) / 36 + 1 + ((ev.pos[1] - 100 - menuPos[1]) / 36) * 10
						if playGame(level, profiles) == "QUIT":
							_done = True
						drawMainMenu(profiles, menuPos)

play = True
if len(sys.argv) >= 2 and isInt(sys.argv[1]):
	level = int(sys.argv[1])
	if playGame(level, [Profiles.Profile("Player1", 1), Profiles.Profile("Player2", 2)]) == "QUIT":
		play = False
	
if play:
	mainMenu()

#(surface, pos, size, text, drawBorder, bckClr = [0, 0, 0], txtClr = [255, 255, 255])