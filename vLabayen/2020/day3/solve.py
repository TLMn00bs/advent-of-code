from functools import reduce

with open('input.txt') as f: print(reduce(lambda x,y: x*y, [val for p,val in enumerate(reduce(lambda c,enum,s=[(3,1)]: [v for l in [[c[2*i] + 1*(enum[0][x*c[2*i+1] % len(enum[0])] == '#' and enum[1]%y == 0), c[2*i+1] + 1*(enum[1]%y == 0)] for i,(x,y) in enumerate(s)] for v in l], ((line[:-1],i) for i,line in enumerate(f)), [0,0])) if p%2 == 0]))
with open('input.txt') as f: print(reduce(lambda x,y: x*y, [val for p,val in enumerate(reduce(lambda c,enum,s=[(1,1), (3,1), (5,1), (7,1), (1,2)]: [v for l in [[c[2*i] + 1*(enum[0][x*c[2*i+1] % len(enum[0])] == '#' and enum[1]%y == 0), c[2*i+1] + 1*(enum[1]%y == 0)] for i,(x,y) in enumerate(s)] for v in l], ((line[:-1],i) for i,line in enumerate(f)), [0,0]*5)) if p%2 == 0]))
