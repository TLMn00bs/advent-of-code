from functools import reduce

with open('input.txt') as f:
	player1, player2 =  [[int(card) for card in player.split('\n')[1:]] for player in f.read().strip().split('\n\n')]

	while len(player1) > 0 and len(player2) > 0:
		p1_card, p2_card = player1.pop(0), player2.pop(0)

		if p1_card > p2_card: player1 += [p1_card, p2_card]
		else: player2 += [p2_card, p1_card]

	winner = player1 if len(player1) > len(player2) else player2
	weights = [*range(len(winner), 0, -1)]
	print(reduce(lambda x,y: x + (y[0] * y[1]), [*zip(winner, weights)], 0))


def run_game(p1, p2):
	p1_configurations, p2_configurations = {}, {}

	while len(p1) > 0 and len(p2) > 0:
		p1_conf, p2_conf = tuple(p1), tuple(p2)
		if p1_conf in p1_configurations or p2_conf in p2_configurations: return p1, p2, 'p1'
		else:
			p1_configurations[p1_conf] = None
			p2_configurations[p2_conf] = None

		p1_card, p2_card = p1.pop(0), p2.pop(0)

		if len(p1) >= p1_card and len(p2) >= p2_card:
			_p1, _p2, winner = run_game([card for card in p1[:p1_card]], [card for card in p2[:p2_card]])

			if winner == 'p1': p1 += [p1_card, p2_card]
			else: p2 += [p2_card, p1_card]
		else:
			if p1_card > p2_card: p1 += [p1_card, p2_card]
			else: p2 += [p2_card, p1_card]

	return p1, p2, ('p1' if len(p1) > len(p2) else 'p2')

with open('input.txt') as f:
	player1, player2 =  [[int(card) for card in player.split('\n')[1:]] for player in f.read().strip().split('\n\n')]

	p1, p2, _winner = run_game([card for card in player1], [card for card in player2])

	winner = p1 if _winner == 'p1' else p2
	weights = [*range(len(winner), 0, -1)]
	print(reduce(lambda x,y: x + (y[0] * y[1]), [*zip(winner, weights)], 0))
