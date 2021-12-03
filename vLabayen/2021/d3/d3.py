#!/bin/python3
from collections import Counter, defaultdict
from itertools import count

def p1(args):
	bit_counter = defaultdict(lambda: Counter())

	with open(args.file, 'r') as f:
		for bin in (line.strip() for line in f):
			for i,bit in enumerate(bin): bit_counter[i].update([bit])

	gamma = ''.join([c.most_common()[0][0] for bit, c in bit_counter.items()])
	epsilon = ''.join([c.most_common()[-1][0] for bit, c in bit_counter.items()])

	print(f'{gamma=}: {int(gamma, 2)}, {epsilon=}: {int(epsilon, 2)} ==> {int(gamma, 2) * int(epsilon, 2)}')

def p2(args):
	bit_counter = defaultdict(lambda: Counter())
	report = []

	with open(args.file, 'r') as f:
		for bin in (line.strip() for line in f):
			for i, bit in enumerate(bin): bit_counter[i].update([bit])
			report.append(bin)

	oxygen_opts = [bin for bin in report]
	oxygen_counter = bit_counter
	for i in count():
		mcb = '1' if oxygen_counter[i]['1'] >= oxygen_counter[i]['0'] else '0'
		oxygen_opts = [bin for bin in oxygen_opts if bin[i] == mcb]
		if len(oxygen_opts) <= 1: break
		oxygen_counter = {i: Counter([bin[i] for bin in oxygen_opts]) for i in bit_counter}

	co2_opts = [bin for bin in report]
	co2_counter = bit_counter
	for i in count():
		lcb = '0' if co2_counter[i]['0'] <= co2_counter[i]['1'] else '1'
		co2_opts = [bin for bin in co2_opts if bin[i] == lcb]
		if len(co2_opts) <= 1: break
		co2_counter = {i: Counter([bin[i] for bin in co2_opts]) for i in bit_counter}

	oxygen = ''.join(oxygen_opts)
	co2 = ''.join(co2_opts)
	print(f'{oxygen=}: {int(oxygen, 2)}, {co2=}: {int(co2, 2)} ==> {int(oxygen, 2) * int(co2, 2)}')

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

#	p1(args)
	p2(args)
