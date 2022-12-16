#!/bin/python3
from domain import *

def read_file(file):
	pass

def p1(args):
	pass

def p2(args):
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
