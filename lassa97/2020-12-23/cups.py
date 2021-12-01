from itertools import product
from os import rename


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def parse_data(cups):
    for i in range(len(cups)):
        cups[i] = int(cups[i])

    return cups

def search_1(cups, moves):

    for _ in range(moves):
        picked_cups = cups[1:4]
        value = cups[0] - 1

        if (value == 0):
            value = len(cups)

        while (value in picked_cups):
            value -= 1
            if (value == 0):
                value = len(cups)

        updated_cups = cups[:1] + cups[4:]
        index = updated_cups.index(value) + 1
        updated_cups = updated_cups[:index] + picked_cups + updated_cups[index:]

        cups = updated_cups[1:] + updated_cups[:1]

    cups = cups[cups.index(1) + 1:] + cups[:cups.index(1)]
    return cups

def search_2(cups, size, moves):
    lookup = {}

    prev = None
    for i in range(len(cups) - 1, -1, -1):
        node = Node(cups[i])
        node.next = prev
        lookup[cups[i]] = node
        prev = node

    for i in range(size, len(cups), -1):
        node = Node(i)
        node.next = prev
        lookup[i] = node
        prev = node

    lookup[cups[-1]].next = lookup[len(cups) + 1]
    current_cup = lookup[cups[0]]

    for _ in range(moves):
        picked_cup1 = current_cup.next
        picked_cup2 = picked_cup1.next
        picked_cup3 = picked_cup2.next
        current_cup.next = picked_cup3.next

        picked_cups = {current_cup.value, picked_cup1.value, picked_cup2.value, picked_cup3.value}
        value = current_cup.value

        while (value in picked_cups):
            value -= 1
            if (value == 0):
                value = size

        index = lookup[value]
        next_cup = index.next

        index.next = picked_cup1
        picked_cup3.next = next_cup

        current_cup = current_cup.next

    cup = lookup[1]
    picked_cup1 = cup.next
    picked_cup2 = picked_cup1.next

    num = (picked_cup1.value * picked_cup2.value)

    return num

cups = open('input.txt').read().splitlines()

cups = parse_data(cups)

cups_1 = search_1(cups, 100)

labels = ''

for cup in cups_1:
    labels += str(cup)

print('The labels are: {LABELS}'.format(LABELS=labels))

product = search_2(cups, 1000000, 10000000)
print('The product is: {PRODUCT}'.format(PRODUCT=product))
