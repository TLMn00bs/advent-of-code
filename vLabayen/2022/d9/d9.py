#!/bin/python3
from domain import *

def read_file(file):
	with open(file, 'r') as f:
		steps = [MotionStep.from_text(line.strip()) for line in f]

	return [step.direction for step in steps for _ in range(step.amount)]

def p1(args):
	steps = read_file(args.file)
	rope = Rope(2)

	tail_visited_positions = set()
	for direction in steps:
		rope.move(direction)
		tail_visited_positions.add(rope.knots[-1])

	print(len(tail_visited_positions))

def p2(args):
	steps = read_file(args.file)
	rope = Rope(10)

	tail_visited_positions = set()
	for direction in steps:
		rope.move(direction)
		tail_visited_positions.add(rope.knots[-1])

	print(len(tail_visited_positions))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
