def part1(depths):
    solution = 0
    previous_depth = depths[0]
    for depth in depths:
        if depth > previous_depth:
            solution += 1
        previous_depth = depth
    return solution

def part2(depths):
    index = 1
    previous_sum = depths[index - 1] + depths[index] + depths[index + 1]
    solution = 0

    for index in range(2, len(depths)):
        try:
            current_sum = depths[index - 1] + depths[index] + depths[index + 1]
            if current_sum > previous_sum:
                solution += 1
            previous_sum = current_sum
        except IndexError:
            pass
    return solution

def read_file(file='input.txt'):
    depths = list(map(int, open(file, 'r').read().splitlines()))
    return depths

depths = read_file()
solution = part1(depths)
print(solution)
solution = part2(depths)
print(solution)