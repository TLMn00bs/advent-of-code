#!/bin/python3
from functools import lru_cache

def p1(args):
	with open(args.file, 'r') as f: hpositions = [int(h) for h in f.readline().strip().split(',')]
	min_h, max_h = min(hpositions), max(hpositions)
	best_fuel = min(sum(abs(hp - h) for hp in hpositions) for h in range(min_h, max_h + 1))
	print(best_fuel)

def fuel_usage(start, end):
	if start > end: start, end = end, start
	return fuel_cost(end - start)

@lru_cache(maxsize=500000)
def fuel_cost(diff): return sum(range(1, diff + 1))

def p2(args):
	with open(args.file, 'r') as f: hpositions = [int(h) for h in f.readline().strip().split(',')]
	min_h, max_h = min(hpositions), max(hpositions)
	best_fuel = min(sum(fuel_usage(h, hp) for hp in hpositions) for h in range(min_h, max_h + 1))
	print(best_fuel)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
