import typing
import logging
from dataclasses import dataclass
from collections import deque
from itertools import repeat
import re

parse_starting_items_rgx = re.compile('Starting items: (.*)')
def get_starting_items(text: str) -> typing.List[int]:
	''' Parse starting items

	>>> get_starting_items('Starting items: 79, 98')
	[79, 98]
	>>> get_starting_items('Starting items: 54, 65, 75, 74')
	[54, 65, 75, 74]
	'''
	items = parse_starting_items_rgx.match(text).group(1).split(', ')
	return [int(item) for item in items]

parse_operation_rgx = re.compile('Operation: new = (.*)')
def get_operation(text: str) -> typing.Callable[[int], int]:
	''' Parse operation
	
	>>> get_operation('Operation: new = old * 19')(79)
	1501
	>>> get_operation('Operation: new = old + 6')(54)
	60
	>>> get_operation('Operation: new = old * old')(79)
	6241
	'''
	expression = parse_operation_rgx.match(text).group(1)
	return lambda old: eval(expression)

parse_divisible_rgx = re.compile('Test: divisible by ([0-9]+)')
parse_target_monkey_rgx = re.compile('If (?:true|false): throw to monkey ([0-9]+)')
def get_action(lines: typing.List[str]) -> typing.Tuple[int, int, int]:
	''' Parse action
	
	>>> get_action([
	...		'Test: divisible by 23',
	...		'If true: throw to monkey 2',
	...		'If false: throw to monkey 3',
	... ])
	(23, 2, 3)

	>>> get_action([
	...		'Test: divisible by 19',
	...		'If true: throw to monkey 2',
	...		'If false: throw to monkey 0',
	... ])
	(19, 2, 0)
	'''
	divisible_by = int(parse_divisible_rgx.match(lines[0]).group(1))
	monkey_if_true  = int(parse_target_monkey_rgx.match(lines[1]).group(1))
	monkey_if_false = int(parse_target_monkey_rgx.match(lines[2]).group(1))
	return divisible_by, monkey_if_true, monkey_if_false
	# return lambda new: 

@dataclass
class Monkey:
	items: typing.Deque[int]
	operation: typing.Callable[[int], int]
	divisible_by: int
	monkey_if_true: int
	monkey_if_false: int
	num_inspected_items: int = 0

	@staticmethod
	def from_text(lines: typing.List[str]):
		''' Returns a Monkey from it's text definition

		>>> Monkey.from_text([
		...		'Monkey 0:',
		...		'  Starting items: 79, 98',
		...		'  Operation: new = old * 19',
		...		'  Test: divisible by 23',
		...		'    If true: throw to monkey 2',
		...		'    If false: throw to monkey 3',
		... ])
		Monkey(items=deque([79, 98]), operation=..., divisible_by=23, monkey_if_true=2, monkey_if_false=3, num_inspected_items=0)

		>>> Monkey.from_text([
		...		'Monkey 1:',
		...		'Starting items: 54, 65, 75, 74',
		...		'Operation: new = old + 6',
		...		'Test: divisible by 19',
		...		'  If true: throw to monkey 2',
		...		'  If false: throw to monkey 0',
		...	])
		Monkey(items=deque([54, 65, 75, 74]), operation=..., divisible_by=19, monkey_if_true=2, monkey_if_false=0, num_inspected_items=0)

		>>> Monkey.from_text([
		... 	'Monkey 3:',
		...		'Starting items: 74',
		...		'Operation: new = old + 3',
		...		'Test: divisible by 17',
		...		'  If true: throw to monkey 0',
		...		'  If false: throw to monkey 1',
		... ])
		Monkey(items=deque([74]), operation=..., divisible_by=17, monkey_if_true=0, monkey_if_false=1, num_inspected_items=0)
		'''
		items = deque(get_starting_items(lines[1].strip()))
		operation = get_operation(lines[2].strip())
		divisible_by, if_true, if_false = get_action([line.strip() for line in lines[3:]])
		return Monkey(items, operation, divisible_by, if_true, if_false)

	def run_turn(self) -> typing.Iterable[typing.Tuple[int, int]]:
		''' Runs a monkey's turn
		
		>>> list(Monkey.from_text([
		...		'Monkey 0:',
		...		'  Starting items: 79, 98',
		...		'  Operation: new = old * 19',
		...		'  Test: divisible by 23',
		...		'    If true: throw to monkey 2',
		...		'    If false: throw to monkey 3',
		... ]).run_turn())
		[(500, 3), (620, 3)]

		>>> list(Monkey.from_text([
		...		'Monkey 1:',
		...		'Starting items: 54, 65, 75, 74',
		...		'Operation: new = old + 6',
		...		'Test: divisible by 19',
		...		'  If true: throw to monkey 2',
		...		'  If false: throw to monkey 0',
		...	]).run_turn())
		[(20, 0), (23, 0), (27, 0), (26, 0)]
		'''
		for _ in repeat(None, len(self.items)):
			worry_level = self.items.popleft()
			new_worry_level = self.operation(worry_level) // 3
			target_monkey = self.monkey_if_true if (new_worry_level % self.divisible_by == 0) else self.monkey_if_false

			self.num_inspected_items += 1
			yield new_worry_level, target_monkey

	def add_item(self, worry_level) -> None:
		self.items.append(worry_level)

