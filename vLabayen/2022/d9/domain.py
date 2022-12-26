import typing
from dataclasses import dataclass
from enum import Enum

class MotionDirection(Enum):
	UP    = 'U'
	RIGHT = 'R'
	DOWN  = 'D'
	LEFT  = 'L'

	def incr(self) -> typing.Tuple[int, int]:
		if self == MotionDirection.UP   : return ( 1,  0)
		if self == MotionDirection.DOWN : return (-1,  0)
		if self == MotionDirection.RIGHT: return ( 0,  1)
		if self == MotionDirection.LEFT : return ( 0, -1)

@dataclass
class MotionStep:
	direction: MotionDirection
	amount: int

	@staticmethod
	def from_text(text: str):
		''' Return a MotionStep based on it's text definition
		
		>>> MotionStep.from_text('R 4')
		MotionStep(direction=<MotionDirection.RIGHT: 'R'>, amount=4)
		>>> MotionStep.from_text('U 4')
		MotionStep(direction=<MotionDirection.UP: 'U'>, amount=4)
		>>> MotionStep.from_text('L 3')
		MotionStep(direction=<MotionDirection.LEFT: 'L'>, amount=3)
		>>> MotionStep.from_text('D 1')
		MotionStep(direction=<MotionDirection.DOWN: 'D'>, amount=1)
		'''
		direction, amount = text.split(' ')
		return MotionStep(MotionDirection(direction), int(amount))

@dataclass
class Rope:
	knots: typing.List[typing.Tuple[int, int]]

	def __init__(self, num_knots:int):
		assert num_knots > 1
		self.knots = [(0, 0) for _ in range(num_knots)]

	@staticmethod
	def is_touching(head: typing.Tuple[int, int], tail: typing.Tuple[int, int]):
		''' Returns whether the head and tail are touching
		
		>>> Rope.is_touching((0, 0), (0, 0))
		True
		>>> Rope.is_touching((0, 1), (0, 0))
		True
		>>> Rope.is_touching((1, 1), (0, 0))
		True
		>>> Rope.is_touching((2, 1), (3, 2))
		True
		>>> Rope.is_touching((2, 0), (0, 0))
		False
		>>> Rope.is_touching((2, 1), (0, 0))
		False
		>>> Rope.is_touching((0, 0), (2, 1))
		False
		>>> Rope.is_touching((2, 1), (4, 2))
		False
		'''
		head_y, head_x = head
		tail_y, tail_x = tail
		in_range = lambda head_coord, tail_coord: abs(head_coord - tail_coord) <= 1
		return in_range(head_x, tail_x) and in_range(head_y, tail_y)

	def move(self, direction: MotionDirection):
		''' Move both the head & tail
		
		>>> r = Rope(2)
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(0, 1), (0, 0)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(0, 2), (0, 1)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(0, 3), (0, 2)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(0, 4), (0, 3)])
		>>> r.move(MotionDirection.UP)
		Rope(knots=[(1, 4), (0, 3)])
		>>> r.move(MotionDirection.UP)
		Rope(knots=[(2, 4), (1, 4)])
		>>> r.move(MotionDirection.UP)
		Rope(knots=[(3, 4), (2, 4)])
		>>> r.move(MotionDirection.UP)
		Rope(knots=[(4, 4), (3, 4)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(4, 3), (3, 4)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(4, 2), (4, 3)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(4, 1), (4, 2)])
		>>> r.move(MotionDirection.DOWN)
		Rope(knots=[(3, 1), (4, 2)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(3, 2), (4, 2)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(3, 3), (4, 2)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(3, 4), (3, 3)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(3, 5), (3, 4)])
		>>> r.move(MotionDirection.DOWN)
		Rope(knots=[(2, 5), (3, 4)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(2, 4), (3, 4)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(2, 3), (3, 4)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(2, 2), (2, 3)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(2, 1), (2, 2)])
		>>> r.move(MotionDirection.LEFT)
		Rope(knots=[(2, 0), (2, 1)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(2, 1), (2, 1)])
		>>> r.move(MotionDirection.RIGHT)
		Rope(knots=[(2, 2), (2, 1)])
		'''
		head_y, head_x = self.knots[0]

		inc_y, inc_x = direction.incr()
		self.knots[0] = head_y + inc_y, head_x + inc_x

		for i in range(1, len(self.knots)):
			self.follow(i)
		
		return self

	def follow(self, tail_idx):
		head = self.knots[tail_idx - 1]
		tail = self.knots[tail_idx]
		if Rope.is_touching(head, tail): return

		head_y, head_x = head
		tail_y, tail_x = tail

		y_diff = head_y - tail_y
		x_diff = head_x - tail_x

		def get_tail_movement(diff):
			if diff == 0: return 0
			return -1 if diff < 0 else 1

		self.knots[tail_idx] = (
			tail_y + get_tail_movement(y_diff),
			tail_x + get_tail_movement(x_diff),
		)

if __name__ == '__main__':
	import doctest
	doctest.testmod()