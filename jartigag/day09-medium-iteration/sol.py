#!/usr/bin/env python

input = [int(line) for line in open("input").readlines()]

n = 24
for num in input[25:]:
    n+=1
    valid = False
    for i in range(0,25+1): # because `for i in range(0,3): print(i)` -> `0 1 2`
        for j in range(1,i):
            if num==input[n-i]+input[n-i+j]: valid=True
    if not valid:
        print(num)
        break

#num = 25918798
for i in range(0,len(input)-1):
    valid = False
    s = [input[i]]
    for j in range(1,i):
        s.append(input[i-j])
        if num==sum(s):
            valid=True
            break
    if valid:
        print(max(s)+min(s))
        break
