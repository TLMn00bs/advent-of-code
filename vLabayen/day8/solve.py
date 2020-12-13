#!/bin/python3
from functools import reduce


# Puzzle 1
# Step by step
with open('input.txt') as f:
	instructions = [(line[:3], int(line[4:-1])) for line in f]

	#Store a list with the index of the visited instructions
	vinst = []

	#Store the acumulator, the index of the current instruction and none
	memory = [
		0, 	# The acumulador
		0, 	# The index of the current instruction
		None	# Just None. Required in the one-liner solution
	]

	# Loop until the list contains elements (to avoid crash with [-1]) and the last element is present more than 1 times
	while not (len(vinst) > 0 and vinst.count(vinst[-1]) > 1):
		memory[2] = vinst.append(memory[1])		# Append returns None but modifies the list. (Here is the trick in the one-liner)

		inst, n = instructions[memory[1]]
		if inst == 'acc':
			memory[0] += n
			memory[1] += 1

		elif inst == 'nop':
			memory[1] += 1

		elif inst == 'jmp':
			memory[1] += n

	print(memory[0])

# As one-liner
# Explanation:
# reduce is used to have the memory variable.
# reduce call is surrounded in a [reduce(...) for vinst in [[]]] to create the array for visited instructions, which will be updated inside reduce.
# The iter(lambda: (...), True) function creates an iterable that return the result of executing the lambda function until the returned value matches the sentinel. See help(iter). This acts as the
#	while loop. The lambda function will check if a instruction is visited twice, using the vinst list we have already created and will be updated in the reduce call
# Here we use the None slot in the memory variable to append a instruction to the visited instructions array.

# Simplest example of this concept
#print([reduce(lambda memory,_: (ref_list.append(len(ref_list) > 3)), iter(lambda: True in ref_list, True), (None)) for ref_list in [[]]][0])

# Another example a little bit more complicated to allow showing whats going on
#def debug(x, prefix = ''):
#	print('{} {}'.format(prefix, x))
#	return x
#print([reduce(lambda memory,_: (ref_list.append(len(debug(ref_list, 'reduce1')) > 3), print('reduce2 {}'.format(ref_list))), iter(lambda: True in debug(ref_list, 'iter'), True), (None, None)) for ref_list in [[]]])

# Actual solution
with open('input.txt') as f: print([[reduce(lambda memory,_: [(memory[0] + n*(inst == 'acc'), (memory[1] + 1) if inst != 'jmp' else (memory[1] + n), vinst.append(memory[1])) for inst,n in [instructions[memory[1]]]][0], iter(lambda: len(vinst) > 0 and vinst.count(vinst[-1]) > 1, True), (0, 0, None)) for vinst in [[]]][0] for instructions in [[(line[:3], int(line[4:-1])) for line in f]]][0][0])


# Puzzle 2
# Step by step
with open('input.txt') as f:
	instructions = [(line[:3], int(line[4:-1])) for line in f]

	# Store the last idx and acumulator of each run
	run_results = []

	# Loop for all the instructions that can be replaced and get the replaced instruction and its index
	for replace_inst,replace_idx in (('nop' if _inst == 'jmp' else 'jmp', _idx) for _idx,(_inst,_n) in enumerate(instructions) if _inst != 'acc'):
		vinst = [0]		#In this puzzle, we must start with the first index here
		memory = [0, 0, None]

		# Add a new condition to check whether the new instruction index will be out of range
		while not (len(vinst) > 0 and (vinst.count(vinst[-1]) > 1 or vinst[-1] >= len(instructions))):
			#memory[2] = vinst.append(memory[1])		#We must append the index at the end of the loop
			# In this way, we can append the NEXT index and avoid the IndexError.
			# If we keep it the other way, the while will be checking one iteration late.

			# Get the replaced instruction (if we are in that index) and n
			inst, n = [(__inst, __n) if memory[1] != replace_idx else (replace_inst, __n) for __inst,__n in [instructions[memory[1]]]][0]

			if inst == 'acc':
				memory[0] += n
				memory[1] += 1

			elif inst == 'nop':
				memory[1] += 1

			elif inst == 'jmp':
				memory[1] += n

			vinst.append(memory[1])		# Append at the end

		run_results.append((memory[0], memory[1]))

	print([rr[0] for rr in run_results if rr[1] >= len(instructions)][0])

# As one-liner
# In order to simulate the 'append at the end of the loop', we have to repeat the new_index calculation in the append call
with open('input.txt') as f: print([[rr[0] for rr in [[reduce(lambda memory,_: [(memory[0] + n*(inst == 'acc'), (memory[1] + 1) if inst != 'jmp' else (memory[1] + n), vinst.append((memory[1] + 1) if inst != 'jmp' else (memory[1] + n))) for inst, n in [(__inst, __n) if memory[1] != replace_idx else (replace_inst, __n) for __inst,__n in [instructions[memory[1]]]]][0], iter(lambda: len(vinst) > 0 and (vinst.count(vinst[-1]) > 1 or vinst[-1] >= len(instructions)), True), (0, 0, None)) for vinst in [[]] ][0] for replace_inst,replace_idx in (('nop' if _inst == 'jmp' else 'jmp', _idx) for _idx,(_inst,_n) in enumerate(instructions) if _inst != 'acc')] if rr[1] >= len(instructions)][0] for instructions in [[(line[:3], int(line[4:-1])) for line in f]]][0])

# Same, but as legible as i can put that f***ing sh**
#with open('input.txt') as f: print([
#	[rr[0] for rr in
#		[
#			[reduce(
#				lambda memory,_: [(
#					memory[0] + n*(inst == 'acc'),
#					(memory[1] + 1) if inst != 'jmp' else (memory[1] + n),
#					vinst.append((memory[1] + 1) if inst != 'jmp' else (memory[1] + n))
#				) for inst, n in [
#					(__inst, __n) if memory[1] != replace_idx else (replace_inst, __n) for __inst,__n in [instructions[memory[1]]]
#				]][0],
#				iter(lambda: len(vinst) > 0 and (vinst.count(vinst[-1]) > 1 or vinst[-1] >= len(instructions)), True),
#				(0, 0, None)
#			) for vinst in [[]] ][0]
#		for replace_inst,replace_idx in (
#			('nop' if _inst == 'jmp' else 'jmp', _idx) for _idx,(_inst,_n) in enumerate(instructions) if _inst != 'acc'
#		)]
#	if rr[1] >= len(instructions)][0]
#for instructions in [[(line[:3], int(line[4:-1])) for line in f]]][0])

# Some reources i have read
# iter as a 'infinite generator': https://stackoverflow.com/questions/5737196/is-there-an-expression-for-an-infinite-iterator
# also check the oficial documentation: help(iter)
# Other resources i have read that finally doesn't end up in the solution
#	https://stackoverflow.com/questions/9572833/using-break-in-a-list-comprehension#9572933
#	https://stackoverflow.com/questions/9059173/what-is-the-purpose-in-pythons-itertools-repeat
# The ref_list trick was developed on my own
# Thanks for reading if you got this far ;)
