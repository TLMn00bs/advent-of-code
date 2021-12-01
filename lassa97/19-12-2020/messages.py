from io import RawIOBase
import operator


def prepare_file(file_name):
    file = open(file_name).read().splitlines()

    rules = {}

    for line in file:
        if (line == ''):
            return rules
        else:
            aux = line.split(':')
            rules[int(aux[0])] = aux[1][1:]

    return rules

data = prepare_file('input.txt')

rules = dict(sorted(data.items(), key=operator.itemgetter(0)))

print(rules)

