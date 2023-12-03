from typing import Iterable, Tuple, List, Dict
from domain import Tile, Coordinate, TileType, Path
from domain import wrap_right, wrap_left, wrap_down, wrap_up
from itertools import takewhile
import re

def parse_tiles(raw_tiles: Iterable[Tuple[int, int, str]]) -> List[Tile]:
	tiles: Dict[Coordinate, Tile] = {}
	for x, y, c in raw_tiles:
		if not TileType.valid_type(c): continue
		tiles[(x, y)] = Tile(
			(x, y), TileType(c),
			None, None, None, None		# type: ignore
		)

	for (x, y), tile in tiles.items():
		tile.right = tiles.get((x + 1, y)) or wrap_right((x, y), tiles)
		tile.left  = tiles.get((x - 1, y)) or wrap_left ((x, y), tiles)
		tile.down  = tiles.get((x, y + 1)) or wrap_down ((x, y), tiles)
		tile.up    = tiles.get((x, y - 1)) or wrap_up   ((x, y), tiles)

	return list(tiles.values())


parse_path_rgx = re.compile('([0-9]+|L|R)')
def parse_path(raw_path: str) -> Path:
	steps = parse_path_rgx.findall(raw_path)
	return Path([int(step) if step.isnumeric() else step for step in steps])


def read_file(file: str) -> Tuple[List[Tile], Path]:
	with open(file, 'r') as f:
		lines_gen = (l.rstrip() for l in f)
		tiles_lines = ((y, line) for y, line in enumerate(takewhile(lambda line: line != '', lines_gen)))

		tiles = parse_tiles((x + 1, y + 1, c) for y, line in tiles_lines for x, c in enumerate(line))
		path = parse_path(next(lines_gen))

	return tiles, path