def run_round(monkeys: typing.List[Monkey]) -> None:
	''' Run a round
	
	>>> monkeys = [
	... 	Monkey.from_text([
	... 		'Monkey 0:',
  	...			'Starting items: 79, 98',
  	...			'Operation: new = old * 19',
  	...			'Test: divisible by 23',
  	...			'  If true: throw to monkey 2',
  	...			'  If false: throw to monkey 3',
	... 	]),
	... 	Monkey.from_text([
	... 		'Monkey 1:',
  	...			'Starting items: 54, 65, 75, 74',
  	...			'Operation: new = old + 6',
  	...			'Test: divisible by 19',
  	...			'  If true: throw to monkey 2',
  	...			'  If false: throw to monkey 0',
	... 	]),
	... 	Monkey.from_text([
	... 		'Monkey 2:',
  	...			'Starting items: 79, 60, 97',
  	...			'Operation: new = old * old',
  	...			'Test: divisible by 13',
  	...			'  If true: throw to monkey 1',
  	...			'  If false: throw to monkey 3',
	... 	]),
	... 	Monkey.from_text([
	... 		'Monkey 3:',
  	...			'Starting items: 74',
  	...			'Operation: new = old + 3',
  	...			'Test: divisible by 17',
  	...			'  If true: throw to monkey 0',
  	...			'  If false: throw to monkey 1',
	... 	]),
	... ]
	>>> get_items = lambda monkeys: {idx: list(monkey.items) for idx, monkey in enumerate(monkeys)}

	>>> get_items(run_round(monkeys))
	{0: [20, 23, 27, 26], 1: [2080, 25, 167, 207, 401, 1046], 2: [], 3: []}
	>>> get_items(run_round(monkeys))
	{0: [695, 10, 71, 135, 350], 1: [43, 49, 58, 55, 362], 2: [], 3: []}
	>>> get_items(run_round(monkeys))
	{0: [16, 18, 21, 20, 122], 1: [1468, 22, 150, 286, 739], 2: [], 3: []}
	>>> get_items(run_round(monkeys))
	{0: [491, 9, 52, 97, 248, 34], 1: [39, 45, 43, 258], 2: [], 3: []}
	>>> get_items(run_round(monkeys))
	{0: [15, 17, 16, 88, 1037], 1: [20, 110, 205, 524, 72], 2: [], 3: []}

	>>> for _ in repeat(None, 15): _ = run_round(monkeys)
	>>> get_items(monkeys)
	{0: [10, 12, 14, 26, 34], 1: [245, 93, 53, 199, 115], 2: [], 3: []}
	'''
	for monkey in monkeys:
		for worry_level, target_monkey in monkey.run_turn():
			monkeys[target_monkey].add_item(worry_level)

	return monkeys

if __name__ == '__main__':
	import doctest
	logging.basicConfig(level=logging.DEBUG)
	doctest.testmod(optionflags=doctest.ELLIPSIS)