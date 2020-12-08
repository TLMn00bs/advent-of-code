file = open('input3.txt')

myArray = []
for inx,line in enumerate(file):
#    print(inx,line)
    myArray.append(line*25)

print(myArray)
