#!/bin/python3
from domain import *
import logging

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	return parse_sensors(lines)

def get_conf(p: str) -> int:
	test_target_row, test_max_coord = 10, 20
	prod_target_row, prod_max_coord = 2000000, 4000000

	env = 'test' if args.file == 'example.txt' else 'prod'
	return {
		'test': {
			'p1': test_target_row,
			'p2': test_max_coord
		},
		'prod': {
			'p1': prod_target_row,
			'p2': prod_max_coord
		}
	}[env][p]

def p1(args):
	target_row = get_conf('p1')
	interval = Interval([])

	sensors = read_file(args.file)
	sensors_in_reach = [sensor for sensor in sensors if can_provide_info(sensor, target_row)]

	for sensor in sensors_in_reach:
		start_x, _ = first_position_in_row(sensor, target_row)
		end_x  , _ = last_position_in_row(sensor, target_row)
		interval = interval.add((start_x, end_x))

	for (sensor_x, sensor_y), (beacon_x, beacon_y), d in sensors_in_reach:
		if sensor_y == target_row:
			interval = interval.add((sensor_x, sensor_x))

		if beacon_y == target_row:
			interval = interval.subtract((beacon_x, beacon_x))

	print(len(interval))

import time
def p2(args):
	max_coord = get_conf('p2')

	sensors = read_file(args.file)
	rows_in_reach = {sensor: reached_rows(sensor) for sensor in sensors}

	for target_row in range(max_coord + 1):
		interval: Interval = Interval([])

		sensors_in_reach = [sensor for sensor, rows in rows_in_reach.items() if target_row in rows]
		for sensor in sensors_in_reach:
			start_x, _ = first_position_in_row(sensor, target_row)
			end_x  , _ = last_position_in_row(sensor, target_row)
			interval = interval.add((start_x, end_x))

		for (sensor_x, sensor_y), (beacon_x, beacon_y), d in sensors_in_reach:
			if sensor_y == target_row:
				interval = interval.add((sensor_x, sensor_x))

			if beacon_y == target_row:
				interval = interval.add((beacon_x, beacon_x))

		if interval.min() < 0:
			interval = interval.subtract((interval.min(), -1))

		if interval.max() > max_coord:
			interval = interval.subtract((max_coord + 1, interval.max()))

		if len(interval) == max_coord:
			beacon_x = interval.ranges[0][1] + 1
			print(4_000_000 * beacon_x + target_row)
			break

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
