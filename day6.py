file = open('input6.txt').read().split('\n\n')
#import string
#ab = string.ascii_lowercase
#'abcdefghijklmnopqrstuvwxyz'
result = 0
for group in file:
	resp = group.replace('\n','')
	cosas = []
	for i in resp:
		if not i in cosas:
			cosas.append(i)
	print(len(cosas))
	result += len(cosas)
print(result)
