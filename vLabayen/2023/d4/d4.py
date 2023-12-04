import logging
from typing import Set, Iterable
import re
from attrs import define
from math import pow


@define
class Card:
	id: int
	winning_numbers: Set[int]
	card_numbers: Set[int]

	@property
	def points(self) -> int:
		matched_numbers = self.card_numbers.intersection(self.winning_numbers)
		if len(matched_numbers) == 0: return 0
		return int(pow(2, len(matched_numbers) - 1))

def read_file(file: str) -> Iterable[Card]:
	split_card_info_rgx = re.compile(r'Card +([0-9]+): ([0-9 ]+) \| ([0-9 ]+)')
	parse_numbers_rgx = re.compile('([0-9]+)')

	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			card_id, winning_numbers_text, card_numbers_text = split_card_info_rgx.match(line).groups()		# type: ignore
			yield Card(
				id = int(card_id),
				winning_numbers = set(int(n) for n in parse_numbers_rgx.findall(winning_numbers_text)),
				card_numbers = set(int(n) for n in parse_numbers_rgx.findall(card_numbers_text))
			)

def p1(args):
	cards = read_file(args.file)
	print(sum(card.points for card in cards))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
