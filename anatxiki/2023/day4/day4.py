def get_number_of_winning_numbers(winning_numbers, my_numbers):
    game_value = 0
    for number in winning_numbers:
        if number in my_numbers:
            game_value += 1 
    return game_value

def get_points(game_value):
        if game_value != 0: return 2 ** (game_value -1)
        else: return 0

def get_array_of_games(lines):
    return [1 for x in lines]

def update_array_of_games(my_array, number_of_winning_games, index):
    starting_point = index
    ending_point = index + number_of_winning_games
    number_of_copies = my_array[index]
    for i in range(starting_point, ending_point):
        my_array[i+1] += number_of_copies
    return

solution_part1 = 0
solution_part2 = 0

with open('input.txt', 'r') as file:
    lines = file.readlines()
    array_of_games = get_array_of_games(lines)

    for idx, line in enumerate(lines):
        data, mynumbers = line.split('|')
        winning_numbers = [x for x in data.split(':')[-1].split()]
        mynumbers = [x for x in mynumbers.strip().split()]

        number_of_winning_numbers = get_number_of_winning_numbers(winning_numbers,mynumbers)
        update_array_of_games(array_of_games, number_of_winning_numbers, idx)
        
        solution_part1 += get_points(number_of_winning_numbers)
        
    print('solution part 1',solution_part1)
    print('solution part 2', sum(array_of_games))