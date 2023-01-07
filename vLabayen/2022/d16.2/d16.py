#!/bin/python3
from domain import *
import logging
from collections import deque

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	layout = parse_tunnels_layout(lines)
	distance_map = {valve: get_distances_from(valve, layout) for valve in layout.keys()}
	flow_rates = {valve: d['flow_rate'] for valve, d in layout.items() if d['flow_rate'] > 0}
	return distance_map, flow_rates

def p1(args):
	distance_map, flow_rates = read_file(args.file)

	valves = list(sorted(flow_rates.keys()))
	
	lower_limit = 0
	available_valves = set(valves)
	path = deque([{
		'valve': 'AA',
		'time': 30,
		'released_pressure': 0,
		'upper_limit': get_remaining_pressure('AA', 30, valves, distance_map, flow_rates),
		'options': deque(valves)
	}])

	while len(path[0]['options']) > 0:
		while len(path[-1]['options']) > 0:
			logging.debug(f"{' - '.join(step['valve'] for step in path)} -> {set(path[-1]['options'])}")

			prev = path[-1]
			valve = prev['options'].popleft()

			time = prev['time'] - distance_map[prev['valve']][valve] - 1
			if time < 0:
				continue

			released_pressure = prev['released_pressure'] + (flow_rates[valve] * time)
			if released_pressure > lower_limit:
				lower_limit = released_pressure
				logging.info(f"{released_pressure}: {' - '.join(step['valve'] for step in path)} - {valve}")

			available_valves.remove(valve)
			if len(available_valves) == 0:
				available_valves.add(valve)
				break

			upper_limit = released_pressure + get_remaining_pressure(valve, time, available_valves, distance_map, flow_rates)

			if upper_limit < lower_limit:
				available_valves.add(valve)
				continue

			path.append({
				'valve': valve,
				'time': time,
				'released_pressure': released_pressure,
				'upper_limit': upper_limit,
				'options': deque(available_valves)
			})

		prev = path.pop()
		available_valves.add(prev['valve'])

	print(lower_limit)

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose, format='%(message)s')

	# p0(args)
	p1(args)
	# p2(args)
