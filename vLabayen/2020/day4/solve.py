data = []

with open('input.txt') as f:
#with open('test2.txt') as f:
	passport = {}
	line = None
	for line in f:
		if line == '\n':
			data.append(passport)
			passport = {}
		else:
			for field,value in [fv.split(':') for fv in line[:-1].split(' ')]:
				passport[field] = value
	data.append(passport)


valid = 0
for p in data:
	if all(field in p for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']):
		isValid = True
		try:
			isValid = (isValid and (1920 <= int(p['byr']) <= 2002))
			if not isValid: print('invalid byr : {}'.format(p))

			isValid = (isValid and (2010 <= int(p['iyr']) <= 2020))
			if not isValid: print('invalid iyr : {}'.format(p))

			isValid = (isValid and (2020 <= int(p['eyr']) <= 2030))
			if not isValid: print('invalid eyr : {}'.format(p))

			num, unit = p['hgt'][:-2], p['hgt'][-2:]
			if unit == 'cm': isValid = (isValid and (150 <= int(num) <= 193))
			elif unit == 'in': isValid = (isValid and (59 <= int(num) <= 76))
			else: isValid = False
			if not isValid: print('invalid hgt : {}'.format(p))

			isValid = (isValid and (len(p['hcl']) == 7 and p['hcl'][0] == '#' and all(l in '0123456789abcdef' for l in p['hcl'][1:])))
			if not isValid: print('invalid hcl : {}'.format(p))

			isValid = (isValid and (p['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']))
			if not isValid: print('invalid ecl : {}'.format(p))

			isValid = (isValid and (len(p['pid']) == 9))
			if not isValid: print('invalid pid : {}'.format(p))

		except : isValid = False

		if isValid:
			valid += 1
			print('valid : {}'.format(p))
#		else: print('invalid : {}'.format(p))
#	else: print('invalid : {}'.format(p))

print(valid)
