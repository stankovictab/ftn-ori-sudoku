# ftn-ori-sudoku
[Osnove Računarske Inteligencije]  
Predmetni Projekat  
AI Sudoku rešavač u Python-u koji radi po principima Backtracking i Depth First Search algoritma.\
Q2 2021  

Za kreiranje početnih sudoku zagonetki je korišćena biblioteka [py-sudoku](https://pypi.org/project/py-sudoku/).\
Za kontrolu verzija je korišćen GitHub, pa su neophodni `.gitignore` i `README.md` fajlovi.
### Uputstvo

1. Instalirati PyGame biblioteku u Python okruženje u kojem bi pokretali program preko pip package installer-a :\
`pip install pygame`
2. Instalirati `numpy` biblioteku preko conda package manager-a :\
`conda install -c anaconda numpy`
3. U `sudoku.py` možete podesiti parametre programa, kao što su težina zagonetke (`DIFFICULTY`), da li ce se sudoku iscrtavati u prozoru (`DRAWBOOL`), brzina ispisa (`DRAWSPEED`), i boje (`STARTINGELEMENTCOLOUR` i `INSERTEDELEMENTCOLOUR`) preko globalnih konstanti na pocetku fajla.
4. Pokrenuti program preko `sudoku.py` unutar tog Python okruženja.



![Sudoku Gif](https://user-images.githubusercontent.com/62820268/118686206-16648b00-b804-11eb-8ad0-374a226b337c.gif)
