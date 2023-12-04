from typing import Tuple, Dict, List
import math
from itertools import product

from data_models import Tile, TileType, Facing, Step 
from wrap import Wrapper


def get_next(tile: Tile, facing: Facing, wrapper: Wrapper) -> Tile:
	if facing == Facing.RIGHT: return wrapper.get_right(tile)
	if facing == Facing.LEFT : return wrapper.get_left(tile)
	if facing == Facing.DOWN : return wrapper.get_down(tile)
	if facing == Facing.UP   : return wrapper.get_up(tile)


def apply_step(tile: Tile, facing: Facing, step: Step, wrapper: Wrapper) -> Tuple[Tile, Facing]:
	if step == 'R': return tile, facing.rotate_clockwise()
	if step == 'L': return tile, facing.rotate_counterclockwise()

	for _ in range(step):
		next = get_next(tile, facing, wrapper)
		if next.type == TileType.WALL: return tile, facing
		tile = next
	
	return tile, facing


def top_left_tile(tiles: List[Tile]) -> Tile:
	return min((tile for tile in tiles), key = lambda tile: (tile.position[1], tile.position[0]))
