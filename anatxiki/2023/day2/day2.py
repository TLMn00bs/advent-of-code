RED = 12
GREEN = 13
BLUE = 14

solution = 0
part2_solution = 0


def isPossibleGame(plays):
    for play in plays:
        cubes = play.split(',')
        for cube in cubes:
            number_of_cubes, color = cube.strip().split(' ')
            # print(number_of_cubes, color)
            if color == 'red' and int(number_of_cubes) > RED:
                return False
            if color == 'blue' and int(number_of_cubes) > BLUE:
                return False
            if color == 'green' and int(number_of_cubes) > GREEN:
                return False
    return True


def powerOfTheCubes(plays):
    max_red_cubes = 0
    max_blue_cubes = 0
    max_green_cubes = 0
    for play in plays:
        cubes = play.split(',')
        for cube in cubes:
            number_of_cubes, color = cube.strip().split(' ')
            if color == 'red' and int(number_of_cubes) > max_red_cubes:
                max_red_cubes = int(number_of_cubes)
            if color == 'blue' and int(number_of_cubes) > max_blue_cubes:
                max_blue_cubes = int(number_of_cubes)
            if color == 'green' and int(number_of_cubes) > max_green_cubes:
                max_green_cubes = int(number_of_cubes)
    print('blue:', max_blue_cubes, ', green:',
          max_green_cubes, ', red:', max_red_cubes)
    return max_red_cubes * max_blue_cubes * max_green_cubes


with open('input.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        game, plays = line.split(':')
        game_id = int(game.split(' ')[1])
        plays = plays.split(';')
        print(game)
        if isPossibleGame(plays):
            solution += int(game_id)
        part2_solution += powerOfTheCubes(plays)
    print(part2_solution)
