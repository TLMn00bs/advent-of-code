#!/bin/python3
from domain import *
import logging
from itertools import repeat
from functools import reduce

def read_file(file: str):
	with open(file, 'r') as f:
		content = f.read().strip()
	
	monkeys_lines = content.split('\n\n')
	return [Monkey.from_text(lines.split('\n')) for lines in monkeys_lines]

def p1(args):
	monkeys = read_file(args.file)
	for _ in repeat(None, 20): run_round(monkeys, lambda worry_level: worry_level // 3)
	top_inspected_items = sorted([m.num_inspected_items for m in monkeys], reverse=True)[:2]
	print(reduce(lambda acc, num: acc * num, top_inspected_items, 1))

def p2(args):
	monkeys = read_file(args.file)

	# To keep numbers in a asumible size, use a relief action that applies a circular arithmetic
	# using the mcm the divisible_by property of every monkey.
	# Since all seems to be primes, and there is no real requirement to use the real mcm,
	# just multiply all together to get a common multiple of all divisors.
	# Nevertheless, we can easyly remove duplicate factors.
	divisors = set(monkey.divisible_by for monkey in monkeys)
	mcm = reduce(lambda acc, divisor: acc * divisor, divisors, 1)

	for _ in repeat(None, 10_000): run_round(monkeys, lambda worry_level: worry_level % mcm)
	top_inspected_items = sorted([m.num_inspected_items for m in monkeys], reverse=True)[:2]
	print(reduce(lambda acc, num: acc * num, top_inspected_items, 1))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
