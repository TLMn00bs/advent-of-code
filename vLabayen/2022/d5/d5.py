#!/bin/python3
from domain import *

def read_file(file):
	with open(file, 'r') as f:
		lines = f.read()
	
	placement_lines, steps_lines = lines.split('\n\n')
	return (
		CratesPlacement.from_text_lines(placement_lines.split('\n')),
		[RearrangementStep.from_text(line) for line in steps_lines.strip().split('\n')]
	)

def p1(args):
	placement, steps = read_file(args.file)
	for step in steps: placement.apply_step_one_crate_at_a_time(step)
	print(''.join(placement.get_top_crates()))

def p2(args):
	placement, steps = read_file(args.file)
	for step in steps: placement.apply_step_multiple_crates_at_once(step)
	print(''.join(placement.get_top_crates()))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
