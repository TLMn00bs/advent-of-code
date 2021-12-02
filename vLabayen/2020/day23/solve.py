from itertools import cycle, islice
from functools import reduce
import cProfile

def action1(current_cup_index, cups, lcups):
	removed_cups = [*islice(cycle(cups), current_cup_index + 1, current_cup_index + 4)]
#	cups = [cup for cup in cups if cup not in removed_cups]
	cups = [*islice(cycle(cups), current_cup_index + 4, current_cup_index + 1 + lcups)]
	return cups, removed_cups

#def action2(current_cup_value, cups):
def action2(current_cup_value, cups, removed_cups, lcups):
#	scups = list(sorted(cups, reverse=True))
#	cup_index = scups.index(current_cup_value)
#	destination_cup_value = [*islice(cycle(scups), cup_index + 1, cup_index + 2)][0]
#	return cups.index(destination_cup_value)

	search_value = current_cup_value - 1 if current_cup_value - 1 > 0 else lcups
	while search_value in removed_cups: search_value = search_value - 1 if search_value - 1 > 0 else lcups
	return cups.index(search_value)

def action3(current_cup_index, current_cup_value, removed_cups, destination_cup_index, cups):
	sliced_cups = cups[:destination_cup_index+1] + removed_cups + cups[destination_cup_index+1:]
	new_current_cup_index = sliced_cups.index(current_cup_value)
	return sliced_cups[new_current_cup_index-current_cup_index:] + sliced_cups[0:new_current_cup_index-current_cup_index]




with open('example.txt') as f:
	cups = [int(cup) for cup in f.read()[:-1]]
	lcups = len(cups)

	for i in range(100):
		current_cup_index, current_cup_value = i % len(cups), cups[i % len(cups)]

		cups, removed_cups = action1(current_cup_index, cups, lcups)
		destination_cup_index = action2(current_cup_value, cups, removed_cups, lcups)
		cups = action3(current_cup_index, current_cup_value, removed_cups, destination_cup_index, cups)

	label_one_index = cups.index(1)
	print(''.join([str(cup) for cup in (cups[label_one_index+1:] + cups[:label_one_index])]))


def p2():
	with open('example.txt') as f: cups = [int(cup) for cup in f.read()[:-1]]
	cups += [*range(max(cups) + 1, 1000000 + 1)]
	lcups = 1000000

	for i in range(1000):
		current_cup_index, current_cup_value = i % len(cups), cups[i % len(cups)]

		cups, removed_cups = action1(current_cup_index, cups, lcups)
		destination_cup_index = action2(current_cup_value, cups, removed_cups, lcups)
		cups = action3(current_cup_index, current_cup_value, removed_cups, destination_cup_index, cups)

	label_one_index = cups.index(1)
	print(reduce(lambda x,y: x*y, [*islice(cycle(cups), label_one_index + 1, label_one_index + 3)]))

#p2()
#cProfile.run('p2()', sort = 'cumtime')
