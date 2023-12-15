#!/usr/bin/env python3.11

from dataclasses import dataclass, field
from typing import Set, Iterable
from collections import Counter

input = [line.strip() for line in open("input").readlines()]

@dataclass
class Card:

    card_id:          int
    winning_numbers:  Set[int]
    numbers_you_have: Set[int]

    matches:          int = field(init=False)
    def __post_init__(self):
        self.matches  = len(self.numbers_you_have.intersection(self.winning_numbers))

    @property
    def points(self) -> int:
        if self.matches == 0:
            return 0
        return pow(2, self.matches - 1)

    @property
    def copies_of_this_card(self) -> Iterable[int]:
        return [ 1 + self.card_id + m for m in range(self.matches) ]

def parse_pile_of_cards(lines: list) -> Iterable[Card]:
    cards = []
    for l in lines:
        card_id_str, card_numbers_str = l.split(':')
        card_id                       = int(card_id_str.strip('Card '))
        winning_numbers               = set(int(n) for n in card_numbers_str.split(' | ')[0].split())
        numbers_you_have              = set(int(n) for n in card_numbers_str.split(' | ')[1].split())
        cards.append( Card(card_id, winning_numbers, numbers_you_have) )
    return cards

def part1(input: list) -> list:
    points = [c.points for c in parse_pile_of_cards(input)]
    return points

def part2(input: list) -> list:
    cards    = {k:v for k,v in enumerate(parse_pile_of_cards(input))}
    how_many = Counter(cards.keys())

    for card in cards.values():
        how_many.update(
            {copy_id: how_many[card.card_id] for copy_id in card.copies_of_this_card}
        )

    return how_many.values()

if __name__ == '__main__':
    print( sum(part1(input)) )
    print( sum(part2(input)) )
