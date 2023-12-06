import logging
from typing import Generator, List
import re
from data_models import Map, Transformation, Range

parse_seeds_rgx = re.compile('[0-9]+')
def read_seeds(lines: Generator[str, None, None]) -> List[int]:
	return [int(seed) for seed in parse_seeds_rgx.findall(next(lines).split(':')[1])]


def seeds_as_ranges(seeds: List[int]) -> List[Range]:
	pairs_gen = (seeds[2*i:2*(i+1)] for i in range(len(seeds) // 2))
	return [Range(start, start + size) for start, size in pairs_gen]

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
	seeds, maps = read_file(args.file)
	map = Map.merge_maps(maps)

	sorted_transformations = sorted(map.transformations, key=lambda t: t.dst_range.start)
	for transform in sorted_transformations:
		for seed_range in seeds_as_ranges(seeds):
			_, union, _ = transform.src_range.merge(seed_range)
			if union is not None:
				print(union.start + transform.add_src2dst)
				return

	# KNOWN BUG: If there is no mapped seeds, the loop above will not return.
	# In that case, just print(min(seed_range.start for seed_range in seeds_as_ranges(seeds))

	# KNOWN BUG: If there is an unmapped seed closer that the closest mapped seed
	# We actually should get the closest mapped seed wrapping the loop above in a function, and returning instead of printing
	# Then compute the closest unmapped seed, and take the min between those values

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
