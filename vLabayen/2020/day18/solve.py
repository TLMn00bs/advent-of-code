import re

def extract_parentheses(exp):
	if not '(' in exp: return []

	matches = []
	nested_level, start_match = 0, 0
	for i,c in enumerate(exp):
		if c == '(':
			if nested_level == 0: start_match = i + 1
			nested_level += 1
		if c == ')':
			nested_level -= 1
			if nested_level == 0: matches.append(exp[start_match:i])

	return matches

def solve1(exp):
	parentheses = extract_parentheses(exp)
	for p in parentheses:
		s = solve1(p)
		exp = exp.replace(f'({p})', str(s), 1)

	while match := re.search('\d+ [\*\+] \d+', exp):
		g = match.group()
		r = eval(g)
		exp = exp.replace(g, str(r), 1)

	return int(exp)

with open('input.txt') as f:
	expressions = [line[:-1] for line in f]
	print(sum(solve1(exp) for exp in expressions))



def solve2(exp):
	parentheses = extract_parentheses(exp)
	for p in parentheses:
		s = solve2(p)
		exp = exp.replace(f'({p})', str(s), 1)

	while match := re.search('\d+ [\+] \d+', exp):
		g = match.group()
		r = eval(g)
		exp = exp.replace(g, str(r), 1)

	return eval(exp)


with open('input.txt') as f:
	expressions = [line[:-1] for line in f]

#	print(solve2('1 + 2 * 3 + 4 * 5 + 6'))

	print(sum(solve2(exp) for exp in expressions))
