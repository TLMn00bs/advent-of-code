import logging
import typing
import doctest
import re
from dataclasses import dataclass, field

TInterval = typing.TypeVar('TInterval', bound='Interval')
Range = typing.Tuple[int, int]

@dataclass
class Interval:
	ranges: typing.List[Range] = field(default_factory=lambda: [])

	def __post_init__(self):
		self.ranges = sorted(self.ranges, key = lambda item: item[0])

	def __str__(self) -> str:
		return ', '.join(f'[{start}, {end}]' for start, end in self.ranges)

	def __repr__(self) -> str:
		return f'Interval({str(self)})'

	def __len__(self) -> int:
		''' Return the number of numbers in the interval
		
		>>> len(Interval())
		0
		>>> len(Interval.from_text('[0, 0]'))
		1
		>>> len(Interval.from_text('[0, 1]'))
		2
		>>> len(Interval.from_text('[1, 10]'))
		10
		'''
		if len(self.ranges) == 0: return 0
		return sum((end - start + 1) for start, end in self.ranges)

	def __contains__(self, num: int) -> bool:
		''' Returns if a number is contained in the interval
		
		>>> interval = Interval.from_text('[0, 10], [20, 30]')
		>>> 5 in interval
		True
		>>> 10 in interval
		True
		>>> 15 in interval
		False
		>>> 20 in interval
		True
		'''
		for start, end in self.ranges:
			if start <= num <= end: return True

		return False

	def min(self) -> int:
		if len(self.ranges) == 0: raise ValueError(f'Cannot get the min value in a empty interval')
		return self.ranges[0][0]

	def max(self) -> int:
		if len(self.ranges) == 0: raise ValueError(f'Cannot get the max value in a empty interval')
		return self.ranges[-1][1]

	@staticmethod
	def from_text(text: str) -> TInterval:
		''' Parse an interval from it's text definition
		
		>>> Interval.from_text('[]')
		Interval()
		>>> Interval.from_text('[0, 10]')
		Interval([0, 10])
		>>> Interval.from_text('[-5, 2], [5, 10]')
		Interval([-5, 2], [5, 10])
		'''
		rgx = re.compile('\[([-0-9]+), ([-0-9]+)\]')

		ranges: typing.List[Range] = []
		for start, end in rgx.findall(text):
			ranges.append((int(start), int(end)))

		return Interval(ranges)

	def copy(self) -> TInterval:
		''' Return a copy of the interval
		
		>>> Interval.from_text('[0, 10]') is Interval.from_text('[0, 10]')
		False

		>>> interval = Interval.from_text('[0, 10]')
		>>> interval_ref = interval
		>>> interval_ref
		Interval([0, 10])

		>>> interval_copy = interval.copy()
		>>> interval_copy
		Interval([0, 10])

		>>> interval is interval_ref
		True
		>>> interval is interval_copy
		False
		'''
		return Interval([(start, end) for start, end in self.ranges])

	def replace_range(self, idx: int, range: Range) -> TInterval:
		''' Return a new interval with one of the ranges replaced 
		The ranges are guarranted to be keept in order but the new range
		must not overlap with the remaining interval ranges.
		
		>>> interval = Interval.from_text('[0, 10]')
		>>> interval.replace_range(0, (0, 15))
		Interval([0, 15])
		>>> interval.from_text('[0, 10], [20, 30]').replace_range(0, (0, 15))
		Interval([0, 15], [20, 30])
		>>> interval.from_text('[0, 10], [20, 30]').replace_range(1, (25, 30))
		Interval([0, 10], [25, 30])
		>>> interval.from_text('[0, 10], [20, 30]').replace_range(0, (50, 60))
		Interval([20, 30], [50, 60])

		The origin interval must not have been modified 
		>>> interval
		Interval([0, 10])
		'''
		# TODO: Check for overlap

		ranges = [r for r in self.ranges]
		ranges[idx] = range
		return Interval(ranges)

	def add(self, range: Range) -> TInterval:
		''' Return a new interval with the range added to the current one

		--- Adding to an empty interval ---
		>>> Interval().add((0, 10))
		Interval([0, 10])

		--- Range is completely outside the interval ---
		>>> Interval.from_text('[0, 10]').add((-10, -5))
		Interval([-10, -5], [0, 10])
		>>> Interval.from_text('[0, 10]').add((11, 20))
		Interval([0, 20])
		>>> Interval.from_text('[0, 10]').add((12, 20))
		Interval([0, 10], [12, 20])

		--- Interval is fully contained in the range --- 
		>>> Interval.from_text('[10, 20]').add((0, 30))
		Interval([0, 30])
		>>> Interval.from_text('[10, 15], [20, 25]').add((0, 30))
		Interval([0, 30])

		--- Range is fully contained in the interval --- 
		>>> Interval.from_text('[0, 30]').add((10, 20))
		Interval([0, 30])

		--- Range is inside the interval but does not touch nor overlap with any range
		>>> Interval.from_text('[0, 10], [20, 30]').add((14, 16))
		Interval([0, 10], [14, 16], [20, 30])

		--- Range extends the interval ---
		>>> Interval.from_text('[5, 25]').add((0, 10))
		Interval([0, 25])
		>>> Interval.from_text('[0, 10]').add((5, 25))
		Interval([0, 25])
		>>> Interval.from_text('[5, 25], [30, 40]').add((0, 10))
		Interval([0, 25], [30, 40])
		>>> Interval.from_text('[0, 10], [30, 40]').add((5, 25))
		Interval([0, 25], [30, 40])

		--- Range joins interval's inner ranges
		>>> Interval.from_text('[0, 10], [20, 30]').add((5, 25))
		Interval([0, 30])
		>>> Interval.from_text('[0, 10], [20, 30]').add((-5, 25))
		Interval([-5, 30])
		>>> Interval.from_text('[0, 10], [20, 30]').add((5, 35))
		Interval([0, 35])
		>>> Interval.from_text('[0, 10], [20, 30], [40, 50]').add((5, 45))
		Interval([0, 50])
		>>> Interval.from_text('[0, 10], [20, 30], [40, 50]').add((5, 55))
		Interval([0, 55])
		>>> Interval.from_text('[0, 10], [20, 30], [40, 50]').add((-5, 55))
		Interval([-5, 55])
		>>> Interval.from_text('[2, 2], [11, 13]').add([3, 13])
		Interval([2, 13])

		--- Corner cases ---
		>>> Interval.from_text('[0, 0]').add((0, 0))
		Interval([0, 0])
		>>> Interval.from_text('[0, 1]').add((0, 0))
		Interval([0, 1])
		>>> Interval.from_text('[0, 0]').add((0, 1))
		Interval([0, 1])
		>>> Interval.from_text('[0, 5]').add((5, 10))
		Interval([0, 10])
		>>> Interval.from_text('[0, 5]').add([6, 10])
		Interval([0, 10])
		'''
		if len(self.ranges) == 0: return Interval([range])
		r_start, r_end = range

		# Range is completely outside the interval
		min_start = self.ranges[0][0]
		if r_end < min_start:
			if r_end + 1 == min_start: return self.replace_range(0, (r_start, self.ranges[0][1]))
			return Interval([range] + self.ranges)

		max_end = self.ranges[-1][1]
		if max_end < r_start:
			if max_end == r_start - 1: return self.replace_range(-1, (self.ranges[-1][0], r_end))
			return Interval(self.ranges + [range])

		# Interval is fully contained in the range
		if r_start <= min_start <= max_end <= r_end: return Interval([range])

		affected_ranges = [(idx, start, end) for idx, (start, end) in enumerate(self.ranges) if not (r_end + 1 < start or end < r_start - 1)]

		# The range is inside the interval max limits but does not touch any range
		if len(affected_ranges) == 0: return Interval(self.ranges + [range])

		if len(affected_ranges) == 1:
			idx, start, end = affected_ranges[0]

			# Range is fully contained in the interval
			if start <= r_start <= r_end <= end: return self.copy()

			# Range extends the interval
			if r_start <= start <= r_end <= end: return self.replace_range(idx, (r_start, end))
			if start <= r_start <= end <= r_end: return self.replace_range(idx, (start, r_end))

		# If there are more than 2 affected ranges, we can drop everyone
		# except the border ones, since the range will contain them
		first_idx, first_start, first_end = affected_ranges[0]
		last_idx, last_start , last_end  = affected_ranges[-1]
		
		# Join ranges
		keep_ranges = [r for idx, r in enumerate(self.ranges) if not (first_idx <= idx <= last_idx)]
		start, end = min(first_start, r_start), max(last_end, r_end)
		return Interval(keep_ranges + [(start, end)])

	def subtract(self, range: Range) -> TInterval:
		''' Return a new interval with the range subtracted from the current one
		
		--- Subtracting from an empty interval
		>>> Interval([]).subtract((0, 10))
		Interval()

		--- Range is completely outside the interval ---
		>>> Interval.from_text('[0, 10]').subtract((-10, -5))
		Interval([0, 10])
		>>> Interval.from_text('[0, 10]').subtract((15, 20))
		Interval([0, 10])
		>>> Interval.from_text('[0, 10], [20, 30]').subtract((12, 18))
		Interval([0, 10], [20, 30])

		--- Interval is fully contained in the range --- 
		>>> Interval.from_text('[10, 20]').subtract((0, 30))
		Interval()
		>>> Interval.from_text('[10, 15], [20, 25]').subtract((0, 30))
		Interval()

		--- Range is fully contained in the interval --- 
		>>> Interval.from_text('[0, 30]').subtract((10, 20))
		Interval([0, 9], [21, 30])

		--- Range reduce one of the interval's ranges ---
		>>> Interval.from_text('[5, 25]').subtract((0, 10))
		Interval([11, 25])
		>>> Interval.from_text('[0, 10]').subtract((5, 25))
		Interval([0, 4])
		>>> Interval.from_text('[5, 25], [30, 40]').subtract((0, 10))
		Interval([11, 25], [30, 40])
		>>> Interval.from_text('[0, 10], [30, 40]').subtract((5, 25))
		Interval([0, 4], [30, 40])

		--- Range reduce some interval's inner ranges
		>>> Interval.from_text('[0, 10], [20, 30]').subtract((5, 25))
		Interval([0, 4], [26, 30])
		>>> Interval.from_text('[0, 10], [20, 30]').subtract((-5, 25))
		Interval([26, 30])
		>>> Interval.from_text('[0, 10], [20, 30]').subtract((5, 35))
		Interval([0, 4])
		>>> Interval.from_text('[0, 10], [14, 16], [20, 30]').subtract((-5, 25))
		Interval([26, 30])
		>>> Interval.from_text('[0, 10], [20, 30], [40, 50]').subtract((-5, 55))
		Interval()

		--- Corner cases ---
		>>> Interval.from_text('[0, 0]').subtract((0, 0))
		Interval()
		>>> Interval.from_text('[0, 1]').subtract((0, 0))
		Interval([1, 1])
		>>> Interval.from_text('[0, 0]').subtract((0, 1))
		Interval()
		>>> Interval.from_text('[0, 5]').subtract((5, 10))
		Interval([0, 4])

		>>> Interval.from_text('[0, 5]').subtract((-5, 4))
		Interval([5, 5])
		>>> Interval.from_text('[0, 5]').subtract((-5, 5))
		Interval()
		>>> Interval.from_text('[0, 5]').subtract((-5, 6))
		Interval()
		'''
		if len(self.ranges) == 0: return Interval()
		r_start, r_end = range

		# Range is completely outside the interval
		min_start = self.ranges[0][0]
		if r_end < min_start: return self.copy()

		max_end = self.ranges[-1][1]
		if max_end < r_start: return self.copy()

		# Interval is fully contained in the range
		if r_start <= min_start <= max_end <= r_end: return Interval()


		affected_ranges = [(idx, start, end) for idx, (start, end) in enumerate(self.ranges) if not (r_end < start or end < r_start)]
		if len(affected_ranges) == 0: return self.copy()

		if len(affected_ranges) == 1:
			idx, start, end = affected_ranges[0]

			# Range is fully contained in the interval
			if start <= r_start <= r_end <= end:
				new_ranges = []
				if start < r_start: new_ranges.append((start, r_start - 1))
				if r_end < end: new_ranges.append((r_end + 1, end))

				keep_ranges = [r for i, r in enumerate(self.ranges) if i != idx]
				return Interval(keep_ranges + new_ranges)

			# Range subtracts the interval
			if r_start <= start <= r_end <= end:
				keep_ranges = [r for i, r in enumerate(self.ranges) if i != idx]
				return Interval(keep_ranges + [(r_end + 1, end)])
			
			if start <= r_start <= end <= r_end:
				keep_ranges = [r for i, r in enumerate(self.ranges) if i != idx]
				return Interval(keep_ranges + [(start, r_start - 1)])

		# If there are more than 2 affected ranges, we can drop everyone
		# except the border ones, since the range will contain them
		first_idx, first_start, first_end = affected_ranges[0]
		last_idx, last_start , last_end  = affected_ranges[-1]
		
		# Split ranges
		if r_start <= first_end <= last_start <= r_end:
			new_ranges = []
			if first_start < r_start: new_ranges.append((first_start, r_start - 1))
			if r_end < last_end: new_ranges.append((r_end + 1, last_end))

			keep_ranges = [r for idx, r in enumerate(self.ranges) if not (first_idx <= idx <= last_idx)]
			return Interval(keep_ranges + new_ranges)

if __name__ == '__main__':
	import doctest
	logging.basicConfig(level=logging.DEBUG)
	doctest.testmod(optionflags=doctest.ELLIPSIS)