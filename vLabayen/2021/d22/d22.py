#!/bin/python3
import re

parse_rgx = re.compile('(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)')
def parse_p1(file, reduce_coords):
	with open(args.file, 'r') as f:
		for line in f:
			state, *ranges = parse_rgx.match(line.strip()).groups()
			x_start, x_end, y_start, y_end, z_start, z_end = reduce_coords(*[int(v) for v in ranges])
			yield state, {(x,y,z) for x in range(x_start, x_end + 1) for y in range(y_start, y_end + 1) for z in range(z_start, z_end + 1)}

def p1(args):
	on_cubes = set()
	reduce_coords = lambda x_start, x_end, y_start, y_end, z_start, z_end: (max(-50, x_start), min(50, x_end), max(-50, y_start), min(50, y_end), max(-50, z_start), min(50, z_end))
	for state, specified_cubes in parse_p1(args.file, reduce_coords):
		if state == 'on' : on_cubes = on_cubes.union(specified_cubes)
		if state == 'off': on_cubes = on_cubes.difference(specified_cubes)

	print(len(on_cubes))

class Cuboid:
	def __init__(self, x_start, x_end, y_start, y_end, z_start, z_end):
		self.x_start = min(x_start, x_end)
		self.x_end   = max(x_start, x_end)
		self.y_start = min(y_start, y_end)
		self.y_end   = max(y_start, y_end)
		self.z_start = min(z_start, z_end)
		self.z_end   = max(z_start, z_end)

	# As the boundaries are inclusive, the length is the difference + 1
	# [0, 5] --> [0, 1, 2, 3, 4, 5] --> len = 5 - 0 + 1 = 6
	# As they are 3D cubes, the total lenght is the product of all dimensions
	def __len__(self): return (self.x_end - self.x_start + 1) * (self.y_end - self.y_start + 1) * (self.z_end - self.z_start + 1)
	def __str__(self): return f'Cuboid(x=({self.x_start}, {self.x_end}), y=({self.y_start}, {self.y_end}), z=({self.z_start}, {self.z_end}))'
	#def __str__(self): return f'x={self.x_start}..{self.x_end},y={self.y_start}..{self.y_end},z={self.z_start}..{self.z_end}'
	def __iter__(self): return ((x, y, z) for x in range(self.x_start, self.x_end + 1)
					      for y in range(self.y_start, self.y_end + 1)
					      for z in range(self.z_start, self.z_end + 1))

	def is_totally_contained_by(self, other):
		'''This Cuboid is totally contained by other. That means, other is bigger than this
		To check whether the other cuboid is totally contained by this, call other.is_totally_contained_by(this)
		'''
		contained_in_x = other.x_start <= self.x_start <= self.x_end <= other.x_end
		contained_in_y = other.y_start <= self.y_start <= self.y_end <= other.y_end
		contained_in_z = other.z_start <= self.z_start <= self.z_end <= other.z_end
		return (contained_in_x and contained_in_y and contained_in_z)

	def intersects_with(self, other):
		intersects_in_x = other.x_start <= self.x_start <= other.x_end or other.x_start <= self.x_end <= other.x_end or self.x_start <= other.x_start <= self.x_end or self.x_start <= other.x_end <= self.x_end
		intersects_in_y = other.y_start <= self.y_start <= other.y_end or other.y_start <= self.y_end <= other.y_end or self.y_start <= other.y_start <= self.y_end or self.y_start <= other.y_end <= self.y_end
		intersects_in_z = other.z_start <= self.z_start <= other.z_end or other.z_start <= self.z_end <= other.z_end or self.z_start <= other.z_start <= self.z_end or self.z_start <= other.z_end <= self.z_end
		return (intersects_in_x and intersects_in_y and intersects_in_z)

	def split_x_ranges(self, other):
		# left cubes: The other x_start must be contained in this cube
		if self.x_start < other.x_start <= self.x_end: yield 'left', (self.x_start, other.x_start - 1)
		# right cubes: The other x_end must be contained in this cube
		if self.x_start <= other.x_end < self.x_end: yield 'right', (other.x_end + 1, self.x_end)
		# There will always be a center cube
		yield 'center', (max(self.x_start, other.x_start), min(self.x_end, other.x_end))

	def split_y_ranges(self, other):
		if self.y_start < other.y_start <= self.y_end: yield 'bottom', (self.y_start, other.y_start - 1)
		if self.y_start <= other.y_end < self.y_end: yield 'top', (other.y_end + 1, self.y_end)
		yield 'center', (max(self.y_start, other.y_start), min(self.y_end, other.y_end))

	def split_z_ranges(self, other):
		if self.z_start < other.z_start <= self.z_end: yield 'back', (self.z_start, other.z_start - 1)
		if self.z_start <= other.z_end < self.z_end: yield 'front', (other.z_end + 1, self.z_end)
		yield 'center', (max(self.z_start, other.z_start), min(self.z_end, other.z_end))


	# This function could (and should) be optimized to reduce the number of cuboids to enhance performance
	# In https://stackoverflow.com/questions/12769386/how-to-calculate-total-volume-of-multiple-overlapping-cuboids is said that
	# we can express the non-intersecting area with up to 5 cuboids, but assumming that no cuboid is fully contained in the other
	# nevertheless, (i think) that the 26 non-intersecting cuboids can be expressed in just 6.
	def split_to_non_intersecting_cuboids(self, other):
		'''There are up to 27 smaller cubes. The can be:
		- In x axis: left,   center, right		x is possitive to the right
		- In y axis: bottom, center, top		y is possitive to the top
		- In z axis: back,   center, front		z is possitive to the front
		The center-center-center is the intersection cube. The boundaries are considered intersection points
		Here we assume that both intersect
		'''
		return [Cuboid(*x_range, *y_range, *z_range)
			for xpos, x_range in self.split_x_ranges(other)
			for ypos, y_range in self.split_y_ranges(other)
			for zpos, z_range in self.split_z_ranges(other)
			if not (xpos == ypos == zpos == 'center')	# The center one is the intersection
		]
