#!/bin/python3
import logging
from typing import List, Tuple
from attrs import define
from functools import reduce

@define
class Node:
	prev: 'Node'
	next: 'Node'
	value: int
	
	def __repr__(self) -> str:
		return f'Node(value={self.value}, prev={self.prev.value} next={self.next.value})'

	def get_next(self, n: int):
		return reduce(lambda node, _: node.next, range(n), self)

	def get_prev(self, n: int):
		return reduce(lambda node, _: node.prev, range(n), self)

	def mixed_neighbours(self, mod: int) -> Tuple['Node', 'Node']:
		if self.value > 0:
			next = self.get_next(+self.value % mod)
			return next, next.next
		if self.value < 0:
			prev = self.get_prev(-self.value % mod)
			return prev.prev, prev

		raise ValueError(f'No new neightbours')

def mix(nodes: List[Node]) -> None:
	for node in nodes:
		# print([node.get_next(i).value for i in range(len(nodes))])

		if node.value != 0:
			node.prev.next = node.next
			node.next.prev = node.prev

			new_prev, new_next = node.mixed_neighbours(len(nodes) - 1)

			new_prev.next = node
			new_next.prev = node
			node.prev = new_prev
			node.next = new_next

		# print([node.get_next(i).value for i in range(len(nodes))])
		# print('---------------------')

def find_zero(nodes: List[Node]) -> Node:
	for node in nodes:
		if node.value == 0: return node

	raise ValueError(f'No zero found')

def read_file(file: str) -> List[Node]:
	with open(file, 'r') as f:
		nodes = [Node(None, None, int(v)) for v in f]	# type: ignore

	for i, node in enumerate(nodes):
		node.prev = nodes[(i - 1) % len(nodes)]
		node.next = nodes[(i + 1) % len(nodes)]

	return nodes


def p1(args):
	nodes = read_file(args.file)
	mix(nodes)

	zero_node = find_zero(nodes)
	first  = zero_node.get_next(1000).value
	second = zero_node.get_next(2000).value
	third  = zero_node.get_next(3000).value
	print(first + second + third)


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
