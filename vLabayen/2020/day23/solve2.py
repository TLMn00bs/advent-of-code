from itertools import islice, cycle
from functools import reduce

def puzzle(npuzzle, file):
	with open(file) as f: cups = [int(cup) for cup in f.read()[:-1]]

	if npuzzle == 1: niter = 100
	elif npuzzle == 2:
#		cups += [*range(max(cups) + 1, 1000000 + 1)]
#		niter = 10000000
		cups += [*range(max(cups) + 1, 1000 + 1)]
		niter = 10000

	label_one_index = cups.index(1)
	lcups = len(cups)
	for i in range(niter):
		# Current cup index
		current_cup_index = i % lcups
		# Current cup value
		current_cup_value = cups[current_cup_index]

		# Pick up indices
		pu_index_1, pu_index_2, pu_index_3 = (i+1) % lcups, (i+2) % lcups, (i+3) % lcups
		# Pick up values
		pu_value_1, pu_value_2, pu_value_3 = cups[pu_index_1], cups[pu_index_2], cups[pu_index_3]

		# Destination value
		destination_value = current_cup_value - 1 if current_cup_value - 1 > 0 else lcups
		while destination_value == pu_value_1 or destination_value == pu_value_2 or destination_value == pu_value_3:
			destination_value = destination_value - 1 if destination_value - 1 > 0 else lcups
		# Destination index
		destination_index = cups.index(destination_value)

		label_one_index = cups.index(1)
		print(i, label_one_index, [cups[(label_one_index + i) % lcups] for i in range(-10, 11)])

#		close_range = 50
#		if any(label_one_index == ((current_cup_index - n) % lcups) for n in range(-close_range, close_range + 1)):
#			perform_shift(cups, current_cup_index, destination_index, lcups, pu_value_1, pu_value_2, pu_value_3)
#		elif any(label_one_index == ((destination_index - n) % lcups) for n in range(-close_range, close_range + 1)):
#			perform_shift(cups, current_cup_index, destination_index, lcups, pu_value_1, pu_value_2, pu_value_3)
#		else: continue

		perform_shift(cups, current_cup_index, destination_index, lcups, pu_value_1, pu_value_2, pu_value_3)

	label_one_index = cups.index(1)
	if npuzzle == 1: print(''.join([str(cup) for cup in (cups[label_one_index+1:] + cups[:label_one_index])]))
	elif npuzzle == 2: print(reduce(lambda x,y: x*y, [*islice(cycle(cups), label_one_index + 1, label_one_index + 3)]))

def perform_shift(cups, current_cup_index, destination_index, lcups, pu_value_1, pu_value_2, pu_value_3):
	# Shift non-picked up values
	for j in range(1, (destination_index - current_cup_index - 2) % lcups):
		cups[(current_cup_index + j) % lcups] = cups[(current_cup_index + j + 3) % lcups]
	# Place picked up values
	cups[(destination_index - 2) % lcups] = pu_value_1
	cups[(destination_index - 1) % lcups] = pu_value_2
	cups[(destination_index - 0) % lcups] = pu_value_3

#puzzle(1, 'input.txt')
puzzle(2, 'example.txt')
