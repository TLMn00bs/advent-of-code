#!/bin/python3
import logging
from attrs import define, field
from typing import Tuple, Iterable, Set, List, Dict, Optional
from collections import defaultdict
from itertools import count

Coordinate = Tuple[int, int]


def print_elves(elves: Set[Coordinate], title: str) -> None:
	max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
	max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

	xrange = range(min_x - 1, max_x + 2)
	yrange = range(min_y - 1, max_y + 2)
	repr = lambda c: '#' if c in elves else '.'

	print(f'== {title} ==')
	for y in yrange: print(''.join(repr((x, y)) for x in xrange))
	print()

def get_containing_rectangle_area(elves: Set[Coordinate]) -> int:
	max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
	max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

	return (max_x - min_x + 1) * (max_y - min_y + 1)

def read_file(file: str) -> Iterable[Coordinate]:
	with open(file, 'r') as f:
		for y, line in enumerate((l.strip() for l in f)):
			for x, c in enumerate(line):
				if c == '#': yield x, y

@define
class SoilMap:
	elves: Set[Coordinate]

	has_neighbours   : Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_north: Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_south: Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_west : Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_east : Dict[Coordinate, bool] = field(init=False, factory=dict)

	def __attrs_post_init__(self):
		self.inner_update()

	def update(self, remove: Set[Coordinate], add: Set[Coordinate]):
		self.elves.difference_update(remove)
		self.elves.update(add)
		self.inner_update()

	def inner_update(self):
		for (x, y) in self.elves:
			self.has_neighbours[(x, y)] = any((
				(x - 1, y - 1) in self.elves,
				(x    , y - 1) in self.elves,
				(x + 1, y - 1) in self.elves,
				(x - 1, y    ) in self.elves,
				(x + 1, y    ) in self.elves,
				(x - 1, y + 1) in self.elves,
				(x    , y + 1) in self.elves,
				(x + 1, y + 1) in self.elves,
			))
			self.should_move_north[(x, y)] = not any((
				(x - 1, y - 1) in self.elves,
				(x    , y - 1) in self.elves,
				(x + 1, y - 1) in self.elves,
			))
			self.should_move_south[(x, y)] = not any((
				(x - 1, y + 1) in self.elves,
				(x    , y + 1) in self.elves,
				(x + 1, y + 1) in self.elves,
			))
			self.should_move_west[(x, y)] = not any((
				(x - 1, y - 1) in self.elves,
				(x - 1, y    ) in self.elves,
				(x - 1, y + 1) in self.elves,
			))
			self.should_move_east[(x, y)] = not any((
				(x + 1, y - 1) in self.elves,
				(x + 1, y    ) in self.elves,
				(x + 1, y + 1) in self.elves,
			))


def run(soil_map: SoilMap, max_rounds: Optional[int] = None) -> int:
	proposing_order: List[Tuple[Dict[Coordinate, bool], int, int]] = [
		(soil_map.should_move_north,  0, -1),
		(soil_map.should_move_south,  0, +1),
		(soil_map.should_move_west , -1,  0),
		(soil_map.should_move_east , +1,  0),
	]

	def rounds():
		if max_rounds is None: return count()
		assert max_rounds > 0
		return range(max_rounds)

	# print_elves(soil_map.elves, 'Initial State')
	for round in rounds():
		round_proposing_order = [proposing_order[(round + i) % 4] for i in range(4)]
		elves_proposed_destinations: Dict[Coordinate, Coordinate] = {}
		requested_destinations = defaultdict(lambda: 0)

		for (x, y) in soil_map.elves:
			if not soil_map.has_neighbours[(x, y)]: continue

			for should_move, dx, dy in round_proposing_order:
				if should_move[(x, y)]:
					new_location = (x + dx, y + dy)
					requested_destinations[new_location] += 1
					elves_proposed_destinations[(x, y)] = new_location
					break
			else: continue

		new_destinations = set(destination for destination, num_times_requested in requested_destinations.items() if num_times_requested == 1)
		moving_elves = set(elve for elve, destination in elves_proposed_destinations.items() if destination in new_destinations)

		if len(new_destinations) == 0: return round + 1
		soil_map.update(moving_elves, new_destinations)
		# print_elves(soil_map.elves, f'End of Round {round + 1}')

	return round + 1	# type: ignore

def p1(args):
	soil_map = SoilMap(set(read_file(args.file)))
	_ = run(soil_map, max_rounds=10)
	print(get_containing_rectangle_area(soil_map.elves) - len(soil_map.elves))

def p2(args):
	soil_map = SoilMap(set(read_file(args.file)))
	num_rounds = run(soil_map)
	print(num_rounds)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
