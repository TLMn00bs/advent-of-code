#!/bin/python3
from collections import Counter

def p1(args):
	with open(args.file, 'r') as f: fishes = [int(n) for n in f.readline().strip().split(',')]

	for day in range(80):
		append_count = 0
		for i,fish_counter in enumerate(fishes):
			if fish_counter == 0:
				fishes[i] = 6
				append_count += 1
				continue

			fishes[i] -= 1

		for _ in range(append_count): fishes.append(8)

	print(len(fishes))

def p2(args):
	with open(args.file, 'r') as f:
		fishes = [int(n) for n in f.readline().strip().split(',')]
		fishes_counter = Counter(fishes)
		fishes = [fishes_counter[i] for i in range(9)]

	for day in range(256):
		fishes_ceros = fishes[0]
		fishes = fishes[1:]
		fishes[6] += fishes_ceros
		fishes.append(fishes_ceros)

	print(sum(fishes))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