#	def get_intersection(self, other): return [Cuboid(*x_range, *y_range, *z_range)
#		for xpos, x_range in self.split_x_ranges(other)
#		for ypos, y_range in self.split_y_ranges(other)
#		for zpos, z_range in self.split_z_ranges(other)
#		if (xpos == ypos == zpos == 'center')
#	][0]

def parse_p2(file):
	with open(args.file, 'r') as f:
		for line in f:
			state, *ranges = parse_rgx.match(line.strip()).groups()
			x_start, x_end, y_start, y_end, z_start, z_end = [int(v) for v in ranges]
			yield state, Cuboid(x_start, x_end, y_start, y_end, z_start, z_end)

def process_cuboid(state, new_cuboid, existing_cuboids):
	if len(existing_cuboids) == 0: return [new_cuboid]

	# Insert the cuboid into a list bc it may be split into more than one
	cuboids_to_process = [new_cuboid]
	while len(cuboids_to_process) > 0:
		n = cuboids_to_process.pop()

		# Copy the list to avoid modifying during the loop
		cuboids = [c for c in existing_cuboids]

		# https://stackoverflow.com/questions/12769386/how-to-calculate-total-volume-of-multiple-overlapping-cuboids
		if state == 'on':
			for e in existing_cuboids:
				if n.is_totally_contained_by(e): break

				if e.is_totally_contained_by(n):
					cuboids.remove(e)
					continue

				if n.intersects_with(e):
					non_intersecting = n.split_to_non_intersecting_cuboids(e)
					for sub_n in non_intersecting: cuboids_to_process.append(sub_n)

					# The new cuboids must be checked vs the remaining existing cuboids,
					# but we should break to avoid going into the else case that appends n to the resulting cuboids.
					# Also, we have to check all new cuboids vs every remaining e, so the best option is return to the start of the while
					# and grab a new cuboid.
					# This implies that we will check the new cuboids vs some existing cuboids that we already know there is no intersection
					# but it should be an acceptable performance penalty in favour of simplicity
					break

			# The previous loop did't reach a exit point
			else: cuboids.append(n)

		if state == 'off':
			for e in existing_cuboids:
				if e.is_totally_contained_by(n):
					cuboids.remove(e)
					continue

				if n.intersects_with(e):
					cuboids.remove(e)
					non_intersecting = e.split_to_non_intersecting_cuboids(n)
					for sub_e in non_intersecting: cuboids.append(sub_e)
					continue

		# Update the list
		existing_cuboids = cuboids

	return existing_cuboids

def p2(args):
	on_cuboids = []
	for i, (state, new_cuboid) in enumerate(parse_p2(args.file)):
		print(i)
		on_cuboids = process_cuboid(state, new_cuboid, on_cuboids)

	print(sum(len(c) for c in on_cuboids))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

#	p1(args)
	p2(args)
