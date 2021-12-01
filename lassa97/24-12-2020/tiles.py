
DIRECTIONS = {
    'se': [1, -1], 'e': [2, 0], 'ne': [1, 1],
    'sw': [-1, -1], 'w': [-2, 0], 'nw': [-1, 1]
}

def get_paths(file):
    paths = []
    for line in file:
        instructions = []
        instruction = ''
        for char in line:
            if ((instruction + char) in DIRECTIONS.keys()):
                instructions.append(instruction + char)
                instruction = ''
            else:
                instruction = char
        paths.append(instructions)
    return paths

def search_1(paths):
    black_tiles = set()
    for path in paths:
        pos = [0, 0]
        for instruction in path:
            move = DIRECTIONS[instruction]

            pos[0] += move[0]
            pos[1] += move[1]

        flipped = tuple(pos)

        if (flipped not in black_tiles):
            black_tiles.add(flipped)
        else:
            black_tiles.remove(flipped)

    return black_tiles

def search_2(black_tiles):
    for _ in range(100):
        adjacent_tiles = {}
        for tile in black_tiles:
            if (tile not in adjacent_tiles):
                adjacent_tiles[tile] = 0
            for direction in DIRECTIONS.values():
                adjacent = [tile[0] + direction[0], tile[1] + direction[1]]
                adjacent = tuple(adjacent)

                if (adjacent in adjacent_tiles.keys()):
                    adjacent_tiles[adjacent] += 1
                else:
                    adjacent_tiles[adjacent] = 1
        
        next_day_black_tiles = set()
        for tile in adjacent_tiles:
            if ((tile in black_tiles) and (adjacent_tiles[tile] in [1, 2])):
                next_day_black_tiles.add(tile)
            elif ((tile not in black_tiles) and (adjacent_tiles[tile] == 2)):
                next_day_black_tiles.add(tile)
        
        black_tiles = next_day_black_tiles

    return black_tiles

file = open('input.txt').read().splitlines()

paths = get_paths(file)

black_tiles = search_1(paths)

print('Black tiles: {BLACK_TILES}'.format(BLACK_TILES=len(black_tiles)))

black_tiles = search_2(black_tiles)

print('Black tiles after 100 days: {BLACK_TILES}'.format(BLACK_TILES=len(black_tiles)))