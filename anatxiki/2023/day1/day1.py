import regex as re

myregex = 'one|two|three|four|five|six|seven|eight|nine|[1-9]'
textToDigits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def part1():
    part1_solution = 0
    with open('input.txt', 'r') as file:
        for line in file:
            digits = [x for x in line if x.isnumeric()]
            checksum = digits[0] + digits[-1]
            part1_solution += int(checksum)

        print(part1_solution)

def part2():
    part2_solution = 0
    with open('input.txt', 'r') as file:
        for line in file:
            matches = re.findall(myregex, line, overlapped=True)
            digits = [textToDigits.get(x,x) for x in matches]
            
            checksum = digits[0] + digits[-1]
            part2_solution += int(checksum)
        print(part2_solution)

part1()
part2()