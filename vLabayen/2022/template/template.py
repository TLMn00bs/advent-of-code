#!/bin/python3
from domain import *

def read_file(file: str):
	with open(file, 'r') as f:
		pass

def p1(args):
	_ = read_file(args.file)

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
