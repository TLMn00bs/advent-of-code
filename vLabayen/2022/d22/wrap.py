from typing import Dict, Tuple
from attrs import define, field
from data_models import Coordinate, Tile, Facing
from cube_hell import Face, Edge, group_by_cube_face, unwrap, get_edges
from collections import defaultdict
import math
from abc import ABC, abstractmethod

@define
class Wrapper(ABC):
	tiles: Dict[Coordinate, Tile]

	@abstractmethod
	def wrap_right(self, tile: Coordinate) -> Tuple[Coordinate, Facing]: ...
	@abstractmethod
	def wrap_left (self, tile: Coordinate) -> Tuple[Coordinate, Facing]: ...
	@abstractmethod
	def wrap_down (self, tile: Coordinate) -> Tuple[Coordinate, Facing]: ...
	@abstractmethod
	def wrap_up   (self, tile: Coordinate) -> Tuple[Coordinate, Facing]: ...

	def get_right(self, tile: Tile) -> Tuple[Tile, Facing]:
		x, y = tile.position
		next_tile = self.tiles.get((x + 1, y), None)
		if next_tile is not None: return next_tile, Facing.RIGHT
		
		next_tile_position, next_facing = self.wrap_right(tile.position)
		return self.tiles[next_tile_position], next_facing

	def get_left(self, tile: Tile) -> Tuple[Tile, Facing]:
		x, y = tile.position
		next_tile = self.tiles.get((x - 1, y), None)
		if next_tile is not None: return next_tile, Facing.LEFT
		
		next_tile_position, next_facing = self.wrap_left(tile.position)
		return self.tiles[next_tile_position], next_facing

	def get_down(self, tile: Tile) -> Tuple[Tile, Facing]:
		x, y = tile.position
		next_tile = self.tiles.get((x, y + 1), None)
		if next_tile is not None: return next_tile, Facing.DOWN
		
		next_tile_position, next_facing = self.wrap_down(tile.position)
		return self.tiles[next_tile_position], next_facing

	def get_up(self, tile: Tile) -> Tuple[Tile, Facing]:
		x, y = tile.position
		next_tile = self.tiles.get((x, y - 1), None)
		if next_tile is not None: return next_tile, Facing.UP
		
		next_tile_position, next_facing = self.wrap_up(tile.position)
		return self.tiles[next_tile_position], next_facing

@define
class LinearWrapper(Wrapper):
	row_edges: Dict[int, Tuple[int, int]] = field(init=False, factory=lambda: defaultdict(lambda: (math.inf, -math.inf)))
	col_edges: Dict[int, Tuple[int, int]] = field(init=False, factory=lambda: defaultdict(lambda: (math.inf, -math.inf)))
	def __attrs_post_init__(self):
		for (x, y) in self.tiles.keys():
			self.row_edges[y] = (min(self.row_edges[y][0], x), max(self.row_edges[y][1], x))
			self.col_edges[x] = (min(self.col_edges[x][0], y), max(self.col_edges[x][1], y))

	def wrap_right(self, position: Coordinate) -> Tuple[Coordinate, Facing]:
		_, y = position
		return (self.row_edges[y][0], y), Facing.RIGHT

	def wrap_left(self, position: Coordinate) -> Tuple[Coordinate, Facing]:
		_, y = position
		return (self.row_edges[y][1], y), Facing.LEFT

	def wrap_down(self, position: Coordinate) -> Tuple[Coordinate, Facing]:
		x, _ = position
		return (x, self.col_edges[x][0]), Facing.DOWN

	def wrap_up(self, position: Coordinate) -> Tuple[Coordinate, Facing]:
		x, _ = position
		return (x, self.col_edges[x][1]), Facing.UP


@define
class CubeWrapper(Wrapper):
	tiles: Dict[Coordinate, Tile]

	side_size: int = field(init=False, repr=False)
	edges: Dict[Tuple[Coordinate, Facing], Edge] = field(init=False, factory=dict)
	def __attrs_post_init__(self):
		self.side_size = int(math.sqrt(len(self.tiles) / 6))

		faces = {face.position: face for face in group_by_cube_face(self.tiles, self.side_size)}
		points = {face.position: points for face, points in unwrap(faces)}
		for edge in get_edges(points, self.side_size):
			self.edges[(edge.face_1_position, edge.face_1_border)] = edge
			self.edges[(edge.face_2_position, edge.face_2_border)] = edge


	def wrap_up(self, position: Coordinate) -> Coordinate:
		face_position = Face.get_coordinate(position, self.side_size)
		edge = self.edges[(face_position, Facing.UP)]
		new_position, new_facing = edge.wrap(position, face_position)


	def get_right(self, tile: Tile) -> Tile:
		...

	def get_left(self, tile: Tile) -> Tile:
		...

	def get_down(self, tile: Tile) -> Tile:
		...

	def get_up(self, tile: Tile) -> Tile:
		x, y = tile.position
		return self.tiles.get((x, y - 1)) or self.tiles[self.wrap_up(tile.position)]
