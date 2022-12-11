from enum import IntEnum
from dataclasses import dataclass

class Hand(IntEnum):
	ROCK = 1
	PAPER = 2
	SCISSORS = 3

class Outcome(IntEnum):
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

def get_points(player: Hand, outcome: Outcome) -> int:
	''' Returns the points associated to the player's hand & game outcome
	
	>>> get_points(Hand.PAPER, Outcome.WIN)
	8
	>>> get_points(Hand.ROCK, Outcome.LOSE)
	1
	>>> get_points(Hand.SCISSORS, Outcome.DRAW)
	6
	'''
	return player.value + outcome.value

if __name__ == '__main__':
	import doctest
	doctest.testmod()
