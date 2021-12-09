#!/bin/python3
from collections import defaultdict, Counter
from numpy import prod

def get_adjacents_idx(row_idx, col_idx, num_rows, num_cols):
	idxs = []
	if row_idx != 0: idxs.append((row_idx - 1, col_idx))
	if col_idx != 0: idxs.append((row_idx, col_idx - 1))
	if row_idx != num_rows - 1: idxs.append((row_idx + 1, col_idx))
	if col_idx != num_cols - 1: idxs.append((row_idx, col_idx + 1))
	return idxs

def follow(flow_map, row_idx, col_idx, low_points):
	if (row_idx, col_idx) in low_points: return (row_idx, col_idx)
	next_row, next_col = flow_map[row_idx, col_idx]
	return follow(flow_map, next_row, next_col, low_points)

def p1(args):
	with open(args.file, 'r') as f: heightmap = [[int(n) for n in line.strip()] for line in f]

	low_points = []
	for i, row in enumerate(heightmap):
		for j, height in enumerate(row):
			min_adj = min(heightmap[row_idx][col_idx] for row_idx, col_idx in get_adjacents_idx(i, j, len(heightmap), len(row)))
			if height < min_adj: low_points.append(height)

	risk_levels = [height + 1 for height in low_points]
	print(sum(risk_levels))

def p2(args):
	with open(args.file, 'r') as f: heightmap = [[int(n) for n in line.strip()] for line in f]

	low_points = set()
	flow_map = {}
	for i, row in enumerate(heightmap):
		for j, height in enumerate(row):
			if height == 9: continue
			min_adj_height, min_adj_row, min_adj_col = min((heightmap[row_idx][col_idx], row_idx, col_idx) for row_idx, col_idx in get_adjacents_idx(i, j, len(heightmap), len(row)))
			min_height, min_row, min_col = min((height, i, j), (min_adj_height, min_adj_row, min_adj_col))

			if height < min_adj_height: low_points.add((i, j))
			flow_map[(i, j)] = (min_row, min_col)

	top_basin_sizes = [size for (row, col), size in Counter((follow(flow_map, i, j, low_points) for i,j in flow_map)).most_common(3)]
	print(prod(top_basin_sizes))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
