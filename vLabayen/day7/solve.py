#!/bin/python3
import re


# Puzzle 1
# Step by step
def parse_rules():
	rules = {}
	with open('input.txt') as f:
		for line in f:
			outer_bag, inner_text = re.search(r'^(.*) bags? contain (.*)', line).groups()
			rules[outer_bag] = {}

			inner_bags_text = re.findall('(\d+ \w+ \w+) bags?', inner_text)
			for num, inner_bag in (inner_bag_text.split(' ', 1) for inner_bag_text in inner_bags_text):
				rules[outer_bag][inner_bag] = int(num)
	return rules

def can_contain(neddle, haystack, rules):
	if neddle in haystack: return True
	return any(can_contain(neddle, rules[k], rules) for k in haystack)

rules = parse_rules()
print(sum(1 for k,v in rules.items() if can_contain('shiny gold', v, rules)))

# As one-liner
# Parse rules
#with open('input.txt') as f: print({outer_bag: {inner_bag: num for num,inner_bag in (inner_bag_text.split(' ', 1) for inner_bag_text in re.findall('(\d+ \w+ \w+) bags?', inner_text))} for outer_bag,inner_text in (re.search(r'^(.*) bags? contain (.*)', line).groups() for line in f)})

# can_contain usage as an anonimous lambda function
#print(sum(1 for k,v in rules.items() if (lambda f,neddle,haystack,rules: f(f, neddle, haystack, rules))(lambda f,neddle,haystack,rules: True if neddle in haystack else any(f(f, neddle, rules[k], rules) for k in haystack), 'shiny gold', v, rules)))

# All in one
with open('input.txt') as f: print([sum(1 for k,v in rules.items() if (lambda f,neddle,haystack,rules: f(f, neddle, haystack, rules))(lambda f,neddle,haystack,rules: True if neddle in haystack else any(f(f, neddle, rules[k], rules) for k in haystack), 'shiny gold', v, rules)) for rules in [{outer_bag: {inner_bag: int(num) for num,inner_bag in (inner_bag_text.split(' ', 1) for inner_bag_text in re.findall('(\d+ \w+ \w+) bags?', inner_text))} for outer_bag,inner_text in (re.search(r'^(.*) bags? contain (.*)', line).groups() for line in f)}]][0])


# Puzzle 2
# Step by step
def count_inside(haystack, rules):
	superficial_bags = sum(haystack[k] for k in haystack)
	deeper_bags = sum(haystack[k] * count_inside(rules[k], rules) for k in haystack)
	return superficial_bags + deeper_bags

rules = parse_rules()
print(count_inside(rules['shiny gold'], rules))

# As one-liner
# count_inside usage as an anonimous lambda function
#print((lambda f,haystack,rules: f(f, haystack, rules))(lambda f,haystack,rules: sum(haystack[k] for k in haystack) + sum(haystack[k] * f(f, rules[k], rules) for k in haystack), rules['shiny gold'], rules))

# All in one
with open('input.txt') as f: print([(lambda f,haystack,rules: f(f, haystack, rules))(lambda f,haystack,rules: sum(haystack[k] for k in haystack) + sum(haystack[k] * f(f, rules[k], rules) for k in haystack), rules['shiny gold'], rules) for rules in [{outer_bag: {inner_bag: int(num) for num,inner_bag in (inner_bag_text.split(' ', 1) for inner_bag_text in re.findall('(\d+ \w+ \w+) bags?', inner_text))} for outer_bag,inner_text in (re.search(r'^(.*) bags? contain (.*)', line).groups() for line in f)}]][0])


# Thanks to
# https://medium.com/python-in-plain-english/how-to-write-terrible-code-using-recursive-python-lambdas-e41374d278f1
# for the insights on recusive anonimous lambdas
