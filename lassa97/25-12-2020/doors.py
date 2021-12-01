def get_loop(key):
    subject_number = 7
    divisor = 20201227
    value = 1

    counter = 0
    while (value != key):
        value *= subject_number
        value %= divisor
        counter += 1
    return counter

def get_encription_key(key, loop):
    divisor = 20201227
    value = 1

    for _ in range(loop):
        value *= key
        value %= divisor
    return value

keys = open('input.txt').read().splitlines()

for i in range(len(keys)):
    keys[i] = int(keys[i])

loops = []

for key in keys:
    loops.append(get_loop(key))

encription_key = get_encription_key(keys[0], loops[1])

print('The encription key is: {ENCRIPTION_KEY}'.format(ENCRIPTION_KEY=encription_key))