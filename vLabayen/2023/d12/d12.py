import logging
from typing import List, Iterable, Tuple
from enum import Enum
from attrs import define, field
from functools import lru_cache


class Spring(Enum):
	OPERATIONAL = '.'
	DAMAGED     = '#'
	UNKNOWN     = '?'

	def __repr__(self): return self.name

@define(hash=True, eq=True)
class Group:
	springs: Tuple[Spring, ...]
	must_exists: bool = field(init=False)

	def __attrs_post_init__(self):
		self.must_exists = any(spring == Spring.DAMAGED for spring in self.springs)

	def __len__(self) -> int: return len(self.springs)
	def __repr__(self) -> str: return ''.join(s.value for s in self.springs)

@define
class SpringRow:
	groups: List[Group]
	damaged_group_sizes: List[int]

	def __repr__(self) -> str:
		springs = ' '.join(g.__repr__() for g in self.groups)
		return f'{springs} {self.damaged_group_sizes}'

def get_groups(springs: List[Spring]) -> List[Group]:
	posible_damaged_groups: List[Group] = []
	current_group: List[Spring] = []
	for spring in springs:
		if spring == Spring.OPERATIONAL:
			if len(current_group) != 0:
				posible_damaged_groups.append(Group(tuple(current_group)))
				current_group = []
			continue
	
		current_group.append(spring)
	if len(current_group) != 0: posible_damaged_groups.append(Group(tuple(current_group)))

	return posible_damaged_groups

def read_file(file: str, unfold_factor: int = 1) -> Iterable[SpringRow]:
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			springs, groups = line.split()
			springs = '?'.join(springs for _ in range(unfold_factor))
			groups  = ','.join(groups  for _ in range(unfold_factor))
			yield SpringRow(
				groups              = get_groups([Spring(c) for c in springs]),
				damaged_group_sizes = [int(n) for n in groups.split(',')]
			)


@lru_cache(maxsize=65536)
def gen_options(groups: Tuple[Group], sizes: Tuple[int, ...]):
	if len(sizes) == 0:
		forced_groups = [group for group in groups if group.must_exists]
		if len(forced_groups) == 0: return 1
		return 0

	if len(groups) == 0: return 0

	num_options = 0
	group_offset = 0
	spring_offset = 0
	size = sizes[0]
	while True:
		group = groups[group_offset]
		springs = group.springs[spring_offset:]
		if len(springs) < size:
			if len(groups[group_offset + 1:]) == 0: return num_options
			if group.must_exists: return num_options
			group_offset += 1
			spring_offset = 0
			continue

		if len(springs) == size or springs[size] == Spring.UNKNOWN:
			remaining_springs = springs[size + 1:]
			remaining_groups = tuple([Group(remaining_springs), *groups[group_offset + 1:]]) if len(remaining_springs) > 0 else groups[group_offset + 1:]
			remaining_sizes = sizes[1:]
			num_options += gen_options(remaining_groups, remaining_sizes)

		if springs[0] == Spring.DAMAGED: return num_options
		spring_offset += 1

def p1(args):
	rows = read_file(args.file)
	print(sum(gen_options(tuple(row.groups), tuple(row.damaged_group_sizes)) for row in rows))

def p2(args):
	rows = read_file(args.file, unfold_factor=5)
	print(sum(gen_options(tuple(row.groups), tuple(row.damaged_group_sizes)) for row in rows))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
