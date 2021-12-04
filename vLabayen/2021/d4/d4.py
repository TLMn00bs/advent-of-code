#!/bin/python3
from common.printer import cprepare

def read_file(file):
	with open(file, 'r') as f:
		numbers = [int(n) for n in f.readline().strip().split(',')]
		boards = [[[int(n) for n in f.readline().strip().replace('  ', ' ').split(' ')] for i in range(5)] for empty_line in f]
	return numbers, boards

def check_board(board, drawn_numbers):
	if any(all(n in drawn_numbers for n in row) for row in board): return True
	if any(all(n in drawn_numbers for n in col) for col in ([board[row_idx][col_idx] for row_idx in range(5)] for col_idx in range(5))): return True
	return False

def display_board(board, drawn_numbers, end='\n'):
	for row in board:
		formatted = [cprepare(f'{n:>2}', color = 'green' if n in drawn_numbers else 'default') for n in row]
		print(' '.join(formatted))

	print(end=end)

def get_unmarked(board, drawn_numbers): return [n for row in board for n in row if n not in drawn_numbers]

def p1(args):
	numbers, boards = read_file(args.file)
	drawn_numbers = set()
	for n in numbers:
		drawn_numbers.add(n)
		for b in boards:
			if check_board(b, drawn_numbers):
				unmarked = get_unmarked(b, drawn_numbers)
				print(f'Score: {sum(unmarked) * n}')
				return

def p2(args):
	numbers, boards = read_file(args.file)
	drawn_numbers = set()
	for n in numbers:
		drawn_numbers.add(n)
		to_remove = []		# Remove once the loop has ended
		for i,b in enumerate(boards):
			if check_board(b, drawn_numbers):
				if len(boards) == 1:
					unmarked = get_unmarked(b, drawn_numbers)
					print(f'Score: {sum(unmarked) * n}')
					return

				to_remove.append(b)
		for b in to_remove: boards.remove(b)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
