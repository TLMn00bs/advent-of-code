import logging
from typing import Generator, List
import re
from data_models import Map, Transformation, Range


parse_seeds_rgx = re.compile('[0-9]+')
def read_seeds(lines: Generator[str, None, None]) -> List[int]:
	return [int(seed) for seed in parse_seeds_rgx.findall(next(lines).split(':')[1])]

parse_range_rgx = re.compile('([0-9]+) ([0-9]+) ([0-9]+)')
def read_map(lines: Generator[str, None, None]) -> Map:
	next(lines)

	ranges = []
	current_range = next(lines)
	while current_range != '':
		dst_start, src_start, range_len = (int(n) for n in parse_range_rgx.match(current_range).groups())		# type: ignore
		ranges.append(Transformation(
			src_range = Range(src_start, src_start + range_len),
			dst_range = Range(dst_start, dst_start + range_len),
		))

		try: current_range = next(lines)
		except StopIteration: break

	return Map(ranges)

def read_file(file: str):
	with open(file, 'r') as f:
		lines = (l.strip() for l in f)
		seeds = read_seeds(lines)

		next(lines)
		maps = [read_map(lines) for _ in range(7)]

	return seeds, maps

def p1(args):
	seeds, maps = read_file(args.file)
	map = Map.merge_maps(maps)

	print(min(map.transform(seed) for seed in seeds))
	

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
