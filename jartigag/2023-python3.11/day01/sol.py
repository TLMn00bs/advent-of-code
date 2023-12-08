#!/usr/bin/env python3.11

input = [line.strip() for line in open("input").readlines()]

def part1(input: list) -> list:
    nums = []
    for i in input:
        num = 0
        num_str = "".join([c if c.isdigit() else "" for c in i])
        if num_str.isdigit():
            num = int(num_str[0])*10 + int(num_str[-1])
        nums.append(num)
    return nums

def letters2digits(line: str, digits_dict: dict) -> str:
    new_line = ""
    for pos in range(len(line)):
        if any(line[pos:].startswith(digit := k) for k,v in digits_dict.items()):
            new_line += str(digits_dict[digit])
        elif line[pos].isdigit():
            new_line += line[pos]
    return new_line

def part2(input: list, digits_dict: dict) -> list:
    nums = []
    for i in input:
        num = 0
        num_str = letters2digits(i, digits_dict)
        if num_str.isdigit():
            num = int(num_str[0])*10 + int(num_str[-1])
        nums.append(num)
    return nums

if __name__ == '__main__':
    print( sum(part1(input)) )
    digits_spelled_out_with_letters = {
       'one':   1, 'two':   2, 'three': 3,
       'four':  4, 'five':  5, 'six': 6,
       'seven': 7, 'eight': 8, 'nine': 9
    }
    print( sum( part2(input, digits_spelled_out_with_letters) ) )
