import typing

def get_rucksack_compartments(rucksack: str) -> typing.Tuple[str, str]:
	''' Returns the item in each compartment of a rucksack
	
	>>> get_rucksack_compartments('vJrwpWtwJgWrhcsFMMfFFhFp')
	('vJrwpWtwJgWr', 'hcsFMMfFFhFp')
	>>> get_rucksack_compartments('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
	('jqHRNqRjqzjGDLGL', 'rsFMfFZSrLrFZsSL')
	>>> get_rucksack_compartments('PmmdzqPrVvPwwTWBwg')
	('PmmdzqPrV', 'vPwwTWBwg')
	'''
	compartment_size = len(rucksack) // 2
	return (
		rucksack[:compartment_size],
		rucksack[compartment_size:],
	)

def get_shared_item(*containers: typing.List[str]) -> str:
	''' Returns the common item to all containers
	
	>>> get_shared_item('vJrwpWtwJgWr', 'hcsFMMfFFhFp')
	'p'
	>>> get_shared_item('jqHRNqRjqzjGDLGL', 'rsFMfFZSrLrFZsSL')
	'L'
	>>> get_shared_item('PmmdzqPrV', 'vPwwTWBwg')
	'P'
	'''
	return set.intersection(*[set(c) for c in containers]).pop()

def get_item_priority(item: str) -> int:
	''' Get the items priority

	>>> get_item_priority('p')
	16
	>>> get_item_priority('L')
	38
	>>> get_item_priority('P')
	42
	>>> get_item_priority('v')
	22
	>>> get_item_priority('t')
	20
	>>> get_item_priority('s')
	19
	'''
	# By requirements:
	# 	a-z --> 1  - 26
	#   A-Z --> 27 - 52
	# 
	# https://www.asciitable.com/
	# Subtract 96 to lowerCase codes to offset them to 1
	# Subtract 64 to upperCase codes to offset them to 1, then add 26
	ascii_code = ord(item)
	isLowerCase = ascii_code > 96

	if isLowerCase: return ascii_code - 96
	return ascii_code - 64 + 26

if __name__ == '__main__':
	import doctest
	doctest.testmod()