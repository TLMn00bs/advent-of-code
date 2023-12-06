def get_matrix(lines):
    matrix = []
    row_range = len(lines)
    for i in range(row_range):
        matrix.append([x for x in lines[i].strip()])
    return matrix

def is_char_a_number(character):
    return character.isnumeric()

def is_char_a_symbol(character):
    return character != '.' and not character.isnumeric()

def is_char_a_dot(character):
    return character == '.'

part_numbers = []

def add_part_numbers(number):
    if number != '': part_numbers.append(int(number))

def check_for_surrounding_symbols(i,j,matrix):
    matrix_size = len(matrix)
    if i+1 < matrix_size and is_char_a_symbol(matrix[i+1][j]):
        return True
    if i-1 >= 0 and is_char_a_symbol(matrix[i-1][j]):
        return True
    if j+1 < matrix_size and is_char_a_symbol(matrix[i][j+1]):
        return True
    if j-1 >= 0 and is_char_a_symbol(matrix[i][j-1]):
        return True
    if i+1 < matrix_size and j+1 < matrix_size and is_char_a_symbol(matrix[i+1][j+1]):
        return True
    if i+1 < matrix_size and j-1 >= 0 and is_char_a_symbol(matrix[i+1][j-1]):
        return True
    if i-1 >= 0 and j-1 >= 0 and is_char_a_symbol(matrix[i-1][j-1]):
        return True
    if i-1 >= 0 and j+1 < matrix_size and is_char_a_symbol(matrix[i-1][j+1]):
        return True
    return False
    

def get_part_numbers(matrix):
    matrix_size = len(matrix)
    for i in range(matrix_size):
        possible_number = ''
        is_part_number = False
        for j in range(matrix_size):
            current_character = matrix[i][j]

            if is_char_a_number(current_character):
                possible_number += current_character
                if not is_part_number:
                    is_part_number = check_for_surrounding_symbols(i,j,matrix)
            else:
                if is_part_number: 
                    add_part_numbers(possible_number)

                possible_number = ''
                is_part_number = False
        
        if is_part_number: 
            add_part_numbers(possible_number)
    return 



with open('input.txt', 'r') as file:
    lines = file.readlines()
    matrix = get_matrix(lines)

    get_part_numbers(matrix)
    print('solution part 1',sum(part_numbers))

