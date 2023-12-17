import logging
from typing import List, Iterable, Optional
from attrs import define

@define
class Pattern:
	rows: List[str]

	@property
	def width(self) -> int: return len(self.rows[0])
	@property
	def height(self) -> int: return len(self.rows)

	@property
	def columns(self) -> Iterable[str]:
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
	num_columns_to_the_left = set(range(1, pattern.width))
	for row in pattern.rows:
		for column in num_columns_to_the_left.copy():
			left, right = row[:column], row[column:]
			min_size = min(len(left), len(right))
			left  = left[-min_size:]
			right = right[:min_size]

			if not left[::-1] == right: num_columns_to_the_left.remove(column)

	if len(num_columns_to_the_left) == 1: return num_columns_to_the_left.pop()

def find_horizontal_reflection(pattern: Pattern) -> Optional[int]:
	num_rows_above = set(range(1, pattern.height))
	for column in pattern.columns:
		for row in num_rows_above.copy():
			above, below = column[:row], column[row:]
			min_size = min(len(above), len(below))
			above = above[-min_size:]
			below = below[:min_size]

			if not above[::-1] == below: num_rows_above.remove(row)
	
	if len(num_rows_above) == 1: return num_rows_above.pop()


def p1(args):
	patterns = list(read_file(args.file))
	print(sum(find_vertical_reflection(pattern) or 100 * find_horizontal_reflection(pattern) for pattern in patterns))		# type: ignore


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
