import logging
from typing import Iterable, Tuple, Dict, Optional
from enum import Enum
from attrs import define
from collections import Counter

Cards = Tuple[int, int, int, int, int]

def parse_card(value: str, named_cards: Dict[str, int]) -> int:
	return named_cards.get(value) or int(value)

class HandType(Enum):
	FIVE_OF_A_KIND  = 7
	FOUR_OF_A_KIND  = 6
	FULL_HOUSE      = 5
	THREE_OF_A_KIND = 4
	TWO_PAIR        = 3
	ONE_PAIR        = 2
	HIGH_CARD       = 1

	@staticmethod
	def get_type(num_unique_cards: int, max_repeat: int) -> 'HandType':
		if num_unique_cards == 5: return HandType.HIGH_CARD
		if num_unique_cards == 4: return HandType.ONE_PAIR
		if num_unique_cards == 3 and max_repeat == 3: return HandType.THREE_OF_A_KIND
		if num_unique_cards == 3 and max_repeat == 2: return HandType.TWO_PAIR
		if num_unique_cards == 2 and max_repeat == 4: return HandType.FOUR_OF_A_KIND
		if num_unique_cards == 2 and max_repeat == 3: return HandType.FULL_HOUSE
		if num_unique_cards == 1: return HandType.FIVE_OF_A_KIND
		raise ValueError(f'Unknown hand type: {num_unique_cards=}, {max_repeat=}')

@define
class Hand:
	cards: Cards
	bid  : int

	def type(self, joker: Optional[int] = None) -> HandType:
		num_jokers = sum(1 for card in self.cards if card == joker)
		remaining_cards = [card for card in self.cards if card != joker]

		if len(remaining_cards) == 0: return HandType.get_type(1, 5)

		cards_count = Counter(remaining_cards)
		num_unique_cards = len(cards_count)
		(_, max_repeat), = cards_count.most_common(1)
		return HandType.get_type(num_unique_cards, max_repeat + num_jokers)


def read_file(file: str, named_cards: Dict[str, int]) -> Iterable[Hand]:
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			cards, bid = line.split(' ')
			yield Hand(
				cards = tuple(parse_card(c, named_cards) for c in cards),
				bid   = int(bid)
			)

def p1(args):
	hands = read_file(args.file, {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10})
	sorted_hands = sorted(hands, key = lambda hand: (hand.type().value, *hand.cards))
	print(sum((i + 1) * hand.bid for i, hand in enumerate(sorted_hands)))

def p2(args):
	hands = read_file(args.file, {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10})
	sorted_hands = sorted(hands, key = lambda hand: (hand.type(joker=1).value, *hand.cards))
	print(sum((i + 1) * hand.bid for i, hand in enumerate(sorted_hands)))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
