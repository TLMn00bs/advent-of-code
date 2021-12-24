#!/bin/python3
from collections import Counter
from collections import defaultdict
import re

class DeterministicDice:
	def __init__(self):
		self.prev_roll = 0
		self.num_rolls = 0

	def __next__(self):
		self.num_rolls += 1

		if self.prev_roll ==100:
			self.prev_roll = 1
			return self.prev_roll

		self.prev_roll += 1
		return self.prev_roll

def next_position(current, step):
	virtual_position = current + step
	last_digit = str(virtual_position)[-1]
	if last_digit == '0': return 10
	return int(last_digit)

parse_rgx = re.compile('Player ([0-9]+) starting position: ([0-9]+)')
def parse(file):
	with open(file, 'r') as f: return {int(player): {'pos': int(position), 'score': 0} for player, position in (parse_rgx.match(line.strip()).groups() for line in f)}

def p1(args):
	players = parse(args.file)
	dice = DeterministicDice()

	players_list, turn = list(players.keys()), 0
	while all(player['score'] < 1000 for player in players.values()):
		player = players[players_list[turn % len(players_list)]]
		turn += 1

		step = sum(next(dice) for _ in range(3))
		stopping_position = next_position(player['pos'], step)

		player['score'] += stopping_position
		player['pos'] = stopping_position

	lossing_player_score = min(player['score'] for player in players.values())
	print(lossing_player_score * dice.num_rolls)


def split_universe(universes, dirac_dice_outcomes, player_in_turn):
	for universe in universes:
		for step, num_times in dirac_dice_outcomes.items():
			player = universe['players'][player_in_turn]
			players_not_in_turn = {p: {**pos_score} for p, pos_score in universe['players'].items() if p != player_in_turn}

			stopping_position = next_position(player['pos'], step)
			universe_players = {player_in_turn: {'pos': stopping_position, 'score': player['score'] + stopping_position}, **players_not_in_turn}
			yield {'num_copies': universe['num_copies'] * num_times, 'players': universe_players}

def universe2tuple(u): return (u['players'][1]['pos'], u['players'][1]['score'], u['players'][2]['pos'], u['players'][2]['score'])
def tuple2universe(t): return {1: {'pos': t[0], 'score': t[1]}, 2: {'pos': t[2], 'score': t[3]}}

def collapse_universes(universes):
	unique_universes = defaultdict(lambda: 0)
	for universe in universes:
		universe_hash = universe2tuple(universe)
		unique_universes[universe_hash] += universe['num_copies']

	return [{'num_copies': num_copies, 'players': tuple2universe(hash)} for hash, num_copies in unique_universes.items()]

def p2(args):
	players = parse(args.file)
	universes = [{'num_copies': 1, 'players': {player: {**pos_score} for player, pos_score in players.items()}}]
	dirac_dice_outcomes = {step: num_times for step, num_times in Counter(sum((r1,r2,r3)) for r1 in range(1, 4) for r2 in range(1, 4) for r3 in range(1, 4)).items()}

	winning_universes = {player: 0 for player in players.keys()}
	players_list, turn = list(players.keys()), 0
	while len(universes) != 0:
		player_in_turn = players_list[turn % len(players_list)]
		turn += 1

		universes = [*split_universe(universes, dirac_dice_outcomes, player_in_turn)]
		universes = [*collapse_universes(universes)]

		game_ended_universes = [(idx, universe) for idx, universe in enumerate(universes) if any(player['score'] >= 21 for player in universe['players'].values())]
		if len(game_ended_universes) > 0:
			ended_idx = {idx for idx,_ in game_ended_universes}
			for _, universe in game_ended_universes:
				winning_player = max((player for player in universe['players'].keys()), key = lambda p: universe['players'][p]['score'])
				winning_universes[winning_player] += universe['num_copies']

			universes = [universe for idx, universe in enumerate(universes) if idx not in ended_idx]

	print(max(winning_times for player, winning_times in winning_universes.items()))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

#	p1(args)
	p2(args)
