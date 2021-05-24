import math
import copy
import time

flag = 1
dict = {} # Position <-> List of elements available to set (numbersList)
positionStack = [] # Pravimo: Lista uredjenih parova ((x,y), nacinNaKojiSeUbacio), ako naidje na tried i ne moze, ici ce unazad, postavljace nule na sve ideal-e dok ne naidje na prethodni tried
GTPARtestPuzzle = []

# 0 su prazna mesta
#1
# puzzle = [
# 	[8,7,4, 1,9,2, 0,0,3],
# 	[2,3,0, 0,7,0, 8,1,9],
# 	[6,1,9, 3,0,8, 4,7,2],

# 	[0,0,2, 7,0,5, 0,8,0],
# 	[7,0,0, 0,1,0, 0,2,5],
# 	[0,5,0, 0,2,0, 7,0,0],

# 	[9,6,7, 5,0,1, 2,4,8],
# 	[0,8,0, 2,4,7, 0,9,0],
# 	[4,2,1, 9,8,0, 5,0,7]
# ]
# 2
# puzzle = [
# 	[3,8,9, 2,7,0, 6,0,4],
# 	[7,0,6, 9,1,0, 2,8,5],
# 	[0,0,0, 8,4,0, 0,3,0],

# 	[6,0,4, 3,0,2, 0,0,0],
# 	[0,1,8, 0,0,7, 0,0,2],
# 	[0,0,0, 6,0,0, 0,5,0],

# 	[0,0,0, 7,0,0, 1,0,6],
# 	[1,0,0, 0,0,8, 0,0,0],
# 	[0,6,3, 0,0,0, 5,7,0]
# ]
# 3
puzzle = [
	[0,0,0, 7,0,0, 5,0,1],
	[0,0,0, 2,3,9, 0,0,0],
	[0,0,0, 5,0,0, 8,0,0],

	[0,7,0, 0,0,3, 0,0,0],
	[5,0,0, 0,6,0, 0,0,0],
	[0,1,0, 0,0,0, 4,6,0],

	[0,0,3, 0,7,0, 0,0,2],
	[9,0,2, 0,0,0, 0,5,0],
	[0,0,0, 0,0,0, 0,0,9]
]

# Program radi za 9x9 sudoku, ako hocemo 6x6 ili 12x12 moramo check-u da prosledimo i dimenziju da zna kako da radi

# Ovo govori samo da li je sve u sudokuu uredu, ne da li moze da se resi (za sve nule ce reci da je ok)
# Reci ce da ako ima dva ista u koloni ili redu ili 3x3 da nije dobro
def check(puzzle):
	# Za svaki element gleda svoj red, kolonu i 3x3
	for r in range(9): # od 0 do 8   
		for c in range(9):
			selected = puzzle[r][c] # r i c su indeksi selektovanog elementa
			# print(selected)
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
				# Provera po 3x3
				# Treba da nadje u kom je segmentu po modulu, i po row i po col, pa da proveri sve u tom segmentu osim samog selektovanog
				# print("R = " + str(r) + "   R mod 3 = " + str(math.floor(r / 3)))
				# print("C = " + str(c) + "   C mod 3 = " + str(math.floor(c / 3)))
				# Koordinate sekcije, moze biti 0, 1 ili 2
				r33 = math.floor(r / 3)
				c33 = math.floor(c / 3)
				r33coordinates = [0,0,0] # niz u koji smestamo indekse kolona grida u kom se nalazi trazeni broj
				r33coordinates[0] = r33 * 3
				r33coordinates[1] = r33 * 3 + 1
				r33coordinates[2] = r33 * 3 + 2
				c33coordinates = [0,0,0]
				c33coordinates[0] = c33 * 3
				c33coordinates[1] = c33 * 3 + 1
				c33coordinates[2] = c33 * 3 + 2
				
				# for i in r33coordinates:
				# 	print("R33 Element: " + str(i))
				# for i in c33coordinates:
				# 	print("C33 Element: " + str(i))

				for i in range(3): # od 0 do 2
					for j in range(3):
						# Preskace selektovani
						if(r == r33coordinates[i] and c == c33coordinates[j]): # and mora, ne &
							# print("R33C[i] = " + str(r33coordinates[i]) + "   C33C[j] = " + str(c33coordinates[j]))
							# print("puzzle[r33i,c33j] = " + str(puzzle[r33coordinates[i]][c33coordinates[j]]))
							continue
						# Ako nadje broj u sekciji koji je isti kao selektovani
						if(puzzle[r33coordinates[i]][c33coordinates[j]] == selected): 
							# print("R33C[i] = " + str(r33coordinates[i]) + "   C33C[j] = " + str(c33coordinates[j]))
							# print("puzzle[r33i,c33j] = " + str(puzzle[r33coordinates[i]][c33coordinates[j]]))
							return False
	return True

