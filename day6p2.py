from collections import Counter

file = open('input6.txt').read().split('\n\n')
#file = open('inputprueba.txt').read().split('\n\n')

result = 0
for group in file:
	resp = group.split('\n')
	print(group)
	if '' in resp: resp.remove('')
#	resp = ["".join(set(p)) for p in group.split('\n') if p != '\n']
	resp1 = ''.join(resp)
	count = Counter(resp1)
	print(count)
	for i in count:
		print(count[i],len(resp))
		if count[i] == len(resp):
			result += 1
print(result)
