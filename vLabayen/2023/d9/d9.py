import logging
from typing import Iterable, List


def read_file(file: str) -> Iterable[List[int]]:
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			yield [int(n) for n in line.split()]


# py3.10: from itertools import pairwise
def pairwise(serie: List[int]) -> Iterable[List[int]]:
	for i in range(len(serie) - 1):
		yield serie[i:i+2]

def reduce(serie: List[int]) -> Iterable[int]:
	for p1, p2 in pairwise(serie):
		yield p2 - p1

def predict_next(serie: List[int]) -> int:
	next_number: int = serie[-1]
	while any(n != 0 for n in serie):
		serie = list(reduce(serie))
		next_number += serie[-1]

	return next_number

def predict_prev(serie: List[int]) -> int:
	sign: int = -1
	prev_number: int = serie[0]
	while any(n != 0 for n in serie):
		serie = list(reduce(serie))
		prev_number += sign * serie[0]
		sign *= -1

	return prev_number

def p1(args):
	series = read_file(args.file)
	print(sum(predict_next(serie) for serie in series))

def p2(args):
	series = read_file(args.file)
	print(sum(predict_prev(serie) for serie in series))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
