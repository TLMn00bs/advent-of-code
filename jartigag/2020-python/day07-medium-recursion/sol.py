#!/usr/bin/env python

input = [line.strip() for line in open("input").readlines()]

rules = {}

def singular(x): return x.rstrip('s')

for line in input:
    k,v = line.split(' contain ') #example: k='striped green bags', v='5 posh indigo bags.'
    rules[singular(k)] = {}
    for k2v2 in v.replace('.','').split(', '):
        if k2v2!="no other bags":
            k2, v2 =  " ".join(k2v2.split()[1:]), int(k2v2.split()[0])
            #example: k2='posh indigo bags',      v2=5
            rules[singular(k)][singular(k2)] = v2

eventually_shiny_gold_bag_containers = set()
def find_containers(target):
    for bag,bagrules in rules.items():
        #example: bag      = 'pale coral bag',
        #         bagrules = {'dim gold bag': 5, 'vibrant bronze bag': 1}
        if any(target in bagrule for bagrule in bagrules):
            eventually_shiny_gold_bag_containers.add(bag) # add this bag..
            find_containers(bag)                          # ..and recursion!

find_containers('shiny gold')
print( len(eventually_shiny_gold_bag_containers) )

total_bags_inside_shiny_gold_bag = []
def find_how_many_inside(target, ntimes=1):
    for bag,bagrules in rules.items():
        #example: bag      = 'shiny gold bag',
        #         bagrules = {'dull lime bag': 1, 'pale coral bag': 2, 'wavy silver bag': 1, 'muted black bag': 5}
        if bag==target:
            for next_target in bagrules.keys():
                total_bags_inside_shiny_gold_bag.append(ntimes * bagrules[next_target]) # add this bag's times * next bag's times..
                #example: target      = 'pale coral bag'
                #         next_target = 'dim gold bag'       2 * 5
                find_how_many_inside(next_target, ntimes * bagrules[next_target])       # ..and recursion!

find_how_many_inside('shiny gold bag')
print( sum(total_bags_inside_shiny_gold_bag) )
