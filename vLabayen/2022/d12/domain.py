import typing
import logging
from dataclasses import dataclass, field
from itertools import count

TPosition = typing.Tuple[int, int]
TLocation = typing.TypeVar('TLocation', bound='Location')


def char_to_height(char):
	''' Return's the height defined by the given character
	
	>>> char_to_height('a')
	1
	>>> char_to_height('b')
	2
	>>> char_to_height('z')
	26
	>>> char_to_height('S')
	1
	>>> char_to_height('E')
	26
	'''
	if char == 'S': return char_to_height('a')
	if char == 'E': return char_to_height('z')
	return ord(char) - 96

def get_neighbours(existing_positions: typing.Set[TPosition], position: TPosition) -> typing.List[TPosition]:
	''' Get the existing neighbours positions of a given position
	
	>>> grid = {
	...		(0, 0), (0, 1), (0, 2), (0, 3),
	...		(1, 0), (1, 1), (1, 2), (1, 3),
	...		(2, 0), (2, 1), (2, 2), (2, 3),
	...		(3, 0), (3, 1), (3, 2), (3, 3),
	... }
	>>> get_neighbours(grid, (0, 0))
	[(1, 0), (0, 1)]
	>>> get_neighbours(grid, (2, 2))
	[(1, 2), (3, 2), (2, 1), (2, 3)]
	>>> get_neighbours(grid, (3, 2))
	[(2, 2), (3, 1), (3, 3)]
	'''
	y, x = position
	possible_neighbours: typing.List[TPosition] = [
		(y - 1, x    ),
		(y + 1, x    ),
		(y    , x - 1),
		(y    , x + 1),
	]
	existing_neighbours = [position for position in possible_neighbours if position in existing_positions]
	return existing_neighbours

@dataclass
class Location:
	position: TPosition
	height: int
	reachable_neighbours: typing.List[TLocation] = field(default_factory=lambda: [])
	has_been_visited: bool = False

	def can_reach(self, location: TLocation) -> bool:
		return location.height <= self.height + 1

	def set_neighbours(self, neighbours: typing.List[TLocation]):
		self.reachable_neighbours = [location for location in neighbours if self.can_reach(location)]

	def __repr__(self):
		return f'Location(position={self.position}, height={self.height})'

@dataclass
class HeightMap:
	locations: typing.Dict[TPosition, Location]
	current_location: Location
	best_signal_location: Location

	@staticmethod
	def from_lines(lines: typing.List[str]):
		''' Returns a HeightMap from it's text definition
		
		>>> hm = HeightMap.from_lines([
		...		'Sabqponm',
		...		'abcryxxl',
		...		'accszExk',
		...		'acctuvwj',
		...		'abdefghi',
		... ])
		>>> len(hm.locations)
		40

		>>> hm.current_location.position, hm.current_location.height
		((0, 0), 1)
		>>> [n.position for n in hm.current_location.reachable_neighbours]
		[(1, 0), (0, 1)]

		>>> hm.best_signal_location.position, hm.best_signal_location.height
		((2, 5), 26)

		>>> [n.position for n in hm.locations[(1, 1)].reachable_neighbours]
		[(0, 1), (2, 1), (1, 0), (1, 2)]
		>>> [n.position for n in hm.locations[(1, 2)].reachable_neighbours]
		[(0, 2), (2, 2), (1, 1)]
		'''
		current_location: Location = None
		best_signal_location: Location = None
		locations: typing.Dict[TPosition, Location] = {}

		grid_iter = (((y, x), c) for y, line in enumerate(lines) for x, c in enumerate(line))
		for position, c in grid_iter:
			location = Location(position, char_to_height(c))
			locations[position] = location

			if c == 'S': current_location = location
			if c == 'E': best_signal_location = location

		existing_positions = set(locations.keys())
		for position, location in locations.items():
			neighbours_position = get_neighbours(existing_positions, position)
			location.set_neighbours([locations.get(p) for p in neighbours_position])

		return HeightMap(
			locations = locations,
			current_location = current_location,
			best_signal_location = best_signal_location
		)

	def find_path_lenght(self) -> int:
		self.current_location.has_been_visited = True

		locations_at_current_step = [self.current_location]
		for step in count(1):
			locations_at_next_step = []
			for location in locations_at_current_step:
				for neightbour in location.reachable_neighbours:
					# Since going to an already visited location is equal or less effective
					# than taking the route that already visited that location
					if neightbour.has_been_visited: continue

					neightbour.has_been_visited = True
					locations_at_next_step.append(neightbour)

			if self.best_signal_location in locations_at_next_step:
				return step

			locations_at_current_step = locations_at_next_step

if __name__ == '__main__':
	import doctest
	logging.basicConfig(level=logging.DEBUG)
	doctest.testmod(optionflags=doctest.ELLIPSIS)