import math
import copy
import time

########################################################################################################
# Pravljenje Sudoku-a

DIFFICULTY = 0.9 # Tezina sudoku-a, default je 0.5
DRAWBOOL = 1 # 1 prikazuje sudoku, 0 ne
DRAWSPEED = 0.02 # Koliko sekundi treba da ceka za ispis svakog elementa
STARTINGELEMENTCOLOUR = 250, 132, 100
INSERTEDELEMENTCOLOUR = 130, 215, 255

# pip install pygame
import sudokuConstructor # Fajl je iz pip3 install py-sudoku ili install sudoku_py, nismo sigurni, jedina promena je _empty_cell_value = 0 (bilo je None)
def getSudoku():
	startingElements = []
	puzzle = sudokuConstructor.Sudoku(3).difficulty(DIFFICULTY) # Tezina je 0-1
	for i in range (9):
		for j in range (9):
			if puzzle.board[i][j] != 0:
				startingElements.append((i, j))
	return puzzle.board, startingElements

flag = 1
dict = {} # Position <-> List of elements available to set (numbersList)
positionStack = [] # Lista uredjenih parova ((x,y), nacinNaKojiSeUbacio), ako naidje na tried i ne moze, ici ce unazad, postavljace nule na sve ideal-e dok ne naidje na prethodni tried
GTPARtestPuzzle = []

puzzle, startingElements = getSudoku()
# Special Sudoku - Working against the algorithm
# puzzle = [
# 	[0,0,0, 0,0,0, 0,0,0],
# 	[0,0,0, 0,0,3, 0,8,5],
# 	[0,0,1, 0,2,0, 0,0,0],

# 	[0,0,0, 5,0,7, 0,0,0],
# 	[0,0,4, 0,0,0, 1,0,0],
# 	[0,9,0, 0,0,0, 0,0,0],

# 	[5,0,0, 0,0,0, 0,7,3],
# 	[0,0,2, 0,1,0, 0,0,0],
# 	[0,0,0, 0,4,0, 0,0,9]
# ]
# startingElements = [(1,5),(1,7),(1,8),(2,2),(2,4),(3,3),(3,5),(4,2),(4,6),(5,1),(6,0),(6,7),(6,8),(7,2),(7,4),(8,4),(8,8)]
########################################################################################################
# PyGame Engine

import pygame
if DRAWBOOL == 1:
	screen = pygame.display.set_mode((500, 500))
	pygame.display.set_icon(pygame.image.load('icon.png'))
	pygame.display.set_caption("Sudoku Backtrack Solver")
	pygame.font.init()
	font1 = pygame.font.SysFont("consolas", 40)
	font2 = pygame.font.SysFont("consolas", 20)
	screen.fill((228, 228, 250))

dif = 500 / 9  
# Function to draw required lines for making Sudoku grid         
def draw():
	global puzzle
	# Draw the lines
	for i in range (9):
		for j in range (9):
			if puzzle[j][i] != 0:
				# Fill blue color in already numbered grid
				pygame.draw.rect(screen, (INSERTEDELEMENTCOLOUR), (i * dif, j * dif, dif + 1, dif + 1))
				# Fill grid with default numbers specified
				text1 = font1.render(str(puzzle[j][i]), 1, (0, 0, 0))
				screen.blit(text1, (i * dif + 15, j * dif + 15))
	for element in startingElements:
		j = element[0]
		i = element[1]
		pygame.draw.rect(screen, (STARTINGELEMENTCOLOUR), (i * dif, j * dif, dif + 1, dif + 1))
		text1 = font1.render(str(puzzle[j][i]), 1, (0, 0, 0))
		screen.blit(text1, (i * dif + 15, j * dif + 15))
	# Draw lines horizontally and vertically
	for i in range(10):
		if i % 3 == 0 :
			thick = 7
		else:
			thick = 1
		pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
		pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)
  
# Fill value entered in cell      
def draw_val(val, x, y):
	x, y = 0, 0
	text1 = font1.render(str(val), 1, (0, 0, 0))
	screen.blit(text1, (x * dif + 15, y * dif + 15)) 

