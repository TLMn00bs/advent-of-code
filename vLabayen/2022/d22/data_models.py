from typing import Tuple, Union, Literal, List
from attrs import define
from enum import Enum

Coordinate = Tuple[int, int]
Step = Union[int, Literal['R', 'L']]

class TileType(Enum):
	OPEN = '.'
	WALL = '#'

	@staticmethod
	def valid_type(c: str) -> bool:
		return c in TileType._value2member_map_

class Facing(Enum):
	RIGHT = 0
	DOWN  = 1
	LEFT  = 2
	UP    = 3

	def __repr__(self) -> str: return self.name

	def rotate_clockwise(self) -> 'Facing':
		return Facing((self.value + 1) % 4)
	
	def rotate_counterclockwise(self) -> 'Facing':
		return Facing((self.value - 1) % 4)

	def oposing_direction(self) -> 'Facing':
		return Facing((self.value + 2) % 4)

@define
class Tile:
	position: Coordinate
	type: TileType

	def __str__(self) -> str: return f'Tile(position={self.position}, type={self.type.name}'

@define
class Path:
	steps: List[Step]
