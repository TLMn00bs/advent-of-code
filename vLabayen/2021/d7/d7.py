#!/bin/python3
from numpy import median

def p1(args):
	with open(args.file, 'r') as f: hpositions = [int(h) for h in f.readline().strip().split(',')]
	min_h, max_h = min(hpositions), max(hpositions)

	best_fuel = sum(abs(hp - min_h) for hp in hpositions)
	for h in range(min_h + 1, max_h + 1):
		fuel = sum(abs(hp - h) for hp in hpositions)
		if fuel < best_fuel: best_fuel = fuel

	print(best_fuel)

def fuel_usage(start, end):
	if start > end: start, end = end, start
	return sum(range(1, end - start + 1))

def p2(args):
	with open(args.file, 'r') as f: hpositions = [int(h) for h in f.readline().strip().split(',')]
	min_h, max_h = min(hpositions), max(hpositions)
	best_fuel = min(sum(fuel_usage(h, hp) for hp in hpositions) for h in range(min_h, max_h))
	print(best_fuel)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
