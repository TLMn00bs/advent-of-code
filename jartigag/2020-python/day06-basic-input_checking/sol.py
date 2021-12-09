#!/usr/bin/env python

input = open("input").read().split("\n\n")

sumA,sumB = 0,0
for group in input:
    uniq_answers = set(group.replace("\n",""))
    sumA+=len(uniq_answers)
    for answer in uniq_answers:
        if all(answer in member_answers for member_answers in group.split()):
            sumB+=1

print(sumA)
print(sumB)
