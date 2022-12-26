#!/bin/python3
from domain import *

def read_file(file):
	with open(file) as f:
		lines = [line.strip() for line in f]
		blocks = split_commands_into_blocks(lines)

	tree = {}
	current_path = '/'
	for block in blocks:
		current_path = extract_block_path(block, start_path=current_path)
		ls_output = extract_block_output(block)
		parsed_output = [parse_output_line(line, current_path) for line in ls_output]
		tree[current_path] = parsed_output

	sizes: typing.Dict[str, int] = {}
	dir_paths_longer_first = sorted(tree.keys(), key=lambda path: len(path), reverse=True)
	for path in dir_paths_longer_first:
		total_size = 0

		for item in tree[path]:
			if isinstance(item, File): total_size += item.size
			else: total_size += sizes[item.path]

		sizes[path] = total_size

	return sizes

def p1(args):
	sizes = read_file(args.file)
	dirs_lower_than_100k = {path: size for path, size in sizes.items() if size < 100_000}
	print(sum(dirs_lower_than_100k.values()))

def p2(args):
	sizes = read_file(args.file)
	unused_space = 70_000_000 - sizes['/']
	required_to_free = 30_000_000 - unused_space

	dirs_larger_to_required = {path: size for path, size in sizes.items() if size >= required_to_free}
	print(min(dirs_larger_to_required.values()))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
