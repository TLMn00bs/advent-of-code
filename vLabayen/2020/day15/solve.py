with open('input.txt') as f:
	numbers = [int(n) for n in f.readline()[:-1].split(',')]

	for i in range(len(numbers) + 1, 2020 + 1):
		last_number = numbers[-1]
		if numbers.count(last_number) > 1:
			last_number_index = i - 1
			last_spoken = len(numbers) - 1 - numbers[:-1][::-1].index(last_number)
			numbers.append(last_number_index - last_spoken)

		else: numbers.append(0)

	print(numbers[-1])


with open('input.txt') as f:
	numbers = [int(n) for n in f.readline()[:-1].split(',')]
	spoken_numbers = {n : {'last' : i + 1, 'prev' : None} for i,n in enumerate(numbers)}

	last_number = numbers[-1]
	for i in range(len(numbers) + 1, 30000000 + 1):
		if spoken_numbers[last_number]['prev'] != None: last_number = spoken_numbers[last_number]['last'] - spoken_numbers[last_number]['prev']
		else: last_number = 0

		if last_number in spoken_numbers:
			spoken_numbers[last_number]['prev'] = spoken_numbers[last_number]['last']
			spoken_numbers[last_number]['last'] = i
		else: spoken_numbers[last_number] = {'last' : i, 'prev' : None}

	print(last_number)
