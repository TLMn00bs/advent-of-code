import re

def check_is_valid(num, ranges):
    for range in ranges:
        if (range[0] <= num) and (num <= range[1]):
            return True

    return False

def get_valid_ranges(nums, ranges, rules):
    valid_ranges = {}
    aux_num = []
    for num in nums:
        for i in range(0, len(ranges), 2):
            if (ranges[i][0] <= int(num)) and (int(num) <= ranges[i][1]):
                aux = rules[i//2].split(':')
                valid_ranges[aux[0]] = aux[1][1:]
                #valid_ranges.append(rules[i//2])
                #valid_ranges.append([ranges[i], ranges[i+1]])
            if (ranges[i+1][0] <= int(num)) and (int(num) <= ranges[i+1][1]):
                aux = rules[i//2].split(':')
                valid_ranges[aux[0]] = aux[1][1:]
                #valid_ranges.append(rules[i//2])
                #valid_ranges.append([ranges[i], ranges[i+1]])

        aux_num.append(valid_ranges)
        
    return aux_num

def parse_data(file):
    data = []
    aux = []

    for line in file:
        if (line == ''):
            data.append(aux)
            aux = []
        else:
            aux.append(line)
    data.append(aux)
    return data

def search_1(rules, tickets):
    ranges = []

    for rule in rules:
        num_list = re.findall(r'\d+', rule)
        ranges.append([int(num_list[0]), int(num_list[1])])
        ranges.append([int(num_list[2]), int(num_list[3])])

    valid_tickets = []
    invalid_tickets = []
    invalid_nums = []

    for ticket in tickets:
        nums = ticket.split(',')
        for num in nums:
            if not (check_is_valid(int(num), ranges)):
                invalid_nums.append(int(num))
            else:
                valid_tickets.append(ticket)


    print(invalid_tickets)
    print('Scanning error rate: {ERROR_RATE}'.format(ERROR_RATE=sum(invalid_nums)))

    return
    #return valid_tickets, invalid_tickets

def expresions(tickets, rules):
    for rule in rules:
        rules_aux = re.findall(r'(\d+)-(\d+) or (\d+)-(\d+)', rule)
        print(rules_aux)
    '''
    for rule in rules:
        exists = re.search(r'\b([1-9]|[12][0-9]|3[0-2])\b', rule)
        print(exists.group())

    return
    '''


file = open('aux.txt').read().splitlines()

data = parse_data(file)

rules = data[0]
my_ticket = data[1][1:]
tickets = data[2][1:]

search_1(rules, tickets)

expresions(tickets, rules)