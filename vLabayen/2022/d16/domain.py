import typing
from typing import *
import logging
import re
from ndt.window_iterator import iter_window

TunnelLayout = typing.Dict[str, dict]

rgx = re.compile('Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)')
def parse_tunnels_layout(lines: typing.List[str]) -> TunnelLayout:
	''' Parse the tunnels layout from its text definition '''
	layout: TunnelLayout = {}
	for line in lines:
		valve, flow_rate, connected_valves = rgx.match(line).groups()
		layout[valve] = {
			'flow_rate': int(flow_rate),
			'connected_nodes': set(connected_valves.split(', '))
		}

	return layout

def get_distances_from(src: str, layout: TunnelLayout) -> typing.Dict[str, int]:
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

def get_upper_limit(path: Deque[dict], distance_map: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]) -> int:
	last_valve = path[-1]['valve']
	released_pressure = path[-1]['released_pressure']
	remaining_time = path[-1]['time']

	open_valves = set(step['valve'] for step in path)
	remaining_valves = (valve for valve in flow_rates.keys() if valve not in open_valves)
	remaining_pressure = sum(flow_rates[valve] * (remaining_time - distance_map[last_valve][valve] - 1) for valve in remaining_valves)

	return released_pressure + remaining_pressure

def get_remaining_pressure(starting_valve: str, remaining_time: int,
	remaining_valves: Iterable[str], distance_map: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]) -> int:

	max_time_open = lambda valve: max(0, remaining_time - distance_map[starting_valve][valve] - 1)
	return sum(flow_rates[valve] * max_time_open(valve) for valve in remaining_valves)

def get_multipath_remaining_pressure(states: List[Tuple[str, int]],
	remaining_valves: Iterable[str], distance_map: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]) -> int:

	max_time_open = lambda starting_valve, time, target_valve: max(0, time - distance_map[starting_valve][target_valve] - 1)
	return sum(flow_rates[valve] * max(max_time_open(starting_valve, time, valve) for starting_valve, time in states) for valve in remaining_valves)

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