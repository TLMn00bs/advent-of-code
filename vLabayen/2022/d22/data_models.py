from typing import Tuple, Union, Literal, List
from attrs import define, field, Factory
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

@define(hash=True, frozen=True)
class Point:
	position: Coordinate

	@staticmethod
	def get_coordinates(face_position: Coordinate) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
		x, y = face_position
		return (
			(x, y    ), (x + 1, y    ),
			(x, y + 1), (x + 1, y + 1)
		)

@define
class Point3D:
	x: int = field(repr=False)
	y: int = field(repr=False)
	z: int = field(repr=False)

	# Keep the starting position inmutable
	current_x: int = field(repr=True, default=Factory(lambda self: self.x, takes_self=True))
	current_y: int = field(repr=True, default=Factory(lambda self: self.y, takes_self=True))
	current_z: int = field(repr=True, default=Factory(lambda self: self.z, takes_self=True))

	@property
	def starting_position(self) -> Tuple[int, int, int]:
		return self.x, self.y, self.x

	@property
	def current_position(self) -> Tuple[int, int, int]:
		return self.current_x, self.current_y, self.current_z

	@current_position.setter
	def current_position(self, value: Tuple[int, int, int]):
		self.current_x, self.current_y, self.current_z = value

	def copy(self) -> 'Point3D':
		return Point3D(self.x, self.y, self.z, self.current_x, self.current_y, self.current_z)

@define
class Cube3D:
	points: List[Point3D]

	def _rotation_info(self, direction: Facing) -> Tuple[int, int]:
		return {
			Facing.UP   : ( 0, -1),
			Facing.RIGHT: ( 1,  0),
			Facing.DOWN : ( 0,  1),
			Facing.LEFT : (-1,  0),
		}[direction]

	def rotate(self, direction: Facing) -> 'Cube3D':
		points = [p.copy() for p in self.points]
		incr_x, incr_y = self._rotation_info(direction)

		# Suponiendo que Facing.UP
		max_y = max(p.current_y for p in points)
		min_y = min(p.current_y for p in points)

		if direction == Facing.UP:
			for p in points:
				# Eje de rotacion
				if p.current_z == 0 and p.current_y == max_y: continue

				# Esquina opuesta al eje de rotacion
				if p.current_z == 1 and p.current_y == max_y - 1:
					p.current_position = p.current_x, p.current_y + (2 * incr_y), p.current_z

				# Esquinas adyacentes al eje de rotacion
				else:
					p.current_position = p.current_x, p.current_y + incr_y, (0 if p.current_z == 1 else 1)


		if direction == Facing.DOWN:
			for p in points:
				if p.current_z == 0 and p.current_y == min_y: continue

				# Esquina opuesta al eje de rotacion
				if p.current_z == 1 and p.current_y == min_y + 1:
					p.current_position = p.current_x, p.current_y + (2 * incr_y), p.current_z

				# Esquinas adyacentes al eje de rotacion
				else:
					p.current_position = p.current_x, p.current_y + incr_y, (0 if p.current_z == 1 else 1)

		return Cube3D(points)

@define
class Face:
	position: Coordinate
	side_size: int
	tiles: List[Tile] = field(repr=False)

	points: Tuple[Point, Point, Point, Point] = field(init=False, repr=False)
	def __attrs_post_init__(self):
		self.points = tuple(Point(position) for position in Point.get_coordinates(self.position))

	@staticmethod
	def get_coordinate(tile_position: Coordinate, side_size: int) -> Coordinate:
		''' Get the face coordinate of the given tile's position '''
		x, y = tile_position
		return (x - 1) // side_size, (y - 1) // side_size
