#!/bin/python3
from itertools import count
from numpy import prod

GROUP_SIZE = 5

def parse_packet(p):
	version = int(p[:3], 2)
	id = int(p[3:6], 2)
	payload = p[6:]

	if id == 4:
		literal, remaining = parse_literal_value(payload)
		return {'version': version, 'id': id, 'payload': literal}, remaining

	else:
		ltype, l, subpackets, remaining = parse_operator(payload)
		return {'version': version, 'id': id, 'length_type_id': ltype, 'length': l, 'payload': subpackets}, remaining

def parse_literal_value(payload):
	groups = []
	for i in count():
		group = payload[GROUP_SIZE*i:GROUP_SIZE*(i+1)]

		starting_bit = group[0]
		groups.append(group[1:])

		if starting_bit == '0':
			remaining = payload[GROUP_SIZE*(i+1):]
			return int(''.join(groups), 2), remaining

def parse_operator(payload):
	length_type_id = payload[0]

	if length_type_id == '0':
		total_length = int(payload[1:1 + 15], 2)
		subpackets_payload = payload[1 + 15:1 + 15 + total_length]
		subpackets, _ = parse_subpackets(subpackets_payload)
		return length_type_id, total_length, subpackets, payload[1 + 15 + total_length:]

	if length_type_id == '1':
		num_packets = int(payload[1:1 + 11], 2)
		payload = payload[1 + 11:]
		subpackets, remaining = parse_subpackets(payload, num_packets)
		return length_type_id, num_packets, subpackets, remaining

def parse_subpackets(payload, num_packets = None):
	packets = []
	for i in count():
		packet, payload = parse_packet(payload)
		packets.append(packet)

		# If we run out of payload return
		if len(payload) == 0: return packets, payload
		# If we reach the number of expected packets return. If num_packets == None, this will always be false
		if i + 1 == num_packets: return packets, payload

def iter_packets(p):
	yield p
	if isinstance(p['payload'], list):
		for subp in p['payload']:
			for _p in iter_packets(subp): yield _p

def p1(args):
	with open(args.file, 'r') as f: hex_packet = f.readline().strip()
	bin_packet = bin(int(hex_packet, 16))[2:].zfill(len(hex_packet) * 4)

	p, _ = parse_packet(bin_packet)
	print(sum(_p['version'] for _p in iter_packets(p)))

id2op = lambda id: {
	0: sum,
	1: prod,
	2: min,
	3: max,
	5: lambda arr: 1 if arr[0] > arr[1] else 0,
	6: lambda arr: 1 if arr[0] < arr[1] else 0,
	7: lambda arr: 1 if arr[0] == arr[1] else 0
}[id]

def packet_value(p):
	if not isinstance(p['payload'], list): return p['payload']
	op = id2op(p['id'])
	return op([packet_value(_p) for _p in p['payload']])

def p2(args):
	with open(args.file, 'r') as f: hex_packet = f.readline().strip()
	bin_packet = bin(int(hex_packet, 16))[2:].zfill(len(hex_packet) * 4)

	p, _ = parse_packet(bin_packet)
	print(packet_value(p))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
