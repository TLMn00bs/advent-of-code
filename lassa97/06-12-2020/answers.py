def search_1(answers):
    chars = []
    for answer in answers:
        for char in answer:
            if char not in chars:
                chars.append(char)
    count = len(chars)
    return count


def search_2(answers):
    common = list(set.intersection(*map(set, answers)))
    count = len(common)
    return count


file = open('input.txt').read().splitlines()

counts = 0
answers = []

for line in file:
    if (line is ''):
        counts += search_1(answers)
        answers.clear()
    else:
        line = line.rstrip()
        answers.append(line)

counts += search_1(answers)

print('Answers 1: {COUNTS}'.format(COUNTS=counts))

counts = 0
answers = []

for line in file:
    if (line is ''):
        counts += search_2(answers)
        answers.clear()
    else:
        line = line.rstrip()
        answers.append(line)

counts += search_2(answers)

print('Answers 2: {COUNTS}'.format(COUNTS=counts))