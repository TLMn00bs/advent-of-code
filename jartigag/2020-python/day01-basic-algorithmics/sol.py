#!/usr/bin/env python3

input = [line.strip() for line in open("input").readlines()]

for i,num1 in enumerate(input):
    for num2 in input[i:]:
        if int(num1)+int(num2)==2020:
            print(num1,num2,int(num1)*int(num2))
