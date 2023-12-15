#!/usr/bin/env python3.11

import re

input = [line.strip() for line in open("input").readlines()]

def part1(engine_schematic: list) -> list:
    symbol_adjacent = set()
    nums = []

    symbols_regex = r'[^.\d]'
    for i, line in enumerate(engine_schematic):
        for m in re.finditer(symbols_regex, line):
            j = m.start()
            symbol_adjacent |= {(r, c) for r in range(i-1, i+2) for c in range(j-1, j+2)}

    numbers_regex = r'\d+'
    for i, line in enumerate(engine_schematic):
        for m in re.finditer(numbers_regex, line):
            if any((i, j) in symbol_adjacent for j in range(*m.span())):
                nums.append( int(m.group()) )

    return nums

def part2(engine_schematic: list) -> list:
    gears = dict()
    nums = []

    gears_regex = r'\*'
    for i, line in enumerate(engine_schematic):
        for m in re.finditer(gears_regex, line):
            gears[(i, m.start())] = []

    numbers_regex = r'\d+'
    for i, line in enumerate(engine_schematic):
        for m in re.finditer(numbers_regex, line):
            for r in range(i-1, i+2):
                for n in range(m.start()-1, m.end()+1):
                    if (r, n) in gears:
                        gears[(r, n)].append(int(m.group()))

    for v in gears.values():
        if len(v) == 2:
            nums.append(v[0]*v[1])

    return nums

if __name__ == '__main__':
    print( sum(part1(input)) )
    print( sum(part2(input)) )
