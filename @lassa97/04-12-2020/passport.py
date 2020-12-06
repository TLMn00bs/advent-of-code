import re

def valid_height(height):
    if (height[-2:] == 'cm') and (int(height[:-2]) in range(150, 194)):
        return True
    if (height[-2:] == 'in') and (int(height[:-2]) in range(59, 77)):
        return True
    return False

def search_1(data):
    passports = 0
    valid_passports = []
    for passport in data:
        keys = list(passport.keys())
        if ("ecl" in keys) and ("pid" in keys) and ("eyr" in keys) and ("hcl" in keys) and ("byr" in keys) and ("iyr" in keys) and ("hgt" in keys):
            passports += 1
            valid_passports.append(passport)

    print("Passports: {PASSPORTS}".format(PASSPORTS=passports))
    return valid_passports

def search_2(valid_passports):
    filtered_passports = []
    for passport in valid_passports:
        valid_height(passport['hgt'])
        if (int(passport['byr']) not in range(1920, 2003)):
            continue
        if (int(passport['iyr']) not in range(2010, 2021)):
            continue
        if (int(passport['eyr']) not in range(2020, 2031)):
            continue
        if (valid_height(passport['hgt']) is False):
            continue
        if (re.search(r'#[a-f,0-9]{6}$', passport['hcl']) is None):
            continue
        if (passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']):
            continue
        if (len(passport['pid']) != 9):
            continue
        filtered_passports.append(passport)
    

    print("Passports: {PASSPORTS}".format(PASSPORTS=len(filtered_passports)))

    return filtered_passports


def prepare_file(file):
    with open(file) as f:
        rawdata = []
        s = ''
        for d in f.read().splitlines():
            if d == '':
                rawdata.append(s)
                s = ''
            else:
                s += d + ' '
        rawdata.append(s)

    return [dict([tuple(l.split(':')) for l in d.split()]) for d in rawdata]

data = prepare_file('input.txt')

valid_passports = search_1(data)

filtered_passports = search_2(valid_passports)
