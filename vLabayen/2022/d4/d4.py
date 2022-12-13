#!/bin/python3
from domain import *
import typing

def read_file(file) -> typing.Iterator[PairedAssigments]:
	with open(file, 'r') as f:
		for line in f:
			yield PairedAssigments.from_text(line.strip())

def p1(args):
	paired_assigments = read_file(args.file)
	print(sum(1 for pair in paired_assigments if pair.fully_overlap()))

def p2(args):
	paired_assigments = read_file(args.file)
	print(sum(1 for pair in paired_assigments if pair.partial_overlap()))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
