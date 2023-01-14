from typing import *
import logging
import re
from collections import deque

TunnelLayout = Dict[str, dict]

rgx = re.compile('Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)')
def parse_tunnels_layout(lines: List[str]) -> TunnelLayout:
	''' Parse the tunnels layout from its text definition '''
	layout: TunnelLayout = {}
	for line in lines:
		valve, flow_rate, connected_valves = rgx.match(line).groups()
		layout[valve] = {
			'flow_rate': int(flow_rate),
			'connected_nodes': set(connected_valves.split(', '))
		}

	return layout

def get_distances_from(src: str, layout: TunnelLayout) -> Dict[str, int]:
	''' Compute the minimal distances from src to every other destination '''
	distances = {
		**{dst: None for dst in layout.keys()},
		src: 0
	}

	updated_nodes = set(layout[src]['connected_nodes'])
	while len(updated_nodes) > 0:
		nodes_to_update = set()

		for node in updated_nodes:
			current_distance = distances[node]
			neighbours = layout[node]['connected_nodes']
			neighbour_distances = [distances[n] for n in neighbours]

			valid_paths = [d + 1 for d in neighbour_distances if d is not None]
			if len(valid_paths) == 0: continue

			best_path = min(valid_paths)
			if current_distance is None or best_path < current_distance:
				distances[node] = best_path
				nodes_to_update.update(neighbours)

		updated_nodes = nodes_to_update

	del distances[src]
	return distances

def get_remaining_pressure(starting_valve: str, remaining_time: int,
	remaining_valves: Iterable[str], distance_map: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]) -> int:

	max_time_open = lambda valve: max(0, remaining_time - distance_map[starting_valve][valve] - 1)
	return sum(flow_rates[valve] * max_time_open(valve) for valve in remaining_valves)

def single_path_upper_limit(released_pressure: int, next_valve: str, remaining_time: int,
	remaining_valves: Iterable[str],
	distance_map: Dict[str, Dict[str, int]],
	flow_rates: Dict[str, int]
	) -> Tuple[int, int]:
	
	upper_limit = released_pressure + get_remaining_pressure(next_valve, remaining_time, remaining_valves, distance_map, flow_rates)
	return released_pressure, upper_limit

def double_path_upper_limit(released_pressure: int, next_valve: str, remaining_time: int,
	remaining_valves: Iterable[str],
	distance_map: Dict[str, Dict[str, int]],
	flow_rates: Dict[str, int],
	starting_valve: str, maxTime: int
	) -> Tuple[int, int]:

	_, single_upper_limit = single_path_upper_limit(released_pressure, next_valve, remaining_time, remaining_valves, distance_map, flow_rates)
	second_path_max_pressure, _ = get_max_pressure(starting_valve, maxTime, distance_map, flow_rates, valves=remaining_valves, compute_upper_limit=single_path_upper_limit, log=False)
	return released_pressure + second_path_max_pressure, single_upper_limit + second_path_max_pressure

def path_cache(fnc):
	cache: Dict[FrozenSet[str], Tuple[int, Tuple[str]]] = {}

	def inner(*args, **kwargs) -> Tuple[int, Tuple[str]]:
		input_valves: Set[str] = kwargs['valves']
		for valves, (pressure, path) in cache.items():
			if not input_valves.issubset(valves):
				continue

			if not input_valves.issuperset(path):
				continue

			return pressure, path
		
		pressure, path = fnc(*args, **kwargs)
		cache[frozenset(input_valves)] = (pressure, path)
		return pressure, path

	return inner

