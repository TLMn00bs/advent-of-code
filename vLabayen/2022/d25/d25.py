#!/bin/python3
import logging
from typing import Iterable, List

_SNAFU2decimal = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
def SNAFU2decimal(number: str) -> int:
	return sum(_SNAFU2decimal[n] * (5 ** i) for i, n in enumerate(number[::-1]))

def decimal2SNAFU(number: int) -> str:
	num_digits = 1
	while SNAFU2decimal('2' * num_digits) < number: num_digits += 1

	digits: List[str] = ['2' for _ in range(num_digits)]
	for digit_idx in range(num_digits):
		digits_copy = digits.copy()
		for d in _SNAFU2decimal.keys():
			digits_copy[digit_idx] = d
			decimal = SNAFU2decimal(''.join(digits_copy))

			if decimal < number: break
			digits = digits_copy.copy()

	return ''.join(digits)

def read_file(file: str) -> Iterable[int]:
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			yield SNAFU2decimal(line)

def p1(args):
	numbers = read_file(args.file)
	s = sum(numbers)
	print(decimal2SNAFU(s))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
