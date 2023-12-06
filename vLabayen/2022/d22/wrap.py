from typing import Dict, List, Tuple
from attrs import define, field
from data_models import Coordinate, Tile, Face
from collections import defaultdict
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


@define
class CubeWrapper(Wrapper):
	tiles: Dict[Coordinate, Tile]

	def __attrs_post_init__(self):
		faces = group_by_cube_face(self.tiles)
		for face in faces: print(face)

	def get_right(self, tile: Tile) -> Tile:
		...

	def get_left(self, tile: Tile) -> Tile:
		...

	def get_down(self, tile: Tile) -> Tile:
		...

	def get_up(self, tile: Tile) -> Tile:
		...
