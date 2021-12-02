from itertools import islice, cycle, repeat
from functools import reduce

def puzzle(npuzzle, file):
	with open(file) as f: cups = [int(cup) for cup in f.read()[:-1]]

	if npuzzle == 1: niter = 100
	elif npuzzle == 2:
		cups += [*range(max(cups) + 1, 1000000 + 1)]
		niter = 10000000


	lcups = len(cups)
	linkedlist = {cup : cups[(i + 1) % lcups] for i,cup in enumerate(cups)}
	current_cup_value = cups[0]
	for _ in repeat(None, niter):
		# Tmp variable to lookup the next one
		current_value = current_cup_value
		# Pick up values
		pick_up_values = [current_value := linkedlist[current_value] for _ in repeat(None, 3)]

		# Destination value
		destination_value = current_cup_value - 1 if current_cup_value - 1 > 0 else lcups
		while destination_value in pick_up_values: destination_value = destination_value - 1 if destination_value - 1 > 0 else lcups

		# Current value must be followed by the next of last picked up
		linkedlist[current_cup_value] = linkedlist[pick_up_values[-1]]
		# The last picked up must be followed by the next of the destination value
		linkedlist[pick_up_values[-1]] = linkedlist[destination_value]
		# Destination value must be followed by the first picked up
		linkedlist[destination_value] = pick_up_values[0]

		current_cup_value = linkedlist[current_cup_value]

	current_value = 1
	cups = [current_value := linkedlist[current_value] for _ in range(lcups)]

	label_one_index = cups.index(1)
	if npuzzle == 1: print(''.join([str(cup) for cup in (cups[label_one_index+1:] + cups[:label_one_index])]))
	elif npuzzle == 2: print(reduce(lambda x,y: x*y, [*islice(cycle(cups), label_one_index + 1, label_one_index + 3)]))

puzzle(1, 'input.txt')
puzzle(2, 'input.txt')
