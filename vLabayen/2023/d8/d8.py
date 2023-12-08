import logging
from typing import List, Tuple, Iterable, Dict
from attrs import define
from enum import Enum
import re
from itertools import takewhile
from functools import reduce
from math import gcd

def lcm(numbers: Iterable[int]) -> int:
	return reduce(lambda a, b: a * b // gcd(a, b), numbers)

class Step(Enum):
	LEFT  = 'L'
	RIGHT = 'R'

def steps_gen(steps: List[Step]) -> Iterable[Tuple[int, Step]]:
	while True:
		for i, step in enumerate(steps):
			yield i, step

@define
class Node:
	name : str
	left : str
	right: str

parse_node_rgx = re.compile(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)')
def read_file(file: str) -> Tuple[List[Step], List[Node]]:
	with open(file, 'r') as f:
		lines = (l.strip() for l in f)

		steps = [Step(step) for step in next(lines)]
		next(lines)
		nodes = [Node(*parse_node_rgx.match(node).groups()) for node in lines]	# type: ignore

	return steps, nodes

def p1(args):
	steps, nodes = read_file(args.file)
	nodes_network = {node.name: node for node in nodes}

	current_node = nodes_network['AAA']
	for i, (_, step) in enumerate(steps_gen(steps)):
		next_node_name = current_node.right if step == Step.RIGHT else current_node.left
		current_node = nodes_network[next_node_name]

		if current_node.name == 'ZZZ': break
	
	print(i + 1)	# type: ignore


def detect_loop_frequency(node: Node, steps: List[Step], nodes_network: Dict[str, Node]) -> int:
	visited_nodes: Dict[Tuple[str, int], int] = {}
	current_node = node

	for i, (step_idx, step) in enumerate(steps_gen(steps)):
		key = (current_node.name, step_idx)

		past_visit = visited_nodes.get(key, None)
		if past_visit is not None:
			return i - past_visit
		visited_nodes[key] = i

		next_node_name = current_node.right if step == Step.RIGHT else current_node.left
		current_node = nodes_network[next_node_name]

	raise

def p2(args):
	steps, nodes = read_file(args.file)
	nodes_network = {node.name: node for node in nodes}

	ending_A_nodes = [node for node in nodes if node.name.endswith('A')]
	nodes_cycle_freq = {node.name: detect_loop_frequency(node, steps, nodes_network) for node in ending_A_nodes}

	# As far a I can think, there is no hard requirement for the ending-Z nodes to be located exactly at the cycle freq
	# nevertheless, that's seems that be what happens in the example & my input.
	print(lcm(freq for freq in nodes_cycle_freq.values()))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
