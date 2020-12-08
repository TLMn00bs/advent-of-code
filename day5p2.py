mypass = 'FBFBBFFRLR'

def getId(mypass):
	row = ['1' if letter == 'B' else '0' for letter in mypass[:7]]
	column = ['1' if letter == 'R' else '0' for letter in mypass[7:]]

	id = int(''.join(row),2)*8 + int(''.join(column),2)
	return id

file = open('input5.txt')
mypasses = []
for line in file:
	myid = getId(line.replace('\n',''))
	mypasses.append(myid)

def find_missing(lst):
	return [x for x in range(lst[0], lst[-1]+1)
                               if x not in lst]
print(find_missing(sorted(mypasses)))
