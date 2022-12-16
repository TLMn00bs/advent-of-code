from ndt.window_iterator import iter_window

def find_marker(buffer, window_size):
	''' Finds how many characters there are before
	the window of size window_size with all different characters
	
	>>> find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4)
	7
	>>> find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 4)
	5
	>>> find_marker('nppdvjthqldpwncqszvftbrmjlhg', 4)
	6
	>>> find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4)
	10
	>>> find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4)
	11
	>>> find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14)
	19
	>>> find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 14)
	23
	>>> find_marker('nppdvjthqldpwncqszvftbrmjlhg', 14)
	23
	>>> find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14)
	29
	>>> find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14)
	26
	'''
	for i, window in enumerate(iter_window(buffer, n = window_size)):
		if len(set(window)) == window_size:
			return i + window_size

if __name__ == '__main__':
	import doctest
	doctest.testmod()