def search_1(numbers, turns):
    for turn in range(len(numbers), turns):
        prev = numbers[turn - 1]
        if (numbers.count(prev) > 1):
            aux = list(numbers[:-1])
            aux.reverse()
            index = aux.index(prev)

            numbers.append(turn - abs(len(numbers) - index) + 1)
        else:
            numbers.append(0)

    return numbers[turns - 1]

def search_2(numbers, turns):
    '''
        We create a dict values = {number: index}, 
        so we store as the key the number of the sequence and the index is the last position where
        that number was in the sequence.
        Example:
            input = [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]

            values = {0: 10, 3: 6, 6: 3, 1: 7, 4: 9} (The last time we have seen 0 in the sequence is in the turn 10, number 3 in the turn 6, and so on...)
    '''

    values = dict()
    turn = 1
    for num in numbers[:-1]:
        values[num] = turn
        turn += 1
    prev = numbers[-1]
    turn += 1
    while turn <= turns:
        if (prev not in values):
            values[prev] = turn - 1
            prev = 0
        else:
            index = turn - 1 - values[prev]
            values[prev] = turn - 1
            prev = index
        turn += 1
    return prev

numbers = open('input.txt').read().splitlines()

for i in range(len(numbers)):
    numbers[i] = int(numbers[i])

turns = 2020
value = search_1(numbers, turns)
print('The {TURNS}th value is: {VALUE}'.format(TURNS=turns, VALUE=value))

numbers = [2, 15, 0, 9, 1, 20]
turns = 30000000
value = search_2(numbers, turns)
print('The {TURNS}th value is: {VALUE}'.format(TURNS=turns, VALUE=value))