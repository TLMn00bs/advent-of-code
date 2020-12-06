def search_1(file_name):
    good_pass = 0
    with open(file_name) as file:
        for line in file:
            aux = line.split()
            count = aux[2].count(aux[1][0])
            min, max = aux[0].split('-')

            if count in range(int(min), int(max) + 1):
                good_pass += 1
    
    print(good_pass)
    return

def search_2(file_name):
    good_pass = 0
    with open(file_name) as file:
        for line in file:
            aux = line.split()
            letter = aux[1][0]
            pos_1, pos_2 = aux[0].split('-')

            password = aux[2]

            if (password[int(pos_1) - 1] is letter) ^ (password[int(pos_2) - 1] is letter):
                good_pass += 1

    print(good_pass)
    return

search_1("input.txt")
search_2("input.txt")