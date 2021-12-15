#!/bin/python3
def get_adjacents_idx(row_idx, col_idx, num_rows, num_cols):
	idxs = []
	if row_idx != 0: idxs.append((row_idx - 1, col_idx))
	if col_idx != 0: idxs.append((row_idx, col_idx - 1))
	if row_idx != num_rows - 1: idxs.append((row_idx + 1, col_idx))
	if col_idx != num_cols - 1: idxs.append((row_idx, col_idx + 1))
	return idxs

def p1(args):
	with open(args.file, 'r') as f:
		nodes = {(row, col): {'weight': int(n)} for row,line in enumerate(f) for col,n in enumerate(line.strip())}
		num_rows, num_cols = max(row for row, col in nodes.keys()) + 1, max(col for row, col in nodes.keys()) + 1

		for (r,c), n in nodes.items():
			neighbours = get_adjacents_idx(r, c, num_rows, num_cols)
			n['neighbours'] = [(row, col) for row, col in neighbours]
			n['reach_by'] = None

		# The exit node is already in the target node with no move required
		nodes[(num_rows - 1, num_cols - 1)]['reach_by'] = 0

	while nodes[(0, 0)]['reach_by'] is None:
		for n in (n for n in nodes.values() if n['reach_by'] is not None):
			for neighbour in (nodes[(row, col)] for row, col in n['neighbours']):
				acc_cost = n['reach_by'] + n['weight']
				if neighbour['reach_by'] is None or neighbour['reach_by'] > acc_cost: neighbour['reach_by'] = acc_cost


	print(nodes[(0, 0)])

def display_grid(nodes, num_rows, num_cols):
	for r in range(num_rows): print(''.join(str(nodes[(r, c)]['weight']) for c in range(num_cols)))

def p2(args):
	with open(args.file, 'r') as f:
		nodes = {(row, col): {'weight': int(n)} for row,line in enumerate(f) for col,n in enumerate(line.strip())}
		num_rows, num_cols = max(row for row, col in nodes.keys()) + 1, max(col for row, col in nodes.keys()) + 1

		# Increase the map in both dimensions by a factor of 5
		for (i, j) in ((i, j) for i in range(5) for j in range(5) if not i == j == 0):
			for row, col, n in ((row, col, nodes[(row, col)]) for row in range(num_rows) for col in range(num_cols)):
				w = n['weight'] + i + j
				if w > 9: w = w - 9

				nodes[(row + num_rows * i, col + num_cols * j)] = {'weight': w}
		num_rows, num_cols = 5 * num_rows, 5 * num_cols

		for (r,c), n in nodes.items():
			neighbours = get_adjacents_idx(r, c, num_rows, num_cols)
			n['neighbours'] = [(row, col) for row, col in neighbours]
			n['reach_by'] = None

		# The exit node is already in the target node with no move required
		nodes[(num_rows - 1, num_cols - 1)]['reach_by'] = 0

	# Start with the end node as the only one that needs to update
	update_queue = set([(num_rows - 1, num_cols - 1)])
	while len(update_queue) != 0:

		# Each iteration, update just if the node has been updated.
		# If reach_by has not been updated in last iteration, there is no news for the neightbours so no need to check
		updated_this_iteration = set()
		for r, c in update_queue:
			n = nodes[(r, c)]
			for row, col, neighbour in ((row, col, nodes[(row, col)]) for row, col in n['neighbours']):
				acc_cost = n['reach_by'] + n['weight']
				if neighbour['reach_by'] is None or neighbour['reach_by'] > acc_cost:
					neighbour['reach_by'] = acc_cost
					updated_this_iteration.update([(row, col)])	# Add this node to the queue

		update_queue = updated_this_iteration	# Update the queue

	print(nodes[(0, 0)])

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