if DRAWBOOL == 1:
	draw()
	pygame.display.update() 
	time.sleep(2)

########################################################################################################

# Program radi za 9x9 sudoku, ako hocemo 6x6 ili 12x12 moramo check-u da prosledimo i dimenziju da zna kako da radi

def checkAtPos(puzzle, r, c):
		selected = puzzle[r][c] # r i c su indeksi selektovanog elementa
		if(selected != 0):
			# Provera po koloni, inkrementuje se row
			for i in range(9):
				if(i == r):
					continue
				if(selected == puzzle[i][c]): # i != r znaci da preskace indeks selektovanog
					return False
			# Provera po redu, inkrementuje se col
			for i in range(9):
				if(i == c):
					continue
				if(selected == puzzle[r][i]):
					return False
			# Provera po 3x3, r33 i c33 su pocetni elementi u 3x3 selektovanog elementa
			r33 = math.floor(r / 3)
			c33 = math.floor(c / 3)
			r33coordinates = [r33 * 3, r33 * 3 + 1, r33 * 3 + 2]
			c33coordinates = [c33 * 3, c33 * 3 + 1, c33 * 3 + 2]
			for i in range(3): # od 0 do 2
				for j in range(3):
					# Preskace selektovani
					if(r == r33coordinates[i] and c == c33coordinates[j]): # and mora, ne &
						continue
					# Ako nadje broj u sekciji koji je isti kao selektovani
					if(puzzle[r33coordinates[i]][c33coordinates[j]] == selected): 
						return False
			return True

# Ovo govori samo da li je sve u sudoku-u u redu, ne da li moze da se resi (za sve nule ce reci da je ok)
# Reci ce da ako ima dva ista u koloni ili redu ili 3x3 da nije dobro
def check(puzzle):
	# Za svaki element gleda svoj red, kolonu i 3x3
	for r in range(9): # Od 0 do 8
		for c in range(9):
			if checkAtPos(puzzle, r, c) == False:
				return False
	return True

def trivialFill(puzzle):
	# Svaka globalna promenljiva koja se koristi mora da ima global imePromenljive na pocetku funkcije
	global flag
	flag = 0 # Promena globalne promenljive
	zeroPosition = [0,0]
	# Provera za redove
	for i in range(9):
		zeroCounter = 0
		numbersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		for j in range(9):
			if puzzle[i][j] == 0:
				zeroCounter += 1
				# Cim nadje nulu pamti indekse tog elementa za upis novog, iako ce se ovi indeksi mozda overwrite-ovati ako ima 2 ili vise nula
				zeroPosition[0] = i
				zeroPosition[1] = j
			else:
				numbersList.remove(puzzle[i][j])
		# Ako u redu ima samo jedna nula, upisuje se nedostajuci broj u to polje
		if zeroCounter != 1:
			continue
		else:
			trivialFillElement(zeroPosition[0], zeroPosition[1], numbersList[0])
	
	# Provera za kolone
	for j in range(9):
		zeroCounter = 0
		numbersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		for i in range(9):
			if puzzle[i][j] == 0:
				zeroCounter += 1
				zeroPosition[0] = i
				zeroPosition[1] = j
			else:
				numbersList.remove(puzzle[i][j])
		if zeroCounter != 1:
			continue
		else:
			trivialFillElement(zeroPosition[0], zeroPosition[1], numbersList[0])

	# Provera za 3x3
	for sectionNum in range(9):
		zeroCounter = 0
		numbersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		for elemNum in range(9):
			# print("Section: " + str(sectionNum) + " Elem: " + str(elemNum))
			xOffset = math.floor(elemNum / 3)
			yOffset = elemNum % 3
			x = xOffset + 3 * (math.floor(sectionNum / 3))
			y = yOffset + 3 * (sectionNum % 3)
			if puzzle[x][y] == 0:
				zeroCounter += 1
				zeroPosition[0] = x
				zeroPosition[1] = y
			else:
				numbersList.remove(puzzle[x][y])
		if zeroCounter != 1:
			continue
		else:
			trivialFillElement(zeroPosition[0], zeroPosition[1], numbersList[0])

