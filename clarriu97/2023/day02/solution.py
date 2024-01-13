
def filter_sets(sets: list, max_red: int, max_green: int, max_blue: int):
    for set in sets:
        cubes = set.split(",")
        for cube in cubes:
            x = cube.split(" ")
            n, color = x[1], x[2]
            if "red" in color and int(n) > max_red:
                raise ValueError()
            if "green" in color and int(n) > max_green:
                raise ValueError()
            if "blue" in color and int(n) > max_blue:
                raise ValueError()


def get_id(line: str, max_red: int, max_green: int, max_blue: int):
    """
    Give a string input as a game line, it checks if there are more balls than the maximum allowed,
    and if there are, it raises a ValueError.
    If not, it returns the id of the game.
    """
    id = int(line.split(":")[0].split(" ")[1])
    sets = line.split(":")[1].split(";")
    filter_sets(sets, max_red, max_green, max_blue)
    return id


def part1(lines: list, max_red: int, max_green: int, max_blue: int):
    sum = 0
    for line in lines:
        try:
            id = get_id(line, max_red, max_green, max_blue)
        except ValueError:
            continue
        sum += id
    print(sum)


def get_power(line: str):
    max_red, max_green, max_blue = 0, 0, 0
    sets = line.split(":")[1].split(";")
    for set in sets:
        cubes = set.split(",")
        for cube in cubes:
            x = cube.split(" ")
            n, color = x[1], x[2]
            if "red" in color and int(n) > max_red:
                max_red = int(n)
            if "green" in color and int(n) > max_green:
                max_green = int(n)
            if "blue" in color and int(n) > max_blue:
                max_blue = int(n)
    return max_red * max_green * max_blue


def part2(lines: list):
    sum = 0
    for line in lines:
        power = get_power(line)
        sum += power
    print(sum)


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    max_red = 12
    max_green = 13
    max_blue = 14
    part1(lines, max_red, max_green, max_blue)
    part2(lines)
