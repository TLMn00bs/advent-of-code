#!/bin/python3
from typing import Dict, List
import logging
import re

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

def resolve(name: str, monkeys: Dict[str, str]) -> int:
	job = monkeys[name]

	deps = find_dependencies(job)
	while len(deps) > 0:
		for dep in deps:
			job = job.replace(dep, f'({monkeys[dep]})')

		deps = find_dependencies(job)

	return int(eval(job))

def p1(args):
	monkeys = read_file(args.file)
	print(resolve('root', monkeys))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
