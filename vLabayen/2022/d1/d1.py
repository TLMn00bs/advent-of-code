#!/bin/python3
def process(file):
	with open(file, 'r') as f:
		lines = [l.strip() for l in f]

	elfs = []
	current_elf = []
	for line in lines:
		if line == "":
			elfs.append(sum(current_elf))
			current_elf = []
			continue

		current_elf.append(int(line))

	return elfs

def p1(args):
	elfs = process(args.file)
	print(max(elfs))

def p2(args):
	elfs = process(args.file)
	top_3_elfs = sorted(elfs)[-3:]
	print(sum(top_3_elfs))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
