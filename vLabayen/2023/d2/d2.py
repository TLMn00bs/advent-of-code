import logging
from typing import List, Iterable
from attrs import define
from enum import Enum
import re

class Cube(Enum):
	RED   = 'red'
	GREEN = 'green'
	BLUE  = 'blue'

@define
class CubesSet:
	red  : int = 0
	green: int = 0
	blue : int = 0

	_from_text_rgx = re.compile(f'([0-9]+) ({"|".join(c.value for c in Cube)})')

	@staticmethod
	def from_text(text: str) -> 'CubesSet':
		matched_groups = (m.groups() for m in CubesSet._from_text_rgx.finditer(text))
		reveals = {color: int(value) for value, color in matched_groups}
		return CubesSet(**reveals)
	
	def __gt__(self, other: 'CubesSet') -> bool:
		return any([
			self.red   > other.red,
			self.green > other.green,
			self.blue  > other.blue,
		])
	
	def power(self): return self.red * self.green * self.blue

@define
class Game:
	id: int
	reveals: List[CubesSet]

	_from_text_game_id_rgx = re.compile('Game ([0-9]+): (.*)')
	_from_text_reveals_rgx = re.compile(' ?([0-9 a-z,]+)')

	@staticmethod
	def from_text(text: str) -> 'Game':
		game_id, reveals = Game._from_text_game_id_rgx.match(text).groups()		# type: ignore
		return Game(
			id = int(game_id),
			reveals = [CubesSet.from_text(reveal.group(1)) for reveal in Game._from_text_reveals_rgx.finditer(reveals)]
		)

	def fewest_required_cubes(self) -> CubesSet:
		return CubesSet(
			red   = max(cubes.red   for cubes in self.reveals),
			green = max(cubes.green for cubes in self.reveals),
			blue  = max(cubes.blue  for cubes in self.reveals),
		)

def read_file(file: str) -> Iterable[Game]:
	with open(file, 'r') as f:
		for line in f: yield Game.from_text(line)


def filter_imposibles(games: Iterable[Game], bag_content: CubesSet) -> Iterable[Game]:
	for game in games:
		if any(reveal > bag_content for reveal in game.reveals): continue
		yield game

def p1(args):
	games = read_file(args.file)
	bag_content = CubesSet(
		red   = 12,
		green = 13,
		blue  = 14
	)

	possible_games = filter_imposibles(games, bag_content)
	print(sum(game.id for game in possible_games))

def p2(args):
	games = read_file(args.file)
	game_cubes = [game.fewest_required_cubes() for game in games]
	print(sum(cubes.power() for cubes in game_cubes))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
