#!/usr/bin/env python

input = [line.strip() for line in open("input").readlines()]

def seatcode2rowcolumn(seatcode):
    d = {'F': '0', 'B': '1', 'L': '0', 'R': '1'}
    return int( "".join([d[r] for r in seatcode[:7]]), 2 ), \
           int( "".join([d[c] for c in seatcode[7:]]), 2 )

def seatid(rowcol):
    return rowcol[0]*8 + rowcol[1]

seatids = [seatid( seatcode2rowcolumn(cod) ) for cod in input]

print( max(seatids) )

print( *( set(range(min(seatids),max(seatids))) - set(seatids) ) )
