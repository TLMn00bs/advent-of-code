#!/usr/bin/env python3

input = [line.strip() for line in open("input").readlines()]

ok = 0
for line in input:
    minmax,c,pwd = line.split()
    min,max = [int(i) for i in minmax.split('-')]
    if min <= pwd.count( c.strip(':') ) <= max:
        ok+=1

print(ok)
