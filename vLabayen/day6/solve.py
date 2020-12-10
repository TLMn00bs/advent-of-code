#!/bin/python3


# Puzzle 1
# Step by step
with open('input.txt') as f:
	s = 0
	for group in f.read()[:-1].split('\n\n'):
		persons = [set(person) for person in group.split('\n')]
		s += len(set.union(*persons))
	print(s)

# As one-liner
with open('input.txt') as f: print(sum(len(g) for g in [set.union(*[set(person) for person in group.split('\n')]) for group in f.read()[:-1].split('\n\n')]))


# Puzzle 2
# Step by step
with open('input.txt') as f:
	s = 0
	for group in f.read()[:-1].split('\n\n'):
		persons = [set(person) for person in group.split('\n')]
		s += len(set.intersection(*persons))
	print(s)

# As one-liner
with open('input.txt') as f: print(sum(len(g) for g in [set.intersection(*[set(person) for person in group.split('\n')]) for group in f.read()[:-1].split('\n\n')]))
