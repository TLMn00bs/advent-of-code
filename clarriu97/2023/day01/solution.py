
def get_fixed_problematic_chains(m: dict):
    fixed_problematic_chains = {}
    for key in m.keys():
        for key2 in m.keys():
            if key[-1] == key2[0]:
                fixed_problematic_chains[key + key2[1:]] = key + key2
    return fixed_problematic_chains


def sanitize_line(line: str, fixed_problematic_chains: dict):
    for key, value in fixed_problematic_chains.items():
        if key in line:
            line = line.replace(key, value)
    return line


def get_sum(lines: list):
    sum = 0
    for line in lines:
        first_digit = None
        last_digit = None
        for char in line:
            if char.isdigit():
                if first_digit is None:
                    first_digit = char
                    last_digit = char
                else:
                    last_digit = char
        calibration_value = int(str(first_digit) + str(last_digit))
        sum += calibration_value
    return sum


def part2(lines: list):
    m = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    fixed_problematic_chains = get_fixed_problematic_chains(m)
    fixed_lines = []
    for line in lines:
        line = sanitize_line(line, fixed_problematic_chains)
        for key, value in m.items():
            if key in line:
                line = line.replace(key, value)
        fixed_lines.append(line)
    sum = get_sum(fixed_lines)
    print(sum)


def part1(lines: list):
    sum = get_sum(lines)
    print(sum)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
    part1(lines)
    part2(lines)
