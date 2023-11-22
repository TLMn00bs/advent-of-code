from typing import Iterable, Tuple, Set
import logging

Point = Tuple[int, int, int]

def read_file(file: str) -> Iterable[Point]:
	with open(file, 'r') as f:
		for line in f:
			yield tuple(int(v) for v in line.strip().split(','))

def get_neightbours(p: Point) -> Iterable[Point]:
	x, y, z = p
	yield (x - 1, y, z)
	yield (x + 1, y, z)
	yield (x, y - 1, z)
	yield (x, y + 1, z)
	yield (x, y, z - 1)
	yield (x, y, z + 1)

def p1(args):
	points = read_file(args.file)

	space = set(points)
	print(sum(1 for p in space for n in get_neightbours(p) if n not in space))

def p2(args):
	points = read_file(args.file)

	space = set(points)
	min_x, max_x = min(x for x,y,z in space) - 1, max(x for x,y,z in space) + 1
	min_y, max_y = min(y for x,y,z in space) - 1, max(y for x,y,z in space) + 1
	min_z, max_z = min(z for x,y,z in space) - 1, max(z for x,y,z in space) + 1

	enclosing_space: Set[Point] = set((x, y, z)
		for x in range(min_x, max_x + 1)
		for y in range(min_y, max_y + 1)
		for z in range(min_z, max_z + 1)
	)

	surface: int = 0
	check_points: Set[Point] = {(max_x, max_y, max_z)}
	while len(check_points) > 0:
		p = check_points.pop()
		enclosing_space.remove(p)

		if p in space: continue
		surface += sum(1 for n in get_neightbours(p) if n in space)
		check_points.update(n for n in get_neightbours(p) if n in enclosing_space)

	print(surface)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
