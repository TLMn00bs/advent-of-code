with open('input.txt') as f: print(sum(len(g) for g in [set.union(*[set(p) for p in group.split('\n') if p != '']) for group in f.read().split('\n\n')]))
with open('input.txt') as f: print(sum(len(g) for g in [set.intersection(*[set(p) for p in group.split('\n') if p != '']) for group in f.read().split('\n\n')]))
