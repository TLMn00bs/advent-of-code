import re
file = open('input4.txt').read().split('\n\n')


def getPassport(line):
	passport = {}
	for campos in line.replace('\n',' ').split(' '):
		print(campos)
		if campos == '': continue
		f,v = campos.split(':')
		passport.update({f : v})
	return passport


valid = 0
param = ['byr','eyr','iyr','hgt','hcl','ecl','pid']
eyecolor = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
for line in file:
	passport = getPassport(line)
	isValid = True
	if all(p in passport for p in param):
		if not 1920 <= int(passport['byr']) <= 2002:
			isValid = False
		if not 2010 <= int(passport['iyr']) <= 2020:
			isValid = False
		if not 2020 <= int(passport['eyr']) <= 2030:
			isValid = False
		if passport['hgt'][-2:] == 'cm':
			if not 150 <= int(passport['hgt'][:-2]) <= 193:
				isValid = False
		elif passport['hgt'][-2:] == 'in':
			if not 59 <= int(passport['hgt'][:-2]) <= 76:
				isValid = False
		else: isValid = False
		if not re.match(r'^#[a-f0-9]{6}$',passport['hcl']):
			isValid = False
		if not passport['ecl'] in eyecolor:
			isValid = False
		if not re.match(r"^[0-9]{9}$",passport['pid']):
			isValid = False
	else:
		isValid = False

	if isValid: valid += 1

print(valid)


#	if all(p in passport for p in param):
#		valid += 1

