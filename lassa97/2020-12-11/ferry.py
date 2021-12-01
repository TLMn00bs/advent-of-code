import copy

def parse_data(file):
    plane = []

    for x in range(len(file)):
        aux = []
        for y in range(len(file[0])):
            aux.append(int(file[x][y].replace('L', '0').replace('#', '1').replace('.', '2')))
        plane.append(aux)

    return plane

def get_adjacent_seats(plane, seat):
    x = seat[0]
    y = seat[1]

    occupied_seats = []

    # up
    i = x - 1
    if (0 <= i):
        occupied_seats.append(plane[i][y])

    # down
    i = x + 1
    if (i <= len(plane) - 1):
        occupied_seats.append(plane[i][y])

    # left
    j = y - 1
    if (0 <= j):
        occupied_seats.append(plane[x][j])

    # right
    j = y + 1
    if (j <= len(plane[0]) - 1):
        occupied_seats.append(plane[x][j])

    # leftup
    i = x - 1
    j = y - 1
    if (0 <= i) and (0 <= j):
        occupied_seats.append(plane[i][j])

    # leftdown
    i = x + 1
    j = y - 1
    if (i <= len(plane) - 1) and (0 <= j):
        occupied_seats.append(plane[i][j])

    # rightup
    i = x - 1
    j = y + 1
    if (0 <= i) and (j <= len(plane[0]) - 1):
        occupied_seats.append(plane[i][j])

    # rightdown
    i = x + 1
    j = y + 1
    if (i <= len(plane) - 1) and (j <= len(plane[0]) - 1):
        occupied_seats.append(plane[i][j])

    return occupied_seats

def get_visual_seats(plane, seat):
    x = seat[0]
    y = seat[1]

    occupied_seats = []

    # up
    i = x - 1
    while (0 <= i <= len(plane) - 1):
        if (plane[i][y] == 0):
            break
        elif (plane[i][y] == 1):
            occupied_seats.append(1)
            break
        i -= 1

    # down
    i = x + 1
    while (0 <= i <= len(plane) - 1):
        if (plane[i][y] == 0):
            break
        elif (plane[i][y] == 1):
            occupied_seats.append(1)
            break
        i += 1

    # left
    j = y - 1
    while (0 <= j <= len(plane[0]) - 1):
        if (plane[x][j] == 0):
            break
        elif (plane[x][j] == 1):
            occupied_seats.append(1)
            break
        j -= 1

    # right
    j = y + 1
    while (0 <= j <= len(plane[0]) - 1):
        if (plane[x][j] == 0):
            break
        elif (plane[x][j] == 1):
            occupied_seats.append(1)
            break
        j += 1

    # leftup
    i = x - 1
    j = y - 1
    while (0 <= i <= len(plane) - 1) and (0 <= j <= len(plane[0]) - 1):
        if (plane[i][j] == 0):
            break
        elif (plane[i][j] == 1):
            occupied_seats.append(1)
            break
        i -= 1
        j -= 1

    # leftdown
    i = x + 1
    j = y - 1
    while (0 <= i <= len(plane) - 1) and (0 <= j <= len(plane[0]) - 1):
        if (plane[i][j] == 0):
            break
        elif (plane[i][j] == 1):
            occupied_seats.append(1)
            break
        i += 1
        j -= 1

    # rightup
    i = x - 1
    j = y + 1
    while (0 <= i <= len(plane) - 1) and (0 <= j <= len(plane[0]) - 1):
        if (plane[i][j] == 0):
            break
        elif (plane[i][j] == 1):
            occupied_seats.append(1)
            break
        i -= 1
        j += 1

    # rightdown
    i = x + 1
    j = y + 1
    while (0 <= i <= len(plane) - 1) and (0 <= j <= len(plane[0]) - 1):
        if (plane[i][j] == 0):
            break
        elif (plane[i][j] == 1):
            occupied_seats.append(1)
            break
        i += 1
        j += 1

    return occupied_seats

def update_plane_v1(plane):
    changes = copy.deepcopy(plane)
    for x in range(len(plane)):
        for y in range(len(plane[0])):
            if (plane[x][y] == 2):
                continue
            seat = [x, y]
            adjacent_seats = get_adjacent_seats(plane, seat)
            if (adjacent_seats.count(1) == 0) and (plane[x][y] == 0):
                changes[x][y] = 1
            if (adjacent_seats.count(1) >= 4) and (plane[x][y] == 1):
                changes[x][y] = 0
    return changes

def update_plane_v2(plane):
    changes = copy.deepcopy(plane)
    for x in range(len(plane)):
        for y in range(len(plane[0])):
            if (plane[x][y] == 2):
                continue
            seat = [x, y]
            visual_seats = get_visual_seats(plane, seat)
            if (visual_seats.count(1) >= 5) and (plane[x][y] == 1):
                changes[x][y] = 0
            if (visual_seats.count(1) == 0) and (plane[x][y] == 0):
                changes[x][y] = 1
    return changes
        

def last_plane_v1(plane):
    while True:
        new_plane = update_plane_v1(plane)
        if (new_plane == plane):
            break
        plane = copy.deepcopy(new_plane)

    return plane

def last_plane_v2(plane):
    while True:
        new_plane = update_plane_v2(plane)
        if (new_plane == plane):
            break
        plane = copy.deepcopy(new_plane)
    return plane

def search_1(plane):
    occupied_seats = 0
    for i in plane:
        occupied_seats += i.count(1)

    return occupied_seats

def search_2(plane):
    occupied_seats = 0
    for i in plane:
        occupied_seats += i.count(1)

    return occupied_seats

file = open('input.txt').read().splitlines()

plane = parse_data(file)

final_plane = last_plane_v1(plane)

occupied_seats = search_1(final_plane)

print('Occupied seats: {SEATS}'.format(SEATS=occupied_seats))

final_plane = last_plane_v2(plane)

occupied_seats = search_2(final_plane)

print('Occupied seats: {SEATS}'.format(SEATS=occupied_seats))