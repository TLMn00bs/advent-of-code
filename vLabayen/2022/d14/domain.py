import typing
import logging
from dataclasses import dataclass, field
from ndt.window_iterator import iter_window
from enum import Enum, auto


TPosition = typing.Tuple[int, int]
TCave = typing.TypeVar('TCave', bound='Cave')

class SandStatus(Enum):
	REST = auto()
	VOID = auto()

def parse_position(text: str) -> TPosition:
	''' Parse a position from it's text definition
	
	>>> parse_position('498,4')
	(498, 4)
	>>> parse_position('502,9')
	(502, 9)
	'''
	x, y = text.split(',')
	return int(x), int(y)

def get_rocks_in_path(start: TPosition, end: TPosition) -> typing.Iterable[TPosition]:
	''' Generate all the rocks in the path between start & end
	
	>>> list(get_rocks_in_path((498, 4), (498, 6)))
	[(498, 4), (498, 5), (498, 6)]
	'''
	start_x, start_y = start
	end_x, end_y = end

	path_start_x, path_end_x = sorted([start_x, end_x])
	path_start_y, path_end_y = sorted([start_y, end_y])

	for x in range(path_start_x, path_end_x + 1):
		for y in range(path_start_y, path_end_y + 1):
			yield x, y


@dataclass
class SandGrain:
	position: TPosition

	def fall(self, cave: TCave) -> SandStatus:
		unavailable_positions = cave.rocks.union(cave.sand_grains)

		x, y = self.position
		while (y < cave.void_level):
			if (x, y + 1) not in unavailable_positions:
				y += 1
				continue

			if (x - 1, y + 1) not in unavailable_positions:
				y += 1
				x -= 1
				continue

			if (x + 1, y + 1) not in unavailable_positions:
				y += 1
				x += 1
				continue

			self.position = x, y
			return SandStatus.REST

		self.position = x, y
		return SandStatus.VOID

@dataclass
class Cave:
	rocks: typing.Set[TPosition]
	void_level: int
	sand_origin: TPosition = (500, 0)
	sand_grains: typing.Set[TPosition] = field(default_factory=lambda: set())

	@staticmethod
	def from_lines(lines: typing.List[str]):
		''' Parses the cave structure from the paths in text format
		
		>>> Cave.from_lines([
		...		'498,4 -> 498,6 -> 496,6',
		...		'503,4 -> 502,4 -> 502,9 -> 494,9',
		... ])
		<Cave len(self.rocks)=20 self.void_level=9>
		'''
		rocks: typing.Set[TPosition] = set()
		for path in lines:
			path_points = [parse_position(position) for position in path.split(' -> ')]
			for start, end in iter_window(path_points, n = 2):
				rocks.update(get_rocks_in_path(start, end))

		void_level = max(y for x, y in rocks)
		return Cave(rocks, void_level + 2)

	def add_path(self, start: TPosition, end: TPosition):
		self.rocks.update(get_rocks_in_path(start, end))

	def add_grain(self):
		grain = SandGrain(self.sand_origin)
		
		grain_status = grain.fall(self)
		if grain_status == SandStatus.REST:
			self.sand_grains.add(grain.position)

		return grain_status

	def __repr__(self): return f'<Cave {len(self.rocks)=} {self.void_level=}>'
	def __str__(self):
		min_x = min([x for x, y in self.rocks] + [x for x, y in self.sand_grains] + [self.sand_origin[0]])
		max_x = max([x for x, y in self.rocks] + [x for x, y in self.sand_grains] + [self.sand_origin[0]])
		min_y = min([y for x, y in self.rocks] + [y for x, y in self.sand_grains] + [self.sand_origin[1]])
		max_y = max([y for x, y in self.rocks] + [y for x, y in self.sand_grains] + [self.sand_origin[1]])

		def get_repr(x, y):
			if (x, y) == self.sand_origin: return '+'
			if (x, y) in self.rocks: return '#'
			if (x, y) in self.sand_grains: return 'o'
			return '.'

		get_row = lambda y: ''.join(get_repr(x, y) for x in range(min_x, max_x + 1))
		return '\n'.join(get_row(y) for y in range(min_y, max_y + 1))

if __name__ == '__main__':
	import doctest
	logging.basicConfig(level=logging.DEBUG)
	doctest.testmod()