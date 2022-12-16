#!/bin/python3
from domain import *
from ndt.window_iterator import iter_window_non_overlap

def read_file(file):
	with open(args.file, 'r') as f:
		rucksacks = [line.strip() for line in f]

	return rucksacks

def p1(args):
	rucksacks = read_file(args.file)
	rucksacks_compartments = [get_rucksack_compartments(rucksack) for rucksack in rucksacks]
	shared_items = [get_shared_item(*compartments) for compartments in rucksacks_compartments]
	items_priority = [get_item_priority(item) for item in shared_items]
	print(sum(items_priority))

def p2(args):
	rucksacks = read_file(args.file)
	groups = list(iter_window_non_overlap(rucksacks, 3))
	shared_items = [get_shared_item(*group) for group in groups]
	items_priority = [get_item_priority(item) for item in shared_items]
	print(sum(items_priority))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
