

file = open('input.txt').read().splitlines()

deck = []

for line in file:
    if (line.isdigit()):
        deck.append(int(line))

deck_1, deck_2 = deck[:len(deck)//2], deck[len(deck)//2:]

while ((len(deck_1) != 0) or (len(deck_2) != 0)):
    try:
        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)

        if (card_1 > card_2):
            deck_1.append(card_1)
            deck_1.append(card_2)
        elif (card_2 > card_1):
            deck_2.append(card_2)
            deck_2.append(card_1)
    except:
        break

total = 0

if (len(deck_1) != 0):
    for index in range(len(deck_1)):
        total += (len(deck_1) - index) * deck_1[index]
else:
    for index in range(len(deck_2)):
        total += (len(deck_2) - index) * deck_2[index]

print(total)

def getScore(deck):
    ans = 0
    for i, val in enumerate(deck[::-1]):
        ans += val * (i+1)
    return ans

class Game2:
    def __init__(self, deck1, deck2):
        self.deck1 = deck1
        self.deck2 = deck2
        self.history = set()

    def game(self):
        while self.deck1 and self.deck2:
            if (tuple(self.deck1), tuple(self.deck2)) in self.history:
                return 1
            else:
                self.history.add((tuple(self.deck1), tuple(self.deck2)))
            curr1 = self.deck1.pop(0)
            curr2 = self.deck2.pop(0)
            if curr1 > len(self.deck1) or curr2 > len(self.deck2):
                if curr1 > curr2:
                    self.deck1 += [curr1, curr2]
                else:
                    self.deck2 += [curr2, curr1]
            else:
                sub = Game2(self.deck1[:curr1], self.deck2[:curr2]).game()
                if sub == 1:
                    self.deck1 += [curr1, curr2]
                else:
                    self.deck2 += [curr2, curr1]
        return 1 if self.deck1 else 2


def part2(deck):
    deck_1, deck_2 = deck[:len(deck)//2], deck[len(deck)//2:]
    game = Game2(deck_1, deck_2)
    winnerNum = game.game()
    winner = game.deck1 if winnerNum == 1 else game.deck2
    return getScore(winner)

total = part2(deck)

print(total)