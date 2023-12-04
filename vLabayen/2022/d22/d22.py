#!/bin/python3
import logging
from file_parser import read_file
from domain import Facing, apply_step, top_left_tile
from wrap import LinearWrapper, CubeWrapper

def p1(args):
	tiles, path = read_file(args.file)

	wrapper = LinearWrapper({tile.position: tile for tile in tiles})
	current_tile = top_left_tile(tiles)
	facing = Facing.RIGHT

	# print(current_tile.position, facing)
	for step in path.steps:
		current_tile, facing = apply_step(current_tile, facing, step, wrapper)
		# print(current_tile.position, facing)

	column, row = current_tile.position
	print((1000 * row) + (4 * column) + facing.value)
	

def p2(args):
	tiles, path = read_file(args.file)

	wrapper = CubeWrapper({tile.position: tile for tile in tiles})

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
