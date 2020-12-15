def is_valid(num, preamble):
    for value in preamble:
        for i in preamble:
            if (int(value) + int(i)) == int(num):
                return True
                
    return False

def get_sequence(invalid, file, n=0):
    total = 0
    sequence = []
    index = 0
    while (total < invalid):
            sequence.append(int(file[index + n]))
            total = sum(sequence)
            index += 1

    n += 1
    if (total != invalid):
        get_sequence(invalid, file, n)
    else:
        print('Sum: {SUM}'.format(SUM=max(sequence) + min(sequence)))

    


file = open('input.txt').read().splitlines()

invalid = 0

for i in range(0, len(file) - 25):
    preamble = file[i:i+25]
    num = file[i+25]
    if not is_valid(num, preamble):
        print('Number: {NUM}'.format(NUM=num))
        invalid = num
        break

get_sequence(int(invalid), file)