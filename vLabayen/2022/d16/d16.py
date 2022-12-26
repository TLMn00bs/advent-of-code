#!/bin/python3
from domain import *
import logging

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	return parse_tunnels_layout(lines)

def p1(args):
	t = 30
	current_position = 'AA'
	choices = list(reversed(['DD', 'BB', 'JJ', 'HH', 'EE', 'CC']))


	layout = read_file(args.file)
	distance_map = {valve: get_distances_from(valve, layout) for valve in layout.keys()}
	flow_rates = {valve: d['flow_rate'] for valve, d in layout.items()}
	remaining_valves = set(valve for valve, d in layout.items() if d['flow_rate'] > 0)

	flow_rate = 0
	released_pressure = 0
	while t > 0:
		print(f'== Minute {31 - t} ==')
		print(f'{remaining_valves=} -> {flow_rate=}')

		if len(remaining_valves) == 0:
			released_pressure += flow_rate
			t = t - 1
			continue

		scores = {valve: get_valve_score(
			current_position, valve, t,
			distance_map,
			flow_rates,
			remaining_valves
		) for valve in remaining_valves}
	
		best_valve, _ = max(scores.items(), key = lambda item: item[1])
		# best_valve = choices.pop()
		print(f'You move & open {best_valve}')

		time_inc = distance_map[current_position][best_valve] + 1
		released_pressure += flow_rate * time_inc

		t -= time_inc
		current_position = best_valve
		remaining_valves.difference_update([best_valve])
		flow_rate += flow_rates[best_valve]

	print(released_pressure)

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
