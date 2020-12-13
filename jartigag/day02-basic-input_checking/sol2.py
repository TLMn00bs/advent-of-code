#!/usr/bin/env python3
from operator import xor

input = [line.strip() for line in open("input").readlines()]

ok = 0
for line in input:
    pos,c,pwd = line.split()
    pos1,pos2 = [int(i)-1 for i in pos.split('-')]
    c = c.strip(':')
    if xor( bool(pwd[pos1]==c), bool(pwd[pos2]==c) ):
        ok+=1

print(ok)
