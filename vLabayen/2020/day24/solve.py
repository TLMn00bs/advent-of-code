from itertools import repeat, product
import re

def move(x, y, dir):
	xincr, yincr = {
		'e' : (1, 0),
		'se' : (1, -1),
		'sw' : (0, -1),
		'w' : (-1, 0),
		'nw' : (-1, 1),
		'ne' : (0, 1)
	}[dir]
	return (x + xincr, y + yincr)

def neighbours(x,y): return [(x + _x, y + _y) for _x,_y in product([0,1,-1], [0,1,-1]) if _x != _y]
def add_neighbours(tiles):
	tiles_cpy = {pos : tile for pos,tile in tiles.items()}
	for pos, tile in tiles.items():
		for neighbour in neighbours(*pos):
			if neighbour not in tiles_cpy: tiles_cpy[neighbour] = False
	return tiles_cpy

tiles = {}
with open('input.txt') as f:
	instructions = [line[:-1] for line in f]

	for inst in instructions:
		pos = (0, 0)
		for dir in re.findall('s?e|n?e|s?w|n?w', inst): pos = move(*pos, dir)

		if pos not in tiles: tiles[pos] = True # True = black, False = white
		else: tiles[pos] = not tiles[pos]

	print(sum(1 for tile in tiles.values() if tile))

	tiles = add_neighbours(tiles)
	for _ in repeat(None, 100):
		tiles_cpy = add_neighbours(tiles)

		to_flip = []
		for pos, tile in tiles.items():
			num_blacks = sum(1 for neighbour in neighbours(*pos) if tiles_cpy[neighbour])
			if tile: # Is black
				if 0 == num_blacks or num_blacks > 2: to_flip.append(pos)
			else: # Is white
				if num_blacks == 2: to_flip.append(pos)

		for pos in to_flip:
			tiles_cpy[pos] = not tiles_cpy[pos]
		tiles = tiles_cpy

	print(sum(1 for tile in tiles.values() if tile))
