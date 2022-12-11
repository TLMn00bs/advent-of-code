from enum import Enum
from dataclasses import dataclass

class Hand(Enum):
	ROCK = 1
	PAPER = 2
	SCISSORS = 3

class Outcome(Enum):
	WIN = 6
	DRAW = 3
	LOSE = 0

gameHands = {
	Hand.ROCK: {
		'toWin' : Hand.PAPER,
		'toLose': Hand.SCISSORS,
	},
	Hand.PAPER: {
		'toWin' : Hand.SCISSORS,
		'toLose': Hand.ROCK,
	},
	Hand.SCISSORS: {
		'toWin' : Hand.ROCK,
		'toLose': Hand.PAPER,
	}
}

def get_outcome(opponent: Hand, player: Hand) -> Outcome:
	''' Returns the outcome given the played hands

	>>> get_outcome(Hand.ROCK, Hand.PAPER)
	<Outcome.WIN: 6>
	>>> get_outcome(Hand.PAPER, Hand.ROCK)
	<Outcome.LOSE: 0>
	>>> get_outcome(Hand.SCISSORS, Hand.SCISSORS)
	<Outcome.DRAW: 3>
	'''
	if player == opponent: return Outcome.DRAW
	if player == gameHands[opponent]['toWin']: return Outcome.WIN
	return Outcome.LOSE

def get_points()

if __name__ == '__main__':
	import doctest
	doctest.testmod()
