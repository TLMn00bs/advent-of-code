#!/bin/python3


# Puzzle 1
# Step by step
with open('input.txt') as f:
	s = 0
	for line in f:
		conditions, letter, passwd = line[:-1].split(' ')

		c1, c2 = [int(c) for c in conditions.split('-')]
		l = letter[:-1]
		p = passwd

		if c1 <= p.count(l) <= c2: s += 1
	print(s)

# As one-liner
with open('input.txt') as f: print(sum(1 for c1,c2,l,p in ([int(c) for c in conditions.split('-')] + [letter[:-1]] + [passwd] for conditions,letter,passwd in (line[:-1].split(' ') for line in f)) if c1 <= p.count(l) <= c2))


# Puzzle 2
# Step by step
with open('input.txt') as f:
	s = 0
	for line in f:
		conditions, letter, passwd = line[:-1].split(' ')

		c1, c2 = [int(c) for c in conditions.split('-')]
		l = letter[:-1]
		p = passwd

		if (p[c1 - 1] == l) ^ (p[c2 - 1] == l): s += 1
	print(s)

# As one-liner
with open('input.txt') as f: print(sum(1 for c1,c2,l,p in ([int(c) for c in conditions.split('-')] + [letter[:-1]] + [passwd] for conditions,letter,passwd in (line[:-1].split(' ') for line in f)) if (p[c1 - 1] == l) ^ (p[c2 - 1] == l)))
