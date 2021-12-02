with open('input.txt') as f: inst = [(line[0], int(line[1:-1])) for line in f]

#	N		^
#   W (0,0) E		|
#       S		|
#		       x,y --->
#
# Currently facing east

position = {'x' : 0, 'y' : 0}
orientation = {'x' : 1, 'y' : 0}

def move(n, orientation):
	position['x'] += n * orientation['x']
	position['y'] += n * orientation['y']

for i,n in inst:
#	print(position, i, n)
	if i == 'F': move(n, orientation)
	elif i == 'N': move(n, {'x' : 0,  'y' : 1})
	elif i == 'W': move(n, {'x' : -1, 'y' : 0})
	elif i == 'E': move(n, {'x' : 1,  'y' : 0})
	elif i == 'S': move(n, {'x' : 0,  'y' : -1})
#	if i == 'L':
#		if n == 180:
#			orientation['x'] = -orientation['x']
#			orientation['y'] = -orientation['y']
#		if n == 90:
			# (1, 0) --> (0, 1)
			# (0, 1) --> (-1, 0)
			# (-1, 0) -> (0, -1)
			# (0, -1) -> (1, 0)
#			orientation['x'], orientation['y'] = -orientation['y'], orientation['x']
#		if n == 270:
#			orientation['x'], orientation['y'] = orientation['y'], -orientation['x']
			# (1, 0) --> (0, -1)
                        # (0, -1) --> (-1, 0)
                        # (-1, 0) -> (0, 1)
                        # (0, 1) -> (1, 0)
	else:
		rotation_direction = 1 if (i == 'L') else -1
		if n == 180: orientation['x'], orientation['y'] = -orientation['x'], -orientation['y']
		else:
			if n == 270: rotation_direction *= -1
			orientation['x'], orientation['y'] = -rotation_direction * orientation['y'], rotation_direction * orientation['x']

print(abs(position['x']) + abs(position['y']))


# Puzzle 2
position = {'x' : 0, 'y' : 0}
waypoint = {'x' : 10, 'y' : 1}

def move_w(n, waypoint):
	position['x'] += n * waypoint['x']
	position['y'] += n * waypoint['y']

for i,n in inst:
	#print(position, waypoint, i, n)
	if i == 'F': move_w(n, waypoint)
	elif i == 'N': waypoint['y'] += n
	elif i == 'W': waypoint['x'] -= n
	elif i == 'E': waypoint['x'] += n
	elif i == 'S': waypoint['y'] -= n
	else:
		rotation_direction = 1 if (i == 'L') else -1
		if n == 180: waypoint['x'], waypoint['y'] = -waypoint['x'], -waypoint['y']
		else:
			if n == 270: rotation_direction *= -1
			waypoint['x'], waypoint['y'] = -rotation_direction * waypoint['y'], rotation_direction * waypoint['x']


print(abs(position['x']) + abs(position['y']))

