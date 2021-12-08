#!/bin/python3
digit2len = lambda d: {'0': 6, '1': 2, '2': 5, '3': 5, '4': 4, '5': 5, '6': 6, '7': 3, '8': 7, '9': 6}[d]
len2digit = lambda l: {2: ['1'], 3: ['7'], 4: ['4'], 5: ['2', '3', '5'], 6: ['0', '6', '9'], 7: ['8']}[l]

all_segments = set('abcdefg')
#digit2segments = lambda d: {
#	'0': set(['a', 'b', 'c',      'e', 'f', 'g']),
#	'1': set([          'c',           'f'     ]),
#	'2': set(['a',      'c', 'd', 'e',      'g']),
#	'3': set(['a',      'c', 'd',      'f', 'g']),
#	'4': set([     'b', 'c', 'd',      'f'     ]),
#	'5': set(['a', 'b',      'd',      'f', 'g']),
#	'6': set(['a', 'b',      'd', 'e', 'f', 'g']),
#	'7': set(['a',      'c',           'f'     ]),
#	'8': set(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
#	'9': set(['a', 'b', 'c', 'd',      'f', 'g']),
#}[d]
#segments2digit = lambda s: [str(digit) for digit in range(10) if digit2segment(str(digit)) == s][0]

def a_wire(codes):
	# We can know which is the a wire by taking the difference between 7 and 1.
	# Both 7 and 1 has unique number of segments
	one = [set(code) for code in codes if len(code) == digit2len('1')][0]
	seven = [set(code) for code in codes if len(code) == digit2len('7')][0]
	return list(seven - one)[0]

def e_wire(codes):
	# 4 has segments bcdf. 4 has a unique number of segments
	# 0,6 and 9 has 6 segments.
	# 0 has segments abcefg --> From the segments of 4, d is the only one missing
	# 6 has segments abdefg --> From the segments of 4, c is the only one missing
	# 9 has segments abcdfg --> From the segments of 4, no one is missing. Therefore we can map the missing e to the missing segment of the given 9
	four = [set(code) for code in codes if len(code) == digit2len('4')][0]
	one_six_nine = [set(code) for code in codes if len(code) == digit2len('0')]
	for code in one_six_nine:
		if len(four - code) == 0: return list(all_segments - code)[0]

def nine_segment(codes):
	# Same as e_wire, but return the 9 segment
	four = [set(code) for code in codes if len(code) == digit2len('4')][0]
	one_six_nine = [set(code) for code in codes if len(code) == digit2len('0')]
	for code in one_six_nine:
		if len(four - code) == 0: return code

def six_segment(codes):
	# Similar to nine_segment, but compare with 1 instead of 4.
	one = [set(code) for code in codes if len(code) == digit2len('1')][0]
	one_six_nine = [set(code) for code in codes if len(code) == digit2len('0')]
	for code in one_six_nine:
		if len(one - code) == 1: return code

def zero_segment(codes, six, nine):
	# Get zero by filtering 6 and 9 from codes with len 6
	one_six_nine = [set(code) for code in codes if len(code) == digit2len('0')]
	for code in one_six_nine:
		if code != six and code != nine: return code

def three_segment(codes):
	# Get three by looking at the difference between 1 and 2,3,5
	one = [set(code) for code in codes if len(code) == digit2len('1')][0]
	two_three_five = [set(code) for code in codes if len(code) == digit2len('2')]
	for code in two_three_five:
		if len(one - code) == 0: return code

def two_segment(codes, e_wire):
	# From 2,3 and 5, 2 is the only digit that has the e wire
	two_three_five = [set(code) for code in codes if len(code) == digit2len('2')]
	for code in two_three_five:
		if e_wire in code: return code

def five_segment(codes, two, three):
	# Get 5 from filtering 2 and 3 from the 5 segment digits
	two_three_five = [set(code) for code in codes if len(code) == digit2len('2')]
	for code in two_three_five:
		if code != two and code != three: return code

def p1(args):
	unique_lens = [digit2len(n) for n in {'1', '4', '7', '8'}]

	n_unique_digits = 0
	with open(args.file, 'r') as f:
		for digit_codes in (line.strip().split(' | ')[1].split(' ') for line in f):
			n_unique_digits += len([code for code in digit_codes if len(code) in unique_lens])
	print(n_unique_digits)

def p2(args):
	output_sum = 0
	with open(args.file, 'r') as f:
		for input_codes, output_codes in ((inpt.split(' '), outpt.split(' ')) for inpt, outpt in (line.strip().split(' | ') for line in f)):
			e = e_wire(input_codes)
			six   = six_segment(input_codes)
			nine  = nine_segment(input_codes)
			two   = two_segment(input_codes, e)
			three = three_segment(input_codes)

			digit2messedsegment = lambda d: {
				'0': zero_segment(input_codes, six, nine),
				'1': [set(code) for code in input_codes if len(code) == digit2len('1')][0],
				'2': two,
				'3': three,
				'4': [set(code) for code in input_codes if len(code) == digit2len('4')][0],
				'5': five_segment(input_codes, two, three),
				'6': six,
				'7': [set(code) for code in input_codes if len(code) == digit2len('7')][0],
				'8': [set(code) for code in input_codes if len(code) == digit2len('8')][0],
				'9': nine
			}[d]
			messedsegment2digit = lambda s: [str(digit) for digit in range(10) if digit2messedsegment(str(digit)) == set(s)][0]
			output_digits = [messedsegment2digit(code) for code in output_codes]
			output_number = int(''.join(output_digits))
			output_sum += output_number

	print(output_sum)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
