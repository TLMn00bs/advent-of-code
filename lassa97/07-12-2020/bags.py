def update_containers(file, containers):
    new_containers = containers
    for rule in file:
        for container in containers:
            box, bags = rule.split()[:3], rule.split()[3:]

            if (' '.join(bags).count(container)) > 0:
                if (' '.join(box)[:-1] not in containers):
                    new_containers.append(' '.join(box)[:-1])
                    break

    return new_containers

def generate_dict(rule):
    box, bags = rule.split()[:3], rule.split()[3:]
    box = ' '.join(box)[:-1]
    bags = ' '.join(bags[1:]).split(',')

    contents = {}

    for bag in bags:
        bag_detail = bag.replace('.', '')
        if (bag_detail[:1] == ' '):
            bag_detail = bag_detail.replace(' ', '', 1)
        if (bag_detail[-1:] == 's'):
            bag_name = bag_detail[2:-1]
        else:
            bag_name = bag_detail[2:]
        bag_count = bag_detail[:1]

        if (bag_name[1:] == 'other bag'):
            bag_count = 0
            bag_name = bag_name[1:]

        contents[bag_name] = int(bag_count)
    
    return box, contents

def search_1(file):
    containers = ['shiny gold bag']
    curr_len = len(containers)
    prev_len = 0

    while (curr_len != prev_len):

        prev_len = curr_len
        containers = update_containers(file, containers)
        curr_len = len(containers)


    containers.remove('shiny gold bag')
    print('Bags: {BAGS}'.format(BAGS=len(containers)))
    return

file = open('input.txt').read().splitlines()

search_1(file)

containers = {}

for rule in file:
    box, bags = generate_dict(rule)
    containers[box] = bags

bags_inside = []

# Function made by @jartigag (https://github.com/jartigag)

def find_how_many_inside(target, ntimes=1):
    for bag, bagrules in containers.items():
        #example: bag      = 'shiny gold bag',
        #         bagrules = {'dull lime bag': 1, 'pale coral bag': 2, 'wavy silver bag': 1, 'muted black bag': 5}
        if bag == target:
            for next_target in bagrules.keys():
                #print(next_target, bagrules[next_target])
                bags_inside.append(ntimes * bagrules[next_target]) # add this bag's times * next bag's times..
                #example: target      = 'pale coral bag'
                #         next_target = 'dim gold bag'       2 * 5
                find_how_many_inside(next_target, ntimes * bagrules[next_target])

find_how_many_inside('shiny gold bag')

print('Bags inside: {BAGS}'.format(BAGS=sum(bags_inside)))