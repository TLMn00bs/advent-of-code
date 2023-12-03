import logging
from typing import Tuple, List, Dict, Set, Iterable
from attrs import define, field
import re
from itertools import product

Coordinate = Tuple[int, int]

def get_neighbours(pos: Coordinate) -> Iterable[Coordinate]:
	x, y = pos
	for x_inc, y_inc in product([-1, 0, 1], [-1, 0, 1]):
		if x_inc == y_inc == 0: continue
		yield (x + x_inc, y + y_inc)

@define
class Simbol:
	position: Coordinate
	character: str

@define
class Number:
	positions: List[Coordinate]
	number: int

	def __hash__(self): return id(self)

@define
class Schematic:
	simbols: List[Simbol] = field(factory=list)
	numbers: List[Number] = field(factory=list)


find_numbers_rgx = re.compile(r'([0-9]+)')
find_simbols_rgx = re.compile(r'([^0-9\.])')
def read_file(file: str) -> Schematic:
	schematic = Schematic()

	with open(file, 'r') as f:
		for y, line in enumerate(l.strip() for l in f):
			for number in find_numbers_rgx.finditer(line):
				schematic.numbers.append(Number(
					positions = [(x, y) for x in range(*number.span())],
					number = int(number.group())
				))

			for simbol in find_simbols_rgx.finditer(line):
				schematic.simbols.append(Simbol(
					position = (simbol.start(), y),
					character = simbol.group()
				))

	return schematic


def p1(args):
	schematic = read_file(args.file)
	numbers: Dict[Coordinate, Number] = {
		(x, y): number for number in schematic.numbers for (x, y) in number.positions
	}

	part_numbers: Set[Number] = set()
	for simbol in schematic.simbols:
		for position in get_neighbours(simbol.position):
			n = numbers.get(position, None)
			if n is not None: part_numbers.add(n)

	print(sum(n.number for n in part_numbers))

def p2(args):
	schematic = read_file(args.file)
	numbers: Dict[Coordinate, Number] = {
		(x, y): number for number in schematic.numbers for (x, y) in number.positions
	}

	gear_ratios: List[int] = []
	for gear in (simbol for simbol in schematic.simbols if simbol.character == '*'):
		part_numbers: Set[Number] = set()
		for position in get_neighbours(gear.position):
			n = numbers.get(position, None)
			if n is not None: part_numbers.add(n)
		
		if len(part_numbers) == 2:
			n1, n2 = part_numbers
			gear_ratios.append(n1.number * n2.number)

	print(sum(gear_ratios))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
