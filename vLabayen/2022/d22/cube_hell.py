from typing import Tuple, List, Callable, Tuple, Iterable, Dict, FrozenSet
from attrs import define, field, Factory
from data_models import Coordinate, Tile, Facing
from collections import defaultdict
from itertools import combinations

Coordinate3D = Tuple[int, int, int]

@define
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
	def starting_position(self) -> Coordinate3D:
		return self.x, self.y, self.z

	@property
	def current_position(self) -> Coordinate3D:
		return self.current_x, self.current_y, self.current_z

	@current_position.setter
	def current_position(self, value: Coordinate3D):
		self.current_x, self.current_y, self.current_z = value

	def copy(self) -> 'Point3D':
		return Point3D(self.x, self.y, self.z, self.current_x, self.current_y, self.current_z)

@define
class RotationInfo:
	incr_x: int
	incr_y: int
	is_rotation_axis: Callable[[Point3D], bool]
	is_rotation_oposed_axis: Callable[[Point3D], bool]

@define
class Cube3D:
	'''
	When a cube is rotated over the axis of C, both perpendicular faces to that axis move equal.
	The adyacent corners to C just move diagonally towards the advance direction.
	The oposing corner to C just move towards.
	C just does not move, since it's the origin of the rotation.

	A--B 		D--A
	|  | ---->  |  |
	D--C		B--C

	Visualizing the starting and ending cube touching..
	A--*--A			*--D--*			*--B--*
	|  |  |			|  |  |			|  |  |
	*--C--*			D--C--*			*--C--B
	'''
	points: List[Point3D]

	def _rotation_info(self, direction: Facing) -> RotationInfo:
		max_x = max(p.current_x for p in self.points)
		min_x = min(p.current_x for p in self.points)
		max_y = max(p.current_y for p in self.points)
		min_y = min(p.current_y for p in self.points)

		if direction == Facing.UP: return RotationInfo(
			incr_x = 0, incr_y = -1,
			is_rotation_axis        = lambda p: p.current_z == 0 and p.current_y == min_y,
			is_rotation_oposed_axis = lambda p: p.current_z == 1 and p.current_y == max_y,
		)
		if direction == Facing.RIGHT: return RotationInfo(
			incr_x = 1, incr_y = 0,
			is_rotation_axis        = lambda p: p.current_z == 0 and p.current_x == max_x,
			is_rotation_oposed_axis = lambda p: p.current_z == 1 and p.current_x == min_x,
		)
		if direction == Facing.DOWN: return RotationInfo(
			incr_x = 0, incr_y = 1,
			is_rotation_axis        = lambda p: p.current_z == 0 and p.current_y == max_y,
			is_rotation_oposed_axis = lambda p: p.current_z == 1 and p.current_y == min_y,
		)
		if direction == Facing.LEFT: return RotationInfo(
			incr_x = -1, incr_y = 0,
			is_rotation_axis        = lambda p: p.current_z == 0 and p.current_x == min_x,
			is_rotation_oposed_axis = lambda p: p.current_z == 1 and p.current_x == max_x,
		)

	def rotate(self, direction: Facing) -> 'Cube3D':
		rotation_info = self._rotation_info(direction)
		points = [p.copy() for p in self.points]

		for p in points:
			if rotation_info.is_rotation_axis(p): continue

			if rotation_info.is_rotation_oposed_axis(p): p.current_position = (
				p.current_x + (2 * rotation_info.incr_x),
				p.current_y + (2 * rotation_info.incr_y),
				p.current_z
			)
			else: p.current_position = (
				p.current_x + rotation_info.incr_x,
				p.current_y + rotation_info.incr_y,
				(0 if p.current_z == 1 else 1)
			)

		return Cube3D(points)

@define
class Face:
	position: Coordinate
	tiles: List[Tile] = field(repr=False)

	points: Tuple[Point, Point, Point, Point] = field(init=False, repr=False)
	def __attrs_post_init__(self):
		self.points = tuple(Point(position) for position in Point.get_coordinates(self.position))

	@staticmethod
	def get_coordinate(tile_position: Coordinate, side_size: int) -> Coordinate:
		''' Get the face coordinate of the given tile's position '''
		x, y = tile_position
		return (x - 1) // side_size, (y - 1) // side_size


