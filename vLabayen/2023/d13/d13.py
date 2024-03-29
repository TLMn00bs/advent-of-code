import logging
from typing import List, Iterable, Optional, Set
from attrs import define, field
from collections import Counter


def is_reflective(row_or_column: str, index: int) -> bool:
	side1, side2 = row_or_column[:index], row_or_column[index:]
	min_size = min(len(side1), len(side2))
	side1 = side1[-min_size:]
	side2 = side2[:min_size]

	return side1[::-1] == side2

@define
class Pattern:
	rows: List[str]
	row_reflections: List[Set[int]] = field(init=False)
	col_reflections: List[Set[int]] = field(init=False)

	def __attrs_post_init__(self):
		self.row_reflections = [set(idx for idx in range(1, self.width)  if is_reflective(row, idx)) for row in self.rows]
		self.col_reflections = [set(idx for idx in range(1, self.height) if is_reflective(col, idx)) for col in self.cols]

	@property
	def width(self) -> int: return len(self.rows[0])
	@property
	def height(self) -> int: return len(self.rows)

	@property
	def cols(self) -> Iterable[str]:
		for idx in range(self.width):
			yield ''.join(row[idx] for row in self.rows)

	def __repr__(self): return '\n'.join(self.rows)


def read_file(file: str) -> Iterable[Pattern]:
	with open(file, 'r') as f:
		rows = []
		for line in (l.strip() for l in f):
			if line == '':
				yield Pattern(rows)
				rows = []
				continue
		
			rows.append(line)

		yield Pattern(rows)


def find_vertical_reflection(pattern: Pattern) -> Optional[int]:
	reflection = set.intersection(*pattern.row_reflections)
	if len(reflection) > 0: return reflection.pop()

def find_horizontal_reflection(pattern: Pattern) -> Optional[int]:
	reflection = set.intersection(*pattern.col_reflections)
	if len(reflection) > 0: return reflection.pop()

def find_vertical_smudged_reflection(pattern: Pattern) -> Optional[int]:
	for col, value in Counter(v for reflection in pattern.row_reflections for v in reflection).most_common():
		if value == pattern.height - 1: return col

def find_horizontal_smudged_reflection(pattern: Pattern) -> Optional[int]:
	for row, value in Counter(v for reflection in pattern.col_reflections for v in reflection).most_common():
		if value == pattern.width - 1: return row

def p1(args):
	patterns = read_file(args.file)
	print(sum(find_vertical_reflection(pattern) or 100 * find_horizontal_reflection(pattern) for pattern in patterns))		# type: ignore


def p2(args):
	patterns = read_file(args.file)
	print(sum(find_vertical_smudged_reflection(pattern) or 100 * find_horizontal_smudged_reflection(pattern) for pattern in patterns))		# type: ignore

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
