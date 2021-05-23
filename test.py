recnik = {}
x = "a"
y = "b"
recnik[(x,y)] = [1,2]
if x == 1:
	recnik[(x,y)].pop(0)
for i in recnik:
	print(recnik[i])