from itertools import combinations
import numpy as np

with open('input.txt') as f:
	jolts = sorted([0] + [int(line[:-1]) for line in f])
	jolts.append(jolts[-1] + 3)

diff = [j - jolts[n] for n,j in enumerate(jolts[1:])]

# Solution to puzzle 1
print(diff.count(1) * diff.count(3))


# Puzzle 2 recusive attemp
#def num_arrangement(jolts):
#	s = 0
#	for i,j in enumerate(jolts[1:-1]):
#		if j - jolts[i] < 3:
#			new_jolts = [_j for _j in jolts if _j != j]
#			s += num_arrangement(new_jolts)
#
#	return s + 1
#
#print(num_arrangement(jolts))

jd = [(0,)] + [(j, j - jolts[n]) for n,j in enumerate(jolts[1:])]
fixed = [j[0] for n,j in enumerate(jd) if (n == 0) or (j[1] == 3) or (jd[n + 1][1] == 3)]
pairs = [(fixed[n], f) for n,f in enumerate(fixed[1:])]
p_opts = [(p, [j for j in jolts if p[0] < j < p[1]]) for p in pairs]

def is_valid(jolts):
	return all([(j - jolts[n] <= 3) for n,j in enumerate(jolts[1:])])

def num_pair_opts(p_opts_i):
	opts_i = p_opts_i[1]

	n = 1 if is_valid(p_opts_i[0]) else 0
	for c in (cmb for n in range(len(opts_i)) for cmb in combinations(opts_i, n + 1)):
		if is_valid(sorted(list(p_opts_i[0]) + list(c))): n+=1

	return n

# Solution to puzzle 2
print(np.prod([num_pair_opts(p_opts_i) for p_opts_i in p_opts]))