def trivialFillElement(x, y, element):
	global flag
	flag = 1
	puzzle[x][y] = element
	if (checkAtPos(puzzle, x, y) == False):
		puzzle[x][y] = 0
		goToPreviousAndReplace(x, y)
	else:
		positionStack.append((x, y))
		dict[(x, y)] = []

def findZero(puzzle):
	for i in range(9): # Treba da prodje kroz redove da bi nasao nule
		for j in range(9): # Treba da prodje kroz sve elemente reda
			if puzzle[i][j] == 0:
				return (i,j)
	return None

def fillFirstZero(puzzle):
	returnElements = findZero(puzzle)
	if(returnElements == None):
		return None
	x, y = returnElements[0], returnElements[1] # Koordinate nule po kojoj se radi backtracking
	dict[(x,y)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

	# Provera po redu
	for i in range(9):
		if puzzle[x][i] != 0 and puzzle[x][i] in dict[(x,y)]:
			dict[(x,y)].remove(puzzle[x][i])
	# print("Remaining elements on (" + str(x) + "," + str(y) + ") by fillFirstZero Row are : " + str(dict[(x,y)]))
	# Nikad nece biti len(numbersList) == 1 zbog trivialFill()

	# Provera po koloni
	for j in range(9):
		if puzzle[j][y] != 0 and puzzle[j][y] in dict[(x,y)]:
			dict[(x,y)].remove(puzzle[j][y])
	# print("Remaining elements on (" + str(x) + "," + str(y) + ") po fillFirstZero Col are : " + str(dict[(x,y)]))
	# Iako ima 1 preostao element, on ne moze da se doda a da se ne proveri 3x3

	# Provera po 3x3
	sectionX = math.floor(x / 3) # elemX = sectionX * 3
	sectionY = math.floor(y / 3) # elemY = sectionY * 3 # print("ElemX: " + str(elemX) + "  ElemY: " + str(elemY))
	dim = 3 # Za sad
	sectionNum = sectionX * dim + sectionY # Ide od nule # (2,1), 3x3, => 3+3+2 = x*dim + y
	for elemNum in range(9):
		# print("Section: " + str(sectionNum) + " Elem: " + str(elemNum))
		xOffset = math.floor(elemNum / 3)
		yOffset = elemNum % 3
		xNew = xOffset + 3 * (math.floor(sectionNum / 3))
		yNew = yOffset + 3 * (sectionNum % 3)
		if puzzle[xNew][yNew] != 0 and puzzle[xNew][yNew] in dict[(x,y)]:
			dict[(x,y)].remove(puzzle[xNew][yNew])
	# print("Remaining elements on (" + str(x) + "," + str(y) + ") by fillFirstZero 3x3 are : " + str(dict[(x,y)]))
	for elemNum in range(9):
		# print("Section: " + str(sectionNum) + " Elem: " + str(elemNum))
		xOffset = math.floor(elemNum / 3)
		yOffset = elemNum % 3
		xNew = xOffset + 3 * (math.floor(sectionNum / 3))
		yNew = yOffset + 3 * (sectionNum % 3)
		# Nebitno je koliko imamo elemenata u listi, pisemo prvi
		if puzzle[xNew][yNew] == 0: # x i y vise nisu isti kao pre, ovde ide element po element u 3x3, ali jesu koordinate nule
			# Nije htelo dobro ni testPuzzle = puzzle (default je po referenci), ni = puzzle.copy(), ni = puzzle[:]
			# Mora da se importuje "copy", pa da se koristi ova funkcija
			testPuzzle = copy.deepcopy(puzzle)
			if len(dict[(x,y)]) == 0:
				# Ovo je slucaj gde moramo da backtrack-ujemo, jer to znaci da vec postoji isti broj u redu / koloni / 3x3
				return ("emptyDict", x, y)
			testPuzzle[xNew][yNew] = dict[(x,y)][0]
			if checkAtPos(testPuzzle, xNew, yNew): # Optimizacija, ne gleda ceo check(testPuzzle)
				puzzle[xNew][yNew] = dict[(x,y)][0]
				positionStack.append((x,y)) # Stavlja na kraj
				# print("Inserted " + str(dict[(x,y)][0]) + " into the puzzle on (" + str(x) + "," + str(y) + ") by fillFirstZero 3x3.")
				dict[(x,y)].pop(0)
				return ("tried", x, y)
			else:
				print("Failed, printing...")
				puzzle[xNew][yNew] = 0 
				# print("Inserted 0 into the puzzle on (" + str(xNew) + "," + str(yNew) + ") by fillFirstZero Failed.")
				for i in dict:
					print(dict[i])
				return ("failedCheck", x, y)

def goToPreviousAndReplace(oldX, oldY):
	global GTPARtestPuzzle # Globalni puzzle koji se koristi kod rekurzije
	(x,y) = positionStack.pop() # Uzima sa kraja
	GTPARtestPuzzle = copy.deepcopy(puzzle) # testPuzzle je lokalan za svaki poziv funkcije, sto nije dobro kod rekurzije
	if len(dict[(x,y)]) == 0:
		puzzle[x][y] = 0
		GTPARtestPuzzle[x][y] = 0 
		goToPreviousAndReplace(x, y)
	else:
		GTPARtestPuzzle[x][y] = dict[(x,y)][0]
	if check(GTPARtestPuzzle) == True: # Bitno je da gleda globalne, ne moze checkAtPos(gtpartp, x, y)
		if len(dict[(x,y)]) == 0:
			return
		puzzle[x][y] = dict[(x,y)][0]
		GTPARtestPuzzle[x][y] = dict[(x,y)][0] # Zbog rekurzije, mozda nebitan
		positionStack.append((x,y))
		# print("Inserted " + str(dict[(x,y)][0]) + " into the puzzle on (" + str(x) + "," + str(y) + ") by backtracking.")
		dict[(x,y)].pop(0)
	else:
		puzzle[oldX][oldY] = 0
		GTPARtestPuzzle[x][y] = 0 # Zbog rekurzije
		# print("Resetted 0 into the puzzle on (" + str(oldX) + "," + str(oldY) + ") for recursive backtracking.")
		# Rekurzija
		goToPreviousAndReplace(x, y)

def solve(puzzle):
	global flag
	# Prvo je provera da li je uneseni sudoku ispravan
	if(check(puzzle) == False):
		print("The input puzzle is incorrect.")
	else:
		print("The input puzzle is correct.")
		print("Starting sudoku: ")
		for i in range(9):
			print(puzzle[i])
		print("Please wait...")

		# U petlji ce konstantno trivijalno ubacivati elemente i redom popunjavati prazna polja novim pokusajima
		# Svaki element koji se ubaci, na bilo koji nacin, ce se beleziti na steku ubacenih elemenata
		# Ukoliko dodje do problema rekurzivno se vraca backtracking-om kroz sudoku, odnosno stek, do sledeceg moguceg pokusaja
		while True:
			if DRAWBOOL == 1:
				draw()
				pygame.display.update() 
				time.sleep(DRAWSPEED)
			flag = 1
			while flag == 1:
				trivialFill(puzzle) # Treba nam rad sa stekom i sa ovim brojevima koji se dodaju, da se i oni vracaju uz backtrack
			returnElements = fillFirstZero(puzzle)
			if returnElements == None:
				print("No more zeroes in the working sudoku!")
				return
			status = returnElements[0]
			if status == "emptyDict" or status == "failedCheck":
				x = returnElements[1]
				y = returnElements[2]
				goToPreviousAndReplace(x, y)

startTime = time.time()
solve(puzzle)
print("FINAL:")
for i in range(9):
	print(puzzle[i])
print(f"Time elapsed: {time.time() - startTime}")

if DRAWBOOL == 1:
	print("Time elapsed was calculated with drawing.")
	draw()
	pygame.display.update() 
	time.sleep(5)