#!/bin/python3
import re


# Puzzle 1
# Step by step
with open('input.txt') as f:
	fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

	s = 0
	for pdata in f.read()[:-1].split('\n\n'):
		fv = pdata.replace('\n', ' ').split(' ')
		passport = {f : v for f,v in (_fv.split(':') for _fv in fv)}
		if all(field in passport for field in fields): s += 1
	print(s)

# As one-liner
# const fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
with open('input.txt') as f: print(sum(1 for passport in ({f : v for f,v in (_fv.split(':') for _fv in pdata.replace('\n', ' ').split(' '))} for pdata in f.read()[:-1].split('\n\n')) if all(field in passport for field in fields)))


# Puzzle 2
# Step by step
data = []
with open('input.txt') as f:
	fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
	hgt_check = {'cm' : {'l' : 150, 'h' : 193}, 'in' : {'l' : 59, 'h' : 76}}
	ecl_check = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

	s = 0
	for pdata in f.read()[:-1].split('\n\n'):
		fv = pdata.replace('\n', ' ').split(' ')
		passport = {f : v for f,v in (_fv.split(':') for _fv in fv)}
		if all(field in passport for field in fields):
			if not 1920 <= int(passport['byr']) <= 2002: continue
			if not 2010 <= int(passport['iyr']) <= 2020: continue
			if not 2020 <= int(passport['eyr']) <= 2030: continue
#			if not (passport['hgt'][-2:] in hgt_check and hgt_check[passport['hgt'][-2:]]['l'] <= int(passport['hgt'][:-2]) <= hgt_check[passport['hgt'][-2:]]['h']): continue
			if not any((passport['hgt'][-2:] in hc and hc[passport['hgt'][-2:]]['l'] <= int(passport['hgt'][:-2]) <= hc[passport['hgt'][-2:]]['h']) for hc in [hgt_check]): continue
			if not re.match('^#[0-9a-f]{6}$', passport['hcl']): continue
			if not passport['ecl'] in ecl_check: continue
			if not re.match('^[0-9]{9}$', passport['pid']): continue
			s += 1
	print(s)

# As one-liner
# const fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
# const hgt_check = {'cm' : {'l' : 150, 'h' : 193}, 'in' : {'l' : 59, 'h' : 76}}
# const ecl_check = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
with open('input.txt') as f: print(sum(1 for passport in ({f : v for f,v in (_fv.split(':') for _fv in pdata.replace('\n', ' ').split(' '))} for pdata in f.read()[:-1].split('\n\n')) if all(field in passport for field in fields) and 1920 <= int(passport['byr']) <= 2002 and 2010 <= int(passport['iyr']) <= 2020 and 2020 <= int(passport['eyr']) <= 2030 and any((passport['hgt'][-2:] in hc and hc[passport['hgt'][-2:]]['l'] <= int(passport['hgt'][:-2]) <= hc[passport['hgt'][-2:]]['h']) for hc in [hgt_check]) and re.match('^#[0-9a-f]{6}$', passport['hcl']) and passport['ecl'] in ecl_check and re.match('^[0-9]{9}$', passport['pid'])))
