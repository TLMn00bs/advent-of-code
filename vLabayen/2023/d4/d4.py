import logging
from typing import Set, Iterable
from collections import Counter
import re
from attrs import define, field
from math import pow


@define
class Card:
	id: int
	winning_numbers: Set[int]
	card_numbers: Set[int]

	matched_numbers: int = field(init=False)
	def __attrs_post_init__(self):
		self.matched_numbers = len(self.card_numbers.intersection(self.winning_numbers))

	@property
	def points(self) -> int:
		if self.matched_numbers == 0: return 0
		return int(pow(2, self.matched_numbers - 1))

	@property
	def awarded_cards(self) -> Iterable[int]:
		return (self.id + n for n in range(1, self.matched_numbers + 1))

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
	cards = {card.id: card for card in read_file(args.file)}
	cards_counter = Counter(cards.keys())

	for current_card in cards.values(): cards_counter.update({
		awarded_card_id: cards_counter[current_card.id] for awarded_card_id in current_card.awarded_cards
	})

	print(sum(cards_counter.values()))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
