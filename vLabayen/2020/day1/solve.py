from itertools import combinations

with open('input.txt') as f: print([c[0]*c[1] for c in combinations((int(line[:-1]) for line in f), 2) if (c[0] + c[1] == 2020)][0])
with open('input.txt') as f: print([c[0]*c[1]*c[2] for c in combinations((int(line[:-1]) for line in f), 3) if (c[0] + c[1] + c[2] == 2020)][0])
