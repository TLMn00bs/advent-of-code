with open('input.txt') as f: grid = [[char for char in line] for line in f.read()[:-1].split('\n')]

#A efectos prácticos, los laterales, y las partes superior e inferior estan rodeados de suelo
grid = [['.']*(len(grid[0])+2)] + [['.'] + line + ['.'] for line in grid] + [['.']*(len(grid[0])+2)]

def apply_rules(grid):
	new_grid = [[c for c in r] for r in grid]

	#Skip first and last rows as the are all floor, as well as first and last position in a row
	for i,row in ((_i,_row) for _i,_row in enumerate(grid) if 0 < _i < len(grid) - 1):
		for j,seat in ((_j,_seat) for _j,_seat in enumerate(row) if 0 < _j < len(row) - 1):
			if seat == '.': continue

			adj_seats = [adj_seat for adj_seat in [
				grid[i-1][j-1], grid[i-1][j], grid[i-1][j+1],
				grid[i  ][j-1],               grid[i  ][j+1],
				grid[i+1][j-1], grid[i+1][j], grid[i+1][j+1]
			] if adj_seat != '.']

			if seat == 'L' and adj_seats.count('#') == 0: new_grid[i][j] = '#'
			elif seat == '#' and adj_seats.count('#') >= 4: new_grid[i][j] = 'L'
	return new_grid

def print_grid(grid):
	for row in grid: print(''.join(row))
	print()


#print_grid(grid)
#while True:
#	grid_iter = apply_rules(grid)
#	print_grid(grid_iter)

#	if grid_iter == grid:
#		print([seat for row in grid_iter for seat in row].count('#'))
#		break

#	grid = grid_iter


# Puzzle 2
with open('input.txt') as f: grid = [[char for char in line] for line in f.read()[:-1].split('\n')]
#with open('example.txt') as f: grid = [[char for char in line] for line in f.read()[:-1].split('\n')]
grid = [['.']*(len(grid[0])+2)] + [['.'] + line + ['.'] for line in grid] + [['.']*(len(grid[0])+2)]


def get_adj_seat(grid, i,j, iincr = 0, jincr = 0):
	icount = i + iincr
	jcount = j + jincr

	while 0 <= icount < len(grid) and 0 <= jcount < len(grid[0]):
		if grid[icount][jcount] != '.': return grid[icount][jcount]

		icount += iincr
		jcount += jincr

	return '.'

def get_adj_seats(grid, i, j):
	return [adj_seat for adj_seat in [
		get_adj_seat(grid, i, j, iincr=-1, jincr=-1), get_adj_seat(grid, i, j, iincr=-1), get_adj_seat(grid, i, j, iincr=-1, jincr=1),
		get_adj_seat(grid, i, j,           jincr=-1),                                     get_adj_seat(grid, i, j,           jincr=1),
		get_adj_seat(grid, i, j, iincr=1 , jincr=-1), get_adj_seat(grid, i, j, iincr=1 ), get_adj_seat(grid, i, j, iincr=1 , jincr=1)
	] if adj_seat != '.']


def apply_rules(grid):
	new_grid = [[c for c in r] for r in grid]

	for i,row in ((_i,_row) for _i,_row in enumerate(grid) if 0 < _i < len(grid) - 1):
		for j,seat in ((_j,_seat) for _j,_seat in enumerate(row) if 0 < _j < len(row) - 1):
			if seat == '.': continue

			adj_seats = get_adj_seats(grid, i, j)

			if seat == 'L' and adj_seats.count('#') == 0: new_grid[i][j] = '#'
			elif seat == '#' and adj_seats.count('#') >= 5: new_grid[i][j] = 'L'
	return new_grid

#print_grid(grid)
while True:
       grid_iter = apply_rules(grid)
#       print_grid(grid_iter)

       if grid_iter == grid:
               print([seat for row in grid_iter for seat in row].count('#'))
               break

       grid = grid_iter
