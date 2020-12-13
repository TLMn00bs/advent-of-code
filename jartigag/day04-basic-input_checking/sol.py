#!/usr/bin/env python3

input = open("input").read().split("\n\n")
input = [dict(kv.split(':') for kv in line.split()) for line in input]

def validate_minmax(val,min,max,digits=0):
    base=16 if any(c in val for c in 'abcdef') else 10
    if min<=int(val,base)<=max:
        if digits:
            if len(val)==digits:
                return True
        else:
            return True
    return False

valid=0

for passport in input:

    if all(f in passport for f in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']):

        #valid+=1; continue #solution1

        if      validate_minmax(passport['byr'],1920,2002,4) \
            and validate_minmax(passport['iyr'],2010,2020,4) \
            and validate_minmax(passport['eyr'],2020,2030,4):

            if         ( 'cm'==passport['hgt'][-2:] and validate_minmax(passport['hgt'][:-2],150,193) ) \
                    or ( 'in'==passport['hgt'][-2:] and validate_minmax(passport['hgt'][:-2],59,76) ):

                if '#'==passport['hcl'][0] and validate_minmax(passport['hcl'][1:],0x000000,0xffffff,6):

                    if any(c==passport['ecl'] for c in ['amb','blu','brn','gry','grn','hzl','oth']):

                        if passport['pid'].isnumeric() and validate_minmax(passport['pid'],0,999999999,9):

                            valid+=1

print(valid)
