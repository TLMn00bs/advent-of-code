def search_1(nums):
    for num in nums:
        for i in nums:
            if (int(num) + int(i)) == 2020:
                print(int(num)*int(i))
                #print("{NUM}*{I}={RESULT}".format(NUM=int(num), I=int(i), RESULT=int(num)*int(i)))
                return

def search_2(nums):
    for num in nums:
        for i in nums:
            for j in nums:
                if (int(num) + int(i) + int(j)) == 2020:
                    print(int(num)*int(i)*int(j))
                    #print("{NUM}*{I}*{J}={RESULT}".format(NUM=int(num), I=int(i), J=int(j), RESULT=int(num)*int(i)*int(j)))
                    return

with open("input.txt") as file:
    nums = []
    for num in file:
        nums.append(num)

search_1(nums)
search_2(nums)