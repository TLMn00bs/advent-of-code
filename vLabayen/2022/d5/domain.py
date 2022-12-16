from dataclasses import dataclass
from collections import deque
import typing
import re

parse_step_rgx = re.compile('move ([0-9]+) from ([0-9]+) to ([0-9]+)')

@dataclass
class RearrangementStep:
	amount: int
	src: int
	dst: int

	@staticmethod
	def from_text(text: str):
		''' Returns a RearrangementStep from it's text definition
		
		>>> RearrangementStep.from_text('move 1 from 2 to 1')
		RearrangementStep(amount=1, src=2, dst=1)
		>>> RearrangementStep.from_text('move 3 from 1 to 3')
		RearrangementStep(amount=3, src=1, dst=3)
		>>> RearrangementStep.from_text('move 2 from 2 to 1')
		RearrangementStep(amount=2, src=2, dst=1)
		>>> RearrangementStep.from_text('move 1 from 1 to 2')
		RearrangementStep(amount=1, src=1, dst=2)
		'''
		amount, src, dst = parse_step_rgx.match(text).groups()
		return RearrangementStep(int(amount), int(src), int(dst))

@dataclass
class CratesPlacement:
	crates: typing.List[typing.Deque[str]]

	@staticmethod
	def from_text_lines(lines: typing.List[str]):
		''' Returns a CratesPlacement from it's text definition
		
		>>> CratesPlacement.from_text_lines([
		...		'    [D]    ',
		...		'[N] [C]    ',
		...		'[Z] [M] [P]',
		...		' 1   2   3 ',
		... ])
		CratesPlacement(crates=[deque(['N', 'Z']), deque(['D', 'C', 'M']), deque(['P'])])
		'''
		crates_lines = lines[:-1]
		num_stacks = int(re.match('^.*([0-9]+) $', lines[-1]).group(1))

		def get_crates(stack_idx):
			crates_names = (line[4*stack_idx + 1] for line in crates_lines)
			return [crate for crate in crates_names if crate != ' ']

		crates = [deque(get_crates(stack_idx)) for stack_idx in range(num_stacks)]
		return CratesPlacement(crates)

	def apply_step_one_crate_at_a_time(self, step: RearrangementStep):
		''' Apply one rearrangement step
		
		>>> placement = CratesPlacement(crates=[deque(['N', 'Z']), deque(['D', 'C', 'M']), deque(['P'])])
		>>> placement.apply_step_one_crate_at_a_time(RearrangementStep(amount=1, src=2, dst=1))
		CratesPlacement(crates=[deque(['D', 'N', 'Z']), deque(['C', 'M']), deque(['P'])])
		>>> placement.apply_step_one_crate_at_a_time(RearrangementStep(amount=3, src=1, dst=3))
		CratesPlacement(crates=[deque([]), deque(['C', 'M']), deque(['Z', 'N', 'D', 'P'])])
		>>> placement.apply_step_one_crate_at_a_time(RearrangementStep(amount=2, src=2, dst=1))
		CratesPlacement(crates=[deque(['M', 'C']), deque([]), deque(['Z', 'N', 'D', 'P'])])
		>>> placement.apply_step_one_crate_at_a_time(RearrangementStep(amount=1, src=1, dst=2))
		CratesPlacement(crates=[deque(['C']), deque(['M']), deque(['Z', 'N', 'D', 'P'])])
		'''

		for _ in range(step.amount):
			crate = self.crates[step.src - 1].popleft()
			self.crates[step.dst - 1].appendleft(crate)

		return self

	def apply_step_multiple_crates_at_once(self, step: RearrangementStep):
		''' Apply one rearrangement step
		
		>>> placement = CratesPlacement(crates=[deque(['N', 'Z']), deque(['D', 'C', 'M']), deque(['P'])])
		>>> placement.apply_step_multiple_crates_at_once(RearrangementStep(amount=1, src=2, dst=1))
		CratesPlacement(crates=[deque(['D', 'N', 'Z']), deque(['C', 'M']), deque(['P'])])
		>>> placement.apply_step_multiple_crates_at_once(RearrangementStep(amount=3, src=1, dst=3))
		CratesPlacement(crates=[deque([]), deque(['C', 'M']), deque(['D', 'N', 'Z', 'P'])])
		>>> placement.apply_step_multiple_crates_at_once(RearrangementStep(amount=2, src=2, dst=1))
		CratesPlacement(crates=[deque(['C', 'M']), deque([]), deque(['D', 'N', 'Z', 'P'])])
		>>> placement.apply_step_multiple_crates_at_once(RearrangementStep(amount=1, src=1, dst=2))
		CratesPlacement(crates=[deque(['M']), deque(['C']), deque(['D', 'N', 'Z', 'P'])])
		'''
		crates_to_move = reversed([self.crates[step.src - 1].popleft() for _ in range(step.amount)])
		self.crates[step.dst - 1].extendleft(crates_to_move)

		return self

	def get_top_crates(self):
		''' Return the crates at the most top position of each stack
		
		>>> placement = CratesPlacement(crates=[deque(['C']), deque(['M']), deque(['Z', 'N', 'D', 'P'])])
		>>> placement.get_top_crates()
		['C', 'M', 'Z']
		'''
		return [stack[0] for stack in self.crates]


if __name__ == '__main__':
	import doctest
	doctest.testmod()