#!/bin/python3
from domain import *

def read_file(file):
	with open(file, 'r') as f:
		return f.read().strip()

def p1(args):
	buffer = read_file(args.file)
	print(find_marker(buffer, window_size=4))

def p2(args):
	buffer = read_file(args.file)
	print(find_marker(buffer, window_size=14))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
