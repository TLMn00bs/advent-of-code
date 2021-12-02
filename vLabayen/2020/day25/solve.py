from itertools import repeat

def loop_size(number, subject_number = 7, value = 1):
	loop_size = 0
	while value != number:
		value = (value * subject_number) % 20201227
		loop_size += 1
	return loop_size

def encryption_key(loop_size, public_key):
	value = 1
	for _ in repeat(None, loop_size):
		value = (value * public_key) % 20201227
	return value

with open('input.txt') as f:
	card_key, door_key = [int(n) for n in f.read()[:-1].split('\n')]
	print(card_key, door_key)

	card_loop_size = loop_size(card_key)
	key = encryption_key(card_loop_size, door_key)
	print(key)
