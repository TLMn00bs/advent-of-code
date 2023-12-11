import logging
from typing import Dict, Tuple, Set, Deque, Iterable, List
from attrs import define, field
from collections import deque
from itertools import count

Coordinate = Tuple[int, int]
PipeConnections = List[Coordinate]

pipes_shapes: Dict[str, PipeConnections] = {
	'|': [( 0, -1), ( 0, +1)],
	'-': [(-1,  0), (+1,  0)],
	'L': [( 0, -1), (+1,  0)],
	'J': [( 0, -1), (-1,  0)],
	'7': [( 0, +1), (-1,  0)],
	'F': [( 0, +1), (+1,  0)],
	'S': [( 0, -1), ( 0, +1), (-1, 0), (+1, 0)]
}

@define(hash=True, eq=False)
class Pipe:
	shape: str
	x: int
	y: int

	neighbours: Set[Coordinate] = field(init=False, hash=False, factory=set)
	def __attrs_post_init__(self):
		connections = pipes_shapes[self.shape]
		for x, y in connections:
			self.neighbours.add((self.x + x, self.y + y))

	@staticmethod
	def are_connected(pipe1: 'Pipe', pipe2: 'Pipe') -> bool:
		return all((
			(pipe1.x, pipe1.y) in pipe2.neighbours,
			(pipe2.x, pipe2.y) in pipe1.neighbours,
		))


def read_file(file: str) -> Dict[Coordinate, Pipe]:
	pipes: Dict[Coordinate, Pipe] = {}

	with open(file, 'r') as f:
		for y, line in enumerate(l.strip() for l in f):
			for x, c in enumerate(line):
				if c == '.': continue
				pipes[(x, y)] = Pipe(c, x, y)

	return pipes

def get_connected_pipes(pipe: Pipe, pipes: Dict[Coordinate, Pipe]) -> Iterable[Pipe]:
	for position in pipe.neighbours:
		neighbour = pipes.get(position, None)

		if neighbour is None: continue
		if not Pipe.are_connected(pipe, neighbour): continue
		yield neighbour


def p1(args):
	pipes = read_file(args.file)
	start = [pipe for pipe in pipes.values() if pipe.shape == 'S'][0]

	visited_nodes: Set[Pipe] = set([start])
	next_nodes: Deque[Pipe] = deque([start])

	for i in count():
		for _ in range(len(next_nodes)):
			node = next_nodes.popleft()
			connected_pipes = list(get_connected_pipes(node, pipes))

			if all(pipe in visited_nodes for pipe in connected_pipes):
				print(i + 1)
				return

			for neighbour in connected_pipes:
				if neighbour in visited_nodes: continue

				next_nodes.append(neighbour)
				visited_nodes.add(neighbour)



def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
