#!/usr/bin/env python3.11

input = [line.strip() for line in open("input").readlines()]

NUM_OF_RED_CUBES   = 12
NUM_OF_GREEN_CUBES = 13
NUM_OF_BLUE_CUBES  = 14

def would_have_been_possible(set_of_cubes: list, is_part_1) -> (bool, int):
    max_red_cubes, max_blue_cubes, max_green_cubes = 0, 0, 0

    for rgb_cubes in set_of_cubes:
        cubes = rgb_cubes.split(',')

        for cube in cubes:
            total_num_of_cubes, color = cube.strip().split(' ')

            if color == 'red':
                if is_part_1 and int(total_num_of_cubes) > NUM_OF_RED_CUBES:
                    return (False, 0)
                elif int(total_num_of_cubes) > max_red_cubes:
                    max_red_cubes = int(total_num_of_cubes)

            if color == 'blue':
                if is_part_1 and int(total_num_of_cubes) > NUM_OF_BLUE_CUBES:
                    return (False, 0)
                elif int(total_num_of_cubes) > max_blue_cubes:
                    max_blue_cubes = int(total_num_of_cubes)

            if color == 'green':
                if is_part_1 and int(total_num_of_cubes) > NUM_OF_GREEN_CUBES:
                    return (False, 0)
                elif int(total_num_of_cubes) > max_green_cubes:
                    max_green_cubes = int(total_num_of_cubes)

    return (True, max_red_cubes * max_blue_cubes * max_green_cubes)

def play(input: list, is_part_1=True) -> (int, int):
    sum_of_the_IDs_of_possible_games, power_of_the_IDs_of_possible_games = 0, 0

    for i in input:
        game, set_of_cubes    = i.split(':')
        game_id               = int(game.split(' ')[1])
        set_of_cubes          = set_of_cubes.split(';')
        possible, cubes_power = would_have_been_possible(set_of_cubes, is_part_1)
        if possible:
            sum_of_the_IDs_of_possible_games += game_id
        power_of_the_IDs_of_possible_games   += cubes_power

    return (sum_of_the_IDs_of_possible_games, power_of_the_IDs_of_possible_games)

if __name__ == '__main__':
    print( play(input)[0] )
    print( play(input, is_part_1=False)[1] )
