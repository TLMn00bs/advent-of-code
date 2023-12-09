#!/bin/python3
import logging
from typing import Tuple, Iterable, List, Set, Dict, Optional
from enum import Enum
from attrs import define, field, Factory
from math import gcd
from functools import reduce
from itertools import count
from collections import defaultdict
import math

def lcm(numbers: Iterable[int]) -> int:
	return reduce(lambda a, b: a * b // gcd(a, b), numbers)


Coordinate    = Tuple[int, int]
OpenPositions = Set[Coordinate]

class Direction(Enum):
	LEFT  = '<'
	RIGTH = '>'
	UP    = '^'
	DOWN  = 'v'

	@property
	def dx(self): return {
		Direction.LEFT : -1,
		Direction.RIGTH: +1
	}.get(self, 0)

	@property
	def dy(self): return {
		Direction.UP  : -1,
		Direction.DOWN: +1
	}.get(self, 0)

@define
class Blizzard:
	x        : int
	y        : int
	direction: Direction
	dx       : int = field(init=False, default=Factory(lambda self: self.direction.dx, takes_self=True))
	dy       : int = field(init=False, default=Factory(lambda self: self.direction.dy, takes_self=True))

	@property
	def position(self) -> Coordinate: return self.x, self.y

@define
class Map:
	start_position: Coordinate
	end_position  : Coordinate
	blizzards     : List[Blizzard]
	border_x      : int
	border_y      : int
	period        : int = field(init=False, default=Factory(lambda self: lcm((self.border_x - 1, self.border_y - 1)), takes_self=True))		# type: ignore

	def print(self, title: Optional[str] = None):
		blizzards: Dict[Coordinate, List[Blizzard]] = defaultdict(lambda: [])
		for blizzard in self.blizzards: blizzards[blizzard.position].append(blizzard)

		repr_map: Dict[Coordinate, str] = {
			# Borders
			**{(x, 0            ): '#' for x in range(self.border_x + 1)},
			**{(x, self.border_y): '#' for x in range(self.border_x + 1)},
			**{(0            , y): '#' for y in range(self.border_y + 1)},
			**{(self.border_x, y): '#' for y in range(self.border_y + 1)},

			# start & end positions
			self.start_position: '.',
			self.end_position  : '.',

			# Blizzards
			**{p: str(blz[0].direction.value if len(blz) == 1 else len(blz)) for p, blz in blizzards.items()}
		}

		if title is not None: print(f'== {title} ==')
		for y in range(self.border_y + 1):
			print(''.join(repr_map.get((x, y), '.') for x in range(self.border_x + 1)))
		print()

	def open_positions(self) -> OpenPositions:
		blizzards = set(blizzard.position for blizzard in self.blizzards)
		return set.union(
			set([self.start_position, self.end_position]),
			set((x, y) for x in range(1, self.border_x) for y in range(1, self.border_y) if (x, y) not in blizzards)
		)

	def next_minute(self) -> None:
		for blizzard in self.blizzards:
			blizzard.x += blizzard.dx
			blizzard.y += blizzard.dy

			if blizzard.x == 0            : blizzard.x = self.border_x - 1
			if blizzard.y == 0            : blizzard.y = self.border_y - 1
			if blizzard.x == self.border_x: blizzard.x = 1
			if blizzard.y == self.border_y: blizzard.y = 1

def parse_blizzards(lines: Iterable[str]) -> Iterable[Blizzard]:
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c not in Direction._value2member_map_: continue
			yield Blizzard(x = x, y = y, direction = Direction(c))

def read_file(file: str) -> Map:
	with open(file, 'r') as f:
		lines = [l.strip() for l in f]

	map = Map(
		start_position = (lines[0] .find('.'), 0),
		end_position   = (lines[-1].find('.'), len(lines) - 1),
		blizzards      = list(parse_blizzards(lines)),
		border_x       = len(lines[0])  - 1,
		border_y       = len(lines)     - 1,
	)

	return map

def get_move_options(current_position: Coordinate, next_open_positions: OpenPositions) -> Iterable[Coordinate]:
	# Wait option
	if current_position in next_open_positions: yield current_position

	# Move right, bottom, left, up
	x, y = current_position
	right, bottom, left, up = (
		(x + 1, y    ),
		(x    , y + 1),
		(x - 1, y    ),
		(x    , y - 1),
	)

	if right  in next_open_positions: yield right
	if bottom in next_open_positions: yield bottom
	if left   in next_open_positions: yield left
	if up     in next_open_positions: yield up


def p1(args):
	map = read_file(args.file)
	valley_states: List[OpenPositions] = [map.open_positions()]
	for _ in range(map.period - 1):
		map.next_minute()
		valley_states.append(map.open_positions())

	options = {map.start_position}
	for i in count(1):
		next_options = set()
		next_open_positions = valley_states[i % map.period]

		while options:
			current_position = options.pop()
			if current_position == map.end_position:
				print(i - 1)
				return

			next_options.update(get_move_options(current_position, next_open_positions))
		
		options = next_options


def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
