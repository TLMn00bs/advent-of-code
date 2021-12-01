#!/bin/python3
from itertools import combinations
from functools import reduce
import re

print('Day 1:')
with open('day1/input.txt') as f: print([x*y for x,y in combinations((int(line[:-1]) for line in f), 2) if (x + y == 2020)][0])
with open('day1/input.txt') as f: print([x * y * z for x,y,z in combinations((int(line[:-1]) for line in f), 3) if (x + y + z == 2020)][0])

print('\nDay 2:')
with open('day2/input.txt') as f: print(sum(1 for c1,c2,l,p in ([int(c) for c in conditions.split('-')] + [letter[:-1]] + [passwd] for conditions,letter,passwd in (line[:-1].split(' ') for line in f)) if c1 <= p.count(l) <= c2))
with open('day2/input.txt') as f: print(sum(1 for c1,c2,l,p in ([int(c) for c in conditions.split('-')] + [letter[:-1]] + [passwd] for conditions,letter,passwd in (line[:-1].split(' ') for line in f)) if (p[c1 - 1] == l) ^ (p[c2 - 1] == l)))

print('\nDay 3:')
with open('day3/input.txt') as f: print(sum(1 for r,line in enumerate(_line[:-1] for _r,_line in enumerate(f) if _r%1 == 0) if line[3 * r % len(line)] == '#'))
with open('day3/input.txt') as f: print(reduce(lambda x,y: x*y, [cs[0] for cs in reduce(lambda c,enum,slopes=[(1,1), (3,1), (5,1), (7,1), (1,2)]: [[c[i][0] + 1*(line[x * c[i][1] % len(line)] == '#' and r%y == 0), c[i][1] + 1*(r%y == 0)] for i,(x,y) in enumerate(slopes) for r,line in [enum]], ((_r,_line[:-1]) for _r,_line in enumerate(f)), [[0,0] for _ in range(5)])]))

print('\nDay 4:')
with open('day4/input.txt') as f: print(sum(1 for passport in ({f : v for f,v in (_fv.split(':') for _fv in pdata.replace('\n', ' ').split(' '))} for pdata in f.read()[:-1].split('\n\n')) if all(field in passport for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])))
with open('day4/input.txt') as f: print(sum(1 for passport in ({f : v for f,v in (_fv.split(':') for _fv in pdata.replace('\n', ' ').split(' '))} for pdata in f.read()[:-1].split('\n\n')) if all(field in passport for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']) and 1920 <= int(passport['byr']) <= 2002 and 2010 <= int(passport['iyr']) <= 2020 and 2020 <= int(passport['eyr']) <= 2030 and any((passport['hgt'][-2:] in hc and hc[passport['hgt'][-2:]]['l'] <= int(passport['hgt'][:-2]) <= hc[passport['hgt'][-2:]]['h']) for hc in [{'cm' : {'l' : 150, 'h' : 193}, 'in' : {'l' : 59, 'h' : 76}}]) and re.match('^#[0-9a-f]{6}$', passport['hcl']) and passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'] and re.match('^[0-9]{9}$', passport['pid'])))

print('\nDay 5:')
with open('day5/input.txt') as f: print(max(set(8 * int(''.join([str(1 * (rowcode=='B')) for rowcode in code[:7]]), 2) + int(''.join([str(1 * (colcode=='R')) for colcode in code[7:]]), 2) for code in (line[:-1] for line in f))))
with open('day5/input.txt') as f: print([missing_id for missing_ids in (set(range(max(ids))).difference(ids) for ids in [[8 * int(''.join([str(1 * (rowcode=='B')) for rowcode in code[:7]]), 2) + int(''.join([str(1 * (colcode=='R')) for colcode in code[7:]]), 2) for code in (line[:-1] for line in f)]]) for missing_id in missing_ids if (missing_id-1 not in missing_ids) and (missing_id+1 not in missing_ids)][0])

print('\nDay 6:')
with open('day6/input.txt') as f: print(sum(len(g) for g in [set.union(*[set(person) for person in group.split('\n')]) for group in f.read()[:-1].split('\n\n')]))
with open('day6/input.txt') as f: print(sum(len(g) for g in [set.intersection(*[set(person) for person in group.split('\n')]) for group in f.read()[:-1].split('\n\n')]))

print('\nDay 7:')
with open('day7/input.txt') as f: print([sum(1 for k,v in rules.items() if (lambda f,neddle,haystack,rules: f(f, neddle, haystack, rules))(lambda f,neddle,haystack,rules: True if neddle in haystack else any(f(f, neddle, rules[k], rules) for k in haystack), 'shiny gold', v, rules)) for rules in [{outer_bag: {inner_bag: int(num) for num,inner_bag in (inner_bag_text.split(' ', 1) for inner_bag_text in re.findall('(\d+ \w+ \w+) bags?', inner_text))} for outer_bag,inner_text in (re.search(r'^(.*) bags? contain (.*)', line).groups() for line in f)}]][0])
with open('day7/input.txt') as f: print([(lambda f,haystack,rules: f(f, haystack, rules))(lambda f,haystack,rules: sum(haystack[k] for k in haystack) + sum(haystack[k] * f(f, rules[k], rules) for k in haystack), rules['shiny gold'], rules) for rules in [{outer_bag: {inner_bag: int(num) for num,inner_bag in (inner_bag_text.split(' ', 1) for inner_bag_text in re.findall('(\d+ \w+ \w+) bags?', inner_text))} for outer_bag,inner_text in (re.search(r'^(.*) bags? contain (.*)', line).groups() for line in f)}]][0])

print('\nDay 8:')
with open('day8/input.txt') as f: print([[reduce(lambda memory,_: [(memory[0] + n*(inst == 'acc'), (memory[1] + 1) if inst != 'jmp' else (memory[1] + n), vinst.append(memory[1])) for inst,n in [instructions[memory[1]]]][0], iter(lambda: len(vinst) > 0 and vinst.count(vinst[-1]) > 1, True), (0, 0, None)) for vinst in [[]]][0] for instructions in [[(line[:3], int(line[4:-1])) for line in f]]][0][0])
with open('day8/input.txt') as f: print([[rr[0] for rr in [[reduce(lambda memory,_: [(memory[0] + n*(inst == 'acc'), (memory[1] + 1) if inst != 'jmp' else (memory[1] + n), vinst.append((memory[1] + 1) if inst != 'jmp' else (memory[1] + n))) for inst, n in [(__inst, __n) if memory[1] != replace_idx else (replace_inst, __n) for __inst,__n in [instructions[memory[1]]]]][0], iter(lambda: len(vinst) > 0 and (vinst.count(vinst[-1]) > 1 or vinst[-1] >= len(instructions)), True), (0, 0, None)) for vinst in [[]] ][0] for replace_inst,replace_idx in (('nop' if _inst == 'jmp' else 'jmp', _idx) for _idx,(_inst,_n) in enumerate(instructions) if _inst != 'acc')] if rr[1] >= len(instructions)][0] for instructions in [[(line[:3], int(line[4:-1])) for line in f]]][0])

