from typing import Dict, List, Tuple, Iterable
from attrs import define, field
from data_models import Coordinate, Tile, Face, Point3D, Cube3D, Facing
from collections import defaultdict, Counter
import math
from abc import ABC, abstractmethod

class Wrapper(ABC):
	@abstractmethod
	def get_right(self, tile: Tile) -> Tile: ...
	@abstractmethod
	def get_left (self, tile: Tile) -> Tile: ...
	@abstractmethod
	def get_down (self, tile: Tile) -> Tile: ...
	@abstractmethod
	def get_up   (self, tile: Tile) -> Tile: ...

@define
class LinearWrapper(Wrapper):
	tiles: Dict[Coordinate, Tile]

	row_edges: Dict[int, Tuple[int, int]] = field(init=False, factory=lambda: defaultdict(lambda: (math.inf, -math.inf)))
	col_edges: Dict[int, Tuple[int, int]] = field(init=False, factory=lambda: defaultdict(lambda: (math.inf, -math.inf)))
	def __attrs_post_init__(self):
		for (x, y) in self.tiles.keys():
			self.row_edges[y] = (min(self.row_edges[y][0], x), max(self.row_edges[y][1], x))
			self.col_edges[x] = (min(self.col_edges[x][0], y), max(self.col_edges[x][1], y))

	def wrap_right(self, position: Coordinate) -> Coordinate:
		_, y = position
		return (self.row_edges[y][0], y)

	def wrap_left(self, position: Coordinate) -> Coordinate:
		_, y = position
		return (self.row_edges[y][1], y)

	def wrap_down(self, position: Coordinate) -> Coordinate:
		x, _ = position
		return (x, self.col_edges[x][0])

	def wrap_up(self, position: Coordinate) -> Coordinate:
		x, _ = position
		return (x, self.col_edges[x][1])


	def get_right(self, tile: Tile) -> Tile:
		x, y = tile.position
		return self.tiles.get((x + 1, y)) or self.tiles[self.wrap_right(tile.position)]

	def get_left(self, tile: Tile) -> Tile:
		x, y = tile.position
		return self.tiles.get((x - 1, y)) or self.tiles[self.wrap_left(tile.position)]

	def get_down(self, tile: Tile) -> Tile:
		x, y = tile.position
		return self.tiles.get((x, y + 1)) or self.tiles[self.wrap_down(tile.position)]

	def get_up(self, tile: Tile) -> Tile:
		x, y = tile.position
		return self.tiles.get((x, y - 1)) or self.tiles[self.wrap_up(tile.position)]



def group_by_cube_face(tiles: Dict[Coordinate, Tile]) -> List[Face]:
	side_size = int(math.sqrt(len(tiles) / 6))

	faces = defaultdict(lambda: [])
	for tile in tiles.values():
		face_position = Face.get_coordinate(tile.position, side_size)
		faces[face_position].append(tile)

	return [Face(
		position = face_position,
		side_size = side_size,
		tiles = face_tiles
	) for face_position, face_tiles in faces.items()]

def get_middle_face(faces: Iterable[Face]) -> Face:
	points_count = Counter(p for face in faces for p in face.points)
	_, middle_face = max((sum(points_count[p] for p in face.points), face) for face in faces)
	return middle_face

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

def unwrap(towards: Face, direction: Facing, cube: Cube3D, faces: Dict[Coordinate, Face]) -> Iterable[Tuple[Face, List[Point3D]]]:
	rotated_cube = cube.rotate(direction)

	floor_points = [point for point in rotated_cube.points if point.current_z == 0]
	yield (towards, floor_points)

	for next_face, next_direction in get_neighbours(towards.position, faces):
		if next_direction == direction.oposing_direction(): continue
		for face, points in unwrap(next_face, next_direction, rotated_cube, faces):
			yield face, points

@define
class CubeWrapper(Wrapper):
	tiles: Dict[Coordinate, Tile]

	def __attrs_post_init__(self):
		faces = {face.position: face for face in group_by_cube_face(self.tiles)}
		middle_face = get_middle_face(faces.values())
		cube = Cube3D([Point3D(*p.position, z) for p in middle_face.points for z in {0, 1}])

		neighbour_faces = get_neighbours(middle_face.position, faces)
		for neighbour, direction in neighbour_faces:
			for face, points in unwrap(neighbour, direction, cube, faces):
				print(face, points)


	def get_right(self, tile: Tile) -> Tile:
		...

	def get_left(self, tile: Tile) -> Tile:
		...

	def get_down(self, tile: Tile) -> Tile:
		...

	def get_up(self, tile: Tile) -> Tile:
		...
