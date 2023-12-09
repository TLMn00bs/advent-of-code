#!/bin/python3
import logging
from typing import Tuple, Iterable, List, Set, Dict
from enum import Enum
from attrs import define, field, Factory
from math import gcd
from functools import reduce
from collections import defaultdict

def lcm(numbers: Iterable[int]) -> int:
	return reduce(lambda a, b: a * b // gcd(a, b), numbers)


Coordinate = Tuple[int, int]

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

	def print(self):
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

		for y in range(self.border_y + 1):
			print(''.join(repr_map.get((x, y), '.') for x in range(self.border_x + 1)))


	def blizzard_positions(self) -> Set[Coordinate]:
		return set(blizzard.position for blizzard in self.blizzards)

	def next_minute(self) -> None:
		for blizzard in self.blizzards:
			dx, dy = blizzard.direction.dx, blizzard.direction.dy
			blizzard.x += dx
			blizzard.y += dy

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

def p1(args):
	map = read_file(args.file)
	map.print()
	map.next_minute()
	print('----')
	map.print()

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
