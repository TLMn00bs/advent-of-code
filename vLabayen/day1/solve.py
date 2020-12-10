#!/bin/python3
from itertools import combinations


# Puzzle 1
# Step by step
with open('input.txt') as f:
	nums = [int(line[:-1]) for line in f]
	for c in combinations(nums, 2):
		if c[0] + c[1] == 2020: print(c[0] * c[1])

# As one-liner
with open('input.txt') as f: print([c[0]*c[1] for c in combinations((int(line[:-1]) for line in f), 2) if (c[0] + c[1] == 2020)][0])


# Puzzle 2
# Step by step
with open('input.txt') as f:
	nums = [int(line[:-1]) for line in f]
	for c in combinations(nums, 3):
		if c[0] + c[1] + c[2] == 2020: print(c[0] * c[1] * c[2])

# As one-liner
with open('input.txt') as f: print([c[0]*c[1]*c[2] for c in combinations((int(line[:-1]) for line in f), 3) if (c[0] + c[1] + c[2] == 2020)][0])