def fillOneEmpty(puzzle):
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
			flag = 1
			puzzle[zeroPosition[0]][zeroPosition[1]] = numbersList[0]
			print("Inserted " + str(numbersList[0]) + " into the puzzle on (" + str(zeroPosition[0]) + "," + str(zeroPosition[1]) + ") by rows.")
	
	# Provera za kolone
	for j in range(9):
		zeroCounter = 0
		numbersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		for i in range(9):
			if puzzle[i][j] == 0: # puzzle[i][j] == prvi element prvi red, prvi element drugi red...
				zeroCounter += 1
				zeroPosition[0] = i
				zeroPosition[1] = j
			else:
				#print("TESTIRAM: " + str(puzzle[i][j])) - sesta kolona, pokusava da obrise drugu sesticu ali nema je u listi vise jer je vec obrisana i zato puca
				numbersList.remove(puzzle[i][j])
		if zeroCounter != 1:
			continue
		else:
			flag = 1
			puzzle[zeroPosition[0]][zeroPosition[1]] = numbersList[0]
			print("Inserted " + str(numbersList[0]) + " into the puzzle on (" + str(zeroPosition[0]) + "," + str(zeroPosition[1]) + ") by columns.")

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
			flag = 1
			puzzle[zeroPosition[0]][zeroPosition[1]] = numbersList[0]
			print("Inserted " + str(numbersList[0]) + " into the puzzle on (" + str(zeroPosition[0]) + "," + str(zeroPosition[1]) + ") by 3x3.")

# Trazi redom koje je prvo mesto matrice koje je prazno, za backtracking
def findZero(puzzle):
	for i in range(9): # Treba da prodje kroz redove da bi nasao nule
		for j in range(9): # Treba da prodje kroz sve elemente reda
			if puzzle[i][j] == 0:
				return (i,j)
	return None

