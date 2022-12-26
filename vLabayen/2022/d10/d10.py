#!/bin/python3
from domain import *
from ndt.window_iterator import iter_window
from itertools import repeat

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	return Program.from_lines(lines)

def get_incremental_cycles_to_complete(target_cycles):
	target_completed_cycles = [cycles - 1 for cycles in target_cycles]
	first_step = target_completed_cycles[0]
	next_steps = [target - prev for prev, target in iter_window(target_completed_cycles, n = 2)]
	return [first_step] + next_steps

def p1(args):
	program = read_file(args.file)
	target_cycles = [20, 60, 100, 140, 180, 220]
	run_cycles_by_step = get_incremental_cycles_to_complete(target_cycles)

	signal_strenghts = []
	for target_cycle, run_cycles in zip(target_cycles, run_cycles_by_step):
		program.exec(run_cycles)
		signal_strenghts.append(target_cycle * program.register.X)

	print(sum(signal_strenghts))

def p2(args):
	program = read_file(args.file)
	for _ in range(6):
		for x in range(40):
			sprite_position = program.register.X
			sprite_in_drawing_px = abs(sprite_position - x) <= 1
			print('#' if sprite_in_drawing_px else '.', end='')
			program.exec(1)

		print()

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
