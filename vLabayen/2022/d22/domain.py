from typing import Tuple, Dict, Union, Literal, List
from attrs import define
from enum import Enum


Coordinate = Tuple[int, int]

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

	def rotate_clockwise(self) -> 'Facing':
		return Facing((self.value + 1) % 4)
	
	def rotate_counterclockwise(self) -> 'Facing':
		return Facing((self.value - 1) % 4)

@define
class Tile:
	position: Coordinate
	type: TileType

	right: 'Tile'
	left : 'Tile'
	down : 'Tile'
	up   : 'Tile'

	def __str__(self) -> str:
		return f'Tile(position={self.position}, type={self.type.name}, right={self.right.position}, left={self.left.position}, down={self.down.position}, up={self.up.position})'


def wrap_right(position: Coordinate, tiles: Dict[Coordinate, Tile]) -> Tile:
	_, y = position
	*_, tile = min(((_x, _y, tile) for (_x, _y), tile in tiles.items() if y == _y), key = lambda item: item[0])
	return tile

def wrap_left(position: Coordinate, tiles: Dict[Coordinate, Tile]) -> Tile:
	_, y = position
	*_, tile = max(((_x, _y, tile) for (_x, _y), tile in tiles.items() if y == _y), key = lambda item: item[0])
	return tile

def wrap_up(position: Coordinate, tiles: Dict[Coordinate, Tile]) -> Tile:
	x, _ = position
	*_, tile = max(((_x, _y, tile) for (_x, _y), tile in tiles.items() if x == _x), key = lambda item: item[1])
	return tile

def wrap_down(position: Coordinate, tiles: Dict[Coordinate, Tile]) -> Tile:
	x, _ = position
	*_, tile = min(((_x, _y, tile) for (_x, _y), tile in tiles.items() if x == _x), key = lambda item: item[1])
	return tile


Step = Union[int, Literal['R', 'L']]

@define
class Path:
	steps: List[Step]

def get_next(tile: Tile, facing: Facing) -> Tile:
	if facing == Facing.RIGHT: return tile.right
	if facing == Facing.LEFT : return tile.left
	if facing == Facing.DOWN : return tile.down
	if facing == Facing.UP   : return tile.up

def apply_step(tile: Tile, facing: Facing, step: Step) -> Tuple[Tile, Facing]:
	if step == 'R': return tile, facing.rotate_clockwise()
	if step == 'L': return tile, facing.rotate_counterclockwise()

	for _ in range(step):
		next = get_next(tile, facing)
		if next.type == TileType.WALL: return tile, facing
		tile = next
	
	return tile, facing