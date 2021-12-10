#!/bin/python3
chunk_chars = {'(':')', '[':']', '{':'}', '<':'>'}
opening = set(chunk_chars.keys())
closing = set(chunk_chars.values())
all_chars = opening.union(closing)

corrupted_char2points = lambda c, p: {')': 3, ']': 57, '}': 1197, '>': 25137}[c] + p
def p1(args):
	score = 0
	with open(args.file, 'r') as f:
		for line in (l.strip() for l in f):
			opening_chars = []
			for c in line:
				if c not in all_chars: raise ValueError

				if c in opening:
					opening_chars.append(c)
					continue

				if c != chunk_chars[opening_chars[-1]]:
					score = corrupted_char2points(c, score)
					break

				opening_chars = opening_chars[:-1]
	print(score)

incomplete_char2points = lambda c, p: p * 5 + {')': 1, ']': 2, '}': 3, '>': 4}[c]
def p2(args):
	scores = []
	with open(args.file, 'r') as f:
		for line in (l.strip() for l in f):
			opening_chars = []
			for c in line:
				if c not in all_chars: raise ValueError

				if c in opening:
					opening_chars.append(c)
					continue

				if c != chunk_chars[opening_chars[-1]]: break	# Corrupted line
				opening_chars = opening_chars[:-1]

			else:		# Incomplete line
				score = 0
				for c in opening_chars[::-1]: score = incomplete_char2points(chunk_chars[c], score)
				scores.append(score)

	scores.sort()
	print(scores[len(scores) // 2])


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
