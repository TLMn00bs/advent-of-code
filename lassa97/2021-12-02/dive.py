def part1(instructions):
    position = (0, 0)
    for instruction in instructions:
        if (instruction[0] == 'forward'):
            position = (position[0] + instruction[1], position[1])
        if (instruction[0] == 'up'):
            position = (position[0], position[1] - instruction[1])
        if (instruction[0] == 'down'):
            position = (position[0], position[1] + instruction[1])
    return position

def part2(instructions):
    position = (0, 0, 0)
    for instruction in instructions:
        if (instruction[0] == 'forward'):
            position = (position[0] + instruction[1], position[1] + position[2] * instruction[1], position[2])
        if (instruction[0] == 'up'):
            position = (position[0], position[1], position[2] - instruction[1])
        if (instruction[0] == 'down'):
            position = (position[0], position[1], position[2] + instruction[1])
    return position

def read_file(file='input.txt'):
    file = open(file, 'r')
    instructions = []
    for line in file:
        direction, steps = line.strip().split(' ')[0], int(line.strip().split(' ')[1])
        instructions.append((direction, steps))
    return instructions


instructions = read_file()
position = part1(instructions)
print(position[0] * position[1])
position = part2(instructions)
print(position[0] * position[1])