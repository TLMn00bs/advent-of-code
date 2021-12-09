#!/usr/bin/env python3
import sys
if len(sys.argv)<2: print("usage: ./sol.py incr_x incr_y"); sys.exit()

input = [line.strip() for line in open("input").readlines()]
path = []

incr_x,incr_y = int(sys.argv[1]), int(sys.argv[2])

for i in range(incr_y,len(input),incr_y):
    path.append(input[i][ int(i/incr_y)*incr_x % len(input[i]) ])

print( path.count('#') )

# ./sol.py 1 1; ./sol.py 3 1; ./sol.py 5 1; ./sol.py 7 1; ./sol.py 1 2
