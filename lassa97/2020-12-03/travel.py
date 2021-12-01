def search_1(map, right, down):
    tree = '#'
    trees = 0
    pos = [0, 0]

    while (pos[1] < len(map)):
        x = pos[0]
        y = pos[1]
        if map[y][x] is tree:
            trees += 1

        pos[0] += right
        if len(map[0]) <= pos[0]:
            pos[0] -= len(map[0])

        pos[1] += down

    print("Trees: {TREES}".format(TREES=trees))
    return


def search_2(map, right, down):
    tree = '#'
    trees = 0
    pos = [0, 0]

    while (pos[1] < len(map)):
        x = pos[0]
        y = pos[1]
        if map[y][x] is tree:
            trees += 1

        pos[0] += right
        if len(map[0]) <= pos[0]:
            pos[0] -= len(map[0])

        pos[1] += down
    
    print("Trees: {TREES}".format(TREES=trees))
    return trees

with open("input.txt") as file:
    map = file.read().splitlines()


search_1(map, 3, 1)

trees_1 = search_2(map, 1, 1)
trees_2 = search_2(map, 3, 1)
trees_3 = search_2(map, 5, 1)
trees_4 = search_2(map, 7, 1)
trees_5 = search_2(map, 1, 2)

trees = trees_1 * trees_2 * trees_3 * trees_4 * trees_5

print("Trees: {TREES}".format(TREES=trees))