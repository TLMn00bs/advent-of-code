with open('input.txt') as f: print(sum(1 for c1,c2,l,p in ([int(c) for c in conditions.split('-')] + [letter[:-1]] + [passwd[:-1]] for conditions,letter,passwd in (line.split(' ') for line in f)) if c1 <= p.count(l) <= c2))
with open('input.txt') as f: print(sum(1 for c1,c2,l,p in ([int(c) for c in conditions.split('-')] + [letter[:-1]] + [passwd[:-1]] for conditions,letter,passwd in (line.split(' ') for line in f)) if (p[c1 - 1] == l) ^ (p[c2 - 1] == l)))
