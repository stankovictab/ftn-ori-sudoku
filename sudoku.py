import math

flag = 1

# 0 su prazna mesta
puzzle = [
	[8,7,4, 1,9,2, 0,0,3],
	[2,3,0, 0,7,0, 8,1,9],
	[6,1,9, 3,0,8, 4,7,2],

	[0,0,2, 7,0,5, 0,8,0],
	[7,0,0, 0,1,0, 0,2,5],
	[0,5,0, 0,2,0, 7,0,0],

	[9,6,7, 5,0,1, 2,4,8],
	[0,8,0, 2,4,7, 0,9,0],
	[4,2,1, 9,8,0, 5,0,7]
]

# Program radi za 9x9 sudoku, ako hocemo 6x6 ili 12x12 moramo check-u da prosledimo i dimenziju da zna kako da radi

# Ovo govori samo da li je sve u sudokuu uredu, ne da li moze da se resi (za sve nule ce reci da je ok)
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
			print("Inserted " + str(numbersList[0]) + " into the puzzle on (" + str(zeroPosition[0] + 1) + "," + str(zeroPosition[1] + 1) + ") by rows.")
	
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
			flag = 1
			puzzle[zeroPosition[0]][zeroPosition[1]] = numbersList[0]
			print("Inserted " + str(numbersList[0]) + " into the puzzle on (" + str(zeroPosition[0] + 1) + "," + str(zeroPosition[1] + 1) + ") by columns.")

	# Provera za grid
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
			print("Inserted " + str(numbersList[0]) + " into the puzzle on (" + str(zeroPosition[0] + 1) + "," + str(zeroPosition[1] + 1) + ") by 3x3.")


# Trazi redom koje je prvo mesto matrice koje je prazno, za backtracking
def findZero(puzzle):
	for i in range(9): # treba da prodje kroz redove da bi nasao nule
		for j in range(9): # treba da prodje kroz sve elemente reda
			if puzzle[i][j] == 0:
				return (i,j)
		
		
def fillFirstZero(puzzle):
	x, y = findZero(puzzle)
	numbersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	# Brise elemente koji se vec nalaze u datom redu
	for i in range(9):
		if puzzle[x][i] != 0:
			numbersList.remove(puzzle[x][i])
			
	print("Ostatak elemenata: " + str(numbersList))
				
	
		

def solve(puzzle):
	global flag
	# Prvo je provera da li je uneseni sudoku ispravan
	if(check(puzzle) == False):
		print("The input puzzle is incorrect.")
	else:
		print("The input puzzle is correct.")
		while flag == 1:
			fillOneEmpty(puzzle)
		
solve(puzzle)

# Print sudoku-a
for i in range(9):
	print(puzzle[i])