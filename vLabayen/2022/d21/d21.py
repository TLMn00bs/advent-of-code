#!/bin/python3
from typing import Dict, List
import logging
import re
from sympy.solvers import solve
from sympy import Symbol, Eq

parse_monkey_rgx = re.compile('([a-z]+): (.*)')
def read_file(file: str):
	monkeys: Dict[str, str] = {}
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			name, job = parse_monkey_rgx.match(line).groups()	# type: ignore
			monkeys[name] = job
	
	return monkeys

find_deps_rgx = re.compile('([a-z]+)')
def find_dependencies(job: str) -> List[str]:
	return find_deps_rgx.findall(job)

def resolve(name: str, monkeys: Dict[str, str]) -> str:
	job = monkeys[name]

	deps = find_dependencies(job)
	while len(deps) > 0:
		for dep in deps:
			job = job.replace(dep, f'({monkeys[dep]})')

		deps = find_dependencies(job)

	return job

def p1(args):
	monkeys = read_file(args.file)
	print(int(eval(resolve('root', monkeys))))


def p2(args):
	monkeys = read_file(args.file)
	monkeys['root'] = re.sub('[+-/*]', '=', monkeys['root'])
	monkeys['humn'] = 'X'

	root_eq = resolve('root', monkeys)
	root = re.sub('(.*) = (.*)', r'Eq(\1, \2)', root_eq).replace('X', 'Symbol("x")')
	print(int(solve(eval(root))[0]))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
