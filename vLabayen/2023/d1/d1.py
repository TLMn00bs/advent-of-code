from typing import Iterable, Tuple
import logging
from itertools import product

text2int = {
	'one'  : '1',
	'two'  : '2',
	'three': '3',
	'four' : '4',
	'five' : '5',
	'six'  : '6',
	'seven': '7',
	'eight': '8',
	'nine' : '9',
}

def generate_adyacent_pairs() -> Iterable[Tuple[str, str]]:
	for first, second in product(text2int.keys(), text2int.keys()):
		if first[-1] == second[0]: yield first, second

def get_src(first: str, second: str) -> str: return f'{first[:-1]}{second}'
def get_dst(first: str, second: str) -> str: return f'{first}{second}'

nums_with_shared_letter = {get_src(first, second): get_dst(first, second) for first, second in generate_adyacent_pairs()}


def read_file(file: str) -> Iterable[str]:
	with open(file, 'r') as f:
		for line in f: yield line.strip()

def replace_textual_numbers(line: str) -> str:
	for src, dst in nums_with_shared_letter.items():
		line = line.replace(src, dst)

	for src, dst in text2int.items():
		line = line.replace(src, dst)

	return line

def get_digits(line: str) -> Tuple[int, int]:
	digits = [c for c in line if c.isdigit()]
	if len(digits) == 0: return 0, 0
	return int(digits[0]), int(digits[-1])

def compute_calibration(n1: int, n2: int) -> int:
	return 10 * n1 + n2

def p1(args):
	lines = read_file(args.file)
	calibration_numbers = (compute_calibration(*get_digits(line)) for line in lines)
	print(sum(calibration_numbers))


def p2(args):
	lines = read_file(args.file)
	calibration_numbers = (compute_calibration(*get_digits(replace_textual_numbers(line))) for line in lines)
	print(sum(calibration_numbers))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
