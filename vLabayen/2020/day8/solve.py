acumulator = 0
visited_lines = []

with open('input.txt') as f: lines = [line[:-1] for line in f]


idx = 0
while True:
	if idx in visited_lines:
		print(acumulator)
		break
	visited_lines.append(idx)

	if lines[idx][:3] == 'acc':
		acumulator += int(lines[idx][4:])
		idx += 1

	elif lines[idx][:3] == 'nop':
		idx += 1

	elif lines[idx][:3] == 'jmp':
		idx += int(lines[idx][4:])




def try_change(lines, n):
	acum = 0
	visited_lines = []

	l = [(line if i != n else ('{} {}'.format('nop' if line[:3] == 'jmp' else 'jmp', line[4:]))) for i,line in enumerate(lines)]
	idx = 0
	try:
		while True:
			if idx in visited_lines:
				return -1

			visited_lines.append(idx)

			if l[idx][:3] == 'acc':
				acum += int(l[idx][4:])
				idx += 1

			elif l[idx][:3] == 'nop':
				idx += 1

			elif l[idx][:3] == 'jmp':
				idx += int(l[idx][4:])

	except: return acum


nop_jmp_idx = [i for i,l in enumerate(lines) if l[:3] == 'nop' or l[:3] == 'jmp']
for i in nop_jmp_idx:
	r = try_change(lines, i)
	if r != -1:
		print(r)
		break
