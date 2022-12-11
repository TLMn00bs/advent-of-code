#!/bin/python3
from domain import Hand, get_outcome, get_points

opponent_strategy = {'A': Hand.ROCK, 'B': Hand.PAPER, 'C': Hand.SCISSORS}

def p1(args):
	player_strategy = {'X': Hand.ROCK, 'Y': Hand.PAPER, 'Z': Hand.SCISSORS}

	with open(args.file, 'r') as f:
		games = [line.strip().split(" ") for line in f]
		hands = [{
			'opponent': opponent_strategy[opponent_encrypted_hand],
			'player'  : player_strategy[player_encrypted_hand],
		} for opponent_encrypted_hand, player_encrypted_hand in games]

	outcomes = [get_outcome(**hand) for hand in hands]
	points = [get_points(hand['player'], outcome) for hand, outcome in zip(hands, outcomes)]
	print(sum(points))

def p2(args):
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
