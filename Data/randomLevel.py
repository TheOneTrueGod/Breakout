import random
file = open("Level16.lev", "w")
file.write("SCREENSIZE 8 17\n")
file.write("PLAYERMINYPOS 200\n")
a = [1, 2, 3, 4, 6, 7]
b = [0, 1, 2, 3, 4, 5]
for y in range(10):
	for x in range(8):
		l = b[min(max(10 - y - 5, 0), len(b) - 1):min(max(10 - y, 0), len(b))]
		type = str(random.choice(a)) + str(random.choice(l)) + " "
		if "7" in type and random.random() <= 0.6 or "2" in type and random.random() <= 0.3:
			type = str(random.choice(a)) + str(random.choice(l)) + " "
		file.write(type)
	file.write("\n")