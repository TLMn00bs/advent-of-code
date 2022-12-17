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
	for _ in repeat(None, 20): run_round(monkeys)
	top_inspected_items = sorted([m.num_inspected_items for m in monkeys], reverse=True)[:2]
	print(reduce(lambda acc, num: acc * num, top_inspected_items, 1))

def p2(args):
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
