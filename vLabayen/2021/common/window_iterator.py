from itertools import islice
import types

def iter_window(seq, n=2):
	'''
	>>> list(iter_window(range(7), n = 2))
	[[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
	>>> list(iter_window(range(7), n = 3))
	[[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
	'''
	it = iter(seq)

	result = list(islice(it, n))
	if len(result) == n: yield result

	for elem in it:
		result = result[1:] + [elem]
		yield result

def iter_window_non_overlap(seq, n = 2):
	'''Split a generator in non overlaping windows of size n (except the last one, that can be smaller)
	>>> list(iter_window_non_overlap(range(10), n = 2))
	[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
	>>> list(iter_window_non_overlap(range(10), n = 3))
	[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
	'''

	it = iter(seq) if not isinstance(seq, types.GeneratorType) else seq
	w = list(islice(it, n))
	while len(w) > 0:
		yield w
		w = list(islice(it, n))


if __name__ == '__main__':
	import doctest
	doctest.testmod()
