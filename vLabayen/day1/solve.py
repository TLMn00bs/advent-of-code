#!/bin/python3
from itertools import combinations


# Puzzle 1
# Step by step
with open('input.txt') as f:
	nums = [int(line[:-1]) for line in f]
	for x,y in combinations(nums, 2):
		if x + y == 2020: print(x * y)

# As one-liner
with open('input.txt') as f: print([x*y for x,y in combinations((int(line[:-1]) for line in f), 2) if (x + y == 2020)][0])


# Puzzle 2
# Step by step
with open('input.txt') as f:
	nums = [int(line[:-1]) for line in f]
	for x,y,z in combinations(nums, 3):
		if x + y + z == 2020: print(x * y * z)

# As one-liner
with open('input.txt') as f: print([x * y * z for x,y,z in combinations((int(line[:-1]) for line in f), 3) if (x + y + z == 2020)][0])