def fillFirstZero(puzzle):
	if(findZero(puzzle) == None):
		return None
	x, y = findZero(puzzle) # Koordinate nule po kojoj se radi backtracking
	dict[(x,y)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	
	# Provera po redu
	for i in range(9):
		if puzzle[x][i] != 0 and puzzle[x][i] in dict[(x,y)]:
			dict[(x,y)].remove(puzzle[x][i])
	print("Ostatak elemenata na (" + str(x) + "," + str(y) + ") po fillFirstZero po redu je : " + str(dict[(x,y)]))
	# Nikad nece biti len(numbersList) == 1 zbog fillOneEmpty()

	# Provera po koloni
	for j in range(9):
		if puzzle[j][y] != 0 and puzzle[j][y] in dict[(x,y)]:
			dict[(x,y)].remove(puzzle[j][y])
	print("Ostatak elemenata na (" + str(x) + "," + str(y) + ") po fillFirstZero po koloni je : " + str(dict[(x,y)]))
	# GRESKA - NE MOZE DA STAVLJA PO COL AKO NE PROVERI 3X3
	# if len(dict[(x,y)]) == 1:
	# 	puzzle[x][y] = dict[(x,y)][0] # Da prekrati muke
	# 	positionStack.append((x,y))
	# 	print("Inserted " + str(dict[(x,y)][0]) + " into the puzzle on (" + str(x) + "," + str(y) + ") by backtracking COL.")
	# 	return "ideal"

	# Provera po 3x3
	sectionX = math.floor(x / 3) # elemX = sectionX * 3
	sectionY = math.floor(y / 3) # elemY = sectionY * 3 # print("ElemX: " + str(elemX) + "  ElemY: " + str(elemY))
	dim = 3 # Za sad
	sectionNum = sectionX * dim + sectionY # Ide od nule # (2,1), 3x3, => 3+3+2 = x*dim + y
	# X i Y NISU ISTI, MOZDA PRAVI PROBLEM
	# IPAK MISLIM DA SU ISTI
	for elemNum in range(9):
		# print("Section: " + str(sectionNum) + " Elem: " + str(elemNum))
		xOffset = math.floor(elemNum / 3)
		yOffset = elemNum % 3
		xNew = xOffset + 3 * (math.floor(sectionNum / 3))
		yNew = yOffset + 3 * (sectionNum % 3)
		if puzzle[xNew][yNew] != 0 and puzzle[xNew][yNew] in dict[(x,y)]:
			dict[(x,y)].remove(puzzle[xNew][yNew])
	print("Ostatak elemenata na (" + str(x) + "," + str(y) + ") po fillFirstZero po 3x3 je : " + str(dict[(x,y)]))
	for elemNum in range(9):
		# print("Section: " + str(sectionNum) + " Elem: " + str(elemNum))
		xOffset = math.floor(elemNum / 3)
		yOffset = elemNum % 3
		xNew = xOffset + 3 * (math.floor(sectionNum / 3))
		yNew = yOffset + 3 * (sectionNum % 3)
		# Nebitno je koliko imamo elemenata u listi, pisemo prvi po backtracking principu
		if puzzle[xNew][yNew] == 0: # x i y vise nisu isti kao pre, ovde ide element po element u 3x3, ali jesu koordinate nule
			# Nije htelo dobro ni testPuzzle = puzzle (default je po referenci), ni = puzzle.copy(), ni = puzzle[:]
			# Mora da se importuje "copy", pa da se koristi ova funkcija
			testPuzzle = copy.deepcopy(puzzle)
			print("DICT(X,Y): " + str(dict[(x,y)]))
			if len(dict[(x,y)]) == 0:
				# Ovo je slucaj gde moramo da backtrack-ujemo, jer to znaci da vec postoji isti broj u redu / koloni / 3x3
				print("EMPTY DICT RETURNED X: " + str(x))
				print("EMPTY DICT RETURNED Y: " + str(y))
				return ("emptyDict", x, y, xNew, yNew)
			testPuzzle[xNew][yNew] = dict[(x,y)][0]
			if check(testPuzzle) == True:
				puzzle[xNew][yNew] = dict[(x,y)][0]
				positionStack.append((x,y)) # Stavlja na kraj
				print("Inserted " + str(dict[(x,y)][0]) + " into the puzzle on (" + str(x) + "," + str(y) + ") by backtracking 3X3.")
				dict[(x,y)].pop(0)
				return ("tried", x, y, xNew, yNew) # Posle ovoga postavi globalni flag na 1 da zna da su svi sledeci elementi isto probni, i da pozicije treba da im budu na steku, apendovane
			else:
				print("Failed, printing...")
				puzzle[xNew][yNew] = 0 
				print("Inserted 0 into the puzzle on (" + str(xNew) + "," + str(yNew) + ") by FAILED.")
				for i in dict:
					print(dict[i])
				return ("failedCheck", x, y, xNew, yNew)

def goToPreviousAndReplace(oldX, oldY):
	global GTPARtestPuzzle

	# testPos, testStatus = positionStack.pop() # Pritom i skida sa steka
	# x,y = testPos
	# while testStatus == "ideal":
	# 	x, y = testPos
	# 	puzzle[x][y] = 0
	# 	print("Inserted 0 into the puzzle on (" + str(x) + "," + str(y) + ") by GTPAR WHILE.")
	# 	testPos, testStatus = positionStack.pop()

	(x,y) = positionStack.pop() # Uzima sa kraja
	# Da li moze da bude prazna lista u dict-u kad udje ovde?
	GTPARtestPuzzle = copy.deepcopy(puzzle) # testPuzzle je lokalan za svaki poziv funkcije, sto nije dobro kod rekurzije
	if len(dict[(x,y)]) == 0:
		print("F in the chat")
		puzzle[x][y] = 0
		GTPARtestPuzzle[x][y] = 0 
		# (xOld, yOld) = positionStack.pop()
		goToPreviousAndReplace(x, y) 
		# Kad se vrati iz poziva rekurzije, refresh-uje GTPARtestPuzzle, iako se u samom rekurzivnom pozivu on menja
		# Zbog toga treba :
		# GTPARtestPuzzle[x][y] = 0 
		# Nije, nisu dobri x i y i treba 9 umesto 0
	else:
		GTPARtestPuzzle[x][y] = dict[(x,y)][0]
		# return?
	if check(GTPARtestPuzzle) == True: # Bitno je da gleda globalne
		if len(dict[(x,y)]) == 0:
			return
		puzzle[x][y] = dict[(x,y)][0]
		GTPARtestPuzzle[x][y] = dict[(x,y)][0] # Zbog rekurzije, mozda nebitan
		positionStack.append((x,y))
		print("Inserted " + str(dict[(x,y)][0]) + " into the puzzle on (" + str(x) + "," + str(y) + ") by Previous and Replace.")
		dict[(x,y)].pop(0)
	else:
		print("DJOKEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		print("Old X: " + str(oldX))
		print("Old Y: " + str(oldY))
		puzzle[oldX][oldY] = 0
		GTPARtestPuzzle[x][y] = 0 # Zbog rekurzije
		print("Inserted 0 into the puzzle on (" + str(oldX) + "," + str(oldY) + ") by GOTOPREVIOUS ELSE.")
		# Rekurzija
		goToPreviousAndReplace(x, y)
		

def solve(puzzle):
	global flag
	# global puzzle?
	# Prvo je provera da li je uneseni sudoku ispravan
	if(check(puzzle) == False):
		print("The input puzzle is incorrect.")
	else:
		print("The input puzzle is correct.")
		# Nastavak rada
		# Gleda da li moze trivijalno ubacivanje jednog elementa da uradi, sto se radi po flag-u
		# Kada ne moze vise, radi fillFirstZero koji ubacuje prvi element iz numbersListe u dictu
		while flag == 1:
			fillOneEmpty(puzzle)
		sign = fillFirstZero(puzzle)

		# Tu lezi zec, ovo se poziva samo kada smo 100% sigurni da po fillFirstZero treba da se upise neki broj, to ce biti ili kad se radi po COL pa znamo da je ostao samo jedan element u onoj listi, ili u 3x3 kada dodjemo do tog poslednjeg elementa (to je idealan scenario)
		# Ako se ne radi tako, ako pozivamo fillOneEmpty svaki put kada ubacimo bilo koj element iz liste, to ce pogorsati stvari jer necemo znati koje sve elemente da brisemo kada radimo backtracking, imacemo vise elemenata zbog tog fillOneEmpty
		if sign == "ideal":
			flag = 1
			while flag == 1:
				fillOneEmpty(puzzle) # TODO: Da li ovo moze da se ponavlja u while-u?
		while check(puzzle) == True:
			for i in range(9):
				print(puzzle[i])
			returnElements = fillFirstZero(puzzle)
			if returnElements == None:
				print("Izasao je iz while-a na dobar nacin") # Nema vise nula u sudoku-u
				return
			status = returnElements[0]
			if status == "emptyDict" or status == "failedCheck":
				x = returnElements[1]
				y = returnElements[2]
				goToPreviousAndReplace(x, y)
		print("Pogresno je izasao iz while-a - check() nije dobar")

startTime = time.time()
solve(puzzle)
print("FINAL:")
for i in range(9):
	print(puzzle[i])
print(f"Vreme potrebno: {time.time() - startTime}")