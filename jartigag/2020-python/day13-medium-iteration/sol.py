#!/usr/bin/env python

input = [line.strip() for line in open("input").readlines()]

tstamp = int(input[0])
bus_ids = [int(n) if n!='x' else n for n in input[1].split(',')]

next_tstamps = []
for bus_id in bus_ids:
    if bus_id!='x':
        n_trip = int(tstamp/bus_id)
        next_tstamps.append( [bus_id*(n_trip+1), bus_id] )

next_dep = sorted(next_tstamps)[0]
print("sol1:",next_dep[0]*next_dep[1] )
print( "\t".join(                ["now:", "next:"    , "bus_id:"  ]))
print( "\t".join(str(x) for x in [tstamp, next_dep[0], next_dep[1]]))
print( "\t".join(
    [(lambda x: f"({int(x/60)%24}:{x%60})")(x) for x in [tstamp,next_dep[0]]]
))

earliest_tstamp = 0
incr = bus_ids[0]
for pos,bus_id in enumerate(bus_ids):
    if pos==0: continue # first departure on earliest_tstamp, no need to increment
    if bus_id!='x':
        while (earliest_tstamp+pos)%bus_id != 0:
            earliest_tstamp += incr
        incr *= bus_id

print("\nearliest tstamp such that each\n bus departs on x minutes\n (x=position in list):")
print(earliest_tstamp,"(in {:.2e} years)".format(earliest_tstamp/60/24/365))
