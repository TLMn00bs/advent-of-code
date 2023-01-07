#!/bin/python3

time = 13
EE_p, EE_d = 3, 3
CC_p, CC_d = 2, 5
EE_CC_d = 2

print(1612 + EE_p * (time - EE_d - 1) + CC_p * (time - CC_d - 2))


print(1612 + EE_p * (time - EE_d - 1) + CC_p * (time - EE_d - EE_CC_d - 2))
print(1612 + CC_p * (time - CC_d - 1) + EE_p * (time - CC_d - EE_CC_d - 2))
