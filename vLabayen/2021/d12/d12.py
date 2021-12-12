#!/bin/python3
from collections import defaultdict
import re

small_rgx, big_rgx = re.compile('[a-z]+'), re.compile('[A-Z]+')
is_small = lambda cave: bool(small_rgx.match(cave))
is_big = lambda cave: bool(big_rgx.match(cave))

def bruteforce_path_p1(current_cave, caves, connections, small_caves, big_caves, visited = None):
	if visited is None: visited = {cave: 0 for cave in caves}
	visited[current_cave] += 1

	if current_cave == 'end': return current_cave
	adjacent_caves = connections[current_cave]
	valid_caves = [cave for cave in adjacent_caves if not (cave in small_caves and visited[cave] >= 1)]
	if len(valid_caves) == 0: return current_cave

	paths = [bruteforce_path_p1(cave, caves, connections, small_caves, big_caves, {c: v for c,v in visited.items()}) for cave in valid_caves]
	return [f'{current_cave},{p}' for p in expand_arr(paths)]

def bruteforce_path_p2(current_cave, caves, connections, small_caves, big_caves, visited = None):
	if visited is None: visited = {cave: 0 for cave in caves}
	visited[current_cave] += 1
	any_small_visited_twice = any(cave in small_caves and visited[cave] >= 2 for cave in caves)

	if current_cave == 'end': return current_cave
	adjacent_caves = connections[current_cave]
	valid_caves = [cave for cave in adjacent_caves if cave in big_caves or (visited[cave] == 0 or (visited[cave] == 1 and not any_small_visited_twice))]
	if len(valid_caves) == 0: return current_cave

	paths = [bruteforce_path_p2(cave, caves, connections, small_caves, big_caves, {c: v for c,v in visited.items()}) for cave in valid_caves]
	return [f'{current_cave},{p}' for p in expand_arr(paths)]


def expand_arr(arr):
	for item in arr:
		if isinstance(item, str): yield item
		else:
			for subitem in expand_arr(item): yield subitem

def p1(args):
	caves = set()
	connections = defaultdict(lambda: [])

	with open(args.file, 'r') as f:
		for line in f:
			cave1, cave2 = line.strip().split('-')
			caves.update([cave1, cave2])

			# We may not return to start
			# We may not continue from end
			if cave2 != "start" and cave1 != "end": connections[cave1].append(cave2)
			if cave1 != "start" and cave2 != "end": connections[cave2].append(cave1)

	small_caves = {cave for cave in caves if is_small(cave)}
	big_caves = {cave for cave in caves if is_big(cave)}
	paths = bruteforce_path_p1("start", caves, connections, small_caves, big_caves)
	valid_paths = [p for p in paths if p.endswith('end')]
	print(len(valid_paths))

def p2(args):
	caves = set()
	connections = defaultdict(lambda: [])

	with open(args.file, 'r') as f:
		for line in f:
			cave1, cave2 = line.strip().split('-')
			caves.update([cave1, cave2])

			# We may not return to start
			# We may not continue from end
			if cave2 != "start" and cave1 != "end": connections[cave1].append(cave2)
			if cave1 != "start" and cave2 != "end": connections[cave2].append(cave1)

	small_caves = {cave for cave in caves if is_small(cave)}
	big_caves = {cave for cave in caves if is_big(cave)}
	paths = bruteforce_path_p2("start", caves, connections, small_caves, big_caves)
	valid_paths = [p for p in paths if p.endswith('end')]
	print(len(valid_paths))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
