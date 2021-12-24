#!/bin/python3

def next_infinite_field(current, enhance_img):
	first_pixel, last_pixel = enhance_img[0], enhance_img[-1]
	return first_pixel if current == '.' else last_pixel

def bin_bit(x, y, light, dark, infinite_field):
	if (x, y) in light: return '1'
	if (x, y) in dark: return '0'
	return '1' if infinite_field == '#' else '0'

def bin_code(x, y, light, dark, infinite_field): return int(''.join(bin_bit(_x, _y, light, dark, infinite_field) for _x in range(x - 1, x + 2) for _y in range(y - 1, y + 2)), 2)

def img_boundaries(input_img): return (
	min(x for x,y in input_img),	# min_x
	max(x for x,y in input_img),	# max_x
	min(y for x,y in input_img),	# min_y
	max(y for x,y in input_img)	# max_y
)

def enhance(light, dark, infinite_field, enhance_img):
	min_x, max_x, min_y, max_y = img_boundaries(light.union(dark))
	pixels_gen = ((x, y) for x in range(min_x - 1, max_x + 2) for y in range(min_y - 1, max_y + 2))

	img = [(x, y, enhance_img[bin_code(x, y, light, dark, infinite_field)]) for x, y in pixels_gen]
	light = {(x, y) for x, y, c in img if c == '#'}
	dark  = {(x, y) for x, y, c in img if c == '.'}
	return light, dark

def display_img(img):
	min_x, max_x, min_y, max_y = img_boundaries(img)
	for x in range(min_x - 1, max_x + 2):
		print(''.join('#' if (x,y) in img else '.' for y in range(min_y - 1, max_y + 2)))
	print()

def enhance_n_times(file, n):
	with open(file, 'r') as f:
		enhance_img = f.readline().strip()
		f.readline()
		input_img = [(x, y, c) for x, line in enumerate(f) for y, c in enumerate(line.strip())]

	light_pixels = {(x, y) for x,y,c in input_img if c == '#'}
	dark_pixels  = {(x, y) for x,y,c in input_img if c == '.'}
	infinite_field = '.'

	for i in range(n):
		light_pixels, dark_pixels = enhance(light_pixels, dark_pixels, infinite_field, enhance_img)
		infinite_field = next_infinite_field(infinite_field, enhance_img)

	print(len(light_pixels))

def p1(args): enhance_n_times(args.file, 2)
def p2(args): enhance_n_times(args.file, 50)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
