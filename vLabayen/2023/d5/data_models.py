from typing import List, Tuple, Optional
from attrs import define, field
from functools import reduce

@define
class Range:
	''' Range of numbers: [start, end) '''
	start: int
	end  : int

	def shift(self, n: int) -> 'Range': return Range(
		start = self.start + n,
		end   = self.end   + n
	)

	def merge(self, other: 'Range') -> Tuple[Optional['Range'], Optional['Range'], Optional['Range']]:
		result: List[Optional[Range]] = [None, None, None]

		# Difference before the start
		if other.start < self.start:
			result[0] = Range(other.start, min(other.end, self.start))

		# Intersecction
		if not (self.end <= other.start or other.end <= self.start):
			result[1] = Range(max(self.start, other.start), min(self.end, other.end))

		# Difference after the end
		if self.end < other.end:
			result[2] = Range(max(other.start, self.end), other.end)

		return tuple(result)

@define
class Transformation:
	src_range: Range
	dst_range: Range

	add_src2dst: int = field(init=False, repr=False)
	add_dst2src: int = field(init=False, repr=False)
	def __attrs_post_init__(self):
		self.add_src2dst = self.dst_range.start - self.src_range.start
		self.add_dst2src = -self.add_src2dst
	
	def match(self, n: int) -> bool:
		return self.src_range.start <= n < self.src_range.end

@define
class Map:
	transformations: List[Transformation]

	@staticmethod
	def merge(input: 'Map', output: 'Map') -> 'Map':
		merged_transformations = []

		# Compute merged transformations and input-unmatched transformations
		input_transforms: List[Transformation] = [transform for transform in input.transformations]
		for out_transform in output.transformations:
			unmatched: List[Transformation] = []
			for in_transform in input_transforms:
				left, union, right = out_transform.src_range.merge(in_transform.dst_range)

				if left is not None: unmatched.append(Transformation(
					src_range = left.shift(in_transform.add_dst2src),
					dst_range = left
				))

				if right is not None: unmatched.append(Transformation(
					src_range = right.shift(in_transform.add_dst2src),
					dst_range = right
				))
				
				if union is not None: merged_transformations.append(Transformation(
					src_range = union.shift(in_transform.add_dst2src),
					dst_range = union.shift(out_transform.add_src2dst)
				))

			# Continue with the unmatched ones for the next output
			input_transforms = unmatched

		# Compute output-unmatched transformations
		output_transforms: List[Transformation] = [transform for transform in output.transformations]
		for in_transform in input.transformations:
			unmatched: List[Transformation] = []
			for out_transform in output_transforms:
				left, _, right = in_transform.dst_range.merge(out_transform.src_range)

				if left is not None: unmatched.append(Transformation(
					src_range = left,
					dst_range = left.shift(out_transform.add_src2dst)
				))

				if right is not None: unmatched.append(Transformation(
					src_range = right,
					dst_range = right.shift(out_transform.add_src2dst)
				))

			output_transforms = unmatched

		return Map(merged_transformations + input_transforms + output_transforms)

	@staticmethod
	def merge_maps(maps: List['Map']):
		return reduce(lambda current, next: Map.merge(current, next), maps[1:], maps[0])

	def transform(self, n: int) -> int:
		for transform in self.transformations:
			if transform.match(n): return n + transform.add_src2dst
		
		return n
