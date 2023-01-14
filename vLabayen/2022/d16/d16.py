#!/bin/python3
from domain import *
import logging

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	layout = parse_tunnels_layout(lines)
	distance_map = {valve: get_distances_from(valve, layout) for valve in layout.keys()}
	flow_rates = {valve: d['flow_rate'] for valve, d in layout.items() if d['flow_rate'] > 0}
	return distance_map, flow_rates

def p1(args):
	starting_valve = 'AA'
	max_time = 30
	distance_map, flow_rates = read_file(args.file)
	valves = set(sorted(flow_rates.keys()))

	max_pressure, path = get_max_pressure(starting_valve, max_time,
		distance_map=distance_map,
		flow_rates=flow_rates,
		valves=valves,
		compute_upper_limit=single_path_upper_limit
	)

	logging.info(f'Best path: {path}')
	print(max_pressure)

def p2(args):
	starting_valve = 'AA'
	max_time = 26
	distance_map, flow_rates = read_file(args.file)
	valves = set(sorted(flow_rates.keys()))

	max_pressure, path = get_max_pressure(starting_valve, max_time,
		distance_map=distance_map,
		flow_rates=flow_rates,
		valves=valves,
		compute_upper_limit=lambda *args: double_path_upper_limit(*args, starting_valve=starting_valve, maxTime=max_time)
	)

	available_valves = valves.difference(set(path))
	_, elephant_path = get_max_pressure(starting_valve, max_time,
		distance_map=distance_map,
		flow_rates=flow_rates,
		valves=available_valves,
		compute_upper_limit=single_path_upper_limit
	)

	logging.info(f'Best path: {path} - {elephant_path}')
	print(max_pressure)

if __name__ == '__main__':
	import argparse
	import time

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	parser.add_argument('-t', '--time', default=False, action='store_true')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose, format='%(message)s')

	start = time.perf_counter()
	# 1651: ['AA', 'DD', 'BB', 'JJ', 'HH', 'EE', 'CC']
	# p1(args)
	elapsed_p1 = time.perf_counter() - start

	start = time.perf_counter()
	# 1707: ['AA, 'JJ', 'BB', 'CC'], ['AA', 'DD', 'HH', 'EE']
	p2(args)
	elapsed_p2 = time.perf_counter() - start

	if args.time:
		print(f'Elapsed p1: {elapsed_p1}s')
		print(f'Elapsed p2: {elapsed_p2}s')