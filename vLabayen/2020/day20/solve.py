import re
from itertools import product, repeat
from functools import reduce

def border_rotate_90(img): return {'up':img['right'], 'down':img['left'], 'left':img['up'][::-1], 'right':img['down'][::-1]}
def border_rotate_180(img): return border_rotate_90(border_rotate_90(img))
def border_rotate_270(img): return border_rotate_90(border_rotate_180(img))
def border_flip(img): return {'up':img['down'], 'down':img['up'], 'left':img['left'][::-1], 'right':img['right'][::-1]}
def border_flip_90(img): return border_rotate_90(border_flip(img))
def border_flip_180(img): return border_rotate_180(border_flip(img))
def border_flip_270(img): return border_rotate_270(border_flip(img))
def border_options(img): return {
	'0' : img, '90' : border_rotate_90(img), '180' : border_rotate_180(img), '270' :border_rotate_270(img),
	'f' : border_flip(img), 'f90' : border_flip_90(img), 'f180' : border_flip_180(img), 'f270' : border_flip_270(img)
}
def border_apply_transformation(img, transform): return border_options(img)[transform]

def neighbour_options(id, img, borders):
	options = {'up':None, 'down':None, 'left':None, 'right':None}
	for _id,_img in borders.items():
		if id == _id: continue

		for opt, __img in border_options(_img).items():
			for side, _side in [*zip(['up','down', 'left', 'right'], ['down', 'up', 'right', 'left'])]:
				if img[side] == __img[_side]: options[side] = f'{_id}_{opt}'
	return options

def side2incr(side): return {'up':{'y':-1, 'x':0}, 'down':{'y':1, 'x':0}, 'left':{'y':0, 'x':-1}, 'right':{'y':0, 'x':1}}[side]

def image_rotate_90(img): return [''.join(row) for row in reversed([*zip(*img)])]
def image_rotate_180(img): return image_rotate_90(image_rotate_90(img))
def image_rotate_270(img): return image_rotate_90(image_rotate_180(img))
def image_flip(img): return img[::-1]
def image_flip_90(img): return image_rotate_90(image_flip(img))
def image_flip_180(img): return image_rotate_180(image_flip(img))
def image_flip_270(img): return image_rotate_270(image_flip(img))
def image_options(img): return {
	'0': img, '90': image_rotate_90(img), '180': image_rotate_180(img), '270': image_rotate_270(img),
	'f': image_flip(img), 'f90': image_flip_90(img), 'f180': image_flip_180(img), 'f270': image_flip_270(img)
}
def image_apply_transformation(img, transform): return image_options(img)[transform]

def get_image(tiles_positions, tiles, sidelen):
	image = []
	for row in tiles_positions:
		imgs = [image_apply_transformation(tiles[id], transform) for id, transform in (r.split('_') for r in row)]
		image += [''.join([f'{imgs[i][nrow][1:-1]}' for i in range(sidelen)]) for nrow in range(1, len(imgs[0]) - 1)]
#		image += [' '.join([f'{imgs[i][nrow]}' for i in range(sidelen)]) for nrow in range(len(imgs[0]))]
#		image.append(' '*len(image[-1]))
	return image

def print_image(img):
	for row in img: print(row)

def find_pattern(img, pattern):
	img_cpy = [row for row in img]
	pattern_h, pattern_w = len(pattern), len(pattern[0])
	img_h, img_w = len(img), len(img[0])

	for h_slice in range(img_h - pattern_h + 1):
		for w_slice in range(img_w - pattern_w + 1):
			search_area = [line[w_slice:pattern_w + w_slice] for line in img_cpy[h_slice:pattern_h + h_slice]]
			if match_pattern(search_area, pattern):
				for pattern_row,replace_row in enumerate(range(h_slice, pattern_h + h_slice)):
					replaced_area_row = ''.join('O' if pattern[pattern_row][i] == '#' else c for i,c in enumerate(img_cpy[replace_row][w_slice:pattern_w + w_slice]))
					img_cpy[replace_row] = img_cpy[replace_row][:w_slice] + replaced_area_row + img_cpy[replace_row][pattern_w + w_slice:]

	return img_cpy
def match_pattern(area, pattern):
	for r,row in enumerate(area):
		for c,col in enumerate(row):
			if pattern[r][c] == '#' and col != '#': return False
	return True

#with open('example.txt') as f:
with open('input.txt') as f:
	tiles = {re.match('Tile (\d+):', id).groups()[0] : img.split('\n') for id,img in (tile.split('\n', 1) for tile in f.read().strip().split('\n\n'))}
	borders = {id : {
		'up' : img[0],
		'down' : img[-1],
		'left' : ''.join([row[0] for row in img]),
		'right' :  ''.join([row[-1] for row in img])
	} for id, img in tiles.items()}

	corners = [id for id,img in borders.items() if len([side for side,opt in neighbour_options(id, img, borders).items() if opt is not None]) == 2]
#	print(reduce(lambda x,y: x*y, (int(c) for c in corners)))

	sidelen = int(len(borders) ** 0.5)
	tiles_positions = [[0 for _ in repeat(None, sidelen)] for _ in repeat(None, sidelen)]

	# Pick any corner
	c = corners[0]
	corner_options = neighbour_options(c, borders[c], borders)
	corner_sides = [side for side,opt in corner_options.items() if opt is None]
	corner_position = {'y' : 0 if 'up' in corner_sides else sidelen - 1, 'x' : 0 if 'left' in corner_sides else sidelen - 1}
	tiles_positions[corner_position['y']][corner_position['x']] = f'{c}_0'

	current_position, current_options = corner_position, corner_options
	position_incr = {'y': 1 if 'up' in corner_sides else -1, 'x': 1 if 'left' in corner_sides else -1}
	for _ in repeat(None, sidelen):
		for _ in repeat(None, sidelen):
			for side,tile,transform in ((_side,) + tuple(opt.split('_')) for _side,opt in current_options.items() if opt is not None):
				incr = side2incr(side)
				neighbour_position = {'y' : current_position['y'] + incr['y'], 'x' : current_position['x'] + incr['x']}
				if tiles_positions[neighbour_position['y']][neighbour_position['x']] != 0: continue
				else: tiles_positions[neighbour_position['y']][neighbour_position['x']] = f'{tile}_{transform}'

			current_position = {'y' : current_position['y'], 'x' : current_position['x'] + position_incr['x']}
			if 0 <= current_position['x'] < sidelen:
				tile, transform = tiles_positions[current_position['y']][current_position['x']].split('_')
				current_options = neighbour_options(tile, border_apply_transformation(borders[tile], transform), borders)

		current_position = {'y' : current_position['y'] + position_incr['y'], 'x' : corner_position['x']}
		if 0 <= current_position['y'] < sidelen:
			tile, transform = tiles_positions[current_position['y']][current_position['x']].split('_')
			current_options = neighbour_options(tile, border_apply_transformation(borders[tile], transform), borders)

	full_img = get_image(tiles_positions, tiles, sidelen)
	sea_monster_pattern = [
		'                  # ',
		'#    ##    ##    ###',
		' #  #  #  #  #  #   '
	]

	water_roughness = []
	for opt in image_options(full_img).values():
		matched_pattern = find_pattern(opt, sea_monster_pattern)
		water_roughness.append(sum(row.count('#') for row in matched_pattern))
	print(min(water_roughness))
