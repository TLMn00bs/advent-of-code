#!/bin/python3


# Puzzle 1
# Step by step
with open('input.txt') as f:
	ids = []
	for code in (line[:-1] for line in f):
		row = int(''.join([str(1 * (rowcode=='B')) for rowcode in code[:7]]), 2)
		col = int(''.join([str(1 * (colcode=='R')) for colcode in code[7:]]), 2)
		id = 8 * row + col
		ids.append(id)
	print(max(ids))

# As one-liner
with open('input.txt') as f: print(max(set(8 * int(''.join([str(1 * (rowcode=='B')) for rowcode in code[:7]]), 2) + int(''.join([str(1 * (colcode=='R')) for colcode in code[7:]]), 2) for code in (line[:-1] for line in f))))


# Puzzle 2
# Step by step
with open('input.txt') as f:
	ids = []
	for code in (line[:-1] for line in f):
		row = int(''.join([str(1 * (rowcode=='B')) for rowcode in code[:7]]), 2)
		col = int(''.join([str(1 * (colcode=='R')) for colcode in code[7:]]), 2)
		id = 8 * row + col
		ids.append(id)

	missing_ids = set(range(max(ids))).difference(ids)
	for missing_id in missing_ids:
		if (missing_id-1 not in missing_ids) and (missing_id+1 not in missing_ids): print(missing_id)

# As one-liner
with open('input.txt') as f: print([missing_id for missing_ids in (set(range(max(ids))).difference(ids) for ids in [[8 * int(''.join([str(1 * (rowcode=='B')) for rowcode in code[:7]]), 2) + int(''.join([str(1 * (colcode=='R')) for colcode in code[7:]]), 2) for code in (line[:-1] for line in f)]]) for missing_id in missing_ids if (missing_id-1 not in missing_ids) and (missing_id+1 not in missing_ids)][0])
