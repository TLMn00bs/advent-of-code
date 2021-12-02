from cmath import rect
from math import radians as d2r
from_polar = lambda r,d: rect(r, d2r(d))

with open('input.txt') as f: instructions = [(line[0], int(line[1:-1])) for line in f]

position = 0 + 0j
orientation = 1 + 0j
for inst,n in instructions:
	if   inst == 'F': position += n * orientation
	elif inst == 'N': position += n * +1j
	elif inst == 'W': position += n * -1
	elif inst == 'E': position += n * +1
	elif inst == 'S': position += n * -1j
	else:
		sign = 1 if inst == 'L' else -1
		rotation = from_polar(1, sign * n)
		orientation *= rotation

print(round(abs(position.real) + abs(position.imag)))


position = 0 + 0j
waypoint = 10 + 1j
for inst,n in instructions:
	if   inst == 'F': position += n * waypoint
	elif inst == 'N': waypoint += n * +1j
	elif inst == 'W': waypoint += n * -1
	elif inst == 'E': waypoint += n * +1
	elif inst == 'S': waypoint += n * -1j
	else:
		sign = 1 if inst == 'L' else -1
		rotation = from_polar(1, sign * n)
		waypoint *= rotation

print(round(abs(position.real) + abs(position.imag)))
