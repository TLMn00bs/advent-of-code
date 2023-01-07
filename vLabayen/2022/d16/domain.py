import typing
from typing import *
import logging
import re
from ndt.window_iterator import iter_window

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

def get_open_times(startingPosition: str, maxTime: int,
	choices: List[str],
	distancesMap: Dict[str, Dict[str, int]]) -> Iterable[int]:
	''' Get the times when each valve will be opened '''

	path = [startingPosition] + choices
	distances = [distancesMap[src][dst] for src, dst in iter_window(path, n=2)]

	acc_time = 0
	for d in distances:
		incr = d + 1
		if acc_time + incr >= maxTime: return

		acc_time += incr
		yield acc_time


def get_released_pressure(choices: List[str], maxTime: int,
	open_times: List[int],
	flowRates: Dict[str, int]) -> int:
	''' Get the total released pressure when following a given order '''

	return sum(flowRates[valve] * (maxTime - time) for valve, time in zip(choices, open_times))

def get_upper_limit(choices: List[str], maxTime: int,
	open_times: List[int],
	distancesMap: Dict[str, Dict[str, int]],
	flowRates: Dict[str, int],
	variant: str = 'up'
	) -> int:
	''' Get an upper limit for the released pressure with unfinished choices '''

	already_released = get_released_pressure(choices, maxTime, open_times, flowRates)
	last_position = choices[-1]
	spent_time = open_times[-1]
	remaining_time = maxTime - spent_time
	remaining_valves = [valve for valve in flowRates if valve not in choices]

	if variant == 'up':
		max_pressure = lambda valve: flowRates[valve] * (remaining_time - distancesMap[last_position][valve] - 1)
		max_remaning_pressure = sum(max_pressure(valve) for valve in remaining_valves)
		return already_released + max_remaning_pressure

	if variant == 'down':
		max_pressure = lambda valve, idx: flowRates[valve] * (remaining_time - distancesMap[last_position][valve] - 1 - idx)
		sorted_valves = sorted(remaining_valves, key = lambda valve: flowRates[valve], reverse=True)
		max_remaning_pressure = sum(max_pressure(valve, idx) for idx, valve in enumerate(sorted_valves))
		return already_released + max_remaning_pressure


class Wrapper:
	def __init__(self, file: str, startingPosition: str, maxTime: int):
		self.startingPosition = startingPosition
		self.maxTime = maxTime

		with open(file, 'r') as f:
			self.layout = parse_tunnels_layout([line.strip() for line in f])

		self.distance_map = {valve: get_distances_from(valve, self.layout) for valve in self.layout.keys()}
		self.flow_rates = {valve: d['flow_rate'] for valve, d in self.layout.items() if d['flow_rate'] > 0}

		self.max_pressure = 0

	def valves(self) -> Iterable[str]: return self.flow_rates.keys()
	def flow_rate(self, valve) -> int: return self.flow_rates[valve]

	def get_released_pressure(self, choices: List[str]) -> int:
		# Same here que abajo
		open_times = list(get_open_times(self.startingPosition, self.maxTime, choices, self.distance_map))
		return get_released_pressure(choices, self.maxTime, open_times, self.flow_rates)

	def get_upper_limit(self, choices: List[str], **kwargs) -> int:
		# TODO: De alguna forma tiene que poder acelerarse todo cacheando el recorrido hasta la nueva valvula.
		# Si tengo el path: [XX, YY, ZZ], cuando mire los posibles siguientes pasos, debería poder cachear
		# el computo de XX, YY, ZZ.
		open_times = list(get_open_times(self.startingPosition, self.maxTime, choices, self.distance_map))
		return get_upper_limit(choices, self.maxTime, open_times, self.distance_map, self.flow_rates, **kwargs)

	def get_choices_options(self, required_choices: List[str], lower_limit: int):
		used_valves = set(required_choices)
		for valve in self.valves():
			if valve in used_valves: continue

			choices = required_choices + [valve]
			if self.get_upper_limit(choices) >= lower_limit:
				yield choices

	def get_lower_limit(self):
		scores = {valve: self.get_upper_limit([valve], variant='up') for valve in self.valves()}
		firstChoice = max(self.valves(), key = lambda valve: scores[valve])
		choices = [firstChoice]
		remaining_valves = set(valve for valve in self.valves() if valve != firstChoice)

		while len(remaining_valves) > 0:
			scores = {valve: self.get_upper_limit(choices + [valve], variant='up') for valve in remaining_valves}
			nextChoice = max(scores.keys(), key = lambda valve: scores[valve])
			choices.append(nextChoice)
			remaining_valves.remove(nextChoice)

		return self.get_released_pressure(choices)

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

		def test_get_released_pressure(self):
			startingPosition = 'AA'
			maxTime = 30
			choices = ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC']

			distancesMap = {valve: get_distances_from(valve, self.layout) for valve in self.layout}
			flowRates: Dict[str, int] = {valve: d['flow_rate'] for valve, d in self.layout.items() if d['flow_rate'] > 0}

			openTimes = list(get_open_times(startingPosition, maxTime, choices, distancesMap))
			rp = get_released_pressure(choices, maxTime, openTimes, flowRates)
			self.assertEqual(rp, 1651)

		def test_get_upper_limit(self):
			startingPosition = 'AA'
			maxTime = 30
			choices = ['DD', 'BB', 'HH']

			distancesMap = {valve: get_distances_from(valve, self.layout) for valve in self.layout}
			flowRates: Dict[str, int] = {valve: d['flow_rate'] for valve, d in self.layout.items() if d['flow_rate'] > 0}

			openTimes = list(get_open_times(startingPosition, maxTime, choices, distancesMap))
			rp = get_upper_limit(choices, maxTime, openTimes, distancesMap, flowRates)
			self.assertEqual(rp, 1557)


	logging.info(f'Running doctests')
	doctest.testmod(optionflags=doctest.ELLIPSIS)

	logging.info(f'Running unittests')
	unittest.main()