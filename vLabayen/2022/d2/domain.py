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

def get_player_hand(opponent: Hand, outcome: Outcome) -> int:
	''' Returns the player's required hand to get the given outcome
	
	>>> get_player_hand(Hand.ROCK, Outcome.DRAW)
	<Hand.ROCK: 1>
	>>> get_player_hand(Hand.PAPER, Outcome.LOSE)
	<Hand.ROCK: 1>
	>>> get_player_hand(Hand.SCISSORS, Outcome.WIN)
	<Hand.ROCK: 1>
	'''
	if outcome == Outcome.WIN: return gameHands[opponent]['toWin']
	if outcome == Outcome.LOSE: return gameHands[opponent]['toLose']
	return opponent

if __name__ == '__main__':
	import doctest
	doctest.testmod()
