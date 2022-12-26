import typing
from dataclasses import dataclass
from functools import reduce

@dataclass
class Grid:
	grid: typing.List[typing.List[int]]

	@staticmethod
	def from_text(lines: typing.List[str]):
		''' Creates a grid from it's text definition
		
		>>> Grid.from_text([
		...		'30373',
		...		'25512',
		...		'65332',
		...		'33549',
		...		'35390',
		... ])
		Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
		'''
		return Grid([[int(tree) for tree in row] for row in lines])

	def __len__(self) -> int: len(self.grid)
	def __getitem__(self, position: typing.Tuple[int, int]) -> int:
		x, y = position
		return self.grid[y][x]

	def size(self) -> typing.Tuple[int, int]:
		return len(self.grid), len(self.grid[0])

	def get_left_trees(self, x: int, y: int) -> typing.List[int]:
		''' Return all the trees at the left of the given x, y
		
		>>> g = Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
		>>> g.get_left_trees(1, 1)
		[2]
		>>> g.get_left_trees(2, 1)
		[5, 2]
		>>> g.get_left_trees(1, 2)
		[6]
		>>> g.get_left_trees(3, 3)
		[5, 3, 3]
		'''
		return list(reversed(self.grid[y][:x]))

	def get_right_trees(self, x: int, y: int) -> typing.List[int]:
		''' Return all the trees at the right of the given x, y
		
		>>> g = Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
		>>> g.get_right_trees(1, 1)
		[5, 1, 2]
		>>> g.get_right_trees(2, 1)
		[1, 2]
		>>> g.get_right_trees(1, 2)
		[3, 3, 2]
		>>> g.get_right_trees(3, 3)
		[9]
		'''
		return self.grid[y][x+1:]

	def get_top_trees(self, x: int, y: int) -> typing.List[int]:
		''' Return all the trees at the top of the given x, y
		
		>>> g = Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
		>>> g.get_top_trees(1, 1)
		[0]
		>>> g.get_top_trees(2, 1)
		[3]
		>>> g.get_top_trees(1, 2)
		[5, 0]
		>>> g.get_top_trees(3, 3)
		[3, 1, 7]
		'''
		return list(reversed([row[x] for row in self.grid][:y]))

	def get_bottom_trees(self, x: int, y: int) -> typing.List[int]:
		''' Return all the trees at the bottom of the given x, y
		
		>>> g = Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
		>>> g.get_bottom_trees(1, 1)
		[5, 3, 5]
		>>> g.get_bottom_trees(2, 1)
		[3, 5, 3]
		>>> g.get_bottom_trees(1, 2)
		[3, 5]
		>>> g.get_bottom_trees(3, 3)
		[9]
		'''
		return [row[x] for row in self.grid][y+1:]


def is_visible(x: int, y: int, grid: Grid) -> bool:
	''' Check if a tree is visible from outside the grid

	>>> g = Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
	>>> is_visible(1, 1, g)
	True
	>>> is_visible(1, 2, g)
	True
	>>> is_visible(1, 3, g)
	False
	>>> is_visible(2, 1, g)
	True
	>>> is_visible(2, 2, g)
	False
	>>> is_visible(2, 3, g)
	True
	>>> is_visible(3, 1, g)
	False
	>>> is_visible(3, 2, g)
	True
	>>> is_visible(3, 3, g)
	False
	'''
	tree_height = grid[x, y]
	is_visible = lambda trees: all(height < tree_height for height in trees)

	visibility_by_direction = [
		is_visible(grid.get_left_trees(x, y)),
		is_visible(grid.get_right_trees(x, y)),
		is_visible(grid.get_top_trees(x, y)),
		is_visible(grid.get_bottom_trees(x, y)),
	]

	return any(visibility_by_direction)

def scenic_score(x: int, y: int, grid: Grid) -> int:
	''' Finds the scenic score of a tree in the grid
	
	>>> g = Grid(grid=[[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
	>>> scenic_score(2, 1, g)
	4
	>>> scenic_score(2, 3, g)
	8
	'''
	tree_height = grid[x, y]
	def view_distance(trees):
		if len(trees) == 0: return 0
		for i, height in enumerate(trees):
			if height >= tree_height:
				break

		return i + 1

	view_distances = [
		view_distance(grid.get_left_trees(x, y)),
		view_distance(grid.get_right_trees(x, y)),
		view_distance(grid.get_top_trees(x, y)),
		view_distance(grid.get_bottom_trees(x, y)),
	]
	return reduce(lambda acc, d: acc * d, view_distances, 1)

if __name__ == '__main__':
	import doctest
	doctest.testmod()