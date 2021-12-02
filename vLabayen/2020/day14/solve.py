import re
from itertools import product

def apply_mask(val, mask):
	retval = ''
	valstr = '{0:b}'.format(int(val))
	valstr = '0' * (len(mask) - len(valstr)) + valstr

	for i,bit in enumerate(valstr): retval += (mask[i] if mask[i] != 'X' else bit)

	return int(retval, 2)

with open('input.txt') as f:
	mem = {}
	for line in f:
		if line[:4] == 'mask': mask = line[:-1].split('= ')[1]
		else:
			mempos, memval = re.search('mem\[(\d+)\] = (\d+)', line[:-1]).groups()
			mem[mempos] = apply_mask(memval, mask)

	print(sum(v for v in mem.values()))


def apply_mask2(address, mask):
	w_addresses = []
	address_template = ''

	addrstr = '{0:b}'.format(int(address))
	addrstr = '0' * (len(mask) - len(addrstr)) + addrstr

	num_floating = 0
	for i,bit in enumerate(addrstr):
		if mask[i] == 'X':
			num_floating += 1
			address_template += '{}'
		else: address_template += (bit if mask[i] == '0' else '1')

	for opt in product(*([[0,1]] * num_floating)):
		w_addresses.append(int(address_template.format(*opt), 2))
	return w_addresses

with open('input.txt') as f:
	mem = {}
	for line in f:
		if line[:4] == 'mask': mask = line[:-1].split('= ')[1]
		else:
			mempos, memval = re.search('mem\[(\d+)\] = (\d+)', line[:-1]).groups()
			for _mempos in apply_mask2(mempos, mask):
				mem[_mempos] = int(memval)

	print(sum(v for v in mem.values()))
