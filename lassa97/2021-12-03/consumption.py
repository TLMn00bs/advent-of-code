def get_oxygen_value(diagnosis):
    oxygen = diagnosis.copy()

    for step in range(0, len(diagnosis[0])):
        count_zeroes = 0
        for line in oxygen:
            if line[step] == '0':
                count_zeroes += 1

        oxygen_value = 0
        if len(oxygen) - count_zeroes >= count_zeroes:
            oxygen_value = 1

        new_oxygen = []

        for line in oxygen:
            if int(line[step]) == oxygen_value:
                new_oxygen.append(line)

        oxygen = new_oxygen.copy()

        if len(oxygen) == 1:
            return oxygen[0]

    return oxygen[0]

def get_co2_value(diagnosis):
    co2 = diagnosis.copy()

    for step in range(0, len(diagnosis[0])):
        count_ones = 0
        for line in co2:
            if line[step] == '1':
                count_ones += 1

        co2_value = 1
        if count_ones >= len(co2) - count_ones:
            co2_value = 0

        new_co2 = []

        for line in co2:
            if int(line[step]) == co2_value:
                new_co2.append(line)

        co2 = new_co2.copy()

        if len(co2) == 1:
            return co2[0]

    return co2[0]

def part1(diagnosis):
    # [(nº of zeroes in position 0, nº of ones in position 0), (nº of zeroes in position 1, nº of ones in position 1), ... (nº of zeroes in position n, nº of ones in position n)]
    #values = [(0, 0)] * len(diagnosis[0])

    # Count the number of 0s in each position, the number of 1s is len(diagnosis) - number of 0s in that position
    values = [0] * len(diagnosis[0])
    for line in diagnosis:
        for pos in range(0, len(line)):
            if line[pos] == '0':
                values[pos] += 1

    gamma = [0] * len(values)
    epsilon = [0] * len(values)

    for pos in range(0, len(values)):
        if len(diagnosis) - values[pos] > values[pos]:
            gamma[pos] = 1
        
        if values[pos] > (len(diagnosis) - values[pos]):
            epsilon[pos] = 1

    gamma = int(''.join(map(str, gamma)), 2)
    epsilon = int(''.join(map(str, epsilon)), 2)

    return gamma, epsilon

def part2(diagnosis):
    oxygen = int(get_oxygen_value(diagnosis), 2)
    co2 = int(get_co2_value(diagnosis), 2)

    return oxygen, co2

def read_file(file='input.txt'):
    diagnosis = list(map(str, open(file, 'r').read().splitlines()))
    return diagnosis


diagnosis = read_file()
gamma, epsilon = part1(diagnosis)
print(gamma * epsilon)
oxygen, co2 = part2(diagnosis)
print(oxygen * co2)