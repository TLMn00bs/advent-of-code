def search_1(file):
    ones = 0
    threes = 0

    for i in range(1, len(file)):
        prev = file[i-1]
        curr = file[i]

        if (curr - prev) == 1:
            ones += 1
        if (curr - prev) == 3:
            threes += 1

    print('Total differences: {TOTAL}\n'.format(TOTAL=ones * threes))
    return

def search_2(file):
    '''
        Using a property of the Tribonacci numbers, we can obtain all the combinations from the length
        of all the continuos sequences inside our list.
        NOTE: This property is valid if the size of the gaps is 1 or 3
        Example: 
            If we have an order sequence as the input there are three continuous sequences:
                [1, 2, 3, 6, 9, 10, 12, 13, 14, 15, 17, 18, 19, 21] -> [1, 2, 3], [9, 10], [12, 13, 14, 15] and [17, 18, 19]
            Having the size of each continuous sequence, we can calculate all the combinations with this formula:
            We have one sequence ([8, 9]) with length 2, two with length 3 ([1, 2, 3], [17, 18, 19]) and one with length 4 ([12, 13, 14, 15]).
            With this values, all the posible combinations are:
                total = (1^a) * (2^b) * (4^c), where:
                    a = num of continuous sequences of length 2
                    b = num of continuous sequences of length 3
                    c = num of continuous sequences of length 4
    '''
    all_continuous_sequences = []
    continuous_sequence = []
    continuous_sequences_sizes = []
    for i in range(1, len(file)):
        prev = file[i - 1]
        curr = file[i]

        if (curr - prev) == 1:
            if (prev not in continuous_sequence):
                continuous_sequence.append(prev)
            continuous_sequence.append(curr)
        else:
            all_continuous_sequences.append(continuous_sequence)
            continuous_sequences_sizes.append(len(continuous_sequence))
            continuous_sequence = []
    all_continuous_sequences = list(filter(None, all_continuous_sequences))

    return continuous_sequences_sizes

file = list(map(int, open('input.txt').read().splitlines()))
file.append(0)
file.sort()
file.append(file[len(file) - 1] + 3)
search_1(file)

sizes = search_2(file)

link = 'https://www.reddit.com/r/adventofcode/comments/ka9pc3/2020_day_10_part_2_suspicious_factorisation/'

print('Using some properties of the Tribonacci series, we can do (1^a)*(2^b)*(4^c)*(7^d), where:')
print('\t a = num of continuous sequences of length 2')
print('\t b = num of continuous sequences of length 3')
print('\t c = num of continuous sequences of length 4')
print('\t d = num of continuous sequences of length 5')
print()
print('NOTE: This property is valid if the size of the gaps is 1 or 3')
print()
print('More details in {LINK}'.format(LINK=link))
print('\t or in the comments of the code.')
print()

combinations = pow(1, sizes.count(2)) * pow(2, sizes.count(3)) * pow(4, sizes.count(4)) * pow(7, sizes.count(5))

print('Total combinations: {COMBINATIONS}'.format(COMBINATIONS=combinations))