#!/bin/python3
from domain import Hand, Outcome, get_outcome, get_points, get_player_hand
opponent_strategy = {'A': Hand.ROCK, 'B': Hand.PAPER, 'C': Hand.SCISSORS}

def read_file(file, player_strategy):
	with open(args.file, 'r') as f:
		games = [line.strip().split(" ") for line in f]
		opponent, player = zip(*[(
			opponent_strategy[opponent_encrypted_hand],
			player_strategy[player_encrypted_hand]
		) for opponent_encrypted_hand, player_encrypted_hand in games])

	return opponent, player

def p1(args):
	opponent, player = read_file(args.file, {'X': Hand.ROCK, 'Y': Hand.PAPER, 'Z': Hand.SCISSORS})
	outcomes = [get_outcome(*hands) for hands in zip(opponent, player)]
	points = [get_points(hand, outcome) for hand, outcome in zip(player, outcomes)]
	print(sum(points))

def p2(args):
	opponent, outcomes = read_file(args.file, {'X': Outcome.LOSE, 'Y': Outcome.DRAW, 'Z': Outcome.WIN})
	player = [get_player_hand(hand, outcome) for hand, outcome in zip(opponent, outcomes)]
	points = [get_points(hand, outcome) for hand, outcome in zip(player, outcomes)]
	print(sum(points))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
