#!/bin/python3
from domain import *
import logging
from ndt.window_iterator import iter_window_non_overlap

def read_file(file: str) -> typing.List[Packet]:
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]

	packet_lines = [line for line in lines if line != '']
	packets = [Packet.from_text(line) for line in packet_lines]
	return packets

def p1(args):
	packets = read_file(args.file)
	packet_pairs = [(left, right) for left, right in iter_window_non_overlap(packets, n = 2)]

	index_sum = 0
	for idx, (left, right) in enumerate(packet_pairs):
		if in_order(left.data, right.data):
			index_sum += idx + 1

	print(index_sum)

def p2(args):
	packets = read_file(args.file)
	start_divider = Packet.from_text('[[2]]')
	end_divider   = Packet.from_text('[[6]]')

	packets.extend([start_divider, end_divider])
	ordered_packets = sorted(packets, key=sort_packets)

	start_divider_idx = ordered_packets.index(start_divider) + 1
	end_divider_idx   = ordered_packets.index(end_divider)   + 1
	print(start_divider_idx * end_divider_idx)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
