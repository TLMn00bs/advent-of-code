import re

rules = {}

with open('input.txt') as f:
	for line in f:
		items = re.search(r'^(.*) bag(s?) contain (.*)', line).groups()
		outside_bag = items[0]
		inside_bags = items[2]

		inside_items = inside_bags.replace('bags', ';').replace('bag', ';').replace(';.', '').replace(',', '').strip().split(' ; ')

		rules[outside_bag] = {}
		for item in inside_items:
			if item == 'no other': continue

			num, bag, _ = re.search(r'(\d) (.*)(s?)', item).groups()
			rules[outside_bag][bag] = num


def search_for(haystack, neddle):
	if neddle in haystack: return True
	for k in haystack: return any(search_for(rules[k], neddle) for k in haystack)

def count_inside(haystack):
	level1 = sum(int(haystack[k]) for k in haystack)
	inside_levels = sum(int(haystack[k]) * count_inside(rules[k]) for k in haystack)
	return level1 + inside_levels

print(sum(1 for k in rules if search_for(rules[k], 'shiny gold')))
print(count_inside(rules['shiny gold']))



#with open('input.txt') as f: rules = {obag : {ibag : n for n, ibag, _ in (re.search(r'(\d) (.*)(s?)', item).groups() for item in ibags.replace('bags', ';').replace('bag', ';').replace(';.', '').replace(',', '').strip().split(' ; ') if item != 'no other')} for obag, _, ibags in (re.search(r'^(.*) bag(s?) contain (.*)', line).groups() for line in f)}
with open('input.txt') as f: rules = {obag : {ibag : n for n, ibag, _ in (re.search(r'(\d) (.*)(s?)', item).groups() for item in re.sub('(\s+)?bags?(\s+)?,?.?', ';', ibags).split(';')[:-1] if item != 'no other')} for obag, _, ibags in (re.search(r'^(.*) bag(s?) contain (.*)', line).groups() for line in f)}

#https://medium.com/python-in-plain-english/how-to-write-terrible-code-using-recursive-python-lambdas-e41374d278f1
