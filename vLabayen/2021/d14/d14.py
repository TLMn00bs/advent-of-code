#!/bin/python3
import re
import math
from collections import Counter
#from itertools import permutations, product
from common.window_iterator import iter_window

def apply_rules_p1(template, rules):
	num_pairs = len(template) - 1
	pairs = (''.join(w) for w in iter_window(template))
	inserted_pairs = (rules[pair] for pair in pairs)
	trimmed_pairs = (pair[:-1] if (i != num_pairs - 1) else pair for i,pair in enumerate(inserted_pairs))
	return ''.join(trimmed_pairs)

def p1(args):
	with open(args.file, 'r') as f:
		template = f.readline().strip()
		f.readline()
		rules = {pair: f'{pair[0]}{insert}{pair[1]}' for pair, insert in (line.strip().split(' -> ') for line in f)}

	for i in range(10): template = apply_rules_p1(template, rules)
	c = sorted((v for k,v in Counter(template).most_common()), reverse=True)
	most, least = c[0], c[-1]
	print(most - least)


def p2(args):
	with open(args.file, 'r') as f:
		template = f.readline().strip()
		f.readline()
		rules = {pair: {'new_pairs': (f'{pair[0]}{insert}', f'{insert}{pair[1]}'), 'incr': insert} for pair, insert in (line.strip().split(' -> ') for line in f)}

	counter = Counter(template)
	status = {pair : 0 for pair in rules.keys()}
	for pair in iter_window(template): status[''.join(pair)] += 1

	for i in range(40):
		# Copy to avoid modify during loop. As we are going to modify the num of apearances that are also used for increment/decrement
		current_status = [(existing_pair, num_apearances) for existing_pair, num_apearances in status.items()]
		for existing_pair, num_apearances in current_status:
			if num_apearances == 0: continue
			r = rules[existing_pair]

			# Update status
			status[existing_pair] -= num_apearances
			for new_pair in r['new_pairs']: status[new_pair] += num_apearances

			# Update counter
			counter.update({r['incr']: num_apearances})

	c = sorted((v for k,v in counter.most_common()), reverse=True)
	most, least = c[0], c[-1]
	print(most - least)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
