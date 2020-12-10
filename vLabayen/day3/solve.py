#!/bin/python3
from functools import reduce


# Puzzle 1
# Step by step
with open('input.txt') as f:
	x, y = 3, 1
	c = 0
	for r,line in enumerate(_line[:-1] for _r,_line in enumerate(f) if _r%y == 0):
		if line[x * r % len(line)] == '#': c += 1
	print(c)

# As one-liner
# const y = 1, const x = 3
with open('input.txt') as f: print(sum(1 for r,line in enumerate(_line[:-1] for _r,_line in enumerate(f) if _r%y == 0) if line[x * r % len(line)] == '#'))


# Puzzle 2
# Step by step
with open('input.txt') as f:
	slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]

	# As we want to iterate the file just once, and the i depends for appling line[x * i % len()] depends on y, we cannot use enumerate with _r%y to update the row index
	# We define an array of arrays, one array for each slope, the first element will be the count and the second the index of valid rows.
	c = [[0, 0] for _ in range(len(slopes))]
	for r, line in ((_r,_line[:-1]) for _r,_line in enumerate(f)):
		for i,(x,y) in enumerate(slopes):			# i = the index of each slope
			if r%y == 0:					# Skip rows based on the y slope

				if line[x * c[i][1] % len(line)] == '#': c[i][0] += 1		# Increment the tree count
				c[i][1] += 1                                                    # Increment the efective row of that slope

	print(reduce(lambda x,y: x*y, (cs[0] for cs in c)))		# The result is the product of all counts

# As one-liner
# const slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)], const len(slopes) = 5
with open('input.txt') as f: print(reduce(lambda x,y: x*y, [cs[0] for cs in reduce(lambda c,enum,slopes=slopes: [[c[i][0] + 1*(line[x * c[i][1] % len(line)] == '#' and r%y == 0), c[i][1] + 1*(r%y == 0)] for i,(x,y) in enumerate(slopes) for r,line in [enum]], ((_r,_line[:-1]) for _r,_line in enumerate(f)), [[0,0] for _ in range(len(slopes))])]))
