import typing
import logging
import re
from dataclasses import dataclass
from functools import cmp_to_key

TPacketData = typing.List[typing.Union[int, 'TPacketData']]

@dataclass
class Packet:
	is_data_valid = re.compile('^[0-9\[\], ]+$')

	data: TPacketData

	@staticmethod
	def from_text(text: str) -> 'Packet':
		''' Parse a packet from it's data text definition
		
		>>> Packet.from_text('[1,1,3,1,1]')
		Packet(data=[1, 1, 3, 1, 1])
		>>> Packet.from_text('[[1],[2,3,4]]')
		Packet(data=[[1], [2, 3, 4]])
		>>> Packet.from_text('[1,[2,[3,[4,[5,6,7]]]],8,9]')
		Packet(data=[1, [2, [3, [4, [5, 6, 7]]]], 8, 9])
		>>> Packet.from_text('print("hack")')
		Traceback (most recent call last):
		  ...
		ValueError: Invalid packet data
		'''
		if not Packet.is_data_valid.match(text):
			raise ValueError(f'Invalid packet data')

		return Packet(eval(text))

def in_order(left: TPacketData, right: TPacketData) -> bool:
	''' Check if a pair of packets is in correct order
	
	>>> in_order(
	...		Packet.from_text('[1,1,3,1,1]').data,
	...		Packet.from_text('[1,1,5,1,1]').data,
	... )
	True
	>>> in_order(
	...		Packet.from_text('[[1],[2,3,4]]').data,
	...		Packet.from_text('[[1],4]').data,
	... )
	True
	>>> in_order(
	...		Packet.from_text('[9]').data,
	...		Packet.from_text('[[8,7,6]]').data,
	... )
	False
	>>> in_order(
	...		Packet.from_text('[[4,4],4,4]').data,
	...		Packet.from_text('[[4,4],4,4,4]').data,
	... )
	True
	>>> in_order(
	...		Packet.from_text('[7,7,7,7]').data,
	...		Packet.from_text('[7,7,7]').data,
	... )
	False
	>>> in_order(
	...		Packet.from_text('[]').data,
	...		Packet.from_text('[3]').data,
	... )
	True
	>>> in_order(
	...		Packet.from_text('[[[]]]').data,
	...		Packet.from_text('[[]]').data,
	... )
	False
	>>> in_order(
	...		Packet.from_text('[1,[2,[3,[4,[5,6,7]]]],8,9]').data,
	...		Packet.from_text('[1,[2,[3,[4,[5,6,0]]]],8,9]').data,
	... )
	False
	'''
	for left_value, right_value in zip(left, right):
		if isinstance(left_value, int) and isinstance(right_value, int):
			if left_value == right_value: continue
			return left_value < right_value

		if not isinstance(left_value, list):
			left_value = [left_value]

		if not isinstance(right_value, list):
			right_value = [right_value]

		lists_in_order = in_order(left_value, right_value)
		if lists_in_order is not None: return lists_in_order

	else:
		if len(left) == len(right): return None
		return len(left) < len(right)

@cmp_to_key
def sort_packets(left, right):
	return -1 if in_order(left.data, right.data) else 1

if __name__ == '__main__':
	import doctest
	logging.basicConfig(level=logging.DEBUG)
	doctest.testmod(optionflags=doctest.ELLIPSIS)