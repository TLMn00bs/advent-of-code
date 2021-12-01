from datetime import date, datetime

def search_1(file):
    acc = 0
    executed = {}
    index = 0

    instruction = file[index]

    while (index not in executed.keys()):
        rule, value = instruction[:3], instruction[4:]

        if (rule == 'acc'):
            acc += int(value)
            executed[index] = instruction
            index += 1

        if (rule == 'nop'):
            executed[index] = instruction
            index += 1

        if (rule == 'jmp'):
            executed[index] = instruction
            index += int(value)

    
        instruction = file[index]

    print('Accumulator: {ACC}'.format(ACC=acc))


def search_2(file):
    acc = 0
    index = 0
    instruction = file[index]

    start = datetime.now()
    end = datetime.now()

    while ((end - start).seconds < 1):
        rule, value = instruction[:3], instruction[4:]

        if (rule == 'acc'):
            acc += int(value)
            index += 1

        if (rule == 'nop'):
            index += 1

        if (rule == 'jmp'):
            index += int(value)


        if (index > (len(file) - 1)):
            return acc
        instruction = file[index]
        end = datetime.now()

    acc = 0
    return acc



file = open('input.txt').read().splitlines()

search_1(file)

nops = {}
jmps = {}
index = 0

for instruction in file:
    rule = instruction[:3]

    if (rule == 'nop'):
        nops[index] = instruction

    if (rule == 'jmp'):
        jmps[index] = instruction

    index += 1

acc = 0

if (acc == 0):
    for index, jmp in jmps.items():
        aux = list(file)
        aux[index] = aux[index].replace('jmp', 'nop')
        acc = search_2(aux)
        if (acc != 0):
            print('Accumulator: {ACC}'.format(ACC=acc))
            print('Rule {INDEX}: {ORIGINAL} -> {MODIFIED}'.format(INDEX=index, ORIGINAL=file[index], MODIFIED=aux[index]))
            break

if (acc == 0):
    for index, nop in nops.items():
        aux = list(file)
        aux[index] = aux[index].replace('nop', 'jmp')
        acc = search_2(aux)
        if (acc != 0):
            print('Accumulator: {ACC}'.format(ACC=acc))
            print('Rule {INDEX}: {ORIGINAL} -> {MODIFIED}'.format(INDEX=index, ORIGINAL=file[index], MODIFIED=aux[index]))
            break
