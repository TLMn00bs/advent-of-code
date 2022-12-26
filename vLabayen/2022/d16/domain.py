import typing
import logging
import re

class Valve(typing.TypedDict):
	flow_rate: int
	connected_nodes: typing.Set[str]

TunnelLayout = typing.Dict[str, Valve]

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

def get_available_pressure(flow_rate: int, distance: int, time: int) -> int:
	''' Get the maximun pressure that can be released '''
	p = flow_rate * (time - distance - 1)
	if p > 0: return p
	return 0

def get_remaining_pressure(valves: typing.List[typing.Tuple[int, int]], time: int) -> int:
	''' Get the maximum pressure that can be released '''
	score = 0
	for flow_rate, distance in valves:
		p = flow_rate * (time - distance - 1)
		if p > 0: score += p	
	return score

def get_valve_score(src: str, dst: str, time: int,
	distance_map: typing.Dict[str, typing.Dict[str, int]],
	flow_rates: typing.Dict[str, int],
	remaining_valves: typing.Set[str]
) -> int:
	''' Get the score for remaining valve'''
	released_pressure = get_available_pressure(
		flow_rates[dst],
		distance_map[src][dst],
		time
	)

	next_valves = remaining_valves.difference([dst])
	remaining_pressure = get_remaining_pressure(
		[(flow_rates[next_dst], distance_map[dst][next_dst]) for next_dst in next_valves],
		time - distance_map[src][dst] - 1
	)

	return released_pressure + remaining_pressure


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

		def test_get_available_pressure(self):
			p = get_available_pressure(20, 1, 30)
			self.assertEqual(p, 28 * 20)

		def test_get_remaining_pressure(self):
			distances = get_distances_from('DD', TestDomain.layout)
			t = 30 - TestDomain.distances_from_AA['DD'] - 1

			p = get_remaining_pressure(
				[(TestDomain.layout[dst]['flow_rate'], d) for dst, d in distances.items()],
				t
			)
			self.assertEqual(p, sum([
				13 * (t - distances['BB'] - 1),
				2  * (t - distances['CC'] - 1),
				3  * (t - distances['EE'] - 1),
				22 * (t - distances['HH'] - 1),
				21 * (t - distances['JJ'] - 1),
			]))

	logging.info(f'Running doctests')
	doctest.testmod(optionflags=doctest.ELLIPSIS)

	logging.info(f'Running unittests')
	unittest.main()