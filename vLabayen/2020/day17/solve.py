def add_neighbours(cubes):
	ylen = len(cubes[0]) + 2
	xlen = len(cubes[0][0]) + 2

	for zcoord,z in enumerate(cubes):
		for ycoord,y in enumerate(z):
			cubes[zcoord][ycoord] = [0] + cubes[zcoord][ycoord] + [0]
		cubes[zcoord] = [[0 for x in range(xlen)]] + cubes[zcoord] + [[0 for x in range(xlen)]]
	return [[[0 for x in range(xlen)] for y in range(ylen)]] + cubes + [[[0 for x in range(xlen)] for y in range(ylen)]]

def get_neighbours(cubes, zcoord, ycoord, xcoord):
	return [state for zc,z in enumerate(cubes[zcoord-1:zcoord+2]) for yc,y in enumerate(z[ycoord-1:ycoord+2]) for xc,state in enumerate(y[xcoord-1:xcoord+2]) if not (zc == 1 and yc == 1 and xc == 1)]

def copy_cubes(cubes):
	return [[[x for x in y] for y in z] for z in cubes]

def print_cubes(cubes, cycle):
	print(f'\nAfter {cycle} cycles')
	print('\n\n'.join(['\n'.join([''.join([('#' if x == 1 else '.') for x in y]) for y in z]) for z in cubes]))
	print()


with open('input.txt') as f:
#with open('example.txt') as f:
	boot_cubes = [[[(1 if c == '#' else 0) for c in line[:-1]] for line in f]]

#	print_cubes(boot_cubes, 0)

	cubes_cpy = copy_cubes(add_neighbours(boot_cubes))
	for cycle in range(6):
		cubes = add_neighbours(cubes_cpy)
		cubes_cpy = copy_cubes(cubes)

		zlen, ylen, xlen = len(cubes), len(cubes[0]), len(cubes[0][0])
		for zcoord,z in ((_zcoord, _z) for _zcoord,_z in enumerate(cubes) if _zcoord != 0 and _zcoord != zlen - 1):
			for ycoord,y in ((_ycoord, _y) for _ycoord,_y in enumerate(z) if _ycoord != 0 and _ycoord != ylen - 1):
				for xcoord,x in ((_xcoord, _x) for _xcoord,_x in enumerate(y) if _xcoord != 0 and _xcoord != xlen - 1):
					nsum = sum(get_neighbours(cubes, zcoord, ycoord, xcoord))
					if x == 1:
						if not (2 <= nsum <= 3):
							cubes_cpy[zcoord][ycoord][xcoord] = 0
					else:
						if nsum == 3:
							cubes_cpy[zcoord][ycoord][xcoord] = 1

		#print_cubes(cubes_cpy, cycle + 1)

	print(sum([state for z in cubes_cpy for y in z for state in y]))
