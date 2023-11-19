from typing import List
from enum import Enum

class Jet(Enum):
	left  = '<'
	right = '>'

def read_file(file: str) -> List[Jet]:
	with open(file, 'r') as f:
		return [Jet(jet) for jet in f.read().strip()]

def jets_gen(file: str):
	jets = read_file(file)
	while True:
		for i, jet in enumerate(jets): yield i, jet

