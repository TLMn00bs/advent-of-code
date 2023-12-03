from typing import Iterable, Dict, Tuple, List, Set
from attrs import define, field
from enum import IntEnum, auto
from itertools import count
import re
import logging
from functools import lru_cache


@define(kw_only=True)
class Resources:
	ore     : int = 0
	clay    : int = 0
	obsidian: int = 0
	geode   : int = 0

	def __add__(self, other: 'Resources'): return Resources(
		ore      = self.ore      + other.ore,
		clay     = self.clay     + other.clay,
		obsidian = self.obsidian + other.obsidian,
		geode    = self.geode    + other.geode,
	)
	
	def __sub__(self, other: 'Resources'): return Resources(
		ore      = self.ore      - other.ore,
		clay     = self.clay     - other.clay,
		obsidian = self.obsidian - other.obsidian,
		geode    = self.geode    - other.geode,
	)

	def __le__(self, other: 'Resources'): return all((
		self.ore      <= other.ore,
		self.clay     <= other.clay,
		self.obsidian <= other.obsidian,
		self.geode    <= other.geode,
	))

class BuildOption(IntEnum):
	NOP      = auto()
	ORE      = auto()
	CLAY     = auto()
	OBSIDIAN = auto()
	GEODE    = auto()

	def __repr__(self) -> str: return self.name

@define
class Blueprint:
	id      : int
	ore     : Resources
	clay    : Resources
	obsidian: Resources
	geode   : Resources

	max_costs: 'Resources' = field(init=False)
	robot_costs: Dict[BuildOption, Resources] = field(init=False)
	def __attrs_post_init__(self):
		self.robot_costs = {
			BuildOption.ORE     : self.ore,
			BuildOption.CLAY    : self.clay,
			BuildOption.OBSIDIAN: self.obsidian,
			BuildOption.GEODE   : self.geode,
		}
		self.max_costs = Resources(
			ore      = max(costs.ore      for costs in self.robot_costs.values()),
			clay     = max(costs.clay     for costs in self.robot_costs.values()),
			obsidian = max(costs.obsidian for costs in self.robot_costs.values()),
			geode    = max(costs.geode    for costs in self.robot_costs.values()),
		)

	@staticmethod
	def from_file(file: str) -> Iterable['Blueprint']:
		parse_blueprint = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')
		with open(file, 'r') as f:
			for line in f:
				m = parse_blueprint.match(line)
				if not m: raise ValueError(f'Failed to pase line: {line}')

				bp_id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = (int(v) for v in m.groups())
				yield Blueprint(bp_id,
					ore      = Resources(ore = ore_ore),
					clay     = Resources(ore = clay_ore),
					obsidian = Resources(ore = obsidian_ore, clay = obsidian_clay),
					geode    = Resources(ore = geode_ore, obsidian = geode_obsidian)
				)

# https://es.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
@lru_cache(maxsize=50)
def triangular_number(n: int) -> int:
	if n <= 0: return 0
	return n * (n + 1) // 2

@lru_cache(maxsize=100)
def best_collect_time(mineral_amount: int) -> int:
	''' Compute the best time to collect the given amount of any mineral, assuming a current production of 0 and infinite of the required resources '''
	remaining = mineral_amount
	for i in count():
		remaining -= i
		if remaining <= 0: return i

	raise ValueError(f'Cannot reach this point')

def max_aditional_geode(resources: Resources, production: Resources, blueprint: Blueprint, time: int) -> int:
	# If we assume we have infinite resources, the max generated geodes will be the triangular number of time - 1
	# if no clay robot is available, we need aditional time to at least collect enough clay to build the first obsidian robot
	# if no obsidian robot is available, we need additional time to at least collect enough obsidian for the first geode robot
	build_time = 1
	if production.clay     == 0: build_time += best_collect_time(resources.clay     - blueprint.obsidian.clay)
	if production.obsidian == 0: build_time += best_collect_time(resources.obsidian - blueprint.geode.obsidian)
	return triangular_number(time - build_time)

def ensured_resources(resources: Resources, production: Resources, time: int) -> int:
	return resources.geode + (production.geode * time)