@path_cache
def get_max_pressure(starting_valve: str, maxTime: int,
	distance_map: Dict[str, Dict[str, int]],
	flow_rates: Dict[str, int],
	valves: Set[str],
	compute_upper_limit: Callable[[int, str, int, FrozenSet[str], Dict[str, Dict[str, int]], Dict[str, int]], Tuple[int, int]],
	log: bool = True
	) -> Tuple[int, Tuple[str]]:
	
	max_released_pressure = 0
	best_path = []

	available_valves = set(valves)
	path = deque([{
		'valve': starting_valve,
		'time': maxTime,
		'released_pressure': 0,
		'options': deque(available_valves)
	}])

	while len(path) > 0:
		while len(path[-1]['options']) > 0:
			prev_step = path[-1]
			next_valve = prev_step['options'].popleft()

			time = prev_step['time'] - distance_map[prev_step['valve']][next_valve] - 1
			if time < 0:
				continue

			available_valves.remove(next_valve)
			released_pressure = prev_step['released_pressure'] + flow_rates[next_valve] * time
			max_pressure, pressure_limit = compute_upper_limit(released_pressure, next_valve, time, available_valves, distance_map, flow_rates)

			if max_pressure > max_released_pressure:
				max_released_pressure = max_pressure
				best_path = [step['valve'] for step in path] + [next_valve]
				if log: logging.debug(f"{max_released_pressure}: {' - '.join(step['valve'] for step in path)} - {next_valve}")

			if len(available_valves) == 0:
				available_valves.add(next_valve)
				break

			if pressure_limit <= max_released_pressure:
				available_valves.add(next_valve)
				continue

			path.append({
				'valve': next_valve,
				'time': time,
				'released_pressure': released_pressure,
				'options': deque(available_valves)
			})

		prev_step = path.pop()
		available_valves.add(prev_step['valve'])

	return max_released_pressure, tuple(best_path)


def get_released_pressure(time: int, path: List[str], distance_map: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]) -> int:
	released_pressure = 0
	current_valve = path[0]

	for valve in path[1:]:
		open_time = time - distance_map[current_valve][valve] - 1
		released_pressure += open_time * flow_rates[valve]

		current_valve = valve
		time = open_time

	return released_pressure

if __name__ == '__main__':
	import doctest
	import unittest

	logging.basicConfig(level=logging.DEBUG)

	class TestDomain(unittest.TestCase):
		layout = {
			'AA': {'flow_rate': 0 , 'connected_nodes': {'DD', 'BB', 'II'}},
			'BB': {'flow_rate': 13, 'connected_nodes': {'AA', 'CC'}},
			'CC': {'flow_rate': 2 , 'connected_nodes': {'DD', 'BB'}},
			'DD': {'flow_rate': 20, 'connected_nodes': {'AA', 'EE', 'CC'}},
			'EE': {'flow_rate': 3 , 'connected_nodes': {'DD', 'FF'}},
			'FF': {'flow_rate': 0 , 'connected_nodes': {'EE', 'GG'}},
			'GG': {'flow_rate': 0 , 'connected_nodes': {'HH', 'FF'}},
			'HH': {'flow_rate': 22, 'connected_nodes': {'GG'}},
			'II': {'flow_rate': 0 , 'connected_nodes': {'JJ', 'AA'}},
			'JJ': {'flow_rate': 21, 'connected_nodes': {'II'}}
		}
		distances_from_AA = {
			'BB': 1, 'CC': 2, 'DD': 1, 'EE': 2,
			'FF': 3, 'GG': 4, 'HH': 5, 'II': 1, 'JJ': 2
		}

		def test_parse_tunnels_layout(self):
			layout = parse_tunnels_layout([
				'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
				'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
				'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
				'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
				'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
				'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
				'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
				'Valve HH has flow rate=22; tunnel leads to valve GG',
				'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
				'Valve JJ has flow rate=21; tunnel leads to valve II',
			])
			self.assertDictEqual(layout, TestDomain.layout)

		def test_get_distances_from(self):
			distances = get_distances_from('AA', TestDomain.layout)
			self.assertDictEqual(distances, TestDomain.distances_from_AA)


	logging.info(f'Running doctests')
	doctest.testmod(optionflags=doctest.ELLIPSIS)

	logging.info(f'Running unittests')
	unittest.main()