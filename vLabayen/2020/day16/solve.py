import re
from itertools import takewhile
from functools import reduce

with open('input.txt') as f:
	lines = [line[:-1] for line in f if line != '\n']
	rules_generator = (re.search('(\w+ ?\w*): (\d+)-(\d+) or (\d+)-(\d+)', rule).groups() for rule in takewhile(lambda line: line != 'your ticket:', lines))
	rules = [{'field' : r[0], 'r1' : (int(r[1]), int(r[2])), 'r2' : (int(r[3]), int(r[4]))} for r in rules_generator]
	my_ticket = [int(n) for n in lines[len(rules) + 1].split(',')]
	nearby_tickets = [[int(n) for n in ticket.split(',')] for ticket in lines[len(rules) + 3:]]
	numbers = [n for ticket in nearby_tickets for n in ticket]

	print(sum(n for n in numbers if not any([(rule['r1'][0] <= n <= rule['r1'][1]) or (rule['r2'][0] <= n <= rule['r2'][1]) for rule in rules])))


with open('input.txt') as f:
	lines = [line[:-1] for line in f if line != '\n']
	rules_generator = (re.search('(\w+ ?\w*): (\d+)-(\d+) or (\d+)-(\d+)', rule).groups() for rule in takewhile(lambda line: line != 'your ticket:', lines))
	rules = [{'field' : r[0], 'r1' : (int(r[1]), int(r[2])), 'r2' : (int(r[3]), int(r[4]))} for r in rules_generator]
	[int(n) for n in lines[len(rules) + 1].split(',')]
	nearby_tickets = [[int(n) for n in ticket.split(',')] for ticket in lines[len(rules) + 3:]]

	valid_tickets = [ticket for ticket in nearby_tickets if all(any([(rule['r1'][0] <= n <= rule['r1'][1]) or (rule['r2'][0] <= n <= rule['r2'][1]) for rule in rules]) for n in ticket)]

	field_to_index = {r['field'] : [*range(len(rules))] for r in rules}


	for r in rules:
		for ticket in takewhile(lambda _: sum(len(options) for options in field_to_index.values()) != len(field_to_index), valid_tickets):
			for i,n in enumerate(ticket):
				if not ((r['r1'][0] <= n <= r['r1'][1]) or (r['r2'][0] <= n <= r['r2'][1])):
					field_to_index[r['field']].remove(i)

	sorted_fields = sorted(field_to_index.keys(), key=lambda k: len(field_to_index[k]))
	for i,sf in enumerate(sorted_fields):
		v = field_to_index[sf][0]
		for field in sorted_fields[i+1:]:
			field_to_index[field].remove(v)

	departure_fields_index = [idx[0] for field,idx in field_to_index.items() if field.startswith('departure')]
	print(reduce(lambda x,y: x*y, [my_ticket[idx] for idx in departure_fields_index]))
