import copy

def get_adjacent_cubes(plane, point, same_plane):
    x = point[0]
    y = point[1]

    adjacent_cubes = []

    # up
    i = x - 1
    if (0 <= i):
        adjacent_cubes.append(plane[i][y])

    # down
    i = x + 1
    if (i <= len(plane) - 1):
        adjacent_cubes.append(plane[i][y])
    
    # left
    j = y - 1
    if (0 <= j):
        adjacent_cubes.append(plane[x][j])

    # right
    j = y + 1
    if (j <= len(plane[0]) - 1):
        adjacent_cubes.append(plane[x][j])

    # leftup
    i = x - 1
    j = y - 1
    if (0 <= i) and (0 <= j):
        adjacent_cubes.append(plane[i][j])

    # leftdown
    i = x + 1
    j = y - 1
    if (i <= len(plane) - 1) and (0 <= j):
        adjacent_cubes.append(plane[i][j])

    # rightup
    i = x - 1
    j = y + 1
    if (0 <= i) and (j <= len(plane[0]) - 1):
        adjacent_cubes.append(plane[i][j])

    # rightdown
    i = x + 1
    j = y + 1
    if (i <= len(plane) - 1) and (j <= len(plane[0]) - 1):
        adjacent_cubes.append(plane[i][j])
    
    if not (same_plane):
        adjacent_cubes.append(plane[x][y])

    return adjacent_cubes

def get_active_cubes(x, y, index):
        adjacent_cubes = []
        for i in range(-1, 2):
            if (i == 0):
                adjacent_cubes.append(get_adjacent_cubes(states[index + i], [x, y], True))
            else:
                adjacent_cubes.append(get_adjacent_cubes(states[index + i], [x, y], False))
        #print(adjacent_cubes)
        return adjacent_cubes

def update_states(states, index):
    changes = copy.deepcopy(states)
    for x in range(width):
        for y in range(height):
            active_cubes = get_active_cubes(x, y, index)
            if (active_cubes.count(1) == 3) and (states[index][x][y] == 0):
                changes[index][x][y] = 1
            if ((active_cubes.count(1) != 2) or (active_cubes.count(1) != 3)) and (states[index][x][y] == 1):
                changes[index][x][y] = 0
    return changes

def last_state(states):
    for index in range(num_cycles):
        last_state = update_states(states, index)
        states = copy.deepcopy(last_state)
    return states

def search_1(states):
    active_cubes = 0
    for z in states:
        print(z)
        for i in range(len(z)):
            active_cubes += z[i].count(1)

    return active_cubes

file = open('input.txt').read().splitlines()

num_cycles = 6

height = len(file)
width = len(file[0])
depth = (num_cycles * 2) + 1

states = []

state = []

for z in range(depth):
    for y in range(width):
        state.append([0] * width)
    states.append(state)
    state = []

for x in range(height):
    for y in range(width):
        states[6][x][y] = int(file[x][y].replace('.', '0').replace('#', '1'))


final_state = last_state(states)
active_cubes = search_1(final_state)
print('Active cubes: {CUBES}'.format(CUBES=active_cubes))

# https://github.com/mebeim/aoc/tree/master/2020#day-17---conway-cubes


'''
for i in range(-1, 2):
    adjacent_cubes = []
    for x in range(height):
        for y in range(width):
            if (i == 0):
                adjacent_cubes.append(get_adjacent_cubes(states[i + 6], [x, y, 6], True))
            else:
                adjacent_cubes.append(get_adjacent_cubes(states[i + 6], [x, y, 6], False))
    print(len(adjacent_cubes))
'''

'''
turn = 1
depth//2 + 1
'''

'''
coord = get_adjacent_cubes([2, 3, 1])

print(len(coord), coord)

coord_corner = get_adjacent_cubes_for_a_corner([4, 4, 4])

print(len(coord_corner), coord_corner)

coord_border = get_adjacent_cubes_for_a_border([4, 2, 1])

print(len(coord_border), coord_border)

#Flat[x + WIDTH * (y + DEPTH * z)] = Original[x, y, z]
'''

'''
def get_adjacent_cubes_v2(cube):
    coord = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                point = [cube[0] + x, cube[1] + y, cube[2] + z]
                if (x == y) and (y == z) and (x == 0):
                    continue
                coord.append(point)
    return coord

def get_adjacent_cubes_for_a_corner(corner):
    coord_corner = []

    for x in range(0, 2):
        for y in range(0, 2):
            for z in range(0, 2):
                point = [corner[0] + x, corner[1] + y, corner[2] + z]
                if (x == y) and (y == z) and (x == 0):
                    continue
                coord_corner.append(point)
    
    return coord_corner

def get_adjacent_cubes_for_a_border(border):
    coord_border = []

    for x in range(0, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                point = [border[0] + x, border[1] + y, border[2] + z]
                if (x == y) and (y == z) and (x == 0):
                    continue
                coord_border.append(point)

    return coord_border
'''