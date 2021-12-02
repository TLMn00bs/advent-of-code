from itertools import product, takewhile, count
import re

def parse_rule(rule, raw_rules, rules = {}, r1 = None, r2 = None):
	if r1 == None: r1 = re.compile('"(\w)"')
	if r2 == None: r2 = re.compile('(\d+) ?(\d+)? ?\|? ?(\d+)? ?(\d+)?')

	rule_number, rule_text = rule.split(': ')
	if rule_number in rules: return rules

	m = r2.match(rule_text)
	if m:
		rc = m.groups()
		for i,constraint in ((_i,_c) for _i,_c in enumerate(rc) if _c != None):
			constraint_rule = raw_rules[constraint]
			parse_rule(f'{constraint}: {constraint_rule}', raw_rules, rules, r1, r2)

		rule_options = [[rules[o] for o in opt if o != None] for opt in ((rc[0], rc[1]), (rc[2], rc[3])) if not all(o is None for o in opt)]
		rules[rule_number] = list(set([opt for optlist in [[''.join(p) for p in product(*ropt)] for ropt in rule_options] for opt in optlist]))
	else:
		g = r1.match(rule_text).groups()[0]
		rules[rule_number] = [g]

	return rules

with open('input.txt') as f:
	text_rules, messages = [group.split('\n') for group in f.read()[:-1].split('\n\n')]
	raw_rules = {k : text for k,text in (tr.split(': ') for tr in text_rules)}
	rules = parse_rule(f'0: {raw_rules["0"]}', raw_rules, {})

	opt42, opt31 = rules['42'], rules['31']
	p1 = re.compile('^({opt42})({opt42})({opt31})$'.format(opt42 = '|'.join(opt42), opt31 = '|'.join(opt31)))
	p2 = [re.compile('^({opt42})({opt42})*({opt42}){repeat11}({opt31})$'.format(
	        opt42 = '|'.join(opt42),
	        opt31 = '|'.join(opt31),
	        repeat11 = ('({opt42})' * n + '({opt31})' * n).format(opt42 = '|'.join(opt42), opt31 = '|'.join(opt31))
	)) for n in range(5)]


	c1, c2 = 0, 0
	for msg in messages:
		if p1.match(msg): c1 += 1
		if any(p.match(msg) for p in p2):  c2 += 1
	print(c1)
	print(c2)