def is_buildable(resources: Resources, costs: Resources) -> bool: return costs <= resources
def should_build(resource_production: int, max_resource_cost: int, resources: Resources, production: Resources, costs: Resources, choices: List[BuildOption]) -> bool:
	'''
	The robot must not have been delayed (when a NOPE is selected having the option to build a robot, that robot should not be built again until something else is built, since there is no point in just delaying it)
	It must make sense building it (it's production is < greater cost of that resource)
	It must be buildable (costs <= resources)
	'''
	was_delayed = False
	if len(choices) > 0 and choices[-1] == BuildOption.NOP:
		prev_resources = resources - production
		was_delayed = is_buildable(prev_resources, costs)

	return (
		not was_delayed                             and
		resource_production < max_resource_cost     and
		is_buildable(resources, costs)
	)

def build_options(resources: Resources, production: Resources, blueprint: Blueprint, time: int, choices: List[BuildOption]) -> Iterable[Tuple[BuildOption, Resources, Resources]]:
	''' Return an iterable with all the available options
	Each option consists in: (OptionIdentifier, OptionCosts, ProductionIncrease)
	'''
	# If there is just one turn left, there is no point in start building anything
	if time <= 1:
		yield BuildOption.NOP, Resources(), Resources()
		return

	# If we can build a geode robot, just do it
	if is_buildable(resources, blueprint.geode):
		yield BuildOption.GEODE, blueprint.geode, Resources(geode=1)
		return


	# Yield every robot that makes sense building
	if should_build(production.obsidian, blueprint.max_costs.obsidian, resources, production, blueprint.obsidian, choices):
		yield BuildOption.OBSIDIAN, blueprint.obsidian, Resources(obsidian=1)

	if should_build(production.clay, blueprint.max_costs.clay, resources, production, blueprint.clay, choices):
		yield BuildOption.CLAY, blueprint.clay, Resources(clay=1)

	if should_build(production.ore, blueprint.max_costs.ore, resources, production, blueprint.ore, choices):
		yield BuildOption.ORE, blueprint.ore, Resources(ore=1)

	# Not to build is always an option
	yield BuildOption.NOP, Resources(), Resources()


def compute_largest_number_of_geodes(resources: Resources, production: Resources, blueprint: Blueprint, time: int, lower_limit: int = 0, choices: List[BuildOption] = [], **kwargs) -> int:
	max_remaining_geodes = max_aditional_geode(resources, production, blueprint, time)
	ensured_geodes = ensured_resources(resources, production, time)
	upper_limit = ensured_geodes + max_remaining_geodes

	# No more geodes extra can be obtained, just return whatever we are ensured to get
	# with the current resources and production
	if max_remaining_geodes == 0:
		# print(f'{lower_limit=}, {ensured_geodes=}, {choices=}')
		return ensured_geodes

	# This branch will not be able to obtain more geodes that we have already gotten in another one
	if upper_limit <= lower_limit:
		return ensured_geodes

	highest_geodes = 0
	for opt, spend, production_increase in build_options(resources, production, blueprint, time, choices):
		max_geodes = compute_largest_number_of_geodes(
			resources - spend + production,
			production + production_increase,
			blueprint,
			time - 1,
			lower_limit = lower_limit,
			choices = [*choices, opt],
			# **{
			# 	'debug_resources': resources - spend + production,
			# 	'debug_production': production + production_increase,
			# 	'debug_time': time - 1,
			# }
		)

		highest_geodes = max(highest_geodes, max_geodes)
		lower_limit    = max(highest_geodes, lower_limit)

	return highest_geodes


def p1(args):
	blueprints = list(Blueprint.from_file(args.file))

	quality_levels = []
	for bp in blueprints:
		max_geodes = compute_largest_number_of_geodes(Resources(), Resources(ore=1), bp, time=24)
		quality_levels.append(bp.id * max_geodes)

	print(sum(quality_levels))

def p2(args):
	blueprints = list(Blueprint.from_file(args.file))[:3]

	result = 1
	for bp in blueprints:
		max_geodes = compute_largest_number_of_geodes(Resources(), Resources(ore=1), bp, time=32)
		result *= max_geodes

	print(result)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
