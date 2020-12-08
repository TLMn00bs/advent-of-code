import numpy as np

#num = [1721,979,366,299,675,1456]

file = open('input.txt')
nums = [int(i) for i in file]
print(nums)
result = 0
result = [if i+j+j == 2020: i*j*k for i in nums for j in nums for k in nums]

print(result)