def group_by_cube_face(tiles: Dict[Coordinate, Tile], side_size: int) -> List[Face]:
	faces = defaultdict(lambda: [])
	for tile in tiles.values():
		face_position = Face.get_coordinate(tile.position, side_size)
		faces[face_position].append(tile)

	return [Face(
		position = face_position,
		tiles = face_tiles
	) for face_position, face_tiles in faces.items()]

def get_neighbours(face_position: Coordinate, faces: Dict[Coordinate, Face]) -> Iterable[Tuple[Face, Facing]]:
	x, y = face_position

	top    = faces.get((x    , y - 1), None)
	right  = faces.get((x + 1, y    ), None)
	bottom = faces.get((x    , y + 1), None)
	left   = faces.get((x - 1, y    ), None)

	if top   : yield top   , Facing.UP
	if right : yield right , Facing.RIGHT
	if bottom: yield bottom, Facing.DOWN
	if left  : yield left  , Facing.LEFT

def get_matching_points(cube: Cube3D) -> List[Point3D]:
	return [point for point in cube.points if point.current_z == 0]

def rotate_and_unwrap(towards: Face, direction: Facing, cube: Cube3D, faces: Dict[Coordinate, Face]) -> Iterable[Tuple[Face, List[Point3D]]]:
	rotated_cube = cube.rotate(direction)

	yield (towards, get_matching_points(rotated_cube))
	for next_face, next_direction in get_neighbours(towards.position, faces):
		if next_direction == direction.oposing_direction(): continue
		for face, points in rotate_and_unwrap(next_face, next_direction, rotated_cube, faces):
			yield face, points


def unwrap(faces: Dict[Coordinate, Face]) -> Iterable[Tuple[Face, List[Point3D]]]:
	starting_face = next(iter(faces.values()))
	cube = Cube3D([Point3D(*p.position, z) for p in starting_face.points for z in {0, 1}])

	yield starting_face, get_matching_points(cube)
	for next_face, next_direction in get_neighbours(starting_face.position, faces):
		for face, points in rotate_and_unwrap(next_face, next_direction, cube, faces):
			yield face, points


def are_adyacent(p1: Coordinate3D, p2: Coordinate3D) -> bool:
	''' Return whether a pair of points are adyacent '''
	are_same_coordinate = [c1 == c2 for c1, c2 in zip(p1, p2)]
	return are_same_coordinate.count(True) == 2

def get_edge_points(points: List[Point3D]) -> Iterable[Tuple[Point3D, Point3D]]:
	''' Return the pair of points that make up a edge '''
	for p1, p2 in combinations(points, 2):
		if are_adyacent(p1.current_position, p2.current_position): yield p1, p2

def get_edge_border(p1: Point3D, p2: Point3D, max_x: int, min_x: int, max_y: int, min_y: int) -> Facing:
	''' Get which is the border of the face were the points are at '''
	if p1.current_x == p2.current_x == max_x: return Facing.RIGHT
	if p1.current_x == p2.current_x == min_x: return Facing.LEFT
	if p1.current_y == p2.current_y == max_y: return Facing.DOWN
	if p1.current_y == p2.current_y == min_y: return Facing.UP
	raise


@define
class Edge:
	face_1_position: Coordinate
	face_1_points: Tuple[Point3D, Point3D]
	face_1_border: Facing
	face_2_position: Coordinate
	face_2_points: Tuple[Point3D, Point3D]
	face_2_border: Facing

	def wrap(self, tile_position: Coordinate, face_position: Coordinate) -> Tuple[Coordinate, Facing]:
		pass

def get_edges(points: Dict[Coordinate, List[Point3D]]) -> Iterable[Edge]:
	''' Compute the edges of each face '''
	edges: Dict[FrozenSet[Coordinate3D], List[dict]] = defaultdict(lambda: [])

	for face_position, face_points in points.items():
		max_x = max(p.current_x for p in face_points)
		min_x = min(p.current_x for p in face_points)
		max_y = max(p.current_y for p in face_points)
		min_y = min(p.current_y for p in face_points)

		for p1, p2 in get_edge_points(face_points):
			edge_key = frozenset((p1.starting_position, p2.starting_position))
			edges[edge_key].append({
				'points': (p1, p2),
				'face_position': face_position,
				'border': get_edge_border(p1, p2, max_x, min_x, max_y, min_y),
			})

	for (face_1, face_2) in edges.values(): yield Edge(
		face_1_position = face_1['position'], face_1_points = face_1['points'], face_1_border = face_1['border'],
		face_2_position = face_2['position'], face_2_points = face_2['points'], face_2_border = face_2['border'],
	)
