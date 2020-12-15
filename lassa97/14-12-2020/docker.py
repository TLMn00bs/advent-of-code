import re

def search_1(file, memories, mask):

    for i in range(1, len(file)):
        if (file[i][0:4] == 'mask'):
            mask = file[i][-36:]
        elif (file[i][0:3] == 'mem'):
            aux = re.findall(r'\d+', file[i])
            mem, value = int(aux[0]), format(int(aux[1]), '036b')
            num = ''
            for j in range(len(mask)):
                if (mask[j] == 'X'):
                    num += value[j]
                else:
                    num += mask[j]
            memories[mem] = int(num, 2)

    return memories

def search_2(file, memories, mask):

    for i in range(1, len(file)):
        if (file[i][0:4] == 'mask'):
            mask = file[i][-36:]
        elif (file[i][0:3] == 'mem'):
            aux = re.findall(r'\d+', file[i])
            mem, value = (format(int(aux[0]), '036b'), int(aux[1]))
            num = ''
            for j in range(len(mask)):
                if (mask[j] != '0'):
                    num += mask[j]
                else:
                    num += mem[j]

            # Take a copy of the original value of the memory, so we can change the correct values
            # aux_num = '000000000000000000000000000000X1001X'
            aux_num = num

            # Iterate over all the posible memories values and replace the 'X' with the binary value of iteration number
            # range(0, 4), because we have two 'X' in the memory and that's a total of 4 combinations (2^2)
            for k in range((2 ** num.count('X'))):
                k_bin = format(k, '0{LEN}b'.format(LEN=num.count('X')))
                # For each value of the number in binary, lest replace the 'X' with that value
                # k_bin = '01', because k is 1 in the example of this iteration
                for c in range(len(k_bin)):
                    # k_bin[0] = 0, so we replace the first 'X' with '0'
                    aux_num = aux_num.replace('X', k_bin[c], 1)
                    # aux_num = '00000000000000000000000000000001001X'

                    # In the next iteration, we replace 'X' with the value of k_bin[1] = 1
                    # aux_num = '000000000000000000000000000000010011'

                memories[aux_num] = value
                aux_num = num
    
    return memories




file = open('input.txt').read().splitlines()

memories = {}
mask = file[0][-36:]

memories = search_1(file, memories, mask)

print('Sum of all values: {SUM}'.format(SUM=sum(memories.values())))
memories = {}

memories = search_2(file, memories, mask)

print('Sum of all values: {SUM}'.format(SUM=sum(memories.values())))
