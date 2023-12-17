import logging
from typing import List, Iterable, Tuple
from enum import Enum
from attrs import define, field

class Spring(Enum):
	OPERATIONAL = '.'
	DAMAGED     = '#'
	UNKNOWN     = '?'

	def __repr__(self): return self.name

@define
class SpringRow:
	springs: List[Spring]
	damaged_group_sizes: List[int]

@define
class Group:
	springs: List[Spring]
	must_exists: bool = field(init=False)

	def __attrs_post_init__(self):
		self.must_exists = any(spring == Spring.DAMAGED for spring in self.springs)

	def __len__(self) -> int: return len(self.springs)
	def __repr__(self) -> str: return ''.join(s.value for s in self.springs)

def get_groups(springs: List[Spring]) -> List[Group]:
	posible_damaged_groups: List[Group] = []
	current_group: List[Spring] = []
	for spring in springs:
		if spring == Spring.OPERATIONAL:
			if len(current_group) != 0:
				posible_damaged_groups.append(Group(current_group))
				current_group = []
			continue
	
		current_group.append(spring)
	if len(current_group) != 0: posible_damaged_groups.append(Group(current_group))

	return posible_damaged_groups

def can_fit(group: Group, group_sizes: List[int]):
	min_total_size = lambda sizes: sum(sizes) + len(sizes) - 1
	if len(group) < min_total_size(group_sizes): return False

	offset = 0
	for i, size in enumerate(group_sizes):
		while True:
			remaining_springs = group.springs[offset:]
			if len(remaining_springs) < min_total_size(group_sizes[i:]):
				return False

			if len(remaining_springs) == size:
				return len(group_sizes) - 1 == i

			next_spring = remaining_springs[size]

			if next_spring == Spring.UNKNOWN:
				offset += size + 1
				break

			if next_spring == Spring.DAMAGED:
				offset += 1
				continue

	return True

def match_groups(groups: List[Group], group_sizes: List[int]) -> Iterable[Iterable[Tuple[Group, List[int]]]]:
	# Exact matches
	if len(groups) == 1:
		yield [(groups[0], group_sizes)]
		return

	forced_groups = [group for group in groups if group.must_exists]
	if len(forced_groups) == len(group_sizes):
		yield ((group, [size]) for group, size in zip(forced_groups, group_sizes))
		return

	# Ignore groups
	if group_sizes[0] > len(groups[0]):
		for combination in match_groups(groups[1:], group_sizes): yield combination
		return

	if group_sizes[-1] > len(groups[-1]):
		for combination in match_groups(groups[:-1], group_sizes): yield combination
		return

	min_size = min(group_sizes)
	big_enough_groups = [group for group in groups if len(group) >= min_size]
	if len(big_enough_groups) != len(groups):
		for combination in match_groups(big_enough_groups, group_sizes): yield combination
		return

	# Forced unique matches
	if groups[0].must_exists and not can_fit(groups[0], group_sizes[:2]):
		for combination in match_groups(groups[1:], group_sizes[1:]): yield [(groups[0], group_sizes[0]), *list(combination)]
		return

	if groups[-1].must_exists and not can_fit(groups[-1], group_sizes[-2:]):
		for combination in match_groups(groups[:-1], group_sizes[:-1]): yield [*list(combination), (groups[-1], group_sizes[-1])]
		return


	# No more matching can be done without looking at whole arrangement
	# for g_idx, group in enumerate(groups):
	# 	for s_idx, size in enumerate(group_sizes):
	# 		left_g, current_g, right_g = groups[:g_idx]
	# 		if can_fit


	# yield ()
	print(*[group for group in groups], group_sizes)


def count_arrangements(row: SpringRow) -> int:
	posible_damaged_groups = get_groups(row.springs)
	for combination in match_groups(posible_damaged_groups, row.damaged_group_sizes):
		for group, consecutive_damaged_springs in combination:
			pass
			# print(group, consecutive_damaged_springs)

	# list(match_groups(posible_damaged_groups, row.damaged_group_sizes))
	# print([len(g.springs) for g in posible_damaged_groups], row.damaged_group_sizes)

def read_file(file: str) -> Iterable[SpringRow]:
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			springs, groups = line.split()
			yield SpringRow(
				springs             = [Spring(c) for c in springs],
				damaged_group_sizes = [int(n) for n in groups.split(',')]
			)

def p1(args):
	rows = read_file(args.file)
	for row in rows: count_arrangements(row)

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
