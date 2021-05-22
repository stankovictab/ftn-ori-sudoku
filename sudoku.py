import math

flag = 1

# 0 su prazna mesta
puzzle = [
	[8,0,4, 1,9,2, 0,0,3],
	[2,3,0, 0,7,0, 0,1,0],
	[6,1,9, 3,0,8, 4,7,2],

	[0,0,2, 0,0,0, 0,8,0],
	[7,0,0, 0,1,0, 0,2,5],
	[0,5,0, 0,2,0, 7,0,0],

	[9,6,7, 0,0,1, 2,0,8],
	[0,8,0, 2,4,0, 0,9,0],
	[4,2,1, 9,8,0, 5,0,7]
]

# Program radi za 9x9 sudoku, ako hocemo 6x6 ili 12x12 moramo check-u da prosledimo i dimenziju da zna kako da radi

# Ovo govori samo da li je sve u sudokuu uredu, ne da li moze da se resi (za sve nule ce reci da je ok)
def check(puzzle):
	# Za svaki element gleda svoj red, kolonu i 3x3
	for r in range(9): # od 0 do 8   
		for c in range(9):
			selected = puzzle[r][c] # r i c su indeksi selektovanog elementa
			print(selected)
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
				print("R = " + str(r) + "   R mod 3 = " + str(math.floor(r / 3)))
				print("C = " + str(c) + "   C mod 3 = " + str(math.floor(c / 3)))
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
	flag = 0
	zeroPositions = [0,0]
	#treba provera za redove
	for i in range(9):
		print("Flag: " + str(flag))
		zeroCounter = 0
		numbersList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		for j in range(9):
			#print("Puzzle i i jot: " + str(puzzle[i][j]))
			if puzzle[i][j] == 0:
				zeroCounter += 1
				zeroPositions[0] = i # ako ima 2 nule, desice se overwrite, medjutim nije toliko bitno jer svakako ima continue i preskocice se
				zeroPositions[1] = j # a ako ima 1 nula, dobijamo indekse te nule i to nam treba
			else:
				print("Numbers list" + str(numbersList))
				print("Broj koji se brise: " + str(puzzle[i][j]))
				numbersList.remove(puzzle[i][j]) # brise broj iz liste na osnovu vrednosti
		print(zeroCounter)		
		if zeroCounter != 1:
			continue
		else: # ovde udje ako ima jednu nulu u redu
			flag = 1
			print("Numbers list" + str(numbersList))
			puzzle[zeroPositions[0]][zeroPositions[1]] = numbersList[0]
			print("3. red puzle: " + str(puzzle[2])) 
			continue
	#treba provera za kolone
	#treba provera za grid

# Trazi redom koje je prvo mesto matrice koje je prazno, za backtracking
def findFree(puzzle):
	return

def solve(puzzle):
	# Prvo je provera da li je uneseni sudoku ispravan
	if(check(puzzle) == False):
		print("The input puzzle is incorrect.")
	else:
		print("The input puzzle is correct.")
		while flag == 1:
			fillOneEmpty(puzzle)
			print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		
solve(puzzle)