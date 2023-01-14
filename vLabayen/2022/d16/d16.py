#!/bin/python3
from domain import *
import logging
from collections import deque
from enum import Enum, auto

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

			if len(available_valves) == 1:
				break

			available_valves.remove(valve)
			upper_limit = released_pressure + get_remaining_pressure(valve, time, available_valves, distance_map, flow_rates)

			if upper_limit <= lower_limit:
				available_valves.add(valve)
				continue

			path.append({
				'valve': valve,
				'time': time,
				'released_pressure': released_pressure,
				'options': deque(available_valves)
			})

		prev = path.pop()
		available_valves.add(prev['valve'])

	print(lower_limit)

def p2_0(args):
	distance_map, flow_rates = read_file(args.file)

	max_time = 26
	valves = list(sorted(flow_rates.keys()))
	people = ('me', 'el')

	lower_limit = 0
	available_valves = set(valves)

	path = deque([{
		'valve': 'AA',
		'who': 'both',
		'released_pressure': 0,
		'options': deque((who, valve) for valve in valves for who in people)
	}])
	paths = {who: deque([{'valve': 'AA', 'time': max_time}]) for who in people}

	while len(path[0]['options']) > 0:
		while len(path[-1]['options']) > 0:
			# logging.debug(f"{' - '.join(':'.join((step['who'], step['valve'])) for step in path)} -> {set(':'.join(opt) for opt in path[-1]['options'])}")

			prev = path[-1]
			who, valve = prev['options'].popleft()
			whos_prev = paths[who][-1]

			time = whos_prev['time'] - distance_map[whos_prev['valve']][valve] - 1
			if time < 0:
				continue

			released_pressure = prev['released_pressure'] + (flow_rates[valve] * time)
			if released_pressure > lower_limit:
				lower_limit = released_pressure
				logging.info(f"{released_pressure}: {' - '.join(':'.join((step['who'], step['valve'])) for step in path)} - {who}:{valve}")

			if len(available_valves) == 1:
				break

			available_valves.remove(valve)
			states = [(valve, time) if w == who else (paths[w][-1]['valve'], paths[w][-1]['time']) for w in people]
			upper_limit = released_pressure + get_multipath_remaining_pressure(states, available_valves, distance_map, flow_rates)

			if upper_limit <= lower_limit:
				available_valves.add(valve)
				continue

			path.append({
				'valve': valve,
				'who': who,
				'released_pressure': released_pressure,
				'options': deque((who, valve) for valve in available_valves for who in people)
			})
			paths[who].append({'valve': valve, 'time': time})

		prev = path.pop()
		paths[prev['who']].pop()
		available_valves.add(prev['valve'])

	print(lower_limit)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose, format='%(message)s')

	p1(args)
	# p2_0(args)
