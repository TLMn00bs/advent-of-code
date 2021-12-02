from itertools import combinations
import sys

with open('input.txt') as f: numbers = [int(line[:-1]) for line in f]
offset = 25

c = 0
invalid_number = -1
for i,n in enumerate(numbers[offset:]):
	opt = numbers[i:offset + i]

	valid = False
	for c in combinations(opt, 2):
		if sum(c) == n:
			valid = True
			break

	if not valid:
		invalid_number = n
		break


print(invalid_number)


for i in range(len(numbers)):
	for j in range(len(numbers)):
		if sum(numbers[i:j]) == invalid_number: print(numbers[i:j], min(numbers[i:j]) + max(numbers[i:j]))
