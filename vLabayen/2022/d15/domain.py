import typing
import logging
import re
from dataclasses import dataclass
from interval import Interval
from enum import Enum

Position = typing.Tuple[int, int]
Sensor = typing.Tuple[Position, Position, int]

def mh_distance(a: Position, b: Position) -> int:
	''' Compute the manhattan distance between two points
	
	>>> mh_distance((0, 10), (10, 10))
	10
	>>> mh_distance((0, 5), (10, 10))
	15
	>>> mh_distance((10, 10), (5, 0))
	15
	'''
	a_x, a_y = a
	b_x, b_y = b
	return abs(a_x - b_x) + abs(a_y - b_y)

rgx = re.compile('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)')
def parse_sensors(lines: typing.List[str]) -> typing.List[Sensor]:
	''' Parse a list of sensors from their reports

	>>> parse_sensors([
	... 	'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
	...		'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
	...		'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
	...		'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
	...		'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
	...		'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
	...		'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
	...		'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
	...		'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
	...		'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
	...		'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
	...		'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
	...		'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
	...		'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
	... ])
	[((2, 18), (-2, 15), 7), ((9, 16), (10, 16), 1), ((13, 2), (15, 3), 3), ((12, 14), (10, 16), 4), ((10, 20), (10, 16), 4), ((14, 17), (10, 16), 5), ((8, 7), (2, 10), 9), ((2, 0), (2, 10), 10), ((0, 11), (2, 10), 3), ((20, 14), (25, 17), 8), ((17, 20), (21, 22), 6), ((16, 7), (15, 3), 5), ((14, 3), (15, 3), 1), ((20, 1), (15, 3), 7)]
	'''
	sensors: typing.List[Sensor] = []

	for line in lines:
		sensor_x, sensor_y, beacon_x, beacon_y = rgx.match(line).groups()
		sensor_position = int(sensor_x), int(sensor_y)
		beacon_position = int(beacon_x), int(beacon_y)
		d = mh_distance(sensor_position, beacon_position)
		sensors.append((sensor_position, beacon_position, d))

	return sensors



def can_provide_info(sensor: Sensor, row: int) -> bool:
	''' Check if sensor can provide any info about the given row

	>>> can_provide_info(((2, 18), (-2, 15), 7), 10)
	False
	>>> can_provide_info(((8, 7), (2, 10), 9), 10)
	True
	>>> can_provide_info(((20, 1), (15, 3), 7), 10)
	False
	>>> can_provide_info(((17, 20), (21, 22), 6), 10)
	False
	>>> can_provide_info(((0, 11), (2, 10), 3), 10)
	True
	'''
	(_, sensor_y), _, d = sensor
	return abs(row - sensor_y) <= d

def can_reach(sensor: Sensor, position: Position) -> bool:
	''' Check if a sensor can reach a position
	
	>>> can_reach(((8, 7), (2, 10), 9), (1, 10))
	False
	>>> can_reach(((8, 7), (2, 10), 9), (1, 9))
	True
	>>> can_reach(((8, 7), (2, 10), 9), (2, 10))
	True
	>>> can_reach(((8, 7), (2, 10), 9), (2, 11))
	False
	'''
	(sensor_x, sensor_y), _, d = sensor
	return d >= mh_distance((sensor_x, sensor_y), position)

def first_position_in_row(sensor: Sensor, row: int) -> Position:
	''' Return the first position of the row that the given sensor can reach
	
	>>> first_position_in_row(((8, 7), (2, 10), 9), 10)
	(2, 10)
	'''
	(sensor_x, sensor_y), _, d = sensor
	x_reach = d - abs(row - sensor_y)
	return (sensor_x - x_reach, row)

def last_position_in_row(sensor: Sensor, row: int) -> Position:
	''' Return the last position of the row that the given sensor can reach
	
	>>> last_position_in_row(((8, 7), (2, 10), 9), 10)
	(14, 10)
	'''
	(sensor_x, sensor_y), _, d = sensor
	x_reach = d - abs(row - sensor_y)
	return (sensor_x + x_reach, row)

def reached_rows(sensor: Sensor) -> Interval:
	''''''
	(_, sensor_y), _, d = sensor
	return Interval([(sensor_y - d, sensor_y + d)])

class Location(Enum):
	SENSOR = 'S'
	BEACON = 'B'
	BLOCKED = '#'
	UNKNOWN = '.'

def get_location(sensors: typing.List[Sensor], position) -> Location:
	for sensor, beacon, d in sensors:
		if sensor == position: return Location.SENSOR
		if beacon == position: return Location.BEACON
	
	reached = any(can_reach(sensor, position) for sensor in sensors)
	if reached: return Location.BLOCKED
	return Location.UNKNOWN

if __name__ == '__main__':
	import doctest
	logging.basicConfig(level=logging.DEBUG)
	doctest.testmod(optionflags=doctest.ELLIPSIS)