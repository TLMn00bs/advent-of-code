file = [line for line in open('input12.txt').read().split('\n') if line != '']
# file = ['F10','N3','F7','R90','F11']

initialPos = {'dirEO': 'E','dirFaceE':1,'posEO':0,'dirNS':'N','dirFaceN':0,'posNS':0}

for line in file:
    print(initialPos, line)
    dir = line[0]
    if dir == 'F':
        if initialPos['dirFaceE'] == 1:
            if initialPos['dirEO'] == 'W': initialPos['posEO'] -= int(line[1:])
            else: 			   initialPos['posEO'] += int(line[1:])

            initialPos['dirEO'] = 'E'
            initialPos['posEO'] = abs(initialPos['posEO'])

        elif initialPos['dirFaceE'] == -1:
            if initialPos['dirEO'] == 'E': initialPos['posEO'] -= int(line[1:])
            else: 			   initialPos['posEO'] += int(line[1:])

            initialPos['dirEO'] = 'W'
            initialPos['posEO'] = abs(initialPos['posEO'])

        elif initialPos['dirFaceN'] == 1:
            if initialPos['dirNS'] == 'S': 
                initialPos['posNS'] -= int(line[1:])
            else: initialPos['posNS'] += int(line[1:])
            initialPos['dirNS'] = 'N'
            initialPos['posNS'] = abs(initialPos['posNS'])
        elif initialPos['dirFaceN'] == -1:
            if initialPos['dirNS'] == 'N': 
                initialPos['posNS'] -= int(line[1:])
            else: initialPos['posNS'] += int(line[1:])
            initialPos['dirNS'] = 'S'
            initialPos['posNS'] = abs(initialPos['posNS'])
        else:
            pass
    elif dir == 'N':
        if initialPos['dirNS'] == 'N':
            initialPos['posNS'] = initialPos['posNS'] + int(line[1:])
        else:
            initialPos['posNS'] = initialPos['posNS'] - int(line[1:])
            if initialPos['posNS'] < 0:
                initialPos['dirNS'] = 'S'
                initialPos['posNS'] = abs(initialPos['posNS'])
            initialPos['dirNS'] == 'N'
    elif dir == 'S':
        if initialPos['dirNS'] == 'S':
            initialPos['posNS'] = initialPos['posNS'] + int(line[1:])
        else:
            initialPos['posNS'] = initialPos['posNS'] - int(line[1:])
            if initialPos['posNS'] < 0:
                initialPos['dirNS'] = 'N'
                initialPos['posNS'] = abs(initialPos['posNS'])
            initialPos['dirNS'] == 'S'
    elif dir == 'E':
        if initialPos['dirEO'] == 'E':
            initialPos['posEO'] = initialPos['posEO'] + int(line[1:])
        else:
            initialPos['posEO'] = initialPos['posEO'] - int(line[1:])
            if initialPos['posEO'] < 0:
                initialPos['dirEO'] = 'W'
                initialPos['posEO'] = abs(initialPos['posEO'])
            initialPos['dirEO'] == 'E'
    elif dir == 'W':
        if initialPos['dirEO'] == 'W':
            initialPos['posEO'] = initialPos['posEO'] + int(line[1:])
        else:
            initialPos['posEO'] = initialPos['posEO'] - int(line[1:])
            if initialPos['posEO'] < 0:
                initialPos['dirEO'] = 'E'
                initialPos['posEO'] = abs(initialPos['posEO'])
            initialPos['dirEO'] == 'W'
    elif dir == 'L':
        degrees = line[1:]
        if initialPos['dirFaceE'] == 1 and initialPos['dirEO'] == 'E':
            if degrees == '270': 
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = -1
            elif degrees == '180':
                initialPos['dirFaceE'] = -1
            elif degrees == '90':
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = 1
            else:
                pass
        elif initialPos['dirFaceE'] == -1:
            if degrees == '270': 
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = 1
            elif degrees == '180':
                initialPos['dirFaceE'] = 1
            elif degrees == '90':
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = -1
            else:
                pass
        elif initialPos['dirFaceN'] == 1:
            if degrees == '270': 
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = 1
            elif degrees == '180':
                initialPos['dirFaceN'] = -1
            elif degrees == '90':
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = -1
            else:
                pass
        elif initialPos['dirFaceN'] == -1:
            if degrees == '270': 
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = -1
            elif degrees == '180':
                initialPos['dirFaceN'] = 1
            elif degrees == '90':
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = 1
            else:
                pass
    elif dir == 'R':
        degrees = line[1:]
        if initialPos['dirFaceE'] == 1 and initialPos['dirEO'] == 'E':
            if degrees == '90': 
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = -1
            elif degrees == '180':
                initialPos['dirFaceE'] = -1
            elif degrees == '270':
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = 1
            else:
                pass
        elif initialPos['dirFaceE'] == 1 and initialPos['dirEO'] == 'W':
            if degrees == '90': 
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = 1
            elif degrees == '180':
                initialPos['dirFaceE'] = 1
            elif degrees == '270':
                initialPos['dirFaceE'] = 0
                initialPos['dirFaceN'] = -1
            else:
                pass
        elif initialPos['dirFaceN'] == 1 and initialPos['dirNS'] == 'N':
            if degrees == '90': 
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = 1
            elif degrees == '180':
                initialPos['dirFaceN'] = -1
            elif degrees == '270':
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = -1
            else:
                pass
        elif initialPos['dirFaceN'] == 1 and initialPos['dirNS'] == 'S':
            if degrees == '90': 
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = -1
            elif degrees == '180':
                initialPos['dirFaceN'] = 1
            elif degrees == '270':
                initialPos['dirFaceN'] = 0
                initialPos['dirFaceE'] = 1
            else:
                pass
    else:
        pass


print('Manhattan distance:',initialPos['posEO'] + initialPos['posNS'])
