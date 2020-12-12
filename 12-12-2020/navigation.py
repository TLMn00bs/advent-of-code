import math

def search_1(ferry, directions):
    for direction in directions:
        axis, units = direction[:1], int(direction[1:])

        if (axis == 'N'):
            ferry[1] += units
        elif (axis == 'S'):
            ferry[1] -= units
        elif (axis == 'E'):
            ferry[2] += units
        elif (axis == 'W'):
            ferry[2] -= units

        if (axis == 'L'):
            ferry[0] -= (units // 90)
            ferry[0] %= 4
        elif (axis == 'R'):
            ferry[0] += (units // 90)
            ferry[0] %= 4
        
        if (axis == 'F') and (ferry[0] == 0):
            ferry[1] += units
        elif (axis == 'F') and (ferry[0] == 1):
            ferry[2] += units
        elif (axis == 'F') and (ferry[0] == 2):
            ferry[1] -= units
        elif (axis == 'F') and (ferry[0] == 3):
            ferry[2] -= units
    
    return ferry

def search_2(ferry, waypoint, directions):
    for direction in directions:
        axis, units = direction[:1], int(direction[1:])

        if (axis == 'N'):
            waypoint[0] += units
        elif (axis == 'S'):
            waypoint[0] -= units
        elif (axis == 'E'):
            waypoint[1] += units
        elif (axis == 'W'):
            waypoint[1] -= units

        if (axis == 'L') or (axis == 'R'):
            angle = (2 * math.pi) * (units / 360)

            if (axis == 'L'):
                angle = -angle

            x = waypoint[0] * math.cos(angle) - waypoint[1] * math.sin(angle)
            y = waypoint[0] * math.sin(angle) + waypoint[1] * math.cos(angle)

            waypoint = [int(round(x)), int(round(y))]

        if (axis == 'F'):
            ferry[1] += units * waypoint[0]
            ferry[2] += units * waypoint[1]

    return ferry

# ferry = [direction, x-axis, y-axis]
# direction = [0: N, 1: E, 2: S, 3: W]
# waypoint = [x-axis, y-axis]

file = open('input.txt').read().splitlines()

ferry = [1, 0, 0]

ferry = search_1(ferry, file)

print('Distance 1: {DISTANCE}'.format(DISTANCE=abs(ferry[1]) + abs(ferry[2])))

ferry = [1, 0, 0]

waypoint = [1, 10]

ferry = search_2(ferry, waypoint, file)

print('Distance 2: {DISTANCE}'.format(DISTANCE=abs(ferry[1]) + abs(ferry[2])))
