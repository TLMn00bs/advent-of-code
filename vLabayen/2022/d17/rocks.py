from typing import Tuple, Callable, Iterable, Set
from abc import ABC, abstractmethod, abstractproperty
from attrs import define

@define
class Rock(ABC):
	start_x: int
	start_y: int

	@abstractproperty
	def rocks(self) -> Iterable[Tuple[int, int]]: ...

	@abstractproperty
	def highest_y(self) -> int: ...

	@abstractmethod
	def collide_down(self, occuped_places: Set[Tuple[int, int]]) -> bool: ...

	@abstractmethod
	def collide_left(self, occuped_places: Set[Tuple[int, int]]) -> bool: ...

	@abstractmethod
	def collide_right(self, occuped_places: Set[Tuple[int, int]]) -> bool: ...

	def move(self, delta_x: int, delta_y: int) -> None:
		self.start_x += delta_x
		self.start_y += delta_y

class FirstShape(Rock):
	'''
	.####
	X....
	'''

	@property
	def rocks(self) -> Iterable[Tuple[int, int]]:
		yield (self.start_x + 1, self.start_y + 1)
		yield (self.start_x + 2, self.start_y + 1)
		yield (self.start_x + 3, self.start_y + 1)
		yield (self.start_x + 4, self.start_y + 1)

	@property
	def highest_y(self) -> int: return self.start_y + 1

	def collide_down(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_y < 1 or any((x, y - 1) in occuped_places for (x, y) in self.rocks)

	def collide_left(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x < 1 or (self.start_x, self.start_y + 1) in occuped_places

	def collide_right(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x + 5 > 7 or (self.start_x + 5, self.start_y + 1) in occuped_places


class SecondShape(Rock):
	'''
	..#.
	.###
	..#.
	X...
	'''

	@property
	def rocks(self) -> Iterable[Tuple[int, int]]:
		yield (self.start_x + 2, self.start_y + 3)
		yield (self.start_x + 1, self.start_y + 2)
		yield (self.start_x + 2, self.start_y + 2)
		yield (self.start_x + 3, self.start_y + 2)
		yield (self.start_x + 2, self.start_y + 1)

	@property
	def highest_y(self) -> int: return self.start_y + 3

	def collide_down(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_y < 1 or (
			((self.start_x + 1, self.start_y + 1) in occuped_places) or
			((self.start_x + 2, self.start_y)     in occuped_places) or
			((self.start_x + 3, self.start_y + 1) in occuped_places)
		)

	def collide_left(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x < 1 or (
			((self.start_x + 1, self.start_y + 3) in occuped_places) or
			((self.start_x    , self.start_y + 2) in occuped_places) or
			((self.start_x + 1, self.start_y + 1) in occuped_places)
		)

	def collide_right(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x + 4 > 7 or (
			((self.start_x + 3, self.start_y + 3) in occuped_places) or
			((self.start_x + 4, self.start_y + 2) in occuped_places) or
			((self.start_x + 3, self.start_y + 1) in occuped_places)
		)

class ThirdShape(Rock):
	'''
	...#
	...#
	.###
	X...
	'''

	@property
	def rocks(self) -> Iterable[Tuple[int, int]]:
		yield (self.start_x + 3, self.start_y + 3)
		yield (self.start_x + 3, self.start_y + 2)
		yield (self.start_x + 1, self.start_y + 1)
		yield (self.start_x + 2, self.start_y + 1)
		yield (self.start_x + 3, self.start_y + 1)

	@property
	def highest_y(self) -> int: return self.start_y + 3

	def collide_down(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_y < 1 or (
			((self.start_x + 1, self.start_y) in occuped_places) or
			((self.start_x + 2, self.start_y) in occuped_places) or
			((self.start_x + 3, self.start_y) in occuped_places)
		)

	def collide_left(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x < 1 or (
			((self.start_x + 2, self.start_y + 3) in occuped_places) or
			((self.start_x + 2, self.start_y + 2) in occuped_places) or
			((self.start_x    , self.start_y + 1) in occuped_places)
		)
	
	def collide_right(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x + 4 > 7 or (
			((self.start_x + 4, self.start_y + 3) in occuped_places) or
			((self.start_x + 4, self.start_y + 2) in occuped_places) or
			((self.start_x + 4, self.start_y + 1) in occuped_places)
		)

class FourthShape(Rock):
	'''
	.#
	.#
	.#
	.#
	X.
	'''

	@property
	def rocks(self) -> Iterable[Tuple[int, int]]:
		yield (self.start_x + 1, self.start_y + 4)
		yield (self.start_x + 1, self.start_y + 3)
		yield (self.start_x + 1, self.start_y + 2)
		yield (self.start_x + 1, self.start_y + 1)

	@property
	def highest_y(self) -> int: return self.start_y + 4

	def collide_down(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_y < 1 or (self.start_x + 1, self.start_y) in occuped_places

	def collide_left(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x < 1 or any((x - 1, y) in occuped_places for (x, y) in self.rocks)

	def collide_right(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x + 2 > 7 or any((x + 1, y) in occuped_places for (x, y) in self.rocks)


class FifthShape(Rock):
	'''
	.##
	.##
	X..
	'''

	@property
	def rocks(self) -> Iterable[Tuple[int, int]]:
		yield (self.start_x + 1, self.start_y + 2)
		yield (self.start_x + 2, self.start_y + 2)
		yield (self.start_x + 1, self.start_y + 1)
		yield (self.start_x + 2, self.start_y + 1)

	@property
	def highest_y(self) -> int: return self.start_y + 2

	def collide_down(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_y < 1 or (
			((self.start_x + 1, self.start_y) in occuped_places) or
			((self.start_x + 2, self.start_y) in occuped_places)
		)

	def collide_left(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x < 1 or (
			((self.start_x, self.start_y + 2) in occuped_places) or
			((self.start_x, self.start_y + 1) in occuped_places)
		)

	def collide_right(self, occuped_places: Set[Tuple[int, int]]) -> bool:
		return self.start_x + 3 > 7 or (
			((self.start_x + 3, self.start_y + 2) in occuped_places) or
			((self.start_x + 3, self.start_y + 1) in occuped_places)
		)

def falling_rocks(n: int, start_x: int, start_y: Callable[[], int]) -> Iterable[Rock]:
	def gen():
		while True:
			yield FirstShape(start_x, start_y())
			yield SecondShape(start_x, start_y())
			yield ThirdShape(start_x, start_y())
			yield FourthShape(start_x, start_y())
			yield FifthShape(start_x, start_y())

	rocks = gen()
	for _ in range(n):
		yield next(rocks)