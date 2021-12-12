#!/bin/python3
from itertools import count

def get_neighbours_idx(row_idx, col_idx, num_rows, num_cols):
	idxs = []
	if row_idx != 0: idxs.append((row_idx - 1, col_idx))
	if col_idx != 0: idxs.append((row_idx, col_idx - 1))
	if row_idx != num_rows - 1: idxs.append((row_idx + 1, col_idx))
	if col_idx != num_cols - 1: idxs.append((row_idx, col_idx + 1))
	if row_idx != 0 and col_idx != 0: idxs.append((row_idx - 1, col_idx - 1))
	if row_idx != 0 and col_idx != num_cols - 1: idxs.append((row_idx - 1, col_idx + 1))
	if row_idx != num_rows - 1 and col_idx != 0: idxs.append((row_idx + 1, col_idx - 1))
	if row_idx != num_rows - 1 and col_idx != num_cols - 1: idxs.append((row_idx + 1, col_idx + 1))
	return idxs

def step(flashed, row, col, octopus):
	octopus['energy'] += 1
	if (row, col) in flashed: return

	if octopus['energy'] > 9:
		flashed.update([(row, col)])
		for (nrow, ncol, n) in octopus['neighbours']: step(flashed, nrow, ncol, n)

def p1(args):
	with open(args.file, 'r') as f: octopuses = {(row, col): {'energy': int(n)} for row,l in enumerate(f) for col,n in enumerate(l.strip())}
	for (row, col), octopus in octopuses.items(): octopus['neighbours'] = [(nrow, ncol, octopuses[(nrow, ncol)]) for nrow, ncol in get_neighbours_idx(row, col, 10, 10)]

	num_flashes = 0
	for i in range(100):
		flashed = set()
		for (row, col), octopus in octopuses.items(): step(flashed, row, col, octopus)
		for row, col in flashed: octopuses[(row, col)]['energy'] = 0
		num_flashes += len(flashed)

	print(num_flashes)

def p2(args):
	with open(args.file, 'r') as f: octopuses = {(row, col): {'energy': int(n)} for row,l in enumerate(f) for col,n in enumerate(l.strip())}
	for (row, col), octopus in octopuses.items(): octopus['neighbours'] = [(nrow, ncol, octopuses[(nrow, ncol)]) for nrow, ncol in get_neighbours_idx(row, col, 10, 10)]

	for i in count():
		flashed = set()
		for (row, col), octopus in octopuses.items(): step(flashed, row, col, octopus)
		for row, col in flashed: octopuses[(row, col)]['energy'] = 0
		if len(flashed) == 100:
			print(i + 1)
			return

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
